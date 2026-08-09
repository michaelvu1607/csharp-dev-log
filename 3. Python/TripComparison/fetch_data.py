import sqlite3
import requests
from duffel_api import Duffel
import os
from dotenv import load_dotenv
import math
import airportsdata

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

    closest = min(commercial_airports, key=lambda coords: calculate_distance(userlat, userlon, coords['lat'], coords['lon']))
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

def get_destination_data(city_name, user_location):
    with sqlite3.connect('trips.db') as connection:
        cursor = connection.cursor()

        # searches through database to find location
        cursor.execute(
            "SELECT * FROM destinations WHERE city_name LIKE ?", (f"%{city_name}%",)
        )

        match = cursor.fetchone()

        # set variables equal to the match
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

            # update data
            geo_data = {
                "destination_id": destination_id,
                "latitude": latitude,
                "longitude": longitude,
                "city_name": city_name,
            }

            get_weather_data(geo_data, connection)

            get_flight_data(user_location, geo_data, connection)
            return match

        # location not found in database -> use geocode_city to search using API
        geo_data = geocode_city(city_name)

        print(f"'{city_name}' not in cache. Fetching location via Geocoding API")
        if not geo_data:
            print(f"Could not find {city_name}")
            return None

        # update database with new location
        cursor.execute("""
        INSERT OR REPLACE INTO destinations
        (destination_id, city_name, country, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            geo_data["destination_id"],
            geo_data["city_name"],
            geo_data["country"],
            geo_data["latitude"],
            geo_data["longitude"],
            geo_data["airport_code"],
            geo_data["climate_zone"],
            geo_data["avg_daily_cost_usd"],
            geo_data["vibe_tags"]
        ))

        print(f"Found {geo_data["city_name"].replace("_"," ").title()}, {geo_data["country"].replace("_"," ").title()}")

        get_flight_data(user_location, geo_data, connection)
        get_weather_data(geo_data, connection)

        # return the new location now saved in the database
        cursor.execute(
            "SELECT * FROM destinations WHERE destination_id = ?",
            (geo_data["destination_id"],)
        )
        new_match = cursor.fetchone()
        return new_match

# prints top one way flight options
def search_flights(origin_iata, destination_iata, departure_date, cabin_class, connection, adults=1, return_date=None):
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
        print("Error from Duffel API:")
        return

    offers = data.get("data", {}).get("offers", [])
    print(f"Found {len(offers)} flight options\n")

    for idx, offer in enumerate(offers[:5], start=1):
        amount = offer.get("total_amount")
        currency = offer.get("total_currency")
        airline_name = offer.get("owner", {}).get("name")

        print(f"Option #{idx}: {airline_name} — Total: {amount} {currency} ({adults} adult(s))")

        cursor = connection.cursor()

        for s_idx, flight_slice in enumerate(offer["slices"], start=1):
            segments = flight_slice["segments"]
            dep_time = segments[0].get("departing_at")
            arr_time = segments[-1].get("arriving_at")
            num_layovers = len(segments) - 1
            label = "Outbound" if s_idx == 1 else "Return"
            layover_type = "Direct" if num_layovers == 0 else f"{num_layovers} layovers"

            location = segments[0]["origin"]
            destination = segments[-1]["destination"]

            orig_code = location.get("iata_code") or location.get("iata") or "N/A"
            dest_code = destination.get("iata_code") or destination.get("iata") or "N/A"

            print(f"  {label} - {layover_type} | {orig_code} ➔ {dest_code}")

            print(f"    Departs: {dep_time}")
            print(f"    Arrives: {arr_time}")

            # add flight information to database
            cursor.execute("""
            INSERT OR REPLACE INTO flights
            (origin_code, destination_id, departure_date, return_date, price_usd, airline, segments)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (orig_code, dest_code, departure_date, return_date, amount, airline_name, len(segments)))

        print("-" * 45)

def get_flight_data(user_location, geo_data_destination, connection):
    # user location info
    geo_data_user_location = geocode_city(user_location)
    if not geo_data_user_location:
        print(f"Could not find user location: '{user_location}'")
        return None

    user_origin_code_iata = resolve_location_to_iata(geo_data_user_location)
    destination_origin_code_iata = resolve_location_to_iata(geo_data_destination)

    if not user_origin_code_iata or not destination_origin_code_iata:
        print("Could not resolve valid flight origin or destination airport.")
        return None

    departure_date = input("Enter a departure date [YYYY-MM-DD]: " )
    cabin_class = input("Enter a cabin class [economy, premium_economy, business, first]: ")
    num_adults = int(input("Enter the number of adults boarding: "))
    round_trip = input("Are you planning on returning? [y/n]: ")
    if round_trip == "y":
        return_date = input("Enter a return date [YYYY-MM-DD]: ")

    search_flights(user_origin_code_iata, destination_origin_code_iata, departure_date, cabin_class, connection, num_adults, return_date)

# adds forecast of the next 2 weeks to the database
def get_weather_data(geo_data, connection):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
          "latitude": geo_data["latitude"],
          "longitude": geo_data["longitude"],
          "daily": "temperature_2m_max,precipitation_sum,weather_code",
          "forecast_days": 14
      }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['daily']
    except requests.exceptions.Timeout:
        print("Request timed out")
        return
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return

    try:
        destination_id = geo_data["destination_id"]
        forecast_date = data['time']
        temp_c = data['temperature_2m_max']
        precipitation_sum = data['precipitation_sum']
        weather_code = data["weather_code"]

        cursor = connection.cursor()

        # add forecast information to database
        for i in range(len(forecast_date)):
            cursor.execute("""
            INSERT OR REPLACE INTO weather_forecasts
            (destination_id, forecast_date, avg_temp_c, weather_code, precipitation_mm)
            VALUES (?, ?, ?, ?, ?)
            """, (destination_id, forecast_date[i], temp_c[i], weather_code[i], precipitation_sum[i]))

    except sqlite3.Error as error:
        print(f"An error occurred while setting up the database: {error}")

def search():
    while True:
        user_location = input("Enter your location: ")

        destination_city = input("Enter your destination: ")
        if destination_city == "0":
            break
        get_destination_data(destination_city, user_location)
if __name__ == "__main__":
    search()