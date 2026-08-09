DROP TABLE IF EXISTS weather_forecasts;
DROP TABLE IF EXISTS accommodations;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS climates;

PRAGMA foreign_keys = ON;

CREATE TABLE destinations (
    destination_id TEXT PRIMARY KEY,
    city_name TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    airport_code TEXT,
    climate_zone TEXT,
    avg_daily_cost_usd REAL,
    vibe_tags TEXT
);
CREATE TABLE flights (
    flight_id TEXT PRIMARY KEY,
    origin_code TEXT NOT NULL,
    destination_id TEXT NOT NULL,
    departure_date TEXT,
    return_date TEXT DEFAULT Unknown,
    price_usd REAL NOT NULL,
    airline TEXT,
    segments INTEGER NOT NULL DEFAULT 1,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id) ON DELETE CASCADE
);

CREATE TABLE accommodations (
    hotel_id TEXT PRIMARY KEY,
    destination_id TEXT NOT NULL,
    hotel_name TEXT NOT NULL,
    nightly_rate_usd REAL NOT NULL,
    rating REAL,
    location_score REAL,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id) ON DELETE CASCADE
);


CREATE TABLE weather_forecasts (
    weather_id INTEGER PRIMARY KEY,
    destination_id TEXT NOT NULL,
    forecast_date TEXT NOT NULL,
    avg_temp_c REAL NOT NULL,
    weather_code INTEGER,
    precipitation_mm REAL,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id) ON DELETE CASCADE
);

CREATE TABLE climates (
    destination_id TEXT,
    month INTEGER,
    avg_temp_c REAL,
    avg_rainfall_mm REAL,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id)
);