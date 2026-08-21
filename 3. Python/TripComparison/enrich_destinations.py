import sqlite3
import json
import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()

# Configure built-in SDK HTTP retry handling for rate limits (429) & server errors (5xx)
retry_options = types.HttpRetryOptions(
    attempts=5,
    initial_delay=3.0,
    max_delay=60.0,
    http_status_codes=[408, 429, 500, 502, 503, 504]
)

client = genai.Client(http_options={"retry_options": retry_options})

# Define schema for structured Gemini output
class DestinationMetadata(BaseModel):
    destination_id: str
    climate_zone: str = Field(description="e.g., tropical, mediterranean, temperate, arid, polar")
    avg_daily_cost_usd: float = Field(description="Estimated mid-range daily budget in USD")
    vibe_tags: str = Field(description="Comma-separated tags, e.g., 'nightlife,culture,beach,budget'")

class EnrichmentResponse(BaseModel):
    destinations: List[DestinationMetadata]

def enrich_missing_metadata(batch_size: int = 20, db_name: str = "seed.db") -> Dict[str, Any]:
    """
    Finds destinations with NULL metadata, calls Gemini API to enrich them,
    and updates the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Fetch destinations missing metadata
    cursor.execute("""
        SELECT destination_id, city_name, country 
        FROM destinations 
        WHERE climate_zone IS NULL OR avg_daily_cost_usd IS NULL OR vibe_tags IS NULL
        LIMIT ?
    """, (batch_size,))

    rows = cursor.fetchall()
    if not rows:
        conn.close()
        return {"status": "success", "enriched_count": 0, "failures": []}

    cities_payload = [{"destination_id": r[0], "city": r[1], "country": r[2]} for r in rows]
    prompt = f"""
    Analyze the following list of destination cities and provide accurate travel metadata:
    {json.dumps(cities_payload, indent=2)}
    """

    failures = []
    enriched_count = 0

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=EnrichmentResponse,
                temperature=0.2,
            ),
        )

        parsed_data = EnrichmentResponse.model_validate_json(response.text)

        for item in parsed_data.destinations:
            cursor.execute("""
                UPDATE destinations 
                SET climate_zone = ?, avg_daily_cost_usd = ?, vibe_tags = ?
                WHERE destination_id = ?
            """, (item.climate_zone, item.avg_daily_cost_usd, item.vibe_tags, item.destination_id))
            enriched_count += 1

        conn.commit()

        time.sleep(1.5)

    except APIError as e:
        for city in cities_payload:
            failures.append({
                "destination_id": city["destination_id"],
                "missing_fields": ["climate_zone", "avg_daily_cost_usd", "vibe_tags"],
                "reason": f"Gemini API enrichment error ({e.code}): {e.message}"
            })
    except Exception as e:
        for city in cities_payload:
            failures.append({
                "destination_id": city["destination_id"],
                "missing_fields": ["climate_zone", "avg_daily_cost_usd", "vibe_tags"],
                "reason": f"Unexpected error: {str(e)}"
            })

    conn.close()
    return {"status": "completed", "enriched_count": enriched_count, "failures": failures}

if __name__ == "__main__":
    result = enrich_missing_metadata(batch_size=20, db_name="seed.db")
    print(f"Enrichment finished. Enriched {result['enriched_count']} destinations.")
    if result["failures"]:
        for fail in result["failures"]:
            print(f"Warning: {fail['destination_id']} missing {fail['missing_fields']}. Reason: {fail['reason']}")