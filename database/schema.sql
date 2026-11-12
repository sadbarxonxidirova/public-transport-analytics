PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS agency (
    agency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_code TEXT NOT NULL UNIQUE,
    agency_name TEXT NOT NULL,
    city_region TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS route (
    route_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_id INTEGER NOT NULL,
    source_route_id TEXT NOT NULL,
    UNIQUE(agency_id, source_route_id),
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id)
);
CREATE TABLE IF NOT EXISTS route_period (
    route_period_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_pk INTEGER NOT NULL,
    period_code TEXT NOT NULL CHECK(period_code IN ('12','17')),
    summary_begin_date TEXT NOT NULL,
    stops REAL,
    avg_on_per_trip REAL,
    avg_trips REAL,
    sum_ons REAL,
    avg_ons REAL,
    source_file TEXT NOT NULL,
    UNIQUE(route_pk, period_code),
    FOREIGN KEY (route_pk) REFERENCES route(route_pk)
);
CREATE INDEX IF NOT EXISTS idx_route_period_code ON route_period(period_code);
CREATE INDEX IF NOT EXISTS idx_agency_code ON agency(agency_code);
