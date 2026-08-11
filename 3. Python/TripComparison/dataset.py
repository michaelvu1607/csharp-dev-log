from google import genai
from google.genai import types
import pandas as pd
from pydantic import BaseModel, Field
import torch
import torch.nn as nn
import sqlite3
import numpy as np
import torch
from torch.utils.data import Dataset

# queries sql database and joins destination and flight tables on destination_id
def load_raw_trip_data(db_name = "trips.db"):
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

def clean_raw_data(df: pd.DataFrame):
    df_feat = df.copy()

    # column #1: core numerical features
    cols1 = [
        "latitude",
        "longitude",
        "price_usd",
        "outbound_layovers",
        "return_layovers",
    ]

    for col in cols1:
        df_feat[col] = pd.to_numeric(df_feat[col], errors="coerce")

    essential_cols = ["latitude", "longitude", "price_usd"]
    df_feat = df_feat.dropna(subset=essential_cols)

    df_feat["outbound_layovers"] = df_feat["outbound_layovers"].fillna(0.0)
    df_feat["return_layovers"] = df_feat["return_layovers"].fillna(0.0)

    # column #2: engineered numerical features

    df_feat["outbound_layovers"] = df_feat["outbound_layovers"].fillna(0.0)
    df_feat["return_layovers"] = df_feat["return_layovers"].fillna(0.0)

    outbound_dt = pd.to_datetime(["outbound_layovers"], errors="coerce")
    return_dt = pd.to_datetime(["return_layovers"], errors="coerce")

    duration_days = (return_dt - outbound_dt).dt.total_seconds() / (24 * 3600)
    df_feat["trip_duration_days"] = duration_days
    df_feat["dep_hour"] = outbound_dt.dt.hour.astype(float)
    df_feat["is_weekend_dep"] = outbound_dt.dt.dayofweek.isin([4,5]).astype(float)

    # df_feat["total_estimated_cost"] = df_feat["avg_daily_cost"] * df_feat["trip_duration_days"] + df_feat["price_usd"]

    selected_features = [
        "latitude", "longitude", "avg_daily_cost_usd", "price_usd",
        "outbound_layovers", "return_layovers", "trip_duration_days",
        "dep_hour", "is_weekend_dep", "total_estimated_cost"
    ]

    return df_feat[selected_features]