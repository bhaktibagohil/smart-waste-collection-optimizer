"""
Route Metrics and Performance Evaluation Module.
Computes road distance, travel time, capacity utilization, urgency coverage,
and comparison metrics between baseline and optimized collection plans.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


def compute_route_metrics(
    route_sequence: List[str],
    dist_matrix: Dict[tuple, float],
    bins_lookup: Dict[str, Dict[str, Any]],
    all_bins: List[Dict[str, Any]],
    truck_capacity_kg: float,
    avg_speed_kmh: float = 25.0,
    depot_id: str = "DEPOT"
) -> Dict[str, Any]:
    """
    Compute operational metrics for a planned route sequence.
    Sequence starts and ends at depot_id, e.g.: ['DEPOT', 'BIN-01', 'BIN-03', 'DEPOT'].
    """
    total_dist_km = 0.0
    is_connected = True
    unreachable_segments = []

    # Calculate road distance along the sequence
    for i in range(len(route_sequence) - 1):
        u = route_sequence[i]
        v = route_sequence[i + 1]
        leg_dist = dist_matrix.get((u, v), float("inf"))
        if leg_dist == float("inf"):
            is_connected = False
            unreachable_segments.append(f"{u} -> {v}")
        else:
            total_dist_km += leg_dist

    total_dist_km = round(total_dist_km, 3)

    # Travel time in minutes
    speed = max(5.0, avg_speed_kmh)
    travel_time_min = round((total_dist_km / speed) * 60.0, 1)

    # Visited bins (exclude depot occurrences)
    visited_bin_ids = [node for node in route_sequence if node != depot_id]
    visited_count = len(visited_bin_ids)

    # Waste collected
    total_waste_kg = sum(float(bins_lookup[b_id].get("waste_kg", 0.0)) for b_id in visited_bin_ids if b_id in bins_lookup)
    total_waste_kg = round(total_waste_kg, 2)

    capacity_util_pct = round((total_waste_kg / truck_capacity_kg * 100.0), 1) if truck_capacity_kg > 0 else 0.0
    is_capacity_feasible = total_waste_kg <= truck_capacity_kg

    # Overall route feasibility
    returns_to_depot = (len(route_sequence) >= 2 and
                        route_sequence[0] == depot_id and
                        route_sequence[-1] == depot_id)
    is_route_feasible = is_connected and is_capacity_feasible and returns_to_depot

    # Urgency analysis
    all_critical_count = sum(1 for b in all_bins if b.get("urgency") in ("Critical", "High"))
    visited_critical_count = sum(1 for b_id in visited_bin_ids if bins_lookup.get(b_id, {}).get("urgency") in ("Critical", "High"))
    remaining_critical_count = all_critical_count - visited_critical_count

    total_bins_available = len(all_bins)
    uncollected_count = total_bins_available - visited_count

    # Fuel and environmental estimations (standard urban sanitation truck: 0.28 L/km, 2.68 kg CO2/L)
    est_fuel_liters = round(total_dist_km * 0.28, 2)
    est_co2_kg = round(est_fuel_liters * 2.68, 2)

    return {
        "route_sequence": route_sequence,
        "total_distance_km": total_dist_km,
        "travel_time_min": travel_time_min,
        "bins_visited_count": visited_count,
        "total_bins_available": total_bins_available,
        "uncollected_count": uncollected_count,
        "total_waste_kg": total_waste_kg,
        "truck_capacity_kg": truck_capacity_kg,
        "capacity_utilization_pct": capacity_util_pct,
        "is_capacity_feasible": is_capacity_feasible,
        "is_connected": is_connected,
        "returns_to_depot": returns_to_depot,
        "is_route_feasible": is_route_feasible,
        "unreachable_segments": unreachable_segments,
        "critical_bins_visited": visited_critical_count,
        "critical_bins_total": all_critical_count,
        "critical_bins_remaining": remaining_critical_count,
        "estimated_fuel_liters": est_fuel_liters,
        "estimated_co2_kg": est_co2_kg
    }


def compare_routes(baseline_metrics: Dict[str, Any], optimized_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare baseline route with optimized route and compute realistic savings.
    """
    b_dist = baseline_metrics["total_distance_km"]
    o_dist = optimized_metrics["total_distance_km"]

    diff_km = round(b_dist - o_dist, 3)
    savings_pct = round((diff_km / b_dist * 100.0), 2) if b_dist > 0.0 else 0.0

    b_time = baseline_metrics["travel_time_min"]
    o_time = optimized_metrics["travel_time_min"]
    time_saved_min = round(b_time - o_time, 1)

    fuel_saved_l = round(baseline_metrics["estimated_fuel_liters"] - optimized_metrics["estimated_fuel_liters"], 2)
    co2_saved_kg = round(baseline_metrics["estimated_co2_kg"] - optimized_metrics["estimated_co2_kg"], 2)

    return {
        "baseline_distance_km": b_dist,
        "optimized_distance_km": o_dist,
        "distance_reduction_km": diff_km,
        "distance_savings_pct": savings_pct,
        "baseline_time_min": b_time,
        "optimized_time_min": o_time,
        "time_saved_min": time_saved_min,
        "fuel_saved_liters": fuel_saved_l,
        "co2_saved_kg": co2_saved_kg,
        "baseline_feasible": baseline_metrics["is_route_feasible"],
        "optimized_feasible": optimized_metrics["is_route_feasible"]
    }
