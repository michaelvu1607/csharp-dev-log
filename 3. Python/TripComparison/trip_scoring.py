import os
import json
import torch
import pandas as pd
from google import genai
from google.genai import types

from schema import UserPreferenceSchema
from dataset import TripsDataset, score_and_rank_trips
from enrich_destinations import enrich_missing_metadata

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-3.6-flash"


def parse_user_query(query_text: str) -> UserPreferenceSchema:
    """Uses Gemini Structured Outputs to extract user preferences from natural language."""
    print("Parsing user query with Gemini...")

    system_instruction = (
        "Analyze the user query and assign preference values between 0.0 and 1.0 for all relevant PreferenceWeights fields. "
        "IMPORTANT: Distinguish carefully between target_country and target_region. "
        "If the user mentions a continent or broad geographical region (e.g., 'Southeast Asia', 'Europe', 'Asia'), set target_region to that region and leave target_country as None. "
        "Only set target_country if a specific country is named (e.g., 'Thailand', 'Indonesia', 'Japan')."
    )

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Extract user travel preferences from this query: '{query_text}'",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=UserPreferenceSchema,
            system_instruction=system_instruction
        )
    )

    return UserPreferenceSchema.model_validate_json(response.text)


def map_pydantic_to_tensor_weights(preferences: UserPreferenceSchema) -> torch.Tensor:
    """
    Maps Pydantic preference weights to PyTorch feature dimension W.
    Dimension sequence (9 continuous/binary features):
    [coord_x, coord_y, coord_z, price_usd, avg_daily_cost_usd, outbound_layovers, return_layovers, dep_hour, is_weekend_dep]
    """
    preference_weights = [
        0.0,
        0.0,
        0.0,
        -1.0 * preferences.weights.budget,
        -1.0 * preferences.weights.budget,
        -1.0 * preferences.weights.direct_flights_only,
        -1.0 * preferences.weights.direct_flights_only,
        0.5 * preferences.weights.convenient_departure_time,
        1.0 * preferences.weights.weekend_departure
    ]

    return torch.tensor(preference_weights, dtype=torch.float32).unsqueeze(1)


def generate_recommendation_summary(query: str, ranked_trips: pd.DataFrame) -> str:
    """Sends top ranked trips back to Gemini to produce a natural language recommendation."""
    top_3 = ranked_trips.head(3).to_dict(orient="records")

    prompt = f"""
    The user asked: "{query}"

    Based on our PyTorch vector scoring model, here are the top matching trip options:
    {json.dumps(top_3, indent=2, default=str)}

    Provide a concise, friendly recommendation explaining why the #1 option best matches 
    their request and highlight any trade-offs.
    """

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text


def query():
    user_prompt = input("Prompt: ")

    print("Checking and enriching destination metadata...")
    enrich_result = enrich_missing_metadata(batch_size=50, db_name="seed.db")
    if enrich_result["failures"]:
        for failure in enrich_result["failures"]:
            print(f"[Warning] Destination '{failure['destination_id']}' missing fields: {failure['missing_fields']}. Reason: {failure['reason']}")

    user_prefs = parse_user_query(user_prompt)

    try:
        dataset = TripsDataset(
            "seed.db",
            target_duration=user_prefs.duration_days,
            tolerance_days=user_prefs.tolerance_days or 2,
            target_country=user_prefs.target_country,
            target_region=user_prefs.target_region
        )
    except ValueError:
        # Fallback query without country/region lock
        print("[Notice] No strict region matches found in seed database. Searching global destinations...")
        dataset = TripsDataset(
            "seed.db",
            target_duration=user_prefs.duration_days,
            tolerance_days=user_prefs.tolerance_days or 3,
            target_country=None,
            target_region=None
        )

    W = map_pydantic_to_tensor_weights(user_prefs)
    ranked_df = score_and_rank_trips(dataset, W)

    final_recommendation = generate_recommendation_summary(user_prompt, ranked_df)
    print(final_recommendation)