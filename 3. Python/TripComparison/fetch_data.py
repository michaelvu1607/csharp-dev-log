import sqlite3
import requests
from bs4 import BeautifulSoup

url = "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&daily=temperature_2m_max,precipitation_sum,weather_code"
response = requests.get(url)
print(f"Status Code: {response.status_code}")

try:
    data = response.json()['daily']
    print(data)

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