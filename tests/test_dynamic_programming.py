"""
Unit tests for Dynamic Programming Algorithms.
"""

import pytest
from algorithms.dynamic_programming import (
    binomial_coefficient_dp,
    coin_change_min_coins_dp,
    knapsack_01_dp,
    floyd_warshall_all_pairs,
    matrix_chain_multiplication,
    longest_common_subsequence,
    compare_greedy_vs_dp_coin_change
)


def test_binomial_coefficient_dp():
    assert binomial_coefficient_dp(5, 2)["result"] == 10
    assert binomial_coefficient_dp(6, 3)["result"] == 20
    assert binomial_coefficient_dp(10, 0)["result"] == 1
    assert binomial_coefficient_dp(10, 10)["result"] == 1
    assert binomial_coefficient_dp(4, 5)["result"] == 0


def test_coin_change_min_coins_dp():
    coins = [1, 2, 5]
    res = coin_change_min_coins_dp(coins, 11)
    assert res["min_coins"] == 3  # 5 + 5 + 1
    assert sum(res["coins_used"]) == 11

    # Canonical counterexample where greedy fails
    # Coins: [1, 3, 4], amount 6 -> DP gives 2 (3 + 3)
    res_counter = coin_change_min_coins_dp([1, 3, 4], 6)
    assert res_counter["min_coins"] == 2
    assert sorted(res_counter["coins_used"]) == [3, 3]


def test_knapsack_01_dp():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    res = knapsack_01_dp(weights, values, capacity)
    # Optimal integer items: item 1 (wt 20, val 100) + item 2 (wt 30, val 120) = 220
    assert res["max_value"] == 220
    assert set(res["selected_indices"]) == {1, 2}
    assert res["total_weight_taken"] == 50


def test_floyd_warshall_all_pairs():
    # 4 vertices graph
    inf = float("inf")
    matrix = [
        [0.0, 3.0, inf, 7.0],
        [8.0, 0.0, 2.0, inf],
        [5.0, inf, 0.0, 1.0],
        [2.0, inf, inf, 0.0]
    ]
    res = floyd_warshall_all_pairs(4, matrix)
    assert res["has_negative_cycle"] is False
    dist = res["distance_matrix"]
    assert dist[0][1] == 3.0
    assert dist[0][2] == 5.0  # 0 -> 1 -> 2 (3 + 2 = 5)
    assert dist[0][3] == 6.0  # 0 -> 1 -> 2 -> 3 (3 + 2 + 1 = 6)


def test_matrix_chain_multiplication():
    # Chain of matrices: A1 (10x30), A2 (30x5), A3 (5x60)
    dims = [10, 30, 5, 60]
    res = matrix_chain_multiplication(dims)
    # (A1 * A2) * A3: 10*30*5 + 10*5*60 = 1500 + 3000 = 4500
    assert res["min_scalar_multiplications"] == 4500
    assert "A1" in res["optimal_parenthesization"]


def test_longest_common_subsequence():
    s1 = "AGGTAB"
    s2 = "GXTXAYB"
    res = longest_common_subsequence(s1, s2)
    assert res["lcs_length"] == 4
    assert res["lcs_string"] == "GTAB"


def test_compare_greedy_vs_dp_coin_change():
    res = compare_greedy_vs_dp_coin_change()
    assert res["greedy_is_suboptimal"] is True
    assert res["greedy_coin_count"] == 3
    assert res["dp_coin_count"] == 2
