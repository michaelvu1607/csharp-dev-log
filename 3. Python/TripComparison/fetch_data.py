import sqlite3
import requests
from bs4 import BeautifulSoup
from duffel_api import Duffel
import os
from dotenv import load_dotenv
import math
import airportsdata

load_dotenv()
DUFFEL_TOKEN = os.getenv("DUFFEL_API_KEY")

client = Duffel(access_token=DUFFEL_TOKEN)

def calculate_distance(lat1, lon1, lat2, lon2):
    distance = math.hypot(lat1 - lat2, lon1 - lon2)
    return distance

def get_nearest_airport(userlat, userlon):
    airports = airportsdata.load('IATA')
    closest = min(airports.values(), key=lambda coords: calculate_distance(userlat, userlon, coords['lat'], coords['lon']))
    return closest

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

            get_flight_data(user_location, geo_data)
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

        get_flight_data(user_location, geo_data)
        get_weather_data(geo_data, connection)

        # return the new location now saved in the database
        cursor.execute(
            "SELECT * FROM destinations WHERE destination_id = ?",
            (geo_data["destination_id"],)
        )
        new_match = cursor.fetchone()
        return new_match

# prints top one way flight options
def search_one_way_flights(origin_iata, destination_iata, departure_date, cabin_class, adults=1, return_date=None):
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

        first_segment = offer["slices"][0]["segments"][-1]
        dep_time = first_segment.get("departing_at")
        arr_time = first_segment.get("arriving_at")

        print(f"Option #{idx}: {airline_name}")
        print(f"  Price: {amount} {currency} for {adults} adult passengers")
        print(f"  Departs: {dep_time}")
        print(f"  Arrives: {arr_time}")
        print("-" * 40)

def get_flight_data(user_location, geo_data_destination):
    # user location info
    geo_data_user_location = geocode_city(user_location)
    user_location_id = geo_data_user_location['destination_id']
    print(f"Found {user_location_id}")

    user_lat = geo_data_user_location['latitude']
    user_lon = geo_data_user_location['longitude']

    user_nearest_airport = get_nearest_airport(user_lat, user_lon)
    if user_nearest_airport is None:
        print(f"{user_location} not found")
        return None
    print(f"User nearest airport: {user_nearest_airport}")

    user_origin_code_iata = user_nearest_airport.get("iata")

    # destination location info
    destination_lat = geo_data_destination['latitude']
    destination_lon = geo_data_destination['longitude']

    destination_nearest_airport = get_nearest_airport(destination_lat, destination_lon)
    print(f"Destination nearest airport: {destination_nearest_airport}")

    destination_origin_code_iata = destination_nearest_airport.get("iata")
    departure_date = input("Enter a departure date [YYYY-MM-DD]:" )
    cabin_class = input("Enter a cabin class [economy, premium_economy, business, first]: ")
    num_adults = int(input("Enter the number of adults boarding: "))
    round_trip = input("Are you planning on returning? [y/n]: ")
    if round_trip == "y":
        return_date = input("Enter a return date [YYYY-MM-DD]:")
    elif round_trip == "n":
        return_date = None
    search_one_way_flights(user_origin_code_iata, destination_origin_code_iata, departure_date, cabin_class, num_adults, return_date)

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