"""
Unit 1: Mathematical Analysis of Algorithms.
Covers sets, functions, relations, quantifiers, vectors, series, combinations,
loop execution count analysis, and amortized analysis with dynamic array doubling.
"""

from __future__ import annotations
import math
from typing import Any, Callable, Dict, List, Set, Tuple


# --- 1. Sets, Functions, and Relations ---

def set_operations_demo(set_a: Set[str], set_b: Set[str]) -> Dict[str, Any]:
    """
    Demonstrates fundamental set operations: Union, Intersection, Difference, Symmetric Difference,
    and Cartesian Product size.
    """
    return {
        "set_a": sorted(list(set_a)),
        "set_b": sorted(list(set_b)),
        "union": sorted(list(set_a | set_b)),
        "intersection": sorted(list(set_a & set_b)),
        "difference_a_minus_b": sorted(list(set_a - set_b)),
        "difference_b_minus_a": sorted(list(set_b - set_a)),
        "symmetric_difference": sorted(list(set_a ^ set_b)),
        "cartesian_product_size": len(set_a) * len(set_b)
    }


def check_relation_properties(domain: Set[str], relation: Set[Tuple[str, str]]) -> Dict[str, bool]:
    """
    Verify reflexive, symmetric, and transitive properties of a binary relation R on a finite domain.
    """
    # Reflexive: for all x in domain, (x, x) in R
    is_reflexive = all((x, x) in relation for x in domain)

    # Symmetric: for all (x, y) in R, (y, x) in R
    is_symmetric = all((y, x) in relation for (x, y) in relation)

    # Transitive: for all (x, y) in R and (y, z) in R, (x, z) in R
    is_transitive = True
    for (x, y) in relation:
        for (y2, z) in relation:
            if y == y2 and (x, z) not in relation:
                is_transitive = False
                break
        if not is_transitive:
            break

    is_equivalence = is_reflexive and is_symmetric and is_transitive

    return {
        "is_reflexive": is_reflexive,
        "is_symmetric": is_symmetric,
        "is_transitive": is_transitive,
        "is_equivalence_relation": is_equivalence
    }


# --- 2. Quantifiers in Algorithm Correctness ---

def evaluate_quantifiers(
    items: List[Dict[str, Any]],
    universal_predicate: Callable[[Dict[str, Any]], bool],
    existential_predicate: Callable[[Dict[str, Any]], bool]
) -> Dict[str, Any]:
    """
    Demonstrate Universal (∀) and Existential (∃) quantification over a dataset of items.
    """
    # Universal: ∀ x in items, P(x) is True
    universal_holds = True
    violating_item = None
    for item in items:
        if not universal_predicate(item):
            universal_holds = False
            violating_item = item
            break

    # Existential: ∃ x in items, Q(x) is True
    existential_holds = False
    satisfying_item = None
    for item in items:
        if existential_predicate(item):
            existential_holds = True
            satisfying_item = item
            break

    return {
        "universal_holds": universal_holds,
        "universal_counterexample": violating_item,
        "existential_holds": existential_holds,
        "existential_example": satisfying_item
    }


# --- 3. Series, Factorials, Combinations ---

def arithmetic_series_sum(n: int, a: float = 1.0, d: float = 1.0) -> Tuple[float, float, str]:
    """
    Compute sum of first n terms of arithmetic series: S_n = n/2 * (2a + (n-1)d).
    Returns (formula_result, loop_accumulated_result, derivation_string).
    """
    formula = (n / 2.0) * (2.0 * a + (n - 1) * d)
    accum = sum(a + i * d for i in range(n))
    derivation = f"S_{n} = ({n}/2) * (2*{a} + ({n}-1)*{d}) = {formula}"
    return formula, accum, derivation


def geometric_series_sum(n: int, a: float = 1.0, r: float = 2.0) -> Tuple[float, float, str]:
    """
    Compute sum of first n terms of geometric series: S_n = a*(1 - r^n) / (1 - r) for r != 1.
    """
    if r == 1.0:
        formula = a * n
    else:
        formula = a * (1.0 - (r ** n)) / (1.0 - r)
    accum = sum(a * (r ** i) for i in range(n))
    derivation = f"S_{n} = {a} * (1 - {r}^{n}) / (1 - {r}) = {formula}"
    return formula, accum, derivation


def permutations_combinations(n: int, r: int) -> Dict[str, int]:
    """
    Compute Permutations P(n, r) and Combinations C(n, r).
    P(n, r) = n! / (n-r)!
    C(n, r) = n! / (r! * (n-r)!)
    """
    if r < 0 or r > n:
        return {"n": n, "r": r, "permutations": 0, "combinations": 0}

    fact_n = math.factorial(n)
    fact_n_r = math.factorial(n - r)
    fact_r = math.factorial(r)

    p = fact_n // fact_n_r
    c = fact_n // (fact_r * fact_n_r)

    return {"n": n, "r": r, "permutations": p, "combinations": c}


# --- 4. Loop Operation Count Analysis ---

def analyze_loop_counters(n: int) -> Dict[str, Any]:
    """
    Inspect the exact execution step counts of standard for, nested for, and while loop constructs.
    """
    # 1. Single for-loop: O(n)
    c1 = 0
    for _ in range(n):
        c1 += 1

    # 2. Nested triangular for-loop: O(n^2), exact = n*(n+1)//2
    c2 = 0
    for i in range(n):
        for j in range(i, n):
            c2 += 1

    # 3. Logarithmic while-loop: O(log2 n)
    c3 = 0
    temp = n
    while temp > 1:
        temp //= 2
        c3 += 1

    return {
        "n": n,
        "single_for_count": c1,
        "single_for_theoretical": n,
        "nested_for_count": c2,
        "nested_for_theoretical": (n * (n + 1)) // 2,
        "log_while_count": c3,
        "log_while_theoretical": math.floor(math.log2(n)) if n > 0 else 0
    }


# --- 5. Amortized Analysis (Dynamic Array Resizing) ---

def simulate_dynamic_array_amortization(num_insertions: int) -> Dict[str, Any]:
    """
    Simulate inserting items into a dynamically resizing array with doubling capacity.
    Tracks raw copy costs, new insert costs, and aggregate cost per insertion.
    Proves that although individual resizes cost O(N), the amortized cost per append is O(1).
    """
    capacity = 1
    size = 0
    history = []
    total_cost = 0

    for i in range(1, num_insertions + 1):
        cost = 1  # 1 unit for inserting new element
        resized = False
        old_cap = capacity

        if size == capacity:
            # Table doubling: copy all existing elements
            cost += size
            capacity *= 2
            resized = True

        size += 1
        total_cost += cost
        amortized_cost_so_far = total_cost / i

        if i <= 16 or resized or i == num_insertions:
            history.append({
                "step": i,
                "size": size,
                "capacity": capacity,
                "resized": resized,
                "step_cost": cost,
                "total_cost": total_cost,
                "amortized_cost": round(amortized_cost_so_far, 3)
            })

    return {
        "num_insertions": num_insertions,
        "final_size": size,
        "final_capacity": capacity,
        "total_operations": total_cost,
        "overall_amortized_cost": round(total_cost / num_insertions, 3),
        "history_snapshots": history,
        "theoretical_bound": "Amortized O(1) via Aggregate Method (Total Cost <= 3*N)"
    }
