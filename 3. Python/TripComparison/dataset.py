import sqlite3
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler
from enrich_destinations import enrich_missing_metadata


def check_and_notify_missing_values(df: pd.DataFrame):
    """Scans raw dataframe for missing values and prints explicit notifications to the user."""
    missing_notifications = []

    for idx, row in df.iterrows():
        flight_id = row.get("flight_id", "Unknown")
        dest_id = row.get("destination_id", "Unknown")

        # Check avg_daily_cost_usd
        if pd.isna(row.get("avg_daily_cost_usd")):
            missing_notifications.append(
                f"[Trip Alert] Flight '{flight_id}' (Destination: '{dest_id}') is missing 'avg_daily_cost_usd'. "
                f"Reason: Destination metadata has not been enriched by Gemini API yet."
            )

        # Check return flight details
        if row.get("has_return") and pd.isna(row.get("return_departs")):
            missing_notifications.append(
                f"[Trip Alert] Flight '{flight_id}' is marked as round-trip but missing 'return_departs'. "
                f"Reason: Flight offer payload did not supply a return departure date."
            )
        elif not row.get("has_return") and pd.isna(row.get("return_departs")):
            # Informational notice for one-way flights
            missing_notifications.append(
                f"[Trip Notice] Flight '{flight_id}' is missing 'return_departs'. "
                f"Reason: Trip is a one-way flight, so no return schedule exists."
            )

        # Check pricing
        if pd.isna(row.get("price_usd")):
            missing_notifications.append(
                f"[Trip Alert] Flight '{flight_id}' is missing 'price_usd'. "
                f"Reason: Pricing data was omitted during provider response parsing."
            )

    if missing_notifications:
        print("\n--- DATA VALIDATION NOTIFICATIONS ---")
        for notice in missing_notifications:
            print(notice)
        print("-------------------------------------\n")


def load_raw_trip_data(
    db_name: str = "seed.db",
    target_duration: int = None,
    tolerance_days: int = 0,
    target_country: str = None,
    target_region: str = None
) -> pd.DataFrame:
    """Trigger enrichment on un-enriched destinations before querying raw trip data."""
    enrich_result = enrich_missing_metadata(batch_size=50, db_name=db_name)
    if enrich_result["failures"]:
        for f in enrich_result["failures"]:
            print(f"Enrichment Warning for {f['destination_id']}: Missing {f['missing_fields']}. Reason: {f['reason']}")

    connection = sqlite3.connect(db_name)

    query = """
            SELECT 
                f.flight_id,
                f.destination_id,
                f.price_usd,
                f.outbound_departs,
                f.outbound_arrives,
                f.has_return,
                f.return_departs,
                f.return_arrives,
                f.airline,
                f.outbound_layovers,
                f.return_layovers,
                d.latitude,
                d.longitude,
                d.avg_daily_cost_usd,
                d.country,
                (julianday(f.return_departs) - julianday(f.outbound_departs)) AS calc_duration_days
            FROM flights f
            INNER JOIN destinations d ON f.destination_id = d.destination_id
            WHERE 1=1
        """

    params = []

    if target_duration is not None:
        min_days = max(1, target_duration - tolerance_days)
        max_days = target_duration + tolerance_days
        query += " AND (calc_duration_days BETWEEN ? AND ? OR f.return_departs IS NULL)"
        params.extend([min_days, max_days])

    if target_country:
        query += " AND LOWER(d.country) LIKE LOWER(?)"
        params.append(f"%{target_country}%")

    if target_region:
        query += " AND LOWER(d.region) LIKE LOWER(?)"
        params.append(f"%{target_region}%")

    df = pd.read_sql_query(query, connection, params=params)
    connection.close()

    check_and_notify_missing_values(df)

    return df


def clean_raw_data(df: pd.DataFrame, scaler: StandardScaler = None):
    """Cleans raw data, scales continuous features (including avg_daily_cost_usd), and returns features."""
    df_feat = df.copy()

    # Clean core continuous features
    essential_cols = ["latitude", "longitude", "price_usd", "avg_daily_cost_usd"]
    for col in essential_cols:
        df_feat[col] = pd.to_numeric(df_feat[col], errors="coerce")

    # Drop rows missing critical numeric ground values after user notification
    df_feat = df_feat.dropna(subset=essential_cols)

    for col in ["outbound_layovers", "return_layovers"]:
        extracted = df_feat[col].astype(str).str.extract(r"(\d+)")[0]
        df_feat[col] = pd.to_numeric(extracted, errors="coerce").fillna(0.0)

    # Convert lat & lon to cartesian coordinates
    lat_rad = np.radians(df_feat["latitude"])
    lon_rad = np.radians(df_feat["longitude"])

    df_feat["coord_x"] = np.cos(lat_rad) * np.cos(lon_rad)
    df_feat["coord_y"] = np.cos(lat_rad) * np.sin(lon_rad)
    df_feat["coord_z"] = np.sin(lat_rad)

    # Engineer time & duration features
    outbound_dt = pd.to_datetime(df_feat["outbound_departs"], errors="coerce")
    return_dt = pd.to_datetime(df_feat["return_departs"], errors="coerce")

    duration_days = (return_dt - outbound_dt).dt.total_seconds() / (24 * 3600)
    df_feat["trip_duration_days"] = duration_days.fillna(1.0).apply(lambda x: max(x, 1.0))
    df_feat["dep_hour"] = outbound_dt.dt.hour.fillna(12.0).astype(float)
    df_feat["is_weekend_dep"] = outbound_dt.dt.dayofweek.isin([4, 5]).astype(float)

    # Continuous features now include avg_daily_cost_usd from enrichment
    continuous_cols = [
        "coord_x",
        "coord_y",
        "coord_z",
        "price_usd",
        "avg_daily_cost_usd",
        "outbound_layovers",
        "return_layovers",
        "dep_hour"
    ]

    if scaler is None:
        scaler = StandardScaler()
        df_feat[continuous_cols] = scaler.fit_transform(df_feat[continuous_cols])
    else:
        df_feat[continuous_cols] = scaler.transform(df_feat[continuous_cols])

    selected_features = continuous_cols + ["is_weekend_dep"]

    return df_feat[selected_features], scaler, continuous_cols


class TripsDataset(Dataset):
    """PyTorch Dataset wrapper storing features, tensor X, and fitted StandardScaler."""

    def __init__(
            self,
            db_path: str = "trips.db",
            target_duration: int = None,
            tolerance_days: int = 0,
            target_country: str = None,
            target_region: str = None
    ):
        self.db_path = db_path

        self.df_raw = load_raw_trip_data(
            db_name=self.db_path,
            target_duration=target_duration,
            tolerance_days=tolerance_days or 0,
            target_country=target_country,
            target_region=target_region
        )

        if self.df_raw.empty:
            raise ValueError(
                f"No matching trips found for country '{target_country}' with duration ~{target_duration} days.")

        self.df_features, self.scaler, self.continuous_cols = clean_raw_data(self.df_raw)
        self.feature_names = list(self.df_features.columns)

        features_np = self.df_features.to_numpy(dtype=np.float32)
        self.X = torch.from_numpy(features_np)

    def __len__(self) -> int:
        return self.X.shape[0]

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.X[idx]

    def unscale_continuous_features(self, tensor_data: torch.Tensor) -> pd.DataFrame:
        if tensor_data.ndim == 1:
            tensor_data = tensor_data.unsqueeze(0)

        np_data = tensor_data.detach().cpu().numpy()
        df_scaled = pd.DataFrame(np_data, columns=self.feature_names)

        df_unscaled = df_scaled.copy()
        df_unscaled[self.continuous_cols] = self.scaler.inverse_transform(df_scaled[self.continuous_cols])

        return df_unscaled


def score_and_rank_trips(dataset: TripsDataset, W: torch.Tensor) -> pd.DataFrame:
    """Computes vector dot products using dataset.X and maps scores back to dataset.df_raw."""
    # Compute tensor scores: (N x 9) @ (9 x 1) -> (N x 1)
    scores = torch.matmul(dataset.X, W)

    # Slice raw DataFrame to match the clean feature indices in dataset.X
    df_valid = dataset.df_raw.loc[dataset.df_features.index].copy()

    # Assign scores and rank
    df_valid["match_score"] = scores.squeeze().detach().cpu().numpy()
    df_ranked = df_valid.sort_values(by="match_score", ascending=False)

    return df_ranked