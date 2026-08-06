import sqlite3
import requests
from bs4 import BeautifulSoup

url = "https://api.open-meteo.com/v1/forecast"
params = {
      "latitude": 35.6895,
      "longitude": 139.687,
      "daily": "temperature_2m_max,precipitation_sum",
      "forecast_days": 14
  }

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()['daily']
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print("Request failed:", e)

try:
    destination_id = "TYO"
    forecast_date = data['time']
    temp_c = data['temperature_2m_max']
    precipitation_sum = data['precipitation_sum']

    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()

    for i in range(len(forecast_date)):
        cursor.execute("""
        INSERT OR REPLACE INTO weather_forecasts
        (destination_id, forecast_date, avg_temp_c, precipitation_mm)
        VALUES (?, ?, ?, ?)
        """, (destination_id, forecast_date[i], temp_c[i], precipitation_sum[i]))

        connection.commit()

except sqlite3.Error as error:
    print(f"An error occurred while setting up the database: {error}")

if connection:
    connection.close()