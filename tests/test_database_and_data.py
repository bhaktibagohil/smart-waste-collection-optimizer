"""
Unit tests for SQLite Database operations, schema migrations, and Data Validation.
"""

import os
import tempfile
import pytest

from database.db import (
    init_db,
    get_all_bins,
    get_bin,
    add_bin,
    update_bin,
    delete_bin,
    update_bin_status,
    save_route_run,
    get_route_history,
    clear_route_history,
    reset_to_sample_data
)
from optimizer.data_manager import (
    validate_bin_dict,
    haversine_distance_km,
    load_road_network_graph
)


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(db_path=path, seed_if_empty=False)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_bin_crud_operations(temp_db):
    bin_data = {
        "bin_id": "TEST-01",
        "name": "Test Bin Location",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "waste_level": 85.0,
        "waste_kg": 255.0,
        "urgency": "High",
        "last_collection_days": 3,
        "status": "Pending"
    }

    # 1. Add bin
    success = add_bin(bin_data, db_path=temp_db)
    assert success is True

    # Duplicate insertion should fail
    dup = add_bin(bin_data, db_path=temp_db)
    assert dup is False

    # 2. Get bin
    fetched = get_bin("TEST-01", db_path=temp_db)
    assert fetched is not None
    assert fetched["name"] == "Test Bin Location"
    assert fetched["waste_level"] == 85.0

    # 3. Update bin
    bin_data["waste_level"] = 95.0
    bin_data["urgency"] = "Critical"
    up_success = update_bin(bin_data, db_path=temp_db)
    assert up_success is True

    updated = get_bin("TEST-01", db_path=temp_db)
    assert updated["waste_level"] == 95.0
    assert updated["urgency"] == "Critical"

    # 4. Bulk status update
    status_count = update_bin_status(["TEST-01"], "Collected", db_path=temp_db)
    assert status_count == 1
    assert get_bin("TEST-01", db_path=temp_db)["status"] == "Collected"

    # 5. Delete bin
    del_success = delete_bin("TEST-01", db_path=temp_db)
    assert del_success is True
    assert get_bin("TEST-01", db_path=temp_db) is None


def test_route_history_operations(temp_db):
    run_record = {
        "algorithm_name": "Nearest-Neighbor Greedy",
        "depot_id": "DEPOT",
        "truck_capacity_kg": 1200.0,
        "total_waste_collected_kg": 950.0,
        "capacity_utilization_pct": 79.2,
        "total_distance_km": 14.8,
        "travel_time_min": 35.5,
        "bins_visited_count": 6,
        "uncollected_count": 12,
        "savings_pct": 18.5,
        "route_sequence": ["DEPOT", "BIN-01", "BIN-02", "DEPOT"],
        "execution_time_ms": 12.4
    }

    run_id = save_route_run(run_record, db_path=temp_db)
    assert run_id > 0

    history = get_route_history(limit=10, db_path=temp_db)
    assert len(history) == 1
    assert history[0]["algorithm_name"] == "Nearest-Neighbor Greedy"
    assert history[0]["route_sequence"] == ["DEPOT", "BIN-01", "BIN-02", "DEPOT"]

    clear_route_history(db_path=temp_db)
    assert len(get_route_history(limit=10, db_path=temp_db)) == 0


def test_bin_validation_rules():
    valid_data = {
        "bin_id": "BIN-99",
        "name": "Market Gate",
        "latitude": 18.52,
        "longitude": 73.85,
        "waste_level": 70.0,
        "waste_kg": 210.0,
        "urgency": "High",
        "status": "Pending"
    }
    is_valid, err = validate_bin_dict(valid_data)
    assert is_valid is True
    assert err == ""

    # Invalid coordinates (lat > 90)
    inv_lat = dict(valid_data, latitude=95.0)
    is_valid, err = validate_bin_dict(inv_lat)
    assert is_valid is False
    assert "Latitude" in err

    # Invalid waste level (> 100%)
    inv_level = dict(valid_data, waste_level=120.0)
    is_valid, err = validate_bin_dict(inv_level)
    assert is_valid is False
    assert "Waste level" in err

    # Negative waste kg
    inv_kg = dict(valid_data, waste_kg=-50.0)
    is_valid, err = validate_bin_dict(inv_kg)
    assert is_valid is False
    assert "Waste quantity" in err


def test_haversine_distance():
    # Known distance: approx 3.8 km between coordinates in Pune
    d = haversine_distance_km(18.5204, 73.8567, 18.5365, 73.8610)
    assert 1.0 < d < 5.0
