"""
Unit tests for Waste Route Optimization, Capacity Constraints, Priority Scoring, and Route Metrics.
"""

import os
import pytest
import networkx as nx

from optimizer.data_manager import load_road_network_graph, compute_all_pairs_shortest_distances
from optimizer.priority import compute_priority_score, get_formula_breakdown, rank_bins
from optimizer.capacity import select_bins_knapsack_dp, select_bins_greedy_ratio, validate_truck_capacity
from optimizer.route_planner import RoutePlanner
from optimizer.route_metrics import compute_route_metrics, compare_routes


@pytest.fixture
def sample_road_graph():
    G = nx.DiGraph()
    # Depot connected to BIN-01, BIN-02, BIN-03
    G.add_edge("DEPOT", "BIN-01", weight=1.0, distance_km=1.0)
    G.add_edge("BIN-01", "DEPOT", weight=1.0, distance_km=1.0)
    G.add_edge("BIN-01", "BIN-02", weight=1.5, distance_km=1.5)
    G.add_edge("BIN-02", "BIN-01", weight=1.5, distance_km=1.5)
    G.add_edge("BIN-02", "BIN-03", weight=2.0, distance_km=2.0)
    G.add_edge("BIN-03", "BIN-02", weight=2.0, distance_km=2.0)
    G.add_edge("BIN-03", "DEPOT", weight=2.5, distance_km=2.5)
    G.add_edge("DEPOT", "BIN-03", weight=2.5, distance_km=2.5)
    return G


@pytest.fixture
def sample_bins():
    return [
        {"bin_id": "BIN-01", "name": "East Square", "latitude": 18.52, "longitude": 73.85, "waste_level": 90.0, "waste_kg": 270.0, "urgency": "Critical", "last_collection_days": 4},
        {"bin_id": "BIN-02", "name": "North Gate", "latitude": 18.53, "longitude": 73.86, "waste_level": 75.0, "waste_kg": 225.0, "urgency": "High", "last_collection_days": 3},
        {"bin_id": "BIN-03", "name": "Park Walk", "latitude": 18.51, "longitude": 73.84, "waste_level": 40.0, "waste_kg": 120.0, "urgency": "Low", "last_collection_days": 1}
    ]


def test_priority_score_and_breakdown(sample_bins):
    b1 = sample_bins[0]
    score = compute_priority_score(b1)
    # Waste level: 90 * 0.5 = 45.0
    # Urgency Critical: 80.0
    # Days: 4 * 2.0 = 8.0
    # Total = 45 + 80 + 8 = 133.0
    assert score == 133.0

    breakdown = get_formula_breakdown(b1)
    assert breakdown["total_score"] == 133.0
    assert breakdown["urgency_label"] == "Critical"

    ranked = rank_bins(sample_bins, sort_by="priority")
    assert ranked[0]["bin_id"] == "BIN-01"


def test_capacity_knapsack_and_validation(sample_bins):
    # Capacity 300 kg (only fits BIN-01 or BIN-02 or BIN-03)
    selected, uncollected, total_w, total_p = select_bins_knapsack_dp(sample_bins, capacity_kg=300.0)
    assert total_w <= 300.0
    assert len(selected) >= 1

    # Capacity validation
    check_ok = validate_truck_capacity(selected, capacity_kg=300.0)
    assert check_ok["is_feasible"] is True
    assert check_ok["utilization_pct"] <= 100.0

    # Over-capacity check
    check_over = validate_truck_capacity(sample_bins, capacity_kg=400.0)
    # Total = 270 + 225 + 120 = 615 > 400
    assert check_over["is_feasible"] is False
    assert check_over["excess_kg"] > 0


def test_route_planner_methods(sample_road_graph, sample_bins):
    planner = RoutePlanner(sample_road_graph, depot_id="DEPOT")
    bin_ids = ["BIN-01", "BIN-02", "BIN-03"]
    dist_matrix = planner.build_distance_matrix(bin_ids)

    # 1. Baseline Route
    base_seq, base_dist = planner.plan_baseline_route(bin_ids, dist_matrix)
    assert base_seq[0] == "DEPOT"
    assert base_seq[-1] == "DEPOT"
    assert set(base_seq[1:-1]) == set(bin_ids)

    # 2. Nearest-Neighbor Route
    nn_seq, nn_dist = planner.plan_nearest_neighbor_route(bin_ids, dist_matrix)
    assert nn_seq[0] == "DEPOT"
    assert nn_seq[-1] == "DEPOT"
    assert set(nn_seq[1:-1]) == set(bin_ids)

    # 3. Exact TSP Route
    exact_seq, exact_dist, is_optimal = planner.plan_exact_branch_and_bound_tsp(bin_ids, dist_matrix)
    assert is_optimal is True
    assert exact_dist <= base_dist or exact_dist <= nn_dist


def test_route_metrics_and_comparison(sample_road_graph, sample_bins):
    planner = RoutePlanner(sample_road_graph, depot_id="DEPOT")
    bin_ids = ["BIN-01", "BIN-02", "BIN-03"]
    dist_matrix = planner.build_distance_matrix(bin_ids)
    lookup = {b["bin_id"]: b for b in sample_bins}

    base_seq, _ = planner.plan_baseline_route(bin_ids, dist_matrix)
    nn_seq, _ = planner.plan_nearest_neighbor_route(bin_ids, dist_matrix)

    m_base = compute_route_metrics(base_seq, dist_matrix, lookup, sample_bins, truck_capacity_kg=800.0)
    m_opt = compute_route_metrics(nn_seq, dist_matrix, lookup, sample_bins, truck_capacity_kg=800.0)

    assert m_base["is_route_feasible"] is True
    assert m_opt["is_route_feasible"] is True

    comp = compare_routes(m_base, m_opt)
    assert "distance_savings_pct" in comp
    assert "fuel_saved_liters" in comp
