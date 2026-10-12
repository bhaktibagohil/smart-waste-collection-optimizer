"""
Unit 5: Dynamic Programming.
Direct educational implementations of Binomial Coefficient, Principle of Optimality,
DP Coin Change, 0/1 Knapsack, Floyd-Warshall All-Pairs Shortest Paths,
Matrix-Chain Multiplication, and Longest Common Subsequence (LCS).
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Optional, Tuple


# --- 1. Binomial Coefficient C(n, k) ---

def binomial_coefficient_dp(n: int, k: int) -> Dict[str, Any]:
    """
    Compute C(n, k) using Pascal's identity: C(n, k) = C(n-1, k-1) + C(n-1, k).
    Time Complexity: O(n * k). Auxiliary Space: O(k).
    """
    if k < 0 or k > n:
        return {"n": n, "k": k, "result": 0, "dp_table": []}

    start_t = time.perf_counter()
    dp = [0] * (k + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            dp[j] = dp[j] + dp[j - 1]

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Binomial Coefficient DP",
        "n": n,
        "k": k,
        "result": dp[k],
        "execution_time_ms": round(elapsed_ms, 4),
        "recurrence": "C(n, k) = C(n-1, k-1) + C(n-1, k)",
        "space_complexity": "O(k) optimized 1D DP table"
    }


# --- 2. Coin Change Problem (DP) ---

def coin_change_min_coins_dp(coins: List[int], amount: int) -> Dict[str, Any]:
    """
    Find minimum number of coins to make change for given amount using DP.
    Recurrence: dp[a] = min_{c in coins} (dp[a - c] + 1).
    Time Complexity: O(amount * len(coins)). Space: O(amount).
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if amount == 0:
        return {"amount": 0, "min_coins": 0, "coins_used": []}

    start_t = time.perf_counter()
    dp = [float("inf")] * (amount + 1)
    last_coin = [-1] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if a >= c and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                last_coin[a] = c

    is_possible = dp[amount] != float("inf")
    coins_used = []
    if is_possible:
        curr = amount
        while curr > 0:
            c = last_coin[curr]
            coins_used.append(c)
            curr -= c

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Coin Change Min Coins (DP)",
        "coins_available": coins,
        "amount": amount,
        "is_possible": is_possible,
        "min_coins": dp[amount] if is_possible else -1,
        "coins_used": coins_used,
        "execution_time_ms": round(elapsed_ms, 4),
        "optimality_guarantee": "Provably optimal for all positive coin denominations."
    }


# --- 3. 0/1 Knapsack Problem (DP) ---

def knapsack_01_dp(
    weights: List[int],
    values: List[int],
    capacity: int
) -> Dict[str, Any]:
    """
    0/1 Knapsack using Dynamic Programming:
    Items cannot be split; each item is either included (1) or excluded (0).
    Recurrence: dp[i][w] = max(dp[i-1][w], dp[i-1][w - w_i] + v_i).
    Time: O(n * W). Space: O(n * W).
    """
    if len(weights) != len(values):
        raise ValueError("Weights and values must match in length.")
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    start_t = time.perf_counter()

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking to find selected items
    selected_indices = []
    curr_w = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            selected_indices.append(i - 1)
            curr_w -= weights[i - 1]

    selected_indices.reverse()
    total_val = dp[n][capacity]
    total_wt = sum(weights[idx] for idx in selected_indices)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "0/1 Knapsack (DP)",
        "max_value": total_val,
        "total_weight_taken": total_wt,
        "capacity": capacity,
        "selected_indices": selected_indices,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(n * W) pseudo-polynomial",
        "space_complexity": "O(n * W)"
    }


# --- 4. Floyd-Warshall All-Pairs Shortest Paths ---

def floyd_warshall_all_pairs(num_vertices: int, dist_matrix: List[List[float]]) -> Dict[str, Any]:
    """
    Floyd-Warshall algorithm for All-Pairs Shortest Paths.
    Recurrence: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) for intermediate vertex k.
    Detects negative cycles if dist[i][i] < 0.
    Time Complexity: O(V^3). Space Complexity: O(V^2).
    """
    n = num_vertices
    dist = [[dist_matrix[i][j] for j in range(n)] for i in range(n)]
    next_node = [[j if dist[i][j] != float("inf") and i != j else None for j in range(n)] for i in range(n)]

    start_t = time.perf_counter()

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = round(dist[i][k] + dist[k][j], 4)
                        next_node[i][j] = next_node[i][k]

    # Check for negative cycles
    has_negative_cycle = any(dist[i][i] < 0 for i in range(n))
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Floyd-Warshall All-Pairs Shortest Paths",
        "has_negative_cycle": has_negative_cycle,
        "distance_matrix": dist,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(V^3)"
    }


# --- 5. Matrix Chain Multiplication (MCM) ---

def matrix_chain_multiplication(dimensions: List[int]) -> Dict[str, Any]:
    """
    Matrix Chain Multiplication: Finds optimal parenthesization order for multiplying matrices.
    Dimensions: matrix A_i has dimension dimensions[i-1] x dimensions[i].
    Recurrence: m[i][j] = min_{i <= k < j} (m[i][k] + m[k+1][j] + p_{i-1} * p_k * p_j).
    Time: O(n^3). Space: O(n^2).
    """
    n = len(dimensions) - 1
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]
    start_t = time.perf_counter()

    # l is chain length
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    def build_parentheses(i: int, j: int) -> str:
        if i == j:
            return f"A{i + 1}"
        k = s[i][j]
        left = build_parentheses(i, k)
        right = build_parentheses(k + 1, j)
        return f"({left} * {right})"

    order_str = build_parentheses(0, n - 1) if n > 0 else ""
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Matrix Chain Multiplication",
        "min_scalar_multiplications": m[0][n - 1] if n > 0 else 0,
        "optimal_parenthesization": order_str,
        "matrix_count": n,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(n^3)",
        "space_complexity": "O(n^2)"
    }


# --- 6. Longest Common Subsequence (LCS) ---

def longest_common_subsequence(s1: str, s2: str) -> Dict[str, Any]:
    """
    Longest Common Subsequence: Finds longest subsequence present in both strings in same order.
    Time: O(m * n). Space: O(m * n).
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    start_t = time.perf_counter()

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct LCS string
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_string = "".join(reversed(lcs_chars))
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Longest Common Subsequence (LCS)",
        "s1": s1,
        "s2": s2,
        "lcs_length": dp[m][n],
        "lcs_string": lcs_string,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(m * n)"
    }


# --- 7. Comparative Benchmark: Greedy vs DP Counterexample ---

def compare_greedy_vs_dp_coin_change() -> Dict[str, Any]:
    """
    Canonical demonstration where Greedy fails to find the optimal solution, but DP succeeds.
    Coin system: [1, 3, 4], Target amount: 6.
    Greedy takes: 4 + 1 + 1 (3 coins).
    DP takes: 3 + 3 (2 coins) -> OPTIMAL!
    """
    coins = [1, 3, 4]
    amount = 6

    # Greedy simulation
    greedy_chosen = []
    rem = amount
    for c in sorted(coins, reverse=True):
        while rem >= c:
            greedy_chosen.append(c)
            rem -= c

    # DP optimal
    dp_res = coin_change_min_coins_dp(coins, amount)

    return {
        "coins": coins,
        "amount": amount,
        "greedy_solution": greedy_chosen,
        "greedy_coin_count": len(greedy_chosen),
        "dp_solution": dp_res["coins_used"],
        "dp_coin_count": dp_res["min_coins"],
        "greedy_is_suboptimal": len(greedy_chosen) > dp_res["min_coins"],
        "explanation": "Greedy makes irrevocable local choices (choosing 4 leaves 2, which requires two 1s). DP evaluates all subproblems globally."
    }
