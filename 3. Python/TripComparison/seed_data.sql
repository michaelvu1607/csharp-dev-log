-- Clean out any existing sample data
DELETE FROM weather_forecasts;
DELETE FROM accommodations;
DELETE FROM flights;
DELETE FROM destinations;

-- 1. Destinations Data
INSERT INTO destinations (destination_id, city_name, country, climate_zone, avg_daily_cost_usd, vibe_tags) VALUES
('TYO', 'Tokyo', 'Japan', 'Temperate', 120.00, 'urban, culture, food, tech, historical'),
('PAR', 'Paris', 'France', 'Temperate', 150.00, 'romance, art, food, architecture, walkable'),
('CUN', 'Cancun', 'Mexico', 'Tropical', 85.00, 'beach, nightlife, resort, relaxation'),
('REK', 'Reykjavik', 'Iceland', 'Subpolar', 180.00, 'nature, adventure, scenic, quiet');

-- 2. Flights Data (Assuming Origin: ORD / Chicago O'Hare)
INSERT INTO flights (flight_id, origin_code, destination_id, price_usd, duration_hours, stops, airline) VALUES
('FL-TYO-01', 'ORD', 'TYO', 1150.00, 13.5, 0, 'ANA'),
('FL-TYO-02', 'ORD', 'TYO', 890.00, 16.0, 1, 'United Airlines'),
('FL-PAR-01', 'ORD', 'PAR', 920.00, 8.5, 0, 'Air France'),
('FL-PAR-02', 'ORD', 'PAR', 710.00, 11.0, 1, 'American Airlines'),
('FL-CUN-01', 'ORD', 'CUN', 340.00, 3.8, 0, 'United Airlines'),
('FL-CUN-02', 'ORD', 'CUN', 280.00, 5.5, 1, 'Spirit Airlines'),
('FL-REK-01', 'ORD', 'REK', 650.00, 6.2, 0, 'Icelandair');

-- 3. Accommodations Data
INSERT INTO accommodations (hotel_id, destination_id, hotel_name, nightly_rate_usd, rating, location_score) VALUES
('HOT-TYO-01', 'TYO', 'Shinjuku Granbell Hotel', 140.00, 4.3, 4.7),
('HOT-TYO-02', 'TYO', 'Park Hyatt Tokyo', 550.00, 4.8, 4.9),
('HOT-PAR-01', 'PAR', 'Hôtel CitizenM Paris Gare de Lyon', 190.00, 4.5, 4.6),
('HOT-PAR-02', 'PAR', 'Le Meurice', 980.00, 4.9, 5.0),
('HOT-CUN-01', 'CUN', 'Mayan Monkey Hostel Cancun', 35.00, 4.4, 4.2),
('HOT-CUN-02', 'CUN', 'Hyatt Ziva Cancun', 420.00, 4.7, 4.8),
('HOT-REK-01', 'REK', 'Center Hotels Plaza', 210.00, 4.2, 4.5);

-- 4. Weather Forecasts Data (Sample Monthly Averages)
INSERT INTO weather_forecasts (destination_id, month, avg_temp_c, rainy_days) VALUES
-- Tokyo (Jan, May, Aug, Oct)
('TYO', 1, 5.5, 5),
('TYO', 5, 18.2, 10),
('TYO', 8, 27.5, 8),
('TYO', 10, 17.8, 9),

-- Paris (Jan, May, Aug, Oct)
('PAR', 1, 5.0, 10),
('PAR', 5, 15.5, 9),
('PAR', 8, 20.0, 7),
('PAR', 10, 12.5, 9),

-- Cancun (Jan, May, Aug, Oct)
('CUN', 1, 24.0, 4),
('CUN', 5, 28.5, 5),
('CUN', 8, 29.0, 7),
('CUN', 10, 27.0, 11),

-- Reykjavik (Jan, May, Aug, Oct)
('REK', 1, -0.5, 15),
('REK', 5, 6.5, 10),
('REK', 8, 11.0, 11),
('REK', 10, 4.5, 14);