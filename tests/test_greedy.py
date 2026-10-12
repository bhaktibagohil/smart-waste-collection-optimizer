"""
Unit tests for Greedy Algorithms.
"""

import pytest
from algorithms.greedy import (
    greedy_coin_change,
    prim_mst,
    kruskal_mst,
    dijkstra_shortest_path,
    bellman_ford_shortest_path,
    fractional_knapsack_greedy,
    activity_selection_greedy,
    huffman_encoding
)


def test_greedy_coin_change():
    # Canonical currency
    coins = [25, 10, 5, 1]
    res = greedy_coin_change(coins, 63)
    assert res["success"] is True
    assert res["coins_chosen"] == [25, 25, 10, 1, 1, 1]

    # Non-canonical system where greedy gives suboptimal coin count
    # Coins: [4, 3, 1], Amount: 6 -> greedy gives 4 + 1 + 1 (3 coins)
    res_subopt = greedy_coin_change([4, 3, 1], 6)
    assert res_subopt["coins_chosen"] == [4, 1, 1]
    assert res_subopt["coin_count"] == 3


def test_prim_mst():
    edges = [
        (0, 1, 4.0), (0, 7, 8.0), (1, 2, 8.0), (1, 7, 11.0),
        (2, 3, 7.0), (2, 8, 2.0), (2, 5, 4.0), (3, 4, 9.0),
        (3, 5, 14.0), (4, 5, 10.0), (5, 6, 2.0), (6, 7, 1.0),
        (6, 8, 6.0), (7, 8, 7.0)
    ]
    res = prim_mst(9, edges, start_node=0)
    assert res["is_connected_mst"] is True
    assert res["total_weight"] == 37.0


def test_kruskal_mst():
    edges = [
        (0, 1, 4.0), (0, 7, 8.0), (1, 2, 8.0), (1, 7, 11.0),
        (2, 3, 7.0), (2, 8, 2.0), (2, 5, 4.0), (3, 4, 9.0),
        (3, 5, 14.0), (4, 5, 10.0), (5, 6, 2.0), (6, 7, 1.0),
        (6, 8, 6.0), (7, 8, 7.0)
    ]
    res = kruskal_mst(9, edges)
    assert res["is_connected_mst"] is True
    assert res["total_weight"] == 37.0
    assert len(res["mst_edges"]) == 8


def test_dijkstra_shortest_path():
    adj = {
        0: [(1, 4.0), (2, 1.0)],
        1: [(3, 1.0)],
        2: [(1, 2.0), (3, 5.0)],
        3: []
    }
    res = dijkstra_shortest_path(4, adj, source=0)
    assert res["distances"][0] == 0.0
    assert res["distances"][2] == 1.0
    assert res["distances"][1] == 3.0  # 0 -> 2 -> 1 (1 + 2 = 3)
    assert res["distances"][3] == 4.0  # 0 -> 2 -> 1 -> 3 (1 + 2 + 1 = 4)

    # Negative weight error detection
    adj_neg = {0: [(1, -2.0)], 1: []}
    with pytest.raises(ValueError, match="Dijkstra cannot handle negative edge weight"):
        dijkstra_shortest_path(2, adj_neg, source=0)


def test_bellman_ford_shortest_path():
    edges = [
        (0, 1, 4.0),
        (0, 2, 5.0),
        (1, 2, -3.0),
        (2, 3, 2.0)
    ]
    res = bellman_ford_shortest_path(4, edges, source=0)
    assert res["has_negative_cycle"] is False
    assert res["distances"][2] == 1.0  # 0 -> 1 -> 2 (4 - 3 = 1)
    assert res["distances"][3] == 3.0

    # Negative cycle detection
    cycle_edges = [
        (0, 1, 1.0),
        (1, 2, -2.0),
        (2, 1, -1.0)  # negative cycle: 1 -> 2 -> 1 has sum -3
    ]
    res_neg = bellman_ford_shortest_path(3, cycle_edges, source=0)
    assert res_neg["has_negative_cycle"] is True


def test_fractional_knapsack_greedy():
    weights = [10.0, 20.0, 30.0]
    values = [60.0, 100.0, 120.0]
    res = fractional_knapsack_greedy(weights, values, capacity=50.0)
    # Item 0 (ratio 6): take all 10 kg, gain 60
    # Item 1 (ratio 5): take all 20 kg, gain 100
    # Item 2 (ratio 4): take remaining 20 kg, gain 20/30 * 120 = 80
    # Total = 60 + 100 + 80 = 240
    assert res["total_value"] == 240.0


def test_activity_selection_greedy():
    starts = [1, 3, 0, 5, 8, 5]
    finishes = [2, 4, 6, 7, 9, 9]
    res = activity_selection_greedy(starts, finishes)
    assert res["selected_count"] == 4


def test_huffman_encoding():
    text = "ABRACADABRA"
    res = huffman_encoding(text)
    assert res["compression_ratio"] > 1.0
    assert len(res["codebook"]) == 5  # distinct chars A, B, R, C, D
