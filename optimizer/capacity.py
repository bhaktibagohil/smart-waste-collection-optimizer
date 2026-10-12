"""
Truck Capacity and Bin Selection Module.
Uses 0/1 Knapsack Dynamic Programming and Greedy Knapsack heuristic
to select the optimal subset of waste bins that fit within truck capacity limits.
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple
from optimizer.priority import compute_priority_score


def select_bins_knapsack_dp(
    candidate_bins: List[Dict[str, Any]],
    capacity_kg: float,
    scale_factor: int = 10
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], float, float]:
    """
    Select an optimal subset of bins to collect using 0/1 Knapsack DP.
    
    Item weight = int(round(bin['waste_kg'] * scale_factor))
    Item value  = int(round(priority_score * scale_factor))
    Knapsack capacity = int(round(capacity_kg * scale_factor))
    
    Returns:
      (selected_bins, uncollected_bins, total_waste_kg, total_priority_value)
    """
    if capacity_kg <= 0 or not candidate_bins:
        return [], list(candidate_bins), 0.0, 0.0

    n = len(candidate_bins)
    weights = [max(1, int(round(float(b["waste_kg"]) * scale_factor))) for b in candidate_bins]
    values = [max(1, int(round(compute_priority_score(b) * scale_factor))) for b in candidate_bins]
    W = int(round(capacity_kg * scale_factor))

    # DP Table: dp[i][w] = max value using subset of first i items with weight limit w
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(W + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to reconstruct selected items
    selected_indices = []
    curr_w = W
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            selected_indices.append(i - 1)
            curr_w -= weights[i - 1]

    selected_indices.reverse()
    selected_set = set(selected_indices)

    selected_bins = [candidate_bins[i] for i in selected_indices]
    uncollected_bins = [candidate_bins[i] for i in range(n) if i not in selected_set]

    total_waste = sum(float(b["waste_kg"]) for b in selected_bins)
    total_priority = sum(compute_priority_score(b) for b in selected_bins)

    return selected_bins, uncollected_bins, round(total_waste, 2), round(total_priority, 2)


def select_bins_greedy_ratio(
    candidate_bins: List[Dict[str, Any]],
    capacity_kg: float
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], float, float]:
    """
    Select bins using a Greedy heuristic sorted by Priority / Weight ratio.
    Demonstrates greedy knapsack item selection (0/1 discrete variant).
    """
    if capacity_kg <= 0 or not candidate_bins:
        return [], list(candidate_bins), 0.0, 0.0

    # Enrich with ratio
    items_with_ratio = []
    for b in candidate_bins:
        w = max(0.1, float(b["waste_kg"]))
        score = compute_priority_score(b)
        ratio = score / w
        items_with_ratio.append((ratio, b))

    # Sort descending by ratio
    items_with_ratio.sort(key=lambda x: x[0], reverse=True)

    selected: List[Dict[str, Any]] = []
    uncollected: List[Dict[str, Any]] = []
    current_weight = 0.0
    current_priority = 0.0

    for ratio, b in items_with_ratio:
        w = float(b["waste_kg"])
        if current_weight + w <= capacity_kg:
            selected.append(b)
            current_weight += w
            current_priority += compute_priority_score(b)
        else:
            uncollected.append(b)

    return selected, uncollected, round(current_weight, 2), round(current_priority, 2)


def validate_truck_capacity(
    bins_in_route: List[Dict[str, Any]],
    capacity_kg: float
) -> Dict[str, Any]:
    """
    Verify feasibility of collected waste against truck capacity limit.
    """
    total_waste = sum(float(b.get("waste_kg", 0.0)) for b in bins_in_route)
    is_feasible = total_waste <= capacity_kg
    utilization_pct = (total_waste / capacity_kg * 100.0) if capacity_kg > 0 else 0.0
    excess_kg = max(0.0, total_waste - capacity_kg)

    return {
        "is_feasible": is_feasible,
        "total_waste_kg": round(total_waste, 2),
        "capacity_kg": round(capacity_kg, 2),
        "utilization_pct": round(utilization_pct, 2),
        "excess_kg": round(excess_kg, 2),
        "bins_count": len(bins_in_route)
    }
