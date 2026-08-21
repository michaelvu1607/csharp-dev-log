import sqlite3
import random
import pandas as pd
from datetime import datetime, timedelta

DB_NAME = "seed.db"

# Direct links to OurAirports raw open dataset
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
REGIONS_URL = "https://davidmegginson.github.io/ourairports-data/regions.csv"

AIRLINES = ["Delta", "United", "American", "British Airways", "Air France", "Lufthansa", "Emirates", "Qatar Airways"]


def load_and_seed_database(num_flights=10000):
    print("Fetching global airport and region data from OurAirports...")

    # 1. Load airports and regions via Pandas
    df_airports = pd.read_csv(AIRPORTS_URL)
    df_regions = pd.read_csv(REGIONS_URL)

    # Rename 'name' in df_regions to prevent column collision with df_airports['name']
    df_regions_clean = df_regions[['code', 'name']].rename(columns={'name': 'region_name'})

    # Merge to get country & continent/region details
    df_merged = df_airports.merge(df_regions_clean, left_on='iso_region', right_on='code', how='left')

    # Filter for active, medium/large commercial airports with valid 3-letter IATA codes
    valid_types = ['medium_airport', 'large_airport']
    df_clean = df_merged[
        (df_merged['type'].isin(valid_types)) &
        (df_merged['iata_code'].str.len() == 3) &
        (df_merged['scheduled_service'] == 'yes')
        ].copy()

    print(f"Loaded {len(df_clean)} real commercial airports across the globe.")

    # 2. Build Destination Records (Metadata fields set to None / NULL)
    destinations = []
    destination_ids = []

    for _, row in df_clean.iterrows():
        city_name = str(row['municipality']) if pd.notna(row['municipality']) else str(row['name'])
        country = str(row['iso_country'])
        region = str(row['continent']).lower() if pd.notna(row['continent']) else None

        clean_city = city_name.lower().replace(" ", "_")
        clean_country = country.lower().replace(" ", "_")
        dest_id = f"{clean_city}_{clean_country}"

        destinations.append((
            dest_id,
            city_name,
            country,
            region,
            float(row['latitude_deg']),
            float(row['longitude_deg']),
            str(row['iata_code']),
            None,  # climate_zone -> NULL
            None,  # avg_daily_cost_usd -> NULL
            None  # vibe_tags -> NULL
        ))
        destination_ids.append((dest_id, str(row['iata_code'])))

    # 3. Generate 10,000 Synthetic Flights
    flight_records = []
    base_date = datetime.now()
    common_origins = ["ORD", "JFK", "LAX", "ATL", "SFO", "LHR", "CDG"]

    for i in range(num_flights):
        dest_id, dest_code = random.choice(destination_ids)
        origin_code = random.choice(common_origins)

        while origin_code == dest_code:
            origin_code = random.choice(common_origins)

        flight_id = f"seed_fl_{i:05d}_{random.randint(1000, 9999)}"
        outbound_dt = base_date + timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))
        trip_len = random.randint(3, 14)
        return_dt = outbound_dt + timedelta(days=trip_len)

        outbound_str = outbound_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return_str = return_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        price = round(random.uniform(120.0, 1400.0), 2)
        airline = random.choice(AIRLINES)
        out_layovers = random.choice([0, 0, 1, 2])
        ret_layovers = random.choice([0, 0, 1])

        flight_records.append((
            flight_id, dest_id, origin_code, dest_code,
            outbound_str, outbound_str, 1, return_str, return_str,
            price, airline, out_layovers, ret_layovers
        ))

    # 4. Batch Database Insertion
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Initialize table schema from seed_data.sql if tables don't exist
    with open("seed_data.sql", "r") as f:
        cursor.executescript(f.read())

    cursor.executemany("""
        INSERT OR REPLACE INTO destinations 
        (destination_id, city_name, country, region, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, destinations)

    cursor.executemany("""
        INSERT OR REPLACE INTO destinations 
        (destination_id, city_name, country, region, latitude, longitude, airport_code, climate_zone, avg_daily_cost_usd, vibe_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, destinations)

    cursor.executemany("""
        INSERT OR REPLACE INTO flights 
        (flight_id, destination_id, origin_code, destination_code, outbound_departs, outbound_arrives, has_return, return_departs, return_arrives, price_usd, airline, outbound_layovers, return_layovers)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, flight_records)

    conn.commit()
    conn.close()
    print(
        f"Successfully populated '{DB_NAME}' with {len(destinations)} destinations and {num_flights} flights (metadata left NULL).")


if __name__ == "__main__":
    load_and_seed_database(10000)