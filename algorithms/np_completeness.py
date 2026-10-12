"""
Unit 8: NP-Completeness and Theoretical Complexity.
Covers P, NP, NP-Complete, NP-Hard definitions, Cook-Levin theorem significance,
Polynomial-Time Reduction walkthrough (Hamiltonian Cycle <=_P Decision TSP),
and empirical comparative demonstration between Exact TSP and Nearest-Neighbor Greedy.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Tuple
from algorithms.backtracking import tsp_backtracking_exact, hamiltonian_cycle


NP_COMPLEXITY_CLASSES = {
    "P": {
        "name": "Polynomial Time",
        "definition": "The class of decision problems solvable by a Deterministic Turing Machine in polynomial time O(n^k).",
        "examples": ["Shortest Path (Dijkstra)", "Minimum Spanning Tree (Prim/Kruskal)", "Eulerian Circuit", "Sorting", "2-SAT"]
    },
    "NP": {
        "name": "Nondeterministic Polynomial Time",
        "definition": "The class of decision problems whose proposed solution (certificate) can be VERIFIED in polynomial time by a Deterministic Turing Machine.",
        "examples": ["Hamiltonian Cycle", "Travelling Salesperson Problem", "3-SAT", "0/1 Knapsack", "Graph Coloring", "Subset Sum"]
    },
    "NP-Complete": {
        "name": "NP-Complete (NPC)",
        "definition": "A problem X is NP-Complete if: 1. X is in NP, and 2. Every problem Y in NP is polynomial-time reducible to X (Y <=_P X).",
        "implication": "If ANY NP-Complete problem can be solved in polynomial time, then P = NP.",
        "examples": ["SAT", "3-SAT", "Hamiltonian Cycle", "Vertex Cover", "Clique", "Subset Sum"]
    },
    "NP-Hard": {
        "name": "NP-Hard",
        "definition": "A problem H is NP-Hard if every problem in NP is polynomial-time reducible to H. H need not be in NP (e.g. Halting problem, TSP Optimization).",
        "examples": ["Optimization TSP", "Halting Problem", "Maximum Cut"]
    }
}


def reduction_hamiltonian_cycle_to_tsp() -> Dict[str, Any]:
    """
    Formal walkthrough of Polynomial-Time Reduction:
    Hamiltonian Cycle (HC) <=_P Decision Travelling Salesperson Problem (TSP).
    """
    reduction_steps = [
        "1. Input to HC: An unweighted undirected graph G = (V, E) with n vertices.",
        "2. Question for HC: Does G contain a simple cycle that visits every vertex in V exactly once?",
        "3. Reduction Construction (Transformation f): Construct a complete weighted graph G' = (V, E') with n vertices.",
        "4. Edge Weight Assignment in G':",
        "   - If edge (u, v) ∈ E in original graph G, set weight w(u, v) = 1 in G'.",
        "   - If edge (u, v) ∉ E in original graph G, set weight w(u, v) = 2 in G'.",
        "5. Target Cost Budget for Decision TSP: Set target budget k = n.",
        "6. Question for TSP: Does G' have a travelling salesperson tour with total cost <= n?",
        "7. Correctness Proof (If and Only If):",
        "   - (=>) If G has a Hamiltonian cycle, that cycle traverses n edges, all present in E. In G', each edge costs 1, giving total cost exactly n <= n.",
        "   - (<=) If G' has a TSP tour with total cost <= n, since every tour has n edges and edge weights are >= 1, every chosen edge must have weight 1. Weight 1 edges correspond to actual edges in G. Hence, G has a Hamiltonian cycle.",
        "8. Time Complexity of Reduction: Constructing G' requires examining O(V^2) pairs of vertices, which runs in polynomial time O(V^2).",
        "9. Conclusion: Hamiltonian Cycle <=_P Decision TSP in polynomial time. Since Hamiltonian Cycle is NP-Complete, Decision TSP is also NP-Complete, and Optimization TSP is NP-Hard."
    ]

    return {
        "reduction_name": "Hamiltonian Cycle <=_P Decision TSP",
        "source_problem": "Hamiltonian Cycle (Known NP-Complete)",
        "target_problem": "Decision Travelling Salesperson Problem",
        "reduction_complexity": "O(V^2) Polynomial Time",
        "steps": reduction_steps
    }


def compare_exact_vs_greedy_tsp(dist_matrix: List[List[float]], start_vertex: int = 0) -> Dict[str, Any]:
    """
    Run and contrast Exact Backtracking TSP vs Nearest-Neighbor Greedy Heuristic on the same instance.
    """
    n = len(dist_matrix)
    if n > 10:
        raise ValueError(f"Instance size {n} too large for exact solver demonstration.")

    # 1. Exact TSP
    exact_res = tsp_backtracking_exact(dist_matrix, start_vertex)

    # 2. Nearest-Neighbor Heuristic
    start_t = time.perf_counter()
    visited = [False] * n
    curr = start_vertex
    visited[curr] = True
    greedy_tour = [curr]
    greedy_cost = 0.0

    for _ in range(n - 1):
        nxt = -1
        min_d = float("inf")
        for j in range(n):
            if not visited[j] and dist_matrix[curr][j] < min_d:
                min_d = dist_matrix[curr][j]
                nxt = j
        if nxt == -1 or min_d == float("inf"):
            break
        visited[nxt] = True
        greedy_tour.append(nxt)
        greedy_cost += min_d
        curr = nxt

    # Return to start
    return_dist = dist_matrix[curr][start_vertex]
    greedy_tour.append(start_vertex)
    greedy_cost += return_dist
    greedy_ms = (time.perf_counter() - start_t) * 1000.0

    cost_diff = round(greedy_cost - exact_res["best_tour_cost"], 3)
    error_pct = round((cost_diff / exact_res["best_tour_cost"] * 100.0), 2) if exact_res["best_tour_cost"] > 0 else 0.0

    return {
        "num_vertices": n,
        "exact_solution": {
            "tour": exact_res["best_tour"],
            "cost": exact_res["best_tour_cost"],
            "time_ms": exact_res["execution_time_ms"],
            "optimality": "Globally Optimal"
        },
        "greedy_heuristic": {
            "tour": greedy_tour,
            "cost": round(greedy_cost, 3),
            "time_ms": round(greedy_ms, 4),
            "optimality": "Approximation Heuristic"
        },
        "cost_difference": cost_diff,
        "error_percentage": error_pct,
        "speedup_factor": round(exact_res["execution_time_ms"] / max(0.001, greedy_ms), 1)
    }
