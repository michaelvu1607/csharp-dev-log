import sqlite3
import requests
from bs4 import BeautifulSoup

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

        # Format clean IDs (e.g. "ann_arbor_united_states")
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

def fetch_destination_data(city_name):
   with sqlite3.connect('trips.db') as connection:
       cursor = connection.cursor()
       cursor.execute(
           "SELECT * FROM destinations WHERE city_name LIKE ?", (f"%{city_name}%",)
       )

       match = cursor.fetchone()

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
           print(f"Found {city_name}, {country} | Avg. Cost: {avg_daily_cost_usd} per day")
           print(f"Coordinates: {latitude}, {longitude} | Main Airport: {airport_code}")
           print(f"Climate: {climate_zone} | Vibes: {vibe_tags}")
           print("Location found!")

           geo_data = {
               "destination_id": destination_id,
               "latitude": latitude,
               "longitude": longitude,
               "city_name": city_name,
           }

           fetch_weather_data(geo_data, connection)
           return match

       geo_data = geocode_city(city_name)

       print(f"'{city_name}' not in cache. Fetching location via Geocoding API")
       if not geo_data:
           print(f"Could not find {city_name}")
           return None

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

       fetch_weather_data(geo_data, connection)

       cursor.execute(
           "SELECT * FROM destinations WHERE destination_id = ?",
           (geo_data["destination_id"],)
       )
       new_match = cursor.fetchone()
       return new_match

def fetch_weather_data(geo_data, connection):
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
        weather_code = data.get("weather_code")

        cursor = connection.cursor()

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
        city = input("Enter a city: ")
        fetch_destination_data(city)
        if city == "":
            break

if __name__ == "__main__":
    search()