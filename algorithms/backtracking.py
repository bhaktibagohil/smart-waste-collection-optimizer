"""
Unit 6 & 8: Backtracking Algorithms.
Direct educational implementations of N-Queens / Eight Queens,
Backtracking 0/1 Knapsack with upper bound pruning,
Hamiltonian Cycle on graphs, and Exact Traveling Salesperson Problem (TSP).
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Optional, Tuple


# --- 1. Eight Queens / N-Queens Problem ---

def solve_n_queens(n: int = 8, find_all: bool = True) -> Dict[str, Any]:
    """
    N-Queens puzzle: Place N non-attacking queens on an N x N chessboard.
    Uses backtracking to place one queen per row, checking column and diagonals.
    Time Complexity: O(N!). Auxiliary Space: O(N).
    """
    if n <= 0 or n > 12:
        raise ValueError("N must be between 1 and 12 for responsive execution.")

    solutions: List[List[int]] = []  # solutions[s][row] = col
    cols = set()
    diag_pos = set()  # r + c
    diag_neg = set()  # r - c
    current_board = [-1] * n
    nodes_explored = 0

    start_t = time.perf_counter()

    def backtrack(r: int):
        nonlocal nodes_explored
        nodes_explored += 1

        if r == n:
            solutions.append(list(current_board))
            return

        for c in range(n):
            if c in cols or (r + c) in diag_pos or (r - c) in diag_neg:
                continue

            # Place queen
            cols.add(c)
            diag_pos.add(r + c)
            diag_neg.add(r - c)
            current_board[r] = c

            backtrack(r + 1)

            # Backtrack state
            cols.remove(c)
            diag_pos.remove(r + c)
            diag_neg.remove(r - c)
            current_board[r] = -1

            if not find_all and solutions:
                break

    backtrack(0)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": f"{n}-Queens (Backtracking)",
        "board_size": n,
        "solution_count": len(solutions),
        "solutions": solutions[:10],  # first 10 solutions
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(N!) worst case"
    }


# --- 2. 0/1 Knapsack via Backtracking ---

def knapsack_backtracking(
    weights: List[int],
    values: List[int],
    capacity: int
) -> Dict[str, Any]:
    """
    0/1 Knapsack solved via Backtracking state space search with upper bound pruning.
    Prunes branches where optimistic fractional upper bound <= best value found so far.
    """
    n = len(weights)
    best_value = 0
    best_selection = [0] * n
    current_selection = [0] * n
    nodes_visited = 0

    # Sort items by value/weight ratio descending for effective bounding
    indexed_items = sorted(range(n), key=lambda i: values[i] / weights[i] if weights[i] > 0 else 0, reverse=True)
    w_sorted = [weights[i] for i in indexed_items]
    v_sorted = [values[i] for i in indexed_items]

    start_t = time.perf_counter()

    def calculate_upper_bound(idx: int, cur_w: int, cur_v: int) -> float:
        """Fractional knapsack upper bound for remaining items."""
        bound = cur_v
        rem_cap = capacity - cur_w
        for j in range(idx, n):
            if w_sorted[j] <= rem_cap:
                bound += v_sorted[j]
                rem_cap -= w_sorted[j]
            else:
                bound += (rem_cap / w_sorted[j]) * v_sorted[j]
                break
        return bound

    def backtrack(idx: int, cur_w: int, cur_v: int):
        nonlocal best_value, best_selection, nodes_visited
        nodes_visited += 1

        if cur_w <= capacity and cur_v > best_value:
            best_value = cur_v
            # Map back to original indices
            temp = [0] * n
            for k in range(n):
                temp[indexed_items[k]] = current_selection[k]
            best_selection = temp

        if idx >= n or cur_w >= capacity:
            return

        # Pruning check
        if calculate_upper_bound(idx, cur_w, cur_v) <= best_value:
            return

        # Branch 1: Include item idx
        if cur_w + w_sorted[idx] <= capacity:
            current_selection[idx] = 1
            backtrack(idx + 1, cur_w + w_sorted[idx], cur_v + v_sorted[idx])
            current_selection[idx] = 0

        # Branch 2: Exclude item idx
        backtrack(idx + 1, cur_w, cur_v)

    backtrack(0, 0, 0)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    selected_indices = [i for i in range(n) if best_selection[i] == 1]

    return {
        "algorithm": "0/1 Knapsack (Backtracking with Bounding)",
        "best_value": best_value,
        "selected_indices": selected_indices,
        "nodes_visited": nodes_visited,
        "execution_time_ms": round(elapsed_ms, 4)
    }


# --- 3. Hamiltonian Cycle Problem ---

def hamiltonian_cycle(adj_matrix: List[List[int]], start_vertex: int = 0) -> Dict[str, Any]:
    """
    Hamiltonian Cycle: Finds a closed tour in a graph visiting every vertex exactly once
    and returning to start_vertex.
    Time Complexity: O(N!). NP-Complete decision problem.
    """
    n = len(adj_matrix)
    path = [-1] * n
    path[0] = start_vertex
    nodes_explored = 0
    start_t = time.perf_counter()

    def is_safe(v: int, pos: int) -> bool:
        # Check edge exists between path[pos - 1] and v
        if adj_matrix[path[pos - 1]][v] == 0:
            return False
        # Check v has not already been included
        if v in path[:pos]:
            return False
        return True

    def backtrack(pos: int) -> bool:
        nonlocal nodes_explored
        nodes_explored += 1

        if pos == n:
            # Check edge from last vertex back to start_vertex
            return adj_matrix[path[pos - 1]][path[0]] == 1

        for v in range(n):
            if is_safe(v, pos):
                path[pos] = v
                if backtrack(pos + 1):
                    return True
                path[pos] = -1

        return False

    has_cycle = backtrack(1)
    full_cycle = (path + [start_vertex]) if has_cycle else []
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Hamiltonian Cycle (Backtracking)",
        "has_hamiltonian_cycle": has_cycle,
        "cycle_path": full_cycle,
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4),
        "np_class": "NP-Complete (Karp's 21 NP-complete problems)"
    }


# --- 4. Exact TSP Solver (Backtracking) ---

def tsp_backtracking_exact(dist_matrix: List[List[float]], start_vertex: int = 0) -> Dict[str, Any]:
    """
    Exact Traveling Salesperson Problem (TSP) solver for small instances.
    Finds permutation with minimum total tour distance returning to start_vertex.
    """
    n = len(dist_matrix)
    if n > 10:
        raise ValueError(f"Graph size n={n} exceeds exact search limit (10).")

    visited = [False] * n
    visited[start_vertex] = True
    best_cost = float("inf")
    best_path = []
    nodes_evaluated = 0

    start_t = time.perf_counter()

    def search(curr: int, count: int, cost: float, current_path: List[int]):
        nonlocal best_cost, best_path, nodes_evaluated
        nodes_evaluated += 1

        if cost >= best_cost:
            return  # Prune branch

        if count == n:
            return_cost = dist_matrix[curr][start_vertex]
            if return_cost != float("inf") and cost + return_cost < best_cost:
                best_cost = cost + return_cost
                best_path = current_path + [start_vertex]
            return

        for nxt in range(n):
            if not visited[nxt] and dist_matrix[curr][nxt] != float("inf"):
                visited[nxt] = True
                search(nxt, count + 1, cost + dist_matrix[curr][nxt], current_path + [nxt])
                visited[nxt] = False

    search(start_vertex, 1, 0.0, [start_vertex])
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Exact TSP (Backtracking)",
        "start_vertex": start_vertex,
        "best_tour_cost": round(best_cost, 3),
        "best_tour": best_path,
        "nodes_evaluated": nodes_evaluated,
        "execution_time_ms": round(elapsed_ms, 4),
        "optimality": "Proven mathematically optimal for the given instance"
    }
