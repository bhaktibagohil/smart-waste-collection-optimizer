"""
Unit tests for Graph Exploration Algorithms (BFS, DFS, Topological Sort).
"""

import pytest
from algorithms.graph_algorithms import (
    GraphRepresentation,
    breadth_first_search,
    depth_first_search,
    topological_sort_kahns
)


def test_bfs_undirected():
    g = GraphRepresentation(5, directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    res = breadth_first_search(g, start_vertex=0)
    assert res["traversal_order"][0] == 0
    assert set(res["traversal_order"]) == {0, 1, 2, 3, 4}
    assert res["distances_from_start"][0] == 0
    assert res["distances_from_start"][1] == 1
    assert res["distances_from_start"][3] == 2


def test_dfs_cycle_detection():
    # Graph with cycle: 0 -> 1 -> 2 -> 0
    g_cycle = GraphRepresentation(3, directed=True)
    g_cycle.add_edge(0, 1)
    g_cycle.add_edge(1, 2)
    g_cycle.add_edge(2, 0)
    res_cycle = depth_first_search(g_cycle, start_vertex=0)
    assert res_cycle["has_cycle"] is True

    # DAG without cycle: 0 -> 1 -> 2
    g_dag = GraphRepresentation(3, directed=True)
    g_dag.add_edge(0, 1)
    g_dag.add_edge(1, 2)
    res_dag = depth_first_search(g_dag, start_vertex=0)
    assert res_dag["has_cycle"] is False


def test_topological_sort_kahns():
    # Valid DAG
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    res = topological_sort_kahns(6, edges)
    assert res["is_valid_dag"] is True
    order = res["topological_order"]
    # Check precedence: for each edge (u, v), u must precede v in order
    for u, v in edges:
        assert order.index(u) < order.index(v)

    # Graph with cycle
    cycle_edges = [(0, 1), (1, 2), (2, 0)]
    res_cycle = topological_sort_kahns(3, cycle_edges)
    assert res_cycle["has_cycle"] is True
    assert res_cycle["is_valid_dag"] is False
