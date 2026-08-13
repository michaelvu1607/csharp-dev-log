import sqlite3
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler


def load_raw_trip_data(db_name: str = "trips.db") -> pd.DataFrame:
    """Queries SQL database and joins destination and flight tables on destination_id."""
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
            d.avg_daily_cost_usd
        FROM flights f
        INNER JOIN destinations d ON f.destination_id = d.destination_id
        """

    df = pd.read_sql_query(query, connection)
    connection.close()
    return df


def clean_raw_data(df: pd.DataFrame, scaler: StandardScaler = None):
    """Cleans raw data, scales continuous features, and returns (df_feat, scaler)."""
    df_feat = df.copy()

    # 1. clean core numerical features
    essential_cols = ["latitude", "longitude", "price_usd"]
    for col in essential_cols:
        df_feat[col] = pd.to_numeric(df_feat[col], errors="coerce")
    df_feat = df_feat.dropna(subset=essential_cols)

    for col in ["outbound_layovers", "return_layovers"]:
        extracted = df_feat[col].astype(str).str.extract(r"(\d+)")[0]
        df_feat[col] = pd.to_numeric(df_feat[col], errors="coerce").fillna(0.0)

    # convert lat & lon to cartesian coordinates -> add to df
    lat_rad = np.radians(df_feat["latitude"])
    lon_rad = np.radians(df_feat["longitude"])

    df_feat["coord_x"] = np.cos(lat_rad) * np.cos(lon_rad)
    df_feat["coord_y"] = np.cos(lat_rad) * np.sin(lon_rad)
    df_feat["coord_z"] = np.sin(lat_rad)

    # 2. engineer numerical features
    outbound_dt = pd.to_datetime(df_feat["outbound_departs"], errors="coerce")
    return_dt = pd.to_datetime(df_feat["return_departs"], errors="coerce")

    duration_days = (return_dt - outbound_dt).dt.total_seconds() / (24 * 3600)
    df_feat["trip_duration_days"] = duration_days.fillna(1.0).apply(lambda x: max(x, 1.0))
    df_feat["dep_hour"] = outbound_dt.dt.hour.fillna(12.0).astype(float)
    df_feat["is_weekend_dep"] = outbound_dt.dt.dayofweek.isin([4, 5]).astype(float)

    # 3. separate continuous and binary features
    continuous_cols = [
        "coord_x",
        "coord_y",
        "coord_z",
        "price_usd",
        "outbound_layovers",
        "return_layovers",
        "trip_duration_days",
        "dep_hour"
    ]

    # 4. fit or apply scaler
    if scaler is None:
        scaler = StandardScaler()
        df_feat[continuous_cols] = scaler.fit_transform(df_feat[continuous_cols])
    else:
        df_feat[continuous_cols] = scaler.transform(df_feat[continuous_cols])

    selected_features = continuous_cols + ["is_weekend_dep"]

    return df_feat[selected_features], scaler, continuous_cols


class TripsDataset(Dataset):
    """PyTorch Dataset wrapper storing features, tensor X, and the fitted StandardScaler."""

    def __init__(self, db_path: str = "trips.db"):
        self.db_path = db_path
        self.df_raw = load_raw_trip_data(self.db_path)

        if self.df_raw.empty:
            raise ValueError(f"No records found in {db_path}. Please run fetch_data.py to save trips first!")

        # clean, scale, and store the fit scaler instance
        self.df_features, self.scaler, self.continuous_cols = clean_raw_data(self.df_raw)
        self.feature_names = list(self.df_features.columns)

        # convert to df to tensor
        features_np = self.df_features.to_numpy(dtype=np.float32)
        self.X = torch.from_numpy(features_np)

    def __len__(self) -> int:
        return self.X.shape[0]

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.X[idx]

    # converts scaled tensor rows back to original unscaled units
    def unscale_continuous_features(self, tensor_data: torch.Tensor) -> pd.DataFrame:
        # pandas df and scikit-learn require a 2D matrix instead of a 1D vector
        if tensor_data.ndim == 1:
            tensor_data = tensor_data.unsqueeze(0)

        # converts tensor back to df
        np_data = tensor_data.detach().cpu().numpy()
        df_scaled = pd.DataFrame(np_data, columns=self.feature_names)

        # revert scaling on continuous columns using the saved scaler
        df_unscaled = df_scaled.copy()
        df_unscaled[self.continuous_cols] = self.scaler.inverse_transform(df_scaled[self.continuous_cols])

        return df_unscaled

def score_and_rank_trips(dataset: TripsDataset, preference_weights: torch.Tensor) -> pd.DataFrame:
    if preference_weights.ndim == 1:
        preference_weights = preference_weights.unsqueeze(1)

    scores = dataset.X @ preference_weights

    # insert new "match_score" column into "df_ranked"
    df_ranked = dataset.df_raw.copy()
    df_ranked["match_score"] = scores.squeeze().detach().cpu().numpy()

    df_ranked = df_ranked.sort_values(by="match_score", ascending=False).reset_index(drop=True)
    df_ranked.index += 1

    return df_ranked

def main():
    try:
        dataset = TripsDataset("trips.db")
        print("=== TripsDataset Loaded Successfully ===")
        print(f"Number of samples (n):   {len(dataset)}")
        print(f"Number of features (d):  {len(dataset.feature_names)}")
        print(f"Feature Names:           {dataset.feature_names}\n")

        W = torch.tensor(
            [[0.0], [0.0], [0.0], [-0.8], [-0.4], [-0.4], [0.5], [0.1], [0.6]],
            dtype=torch.float32,
        )

        # Calculate scores and rank trips
        ranked_df = score_and_rank_trips(dataset, W)

        print("=== TOP RANKED TRIPS ===")
        display_cols = ["destination_id", "price_usd", "outbound_layovers", "airline", "match_score"]
        print(ranked_df[display_cols].head())

    except ValueError as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    main()