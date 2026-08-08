import os
from dotenv import load_dotenv
import requests

# Load API key
load_dotenv()
DUFFEL_TOKEN = os.getenv("DUFFEL_API_KEY")


def search_flights(origin_iata, destination_iata, departure_date, adults=1):
  """Searches for flights using Duffel REST API v2 directly."""
  print(
      f"🔍 Searching flights from {origin_iata} to {destination_iata} on"
      f" {departure_date}..."
  )

  # Duffel Offer Requests endpoint (with return_offers=true)
  url = "https://api.duffel.com/air/offer_requests?return_offers=true"

  headers = {
      "Authorization": f"Bearer {DUFFEL_TOKEN}",
      "Duffel-Version": "v2",  # Explicitly set to supported API version!
      "Content-Type": "application/json",
      "Accept": "application/json",
  }

  payload = {
      "data": {
          "slices": [{
              "origin": origin_iata,
              "destination": destination_iata,
              "departure_date": departure_date,
          }],
          "passengers": [{"type": "adult"} for _ in range(adults)],
          "cabin_class": "economy",
      }
  }

  # Make the HTTP POST request
  response = requests.post(url, headers=headers, json=payload)
  res_data = response.json()

  # Check for API errors
  if response.status_code not in (200, 201):
    print("❌ Error from Duffel API:", res_data)
    return

  # Extract flight offers
  offers = res_data.get("data", {}).get("offers", [])
  print(f"✅ Found {len(offers)} flight options!\n")

  # Loop through top 5 results
  for idx, offer in enumerate(offers[:5], start=1):
    amount = offer.get("total_amount")
    currency = offer.get("total_currency")
    airline_name = offer.get("owner", {}).get("name")

    first_segment = offer["slices"][0]["segments"][0]
    dep_time = first_segment.get("departing_at")
    arr_time = first_segment.get("arriving_at")

    print(f"Option #{idx}: {airline_name}")
    print(f"  Price: {amount} {currency}")
    print(f"  Departs: {dep_time}")
    print(f"  Arrives: {arr_time}")
    print("-" * 40)


# --- Example Call ---
search_flights(
    origin_iata="DTW",
    destination_iata="LHR",
    departure_date="2026-10-15",
    adults=1,
)