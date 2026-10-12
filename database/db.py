"""
SQLite Database module for Smart Waste Collection Route Optimizer.
Handles persistent storage for waste bins, collection history, and configuration.
"""

from __future__ import annotations
import sqlite3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "smart_waste.db")
SAMPLE_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_bins.csv")


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Create and return a SQLite database connection with row factory enabled."""
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None, seed_if_empty: bool = True) -> None:
    """Initialize SQLite database tables and default configuration."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bins (
        bin_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        waste_level REAL NOT NULL,
        waste_kg REAL NOT NULL,
        urgency TEXT NOT NULL,
        last_collection_days INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'Pending',
        updated_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes_history (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        algorithm_name TEXT NOT NULL,
        depot_id TEXT NOT NULL,
        truck_capacity_kg REAL NOT NULL,
        total_waste_collected_kg REAL NOT NULL,
        capacity_utilization_pct REAL NOT NULL,
        total_distance_km REAL NOT NULL,
        travel_time_min REAL NOT NULL,
        bins_visited_count INTEGER NOT NULL,
        uncollected_count INTEGER NOT NULL,
        savings_pct REAL NOT NULL,
        route_sequence_json TEXT NOT NULL,
        execution_time_ms REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Default settings
    default_configs = [
        ("depot_id", "DEPOT"),
        ("depot_name", "Central Sanitation Facility"),
        ("depot_latitude", "18.5200"),
        ("depot_longitude", "73.8550"),
        ("default_truck_capacity_kg", "1200.0"),
        ("default_avg_speed_kmh", "25.0"),
        ("critical_threshold_pct", "85.0")
    ]
    for key, val in default_configs:
        cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)", (key, val))

    conn.commit()

    # Seed with sample data if table is currently empty
    cursor.execute("SELECT COUNT(*) FROM bins")
    count = cursor.fetchone()[0]
    if count == 0 and seed_if_empty and os.path.exists(SAMPLE_CSV_PATH):
        load_bins_from_csv(SAMPLE_CSV_PATH, db_path=db_path)

    conn.close()


def get_all_bins(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all bins ordered by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bins ORDER BY bin_id ASC")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result


def get_bins_df(db_path: Optional[str] = None) -> pd.DataFrame:
    """Retrieve all bins as a Pandas DataFrame."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT * FROM bins ORDER BY bin_id ASC", conn)
    conn.close()
    return df


def get_bin(bin_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetch a single bin by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bins WHERE bin_id = ?", (bin_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_bin(bin_data: Dict[str, Any], db_path: Optional[str] = None) -> bool:
    """Insert a new bin record."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""
        INSERT INTO bins (bin_id, name, latitude, longitude, waste_level, waste_kg, urgency, last_collection_days, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bin_data["bin_id"].strip(),
            bin_data["name"].strip(),
            float(bin_data["latitude"]),
            float(bin_data["longitude"]),
            float(bin_data["waste_level"]),
            float(bin_data["waste_kg"]),
            bin_data.get("urgency", "Medium"),
            int(bin_data.get("last_collection_days", 1)),
            bin_data.get("status", "Pending"),
            now_str
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def update_bin(bin_data: Dict[str, Any], db_path: Optional[str] = None) -> bool:
    """Update an existing bin record."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE bins
    SET name = ?, latitude = ?, longitude = ?, waste_level = ?, waste_kg = ?, urgency = ?,
        last_collection_days = ?, status = ?, updated_at = ?
    WHERE bin_id = ?
    """, (
        bin_data["name"].strip(),
        float(bin_data["latitude"]),
        float(bin_data["longitude"]),
        float(bin_data["waste_level"]),
        float(bin_data["waste_kg"]),
        bin_data.get("urgency", "Medium"),
        int(bin_data.get("last_collection_days", 1)),
        bin_data.get("status", "Pending"),
        now_str,
        bin_data["bin_id"].strip()
    ))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def delete_bin(bin_id: str, db_path: Optional[str] = None) -> bool:
    """Delete a bin by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bins WHERE bin_id = ?", (bin_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def update_bin_status(bin_ids: List[str], status: str, db_path: Optional[str] = None) -> int:
    """Bulk update status for a list of bin IDs (e.g., mark as 'Collected')."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    for b_id in bin_ids:
        cursor.execute("UPDATE bins SET status = ?, updated_at = ? WHERE bin_id = ?", (status, now_str, b_id))
        count += cursor.rowcount
    conn.commit()
    conn.close()
    return count


def load_bins_from_csv(csv_path: str, db_path: Optional[str] = None, replace_existing: bool = True) -> int:
    """Load bin records from a CSV file into the database."""
    df = pd.read_csv(csv_path)
    required_cols = {"bin_id", "name", "latitude", "longitude", "waste_level", "waste_kg"}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise ValueError(f"CSV is missing mandatory columns: {missing}")

    conn = get_connection(db_path)
    cursor = conn.cursor()
    if replace_existing:
        cursor.execute("DELETE FROM bins")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserted = 0
    for _, row in df.iterrows():
        b_id = str(row["bin_id"]).strip()
        name = str(row["name"]).strip()
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        w_level = float(row["waste_level"])
        w_kg = float(row["waste_kg"])
        urgency = str(row.get("urgency", "Medium")).strip()
        days = int(row.get("last_collection_days", 1))
        status = str(row.get("status", "Pending")).strip()

        cursor.execute("""
        INSERT OR REPLACE INTO bins (bin_id, name, latitude, longitude, waste_level, waste_kg, urgency, last_collection_days, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (b_id, name, lat, lon, w_level, w_kg, urgency, days, status, now_str))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted


def reset_to_sample_data(sample_csv_path: Optional[str] = None, db_path: Optional[str] = None) -> int:
    """Reset the bins table to the bundled sample dataset."""
    path = sample_csv_path or SAMPLE_CSV_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sample data file not found at {path}")
    return load_bins_from_csv(path, db_path=db_path, replace_existing=True)


def save_route_run(run_data: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """Persist a completed route plan execution into history."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    seq_json = json.dumps(run_data.get("route_sequence", []))

    cursor.execute("""
    INSERT INTO routes_history (
        timestamp, algorithm_name, depot_id, truck_capacity_kg,
        total_waste_collected_kg, capacity_utilization_pct, total_distance_km,
        travel_time_min, bins_visited_count, uncollected_count, savings_pct,
        route_sequence_json, execution_time_ms
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_str,
        run_data["algorithm_name"],
        run_data.get("depot_id", "DEPOT"),
        float(run_data["truck_capacity_kg"]),
        float(run_data["total_waste_collected_kg"]),
        float(run_data["capacity_utilization_pct"]),
        float(run_data["total_distance_km"]),
        float(run_data["travel_time_min"]),
        int(run_data["bins_visited_count"]),
        int(run_data["uncollected_count"]),
        float(run_data.get("savings_pct", 0.0)),
        seq_json,
        float(run_data.get("execution_time_ms", 0.0))
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_route_history(limit: int = 50, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve historical route optimization records."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM routes_history
    ORDER BY run_id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["route_sequence"] = json.loads(d["route_sequence_json"])
        result.append(d)
    conn.close()
    return result


def clear_route_history(db_path: Optional[str] = None) -> bool:
    """Clear all historical route run records."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routes_history")
    conn.commit()
    conn.close()
    return True


def get_config(key: str, default: Optional[str] = None, db_path: Optional[str] = None) -> Optional[str]:
    """Retrieve a config value by key."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default


def set_config(key: str, value: str, db_path: Optional[str] = None) -> None:
    """Set or update a configuration key-value pair."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()
