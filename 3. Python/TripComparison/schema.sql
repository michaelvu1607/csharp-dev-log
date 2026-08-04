PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS weather_forecasts;
DROP TABLE IF EXISTS accommodations;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS destinations;

CREATE TABLE destinations (
    destination_id TEXT PRIMARY KEY,
    city_name TEXT NOT NULL,
    country TEXT NOT NULL,
    climate_zone TEXT,
    avg_daily_cost_usd REAL NOT NULL,
    vibe_tags TEXT
);

CREATE TABLE flights (
    flight_id TEXT PRIMARY KEY,
    origin_code TEXT NOT NULL,
    destination_id TEXT NOT NULL,
    price_usd REAL NOT NULL,
    duration_hours REAL NOT NULL,
    stops INTEGER DEFAULT 0,
    airline TEXT,
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
    month INTEGER NOT NULL,
    avg_temp_c REAL NOT NULL,
    rainy_days INTEGER,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id) ON DELETE CASCADE
);