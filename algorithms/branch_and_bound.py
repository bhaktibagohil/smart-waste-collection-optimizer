"""
Unit 6: Branch and Bound Algorithms.
Educational implementations of:
1. Assignment Problem (Branch and Bound with cost matrix reduction).
2. 0/1 Knapsack (Branch and Bound with Best-First Search and fractional upper bounds).
3. Minimax Algorithm with Alpha-Beta Pruning on a decision game tree.
"""

from __future__ import annotations
import heapq
import time
from typing import Any, Dict, List, Optional, Tuple


# --- 1. Assignment Problem via Branch and Bound ---

class AssignmentNode:
    def __init__(self, parent, worker_idx: int, assigned_job: int, assigned_jobs_mask: int, cost: float):
        self.parent = parent
        self.worker_idx = worker_idx
        self.assigned_job = assigned_job
        self.assigned_jobs_mask = assigned_jobs_mask
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


def solve_assignment_problem_bnb(cost_matrix: List[List[float]]) -> Dict[str, Any]:
    """
    Solve the Assignment Problem using Branch and Bound.
    Assign N workers to N jobs with minimum total cost (one-to-one mapping).
    Lower bound: Row reductions (worker cost + minimum remaining cost for subsequent unassigned workers).
    """
    n = len(cost_matrix)
    if n == 0 or any(len(row) != n for row in cost_matrix):
        raise ValueError("Cost matrix must be a square N x N matrix.")

    start_t = time.perf_counter()

    def calculate_lower_bound(worker: int, mask: int) -> float:
        lb = 0.0
        for w in range(worker + 1, n):
            min_val = float("inf")
            for j in range(n):
                if not (mask & (1 << j)):
                    if cost_matrix[w][j] < min_val:
                        min_val = cost_matrix[w][j]
            if min_val != float("inf"):
                lb += min_val
        return lb

    # Min-heap priority queue
    initial_lb = calculate_lower_bound(-1, 0)
    root = AssignmentNode(None, -1, -1, 0, initial_lb)
    pq = [root]
    best_assignment = []
    min_total_cost = float("inf")
    nodes_generated = 1

    while pq:
        curr = heapq.heappop(pq)
        if curr.cost >= min_total_cost:
            continue

        w = curr.worker_idx + 1
        if w == n:
            if curr.cost < min_total_cost:
                min_total_cost = curr.cost
                # Traceback path
                path = []
                p = curr
                while p and p.worker_idx != -1:
                    path.append((p.worker_idx, p.assigned_job))
                    p = p.parent
                path.reverse()
                best_assignment = path
            continue

        for j in range(n):
            if not (curr.assigned_jobs_mask & (1 << j)):
                new_mask = curr.assigned_jobs_mask | (1 << j)
                actual_cost_so_far = curr.cost - calculate_lower_bound(w - 1, curr.assigned_jobs_mask) + cost_matrix[w][j]
                estimated_lb = actual_cost_so_far + calculate_lower_bound(w, new_mask)

                if estimated_lb < min_total_cost:
                    child = AssignmentNode(curr, w, j, new_mask, estimated_lb)
                    heapq.heappush(pq, child)
                    nodes_generated += 1

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Assignment Problem (Branch and Bound)",
        "matrix_size": n,
        "min_total_cost": round(min_total_cost, 3),
        "worker_job_assignments": best_assignment,
        "nodes_generated": nodes_generated,
        "execution_time_ms": round(elapsed_ms, 4)
    }


# --- 2. 0/1 Knapsack via Branch and Bound (Best-First Search) ---

class KnapsackBnbNode:
    def __init__(self, level: int, current_value: float, current_weight: float, upper_bound: float, taken: List[int]):
        self.level = level
        self.current_value = current_value
        self.current_weight = current_weight
        self.upper_bound = upper_bound
        self.taken = taken

    def __lt__(self, other):
        # Max-heap emulation by negating bound
        return self.upper_bound > other.upper_bound


def knapsack_branch_and_bound(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Dict[str, Any]:
    """
    0/1 Knapsack solved via Least-Cost / Best-First Search Branch and Bound.
    Calculates upper bound at each node using Fractional Knapsack relaxation.
    Prunes subtrees whose upper bound <= best value found so far.
    """
    n = len(weights)
    indexed = sorted(range(n), key=lambda i: values[i] / weights[i] if weights[i] > 0 else 0, reverse=True)
    w_sorted = [weights[i] for i in indexed]
    v_sorted = [values[i] for i in indexed]

    start_t = time.perf_counter()

    def bound(level: int, cur_w: float, cur_v: float) -> float:
        if cur_w >= capacity:
            return 0.0
        b = cur_v
        rem = capacity - cur_w
        for j in range(level, n):
            if w_sorted[j] <= rem:
                b += v_sorted[j]
                rem -= w_sorted[j]
            else:
                b += (rem / w_sorted[j]) * v_sorted[j]
                break
        return b

    root = KnapsackBnbNode(0, 0.0, 0.0, bound(0, 0.0, 0.0), [0] * n)
    pq = [root]
    max_val = 0.0
    best_taken = [0] * n
    nodes_explored = 0

    while pq:
        curr = heapq.heappop(pq)
        nodes_explored += 1

        if curr.upper_bound <= max_val:
            continue

        level = curr.level
        if level == n:
            continue

        # Branch 1: Include item at 'level'
        if curr.current_weight + w_sorted[level] <= capacity:
            new_w = curr.current_weight + w_sorted[level]
            new_v = curr.current_value + v_sorted[level]
            new_taken = list(curr.taken)
            new_taken[level] = 1

            if new_v > max_val:
                max_val = new_v
                best_taken = new_taken

            ub1 = bound(level + 1, new_w, new_v)
            if ub1 > max_val:
                heapq.heappush(pq, KnapsackBnbNode(level + 1, new_v, new_w, ub1, new_taken))

        # Branch 2: Exclude item at 'level'
        ub2 = bound(level + 1, curr.current_weight, curr.current_value)
        if ub2 > max_val:
            new_taken_ex = list(curr.taken)
            new_taken_ex[level] = 0
            heapq.heappush(pq, KnapsackBnbNode(level + 1, curr.current_value, curr.current_weight, ub2, new_taken_ex))

    # Map back to original indices
    final_selection = [0] * n
    for k in range(n):
        final_selection[indexed[k]] = best_taken[k]

    selected_indices = [i for i in range(n) if final_selection[i] == 1]
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "0/1 Knapsack (Branch and Bound LC-Search)",
        "capacity": capacity,
        "max_value": round(max_val, 3),
        "selected_indices": selected_indices,
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4)
    }


# --- 3. Minimax on a Defined Game Tree with Alpha-Beta Pruning ---

def minimax_alphabeta_demo(
    leaf_values: Optional[List[int]] = None,
    branching_factor: int = 2
) -> Dict[str, Any]:
    """
    Minimax evaluation on a small, clearly defined game tree with Alpha-Beta pruning.
    Demonstrates game tree search bounded by [alpha, beta] window.
    """
    leaves = leaf_values or [3, 5, 6, 9, 1, 2, 0, -1]  # 8 leaves = depth 3 binary tree
    eval_count = 0
    pruned_branches = 0
    start_t = time.perf_counter()

    def minimax(node_idx: int, depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        nonlocal eval_count, pruned_branches

        # Leaf condition
        if depth == 0:
            eval_count += 1
            return leaves[node_idx]

        if is_maximizing:
            max_eval = -float("inf")
            for i in range(branching_factor):
                child_idx = node_idx * branching_factor + i
                val = minimax(child_idx, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    pruned_branches += 1
                    break
            return int(max_eval)
        else:
            min_eval = float("inf")
            for i in range(branching_factor):
                child_idx = node_idx * branching_factor + i
                val = minimax(child_idx, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    pruned_branches += 1
                    break
            return int(min_eval)

    import math
    depth = int(math.log(len(leaves), branching_factor))
    optimal_value = minimax(0, depth, True, -float("inf"), float("inf"))
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Minimax with Alpha-Beta Pruning",
        "leaf_values": leaves,
        "tree_depth": depth,
        "branching_factor": branching_factor,
        "optimal_root_value": optimal_value,
        "leaves_evaluated": eval_count,
        "branches_pruned": pruned_branches,
        "execution_time_ms": round(elapsed_ms, 4),
        "note": "Minimax is an adversarial game tree search, independent of municipal vehicle routing."
    }
