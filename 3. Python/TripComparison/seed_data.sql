DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS flights;

CREATE TABLE destinations (
    destination_id TEXT PRIMARY KEY,
    city_name TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    airport_code TEXT DEFAULT NULL,
    climate_zone TEXT,
    avg_daily_cost_usd REAL,
    vibe_tags TEXT
);
CREATE TABLE flights (
    flight_id TEXT PRIMARY KEY,
    destination_id TEXT NOT NULL,
    origin_code TEXT NOT NULL,
    destination_code TEXT NOT NULL,
    outbound_departs TEXT,
    outbound_arrives TEXT,
    has_return BOOLEAN,
    return_departs TEXT,
    return_arrives TEXT,
    price_usd REAL NOT NULL,
    airline TEXT,
    outbound_layovers INTEGER NOT NULL DEFAULT 0,
    return_layovers INTEGER,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations (destination_id) ON DELETE CASCADE
);