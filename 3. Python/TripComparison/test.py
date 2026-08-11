import math
import os
import sqlite3
import airportsdata
import requests
from dotenv import load_dotenv
from duffel_api import Duffel
from google import genai
from google.genai import types
import pandas as pd
from pydantic import BaseModel, Field
import torch
import torch.nn as nn
from datetime import datetime, timedelta

load_dotenv()
DUFFEL_TOKEN = os.getenv("DUFFEL_API_KEY")
client = Duffel(access_token=DUFFEL_TOKEN)

METRO_CITY_CODES = {
    "new_york": "NYC",
    "chicago": "CHI",
    "london": "LON",
    "paris": "PAR",
    "tokyo": "TYO",
    "washington": "WAS",
    "san_francisco": "SFO",
    "los_angeles": "LAX",
    "toronto": "YTO",
    "miami": "MIA",
    "dallas": "DFW",
    "seattle": "SEA"
}


def calculate_distance(lat1, lon1, lat2, lon2):
    distance = math.hypot(lat1 - lat2, lon1 - lon2)
    return distance


def get_nearest_airport(userlat, userlon):
    airports = airportsdata.load('IATA')

    skip_keywords = [
        # --- Private & General Aviation ---
        "private", "executive", "exec", "airpark", "airstrip", "strip",
        "fly-in", "ranch", "estate", "club", "flying club", "gliderport",
        "ultralight", "skydive", "dropzone",
        # --- Specialized & Non-Standard Facilities ---
        "heliport", "helipad", "seaplane", "sea plane", "water aerodrome",
        "water runway", "stolport",
        # --- Municipal & Local Unscheduled Airfields ---
        "municipal", "county", "township", "local", "reliever", "auxiliary",
        "field",
        # --- Medical & Emergency ---
        "hospital", "medical", "clinic", "health", "life flight",
        # --- Military & Government Air Bases ---
        "military", "air force base", "afb", "raf", "naval", "nas",
        "army", "aaf", "base", "garrison", "barracks", "joint reserve",
        # --- Specific Known Non-Commercial Hubs / Outliers ---
        "teterboro", "van nuys", "centennial"
    ]

    commercial_airports = [
        airport for airport in airports.values()
        if not any(keyword in airport["name"].lower() for keyword in skip_keywords)
    ]

    closest = min(commercial_airports,
                  key=lambda coords: calculate_distance(userlat, userlon, coords['lat'], coords['lon']))
    return closest


# Returns an IATA Metro Code if the city is a known multi-airport region, otherwise calculates the nearest commercial airport code spatially.
def resolve_location_to_iata(geo_data: dict) -> str:
    clean_city = geo_data["city_name"].lower().replace(" ", "_")

    # check if the city has a designated metro code
    if clean_city in METRO_CITY_CODES:
        metro_code = METRO_CITY_CODES[clean_city]
        print(f"Using Metro Code '{metro_code}' for {geo_data['city_name']}")
        return metro_code

    # fall back to spatial calculation for smaller cities
    nearest = get_nearest_airport(geo_data["latitude"], geo_data["longitude"])
    if nearest:
        iata_code = nearest.get("iata")
        print(f"Nearest Airport for {geo_data['city_name']}: {nearest.get('name')} ({iata_code})")
        return iata_code

    return None


# searches for location if not already in database
def geocode_city(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return None

        result = data["results"][0]

        clean_city = result["name"].lower().replace(" ", "_")
        clean_country = (
            result.get("country", "unknown").lower().replace(" ", "_")
        )

        return {
            "destination_id": f"{clean_city}_{clean_country}",
            "city_name": result["name"],
            "country": result.get("country", "Unknown"),
            "latitude": result["latitude"],
            "longitude": result["longitude"],

            # need to use other APIs to find this information
            "airport_code": result.get("airport", "Unknown"),
            "climate_zone": result.get("climate_zone", "Unknown"),
            "avg_daily_cost_usd": result.get("cost", "Unknown"),
            "vibe_tags": result.get("vibe", "Unknown")
        }
    except requests.RequestException as e:
        print(f"Error reaching Geocoding API: {e}")
        return None


# prints top one way flight options
def search_flights(destination_id, origin_iata, destination_iata, departure_date, cabin_class, return_date, adults=1):
    print(f"Searching flights from {origin_iata} to {destination_iata} on {departure_date}")

    url = "https://api.duffel.com/air/offer_requests?return_offers=true"

    headers = {
        "Authorization": f"Bearer {DUFFEL_TOKEN}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    slices = [{
        "origin": origin_iata,
        "destination": destination_iata,
        "departure_date": departure_date
    }]

    if return_date:
        slices.append({
            "origin": destination_iata,
            "destination": origin_iata,
            "departure_date": return_date
        })

    payload = {
        "data":
            {
                "slices": slices,
                "passengers": [{"type": "adult"} for _ in range(adults)],
                "cabin_class": cabin_class
            }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if response.status_code not in (200, 201):
        print("Error from Duffel API:", data)
        return []

    offers = data.get("data", {}).get("offers", [])
    parsed_offers = []

    for offer in offers[:5]:
        slices = offer.get("slices", [])

        # Extract Outbound Slice (always index 0)
        outbound_slice = slices[0] if len(slices) > 0 else {}
        out_segments = outbound_slice.get("segments", [])

        # Extract Return Slice (index 1 if round-trip, else None)
        return_slice = slices[1] if len(slices) > 1 else None
        ret_segments = return_slice.get("segments", []) if return_slice else []

        # Helper to format layovers safely
        out_layovers = "Direct" if len(out_segments) == 1 else f"{len(out_segments) - 1} layover(s)"
        ret_layovers = ("Direct" if len(ret_segments) == 1 else f"{len(ret_segments) - 1} layover(s)") if return_slice else None

        parsed_offers.append({
            "flight_id": offer.get("id"),
            "airline": offer.get("owner", {}).get("name"),
            "price_usd": offer.get("total_amount"),

            # Outbound Details
            "outbound_origin": origin_iata,
            "outbound_destination": destination_iata,
            "outbound_departs": out_segments[0].get("departing_at") if out_segments else None,
            "outbound_arrives": out_segments[-1].get("arriving_at") if out_segments else None,
            "outbound_layovers": out_layovers,

            # Return Details
            "has_return": return_slice is not None,
            "return_origin": destination_iata if return_slice else None,
            "return_destination": origin_iata if return_slice else None,
            "return_departs": ret_segments[0].get("departing_at") if ret_segments else None,
            "return_arrives": ret_segments[-1].get("arriving_at") if ret_segments else None,
            "return_layovers": ret_layovers,
        })

    return parsed_offers

def get_flight_data(geo_data_user_location, geo_data_destination, flight_inputs):
    # user location info
    if not geo_data_user_location:
        print(f"Could not find user location: '{geo_data_user_location}'")
        return None

    user_origin_code_iata = resolve_location_to_iata(geo_data_user_location)
    destination_origin_code_iata = resolve_location_to_iata(geo_data_destination)

    if not user_origin_code_iata or not destination_origin_code_iata:
        print("Could not resolve valid flight origin or destination airport.")
        return None

    destination_id = geo_data_destination["destination_id"]
    departure_date, cabin_class, num_adults, round_trip, return_date = flight_inputs
    parsed_offers = search_flights(destination_id, user_origin_code_iata, destination_origin_code_iata, departure_date, cabin_class, return_date, num_adults)

    return parsed_offers


def get_destination_data(destination_city):
    connection = sqlite3.connect("trips.db", timeout=10)

    try:
        cursor = connection.cursor()

        # searches through database to find location
        cursor.execute(
            "SELECT * FROM destinations WHERE city_name LIKE ?", (f"%{destination_city}%",)
        )

        match = cursor.fetchone()

        # assign values to location information in the database instead of using geocode for better speed
        if match:
            (destination_id,
             city_name,
             country,
             latitude,
             longitude,
             airport_code,
             climate_zone,
             avg_daily_cost_usd,
             vibe_tags) = match

            print("Location found!")

            clean_city = city_name.lower().replace(" ", "_")
            clean_country = country.lower().replace(" ", "_")

            # update geo data
            return {
                "destination_id": f"{clean_city}_{clean_country}",
                "city_name": city_name,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,

                # Null for now
                "airport_code": airport_code,
                "climate_zone": climate_zone,
                "avg_daily_cost_usd": avg_daily_cost_usd,
                "vibe_tags": vibe_tags
            }

        # location not found in database -> use geocode_city to search using API
        geo_data = geocode_city(destination_city)
        print(f"'{destination_city}' not in cache. Fetching location via Geocoding API")
        if not geo_data:
            print(f"Could not find {destination_city}")
            return None

        print(f"Found {geo_data["city_name"].replace("_", " ").title()}, {geo_data["country"].replace("_", " ").title()}")

        return geo_data

    finally:
        connection.close()


def search():
    while True:
        user_location = input("Enter your location: ")
        destination_city = input("Enter your destination: ")
        if destination_city == "0":
            break

        departure_date = input("Enter a departure date [YYYY-MM-DD]: ")
        cabin_class = input("Enter a cabin class [economy, premium_economy, business, first]: ")
        num_adults = int(input("Enter the number of adults boarding: "))
        round_trip = input("Are you planning on returning? [y/n]: ")

        return_date = None
        if round_trip == "y":
            return_date = input("Enter a return date [YYYY-MM-DD]: ")

        flight_inputs = (departure_date, cabin_class, num_adults, round_trip, return_date)

        geo_data_user_location = geocode_city(user_location)
        if not geo_data_user_location:
            print(f"Could not resolve user location: '{user_location}'")
            continue

        geo_data_destination = get_destination_data(destination_city)
        if not geo_data_destination:
            continue

        parsed_offers = get_flight_data(geo_data_user_location, geo_data_destination, flight_inputs)

        if parsed_offers:
            print("\n--- Available Flight Options ---")
            for idx, offer in enumerate(parsed_offers, start=1):
                print(f"Option #{idx}: {offer['airline']} — Total: ${offer['price_usd']}")
                print(f"  Outbound ({offer['outbound_layovers']}): {offer['outbound_origin']} ➔ {offer['outbound_destination']}")
                print(f"  Departs: {offer['outbound_departs']} | Arrives: {offer['outbound_arrives']}")

                if offer["has_return"]:
                    print(f"  Return ({offer['return_layovers']}): {offer['return_origin']} ➔ {offer['return_destination']}")
                    print(f"  Departs: {offer['return_departs']} | Arrives: {offer['return_arrives']}")

                print("-" * 45)

            cont = input("Check another location? [y/n]: ")
            if cont == "n":
                break

if __name__ == "__main__":
    search()