"""
Unit tests for Backtracking and Branch & Bound Algorithms.
"""

import pytest
from algorithms.backtracking import (
    solve_n_queens,
    knapsack_backtracking,
    hamiltonian_cycle,
    tsp_backtracking_exact
)
from algorithms.branch_and_bound import (
    solve_assignment_problem_bnb,
    knapsack_branch_and_bound,
    minimax_alphabeta_demo
)


def test_n_queens():
    # 4-queens has exactly 2 solutions
    res_4 = solve_n_queens(4, find_all=True)
    assert res_4["solution_count"] == 2

    # 8-queens has exactly 92 solutions
    res_8 = solve_n_queens(8, find_all=True)
    assert res_8["solution_count"] == 92


def test_knapsack_backtracking():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    res = knapsack_backtracking(weights, values, capacity)
    # Items 0 & 1: wt 2+3=5, val 3+4=7
    assert res["best_value"] == 7
    assert set(res["selected_indices"]) == {0, 1}


def test_hamiltonian_cycle():
    # 4-vertex cycle graph 0-1-2-3-0
    adj_matrix = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ]
    res = hamiltonian_cycle(adj_matrix, start_vertex=0)
    assert res["has_hamiltonian_cycle"] is True
    assert len(res["cycle_path"]) == 5
    assert res["cycle_path"][0] == 0
    assert res["cycle_path"][-1] == 0

    # Disconnected / non-Hamiltonian graph
    adj_no_cycle = [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 0]
    ]
    res_no = hamiltonian_cycle(adj_no_cycle, start_vertex=0)
    assert res_no["has_hamiltonian_cycle"] is False


def test_tsp_backtracking_exact():
    # 4-city symmetric distance matrix
    inf = float("inf")
    dist = [
        [0.0, 10.0, 15.0, 20.0],
        [10.0, 0.0, 35.0, 25.0],
        [15.0, 35.0, 0.0, 30.0],
        [20.0, 25.0, 30.0, 0.0]
    ]
    res = tsp_backtracking_exact(dist, start_vertex=0)
    # Optimal tour: 0 -> 1 (10) -> 3 (25) -> 2 (30) -> 0 (15) = 80
    assert res["best_tour_cost"] == 80.0
    assert res["best_tour"][0] == 0
    assert res["best_tour"][-1] == 0


def test_assignment_problem_bnb():
    cost = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    res = solve_assignment_problem_bnb(cost)
    # Optimal: Worker 0->Job 1 (2), Worker 1->Job 0 (6) or Job 2, Worker 2->Job 2 (1), Worker 3->Job 3 (4) = 13
    assert res["min_total_cost"] == 13.0
    assert len(res["worker_job_assignments"]) == 4


def test_knapsack_branch_and_bound():
    weights = [2.0, 3.0, 4.0, 5.0]
    values = [3.0, 4.0, 5.0, 6.0]
    capacity = 5.0
    res = knapsack_branch_and_bound(weights, values, capacity)
    assert res["max_value"] == 7.0
    assert set(res["selected_indices"]) == {0, 1}


def test_minimax_alphabeta_demo():
    leaves = [3, 5, 6, 9, 1, 2, 0, -1]
    res = minimax_alphabeta_demo(leaves)
    assert res["optimal_root_value"] == 5
    assert res["branches_pruned"] > 0
