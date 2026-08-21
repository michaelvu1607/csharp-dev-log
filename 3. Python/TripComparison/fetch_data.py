import math
import os
import sqlite3
import airportsdata
import requests
from dotenv import load_dotenv
from duffel_api import Duffel
from enrich_destinations import enrich_missing_metadata

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
    return math.hypot(lat1 - lat2, lon1 - lon2)


def get_nearest_airport(userlat, userlon):
    airports = airportsdata.load('IATA')

    skip_keywords = [
        "private", "executive", "exec", "airpark", "airstrip", "strip",
        "fly-in", "ranch", "estate", "club", "flying club", "gliderport",
        "ultralight", "skydive", "dropzone", "heliport", "helipad", "seaplane",
        "sea plane", "water aerodrome", "water runway", "stolport", "municipal",
        "county", "township", "local", "reliever", "auxiliary", "field",
        "hospital", "medical", "clinic", "health", "life flight", "military",
        "air force base", "afb", "raf", "naval", "nas", "army", "aaf", "base",
        "garrison", "barracks", "joint reserve", "teterboro", "van nuys", "centennial"
    ]

    commercial_airports = [
        airport for airport in airports.values()
        if not any(keyword in airport["name"].lower() for keyword in skip_keywords)
    ]

    closest = min(commercial_airports, key=lambda coords: calculate_distance(userlat, userlon, coords['lat'], coords['lon']))
    return closest


def resolve_location_to_iata(geo_data):
    clean_city = geo_data["city_name"].lower().replace(" ", "_")

    if clean_city in METRO_CITY_CODES:
        metro_code = METRO_CITY_CODES[clean_city]
        print(f"Using Metro Code '{metro_code}' for {geo_data['city_name']}")
        return metro_code

    nearest = get_nearest_airport(geo_data["latitude"], geo_data["longitude"])
    if nearest:
        iata_code = nearest.get("iata")
        print(f"Nearest Airport for {geo_data['city_name']}: {nearest.get('name')} ({iata_code})")
        return iata_code

    return None


def geocode_city(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            print(f"[Notice] Geocoding API returned no location results for '{city_name}'. Reason: City name not found.")
            return None

        result = data["results"][0]

        clean_city = result["name"].lower().replace(" ", "_")
        clean_country = result.get("country", "unknown").lower().replace(" ", "_")

        return {
            "destination_id": f"{clean_city}_{clean_country}",
            "city_name": result["name"],
            "country": result.get("country", "Unknown"),
            "region": result.get("admin1", "Unknown").lower(),
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "airport_code": None,
            "climate_zone": None,
            "avg_daily_cost_usd": None,
            "vibe_tags": None
        }
    except requests.RequestException as e:
        print(f"Error reaching Geocoding API for '{city_name}': {e}")
        return None


def search_flights(origin_iata, destination_iata, departure_date, cabin_class, return_date, adults=1):
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
        "data": {
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
        outbound_slice = slices[0] if len(slices) > 0 else {}
        out_segments = outbound_slice.get("segments", [])

        return_slice = slices[1] if len(slices) > 1 else None
        ret_segments = return_slice.get("segments", []) if return_slice else []

        out_layovers = 0 if len(out_segments) == 1 else max(0, len(out_segments) - 1)
        ret_layovers = (0 if len(ret_segments) == 1 else max(0, len(ret_segments) - 1)) if return_slice else 0

        parsed_offers.append({
            "flight_id": offer.get("id"),
            "airline": offer.get("owner", {}).get("name"),
            "price_usd": offer.get("total_amount"),
            "outbound_origin": origin_iata,
            "outbound_destination": destination_iata,
            "outbound_departs": out_segments[0].get("departing_at") if out_segments else None,
            "outbound_arrives": out_segments[-1].get("arriving_at") if out_segments else None,
            "outbound_layovers": out_layovers,
            "has_return": return_slice is not None,
            "return_origin": destination_iata if return_slice else None,
            "return_destination": origin_iata if return_slice else None,
            "return_departs": ret_segments[0].get("departing_at") if ret_segments else None,
            "return_arrives": ret_segments[-1].get("arriving_at") if ret_segments else None,
            "return_layovers": ret_layovers,
        })

    return parsed_offers


def get_flight_data(geo_data_user_location, geo_data_destination, flight_inputs):
    if not geo_data_user_location:
        print("[Notice] Missing user location details. Reason: Location could not be geocoded.")
        return None

    user_origin_code_iata = resolve_location_to_iata(geo_data_user_location)
    destination_origin_code_iata = resolve_location_to_iata(geo_data_destination)

    if not user_origin_code_iata or not destination_origin_code_iata:
        print("[Notice] Missing airport code. Reason: Distance mapping failed to locate a commercial airport.")
        return None

    departure_date, cabin_class, num_adults, round_trip, return_date = flight_inputs
    parsed_offers = search_flights(user_origin_code_iata, destination_origin_code_iata, departure_date, cabin_class, return_date, num_adults)

    return parsed_offers


def get_destination_data(destination_city):
    connection = sqlite3.connect("trips.db", timeout=10)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT destination_id, city_name, country, region, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags FROM destinations WHERE city_name LIKE ?",
            (f"%{destination_city}%",)
        )

        match = cursor.fetchone()

        if match:
            (destination_id, city_name, country, region, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags) = match
            print("Location found in database!")

            clean_city = city_name.lower().replace(" ", "_")
            clean_country = country.lower().replace(" ", "_")

            if climate_zone is None or avg_daily_cost_usd is None or vibe_tags is None:
                print(f"[Notice] Destination '{city_name}' is missing metadata (climate/cost/tags). Triggering enrichment...")
                enrich_missing_metadata(batch_size=10, db_name="trips.db")

            return {
                "destination_id": f"{clean_city}_{clean_country}",
                "city_name": city_name,
                "country": country,
                "region": region,
                "latitude": latitude,
                "longitude": longitude,
                "airport_code": airport_code,
                "climate_zone": climate_zone,
                "avg_daily_cost_usd": avg_daily_cost_usd,
                "vibe_tags": vibe_tags
            }

        geo_data = geocode_city(destination_city)
        print(f"'{destination_city}' not in cache. Fetching location via Geocoding API.")
        if not geo_data:
            print(f"[Notice] Destination '{destination_city}' could not be resolved. Reason: Geocoding lookup failed.")
            return None

        return geo_data

    finally:
        connection.close()


def save_to_db(destination_data, flight_data):
    connection = sqlite3.connect("trips.db", timeout=10)

    try:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO destinations
        (destination_id, city_name, country, region, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            destination_data["destination_id"],
            destination_data["city_name"],
            destination_data["country"],
            destination_data.get("region", "unknown"),
            destination_data["latitude"],
            destination_data["longitude"],
            destination_data["airport_code"],
            destination_data["climate_zone"],
            destination_data["avg_daily_cost_usd"],
            destination_data["vibe_tags"]
        ))

        cursor.execute("""
        INSERT OR REPLACE INTO flights
        (flight_id, destination_id, origin_code, destination_code, outbound_departs, outbound_arrives, has_return, return_departs, return_arrives, price_usd, airline, outbound_layovers, return_layovers)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            flight_data["flight_id"],
            flight_data["destination_id"],
            flight_data["outbound_origin"],
            flight_data["outbound_destination"],
            flight_data["outbound_departs"],
            flight_data["outbound_arrives"],
            flight_data["has_return"],
            flight_data["return_departs"],
            flight_data["return_arrives"],
            flight_data["price_usd"],
            flight_data["airline"],
            flight_data["outbound_layovers"],
            flight_data["return_layovers"]
        ))

        connection.commit()
        print(f"Saved flight '{flight_data['flight_id']}' and destination '{destination_data['destination_id']}' to database.")

        enrich_missing_metadata(batch_size=10, db_name="trips.db")

    except sqlite3.Error as error:
        print(f"An error occurred while saving to database: {error}")

    finally:
        connection.close()


def search():
    while True:
        user_location = input("Enter your location: ")
        destination_city = input("Enter your destination (or '0' to exit): ")
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
            num_flight_options = 0
            print("\n--- Available Flight Options ---")
            for idx, offer in enumerate(parsed_offers, start=1):
                print(f"Option #{idx}: {offer['airline']} — Total: ${offer['price_usd']}")
                print(f"  Outbound ({offer['outbound_layovers']} layovers): {offer['outbound_origin']} ➔ {offer['outbound_destination']}")
                print(f"  Departs: {offer['outbound_departs']} | Arrives: {offer['outbound_arrives']}")
                num_flight_options += 1

                if offer["has_return"]:
                    print(f"  Return ({offer['return_layovers']} layovers): {offer['return_origin']} ➔ {offer['return_destination']}")
                    print(f"  Departs: {offer['return_departs']} | Arrives: {offer['return_arrives']}")

                print("-" * 45)

            range_flight_options = f"1-{num_flight_options}" if num_flight_options > 1 else "1"
            flight_option = int(input(f"Which would you like to save for later? [{range_flight_options} | 0]: "))

            if 1 <= flight_option <= num_flight_options:
                selected_offer = parsed_offers[flight_option - 1]

                destination_data = {
                    "destination_id": geo_data_destination["destination_id"],
                    "city_name": geo_data_destination["city_name"],
                    "country": geo_data_destination["country"],
                    "region": geo_data_destination.get("region", "unknown"),
                    "latitude": geo_data_destination["latitude"],
                    "longitude": geo_data_destination["longitude"],
                    "airport_code": geo_data_destination["airport_code"],
                    "climate_zone": geo_data_destination["climate_zone"],
                    "avg_daily_cost_usd": geo_data_destination["avg_daily_cost_usd"],
                    "vibe_tags": geo_data_destination["vibe_tags"]
                }

                flight_data = {
                    "flight_id": selected_offer.get("flight_id"),
                    "destination_id": geo_data_destination["destination_id"],
                    "outbound_origin": selected_offer.get("outbound_origin"),
                    "outbound_destination": selected_offer.get("outbound_destination"),
                    "outbound_departs": selected_offer.get("outbound_departs"),
                    "outbound_arrives": selected_offer.get("outbound_arrives"),
                    "has_return": selected_offer.get("has_return"),
                    "return_departs": selected_offer.get("return_departs"),
                    "return_arrives": selected_offer.get("return_arrives"),
                    "price_usd": selected_offer.get("price_usd"),
                    "airline": selected_offer.get("airline"),
                    "outbound_layovers": selected_offer.get("outbound_layovers"),
                    "return_layovers": selected_offer.get("return_layovers")
                }

                save_to_db(destination_data, flight_data)

            cont = input("Check another location? [y/n]: ")
            if cont == "n":
                break