"""
Unit 2: Recurrence Solving Analysis and Master Theorem Solver.
Covers Master Theorem, Substitution Method, Linear Homogeneous & Inhomogeneous Recurrences,
Recursion Trees, and Change of Variable transformations.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Tuple


def solve_master_theorem(a: float, b: float, d: float) -> Dict[str, Any]:
    """
    Solve recurrence of the form: T(n) = a * T(n/b) + Θ(n^d)
    Requirements: a >= 1, b > 1, d >= 0.
    """
    if a < 1:
        return {"applicable": False, "error": "Parameter 'a' must be >= 1 (number of subproblems)."}
    if b <= 1:
        return {"applicable": False, "error": "Parameter 'b' must be > 1 (subproblem shrinking factor)."}
    if d < 0:
        return {"applicable": False, "error": "Parameter 'd' must be >= 0 (polynomial degree of split/combine cost)."}

    log_b_a = math.log(a, b)
    epsilon_tol = 1e-6

    recurrence_str = f"T(n) = {a}*T(n/{b}) + Θ(n^{d})"
    log_str = f"log_{b}({a}) = {round(log_b_a, 4)}"

    if d < log_b_a - epsilon_tol:
        case = 1
        complexity = f"Θ(n^{round(log_b_a, 3)})"
        explanation = (
            f"Case 1: d ({d}) < log_b(a) ({round(log_b_a, 3)}). "
            f"Cost at the leaf level dominates the recursion tree. "
            f"Result: T(n) = Θ(n^(log_{b}({a}))) = {complexity}."
        )
    elif abs(d - log_b_a) <= epsilon_tol:
        case = 2
        complexity = f"Θ(n^{round(d, 3)} * log(n))"
        explanation = (
            f"Case 2: d ({d}) == log_b(a) ({round(log_b_a, 3)}). "
            f"Work is evenly distributed across all log_{b}(n) levels of the recursion tree. "
            f"Result: T(n) = Θ(n^{d} * log(n)) = {complexity}."
        )
    else:
        case = 3
        complexity = f"Θ(n^{round(d, 3)})"
        explanation = (
            f"Case 3: d ({d}) > log_b(a) ({round(log_b_a, 3)}). "
            f"Work at the root level dominates the tree (satisfies regularity condition a*(n/b)^d <= c*n^d for c < 1). "
            f"Result: T(n) = Θ(n^{d}) = {complexity}."
        )

    return {
        "applicable": True,
        "recurrence": recurrence_str,
        "a": a,
        "b": b,
        "d": d,
        "log_b_a": round(log_b_a, 4),
        "case": case,
        "complexity": complexity,
        "explanation": explanation
    }


def analyze_recursion_tree(a: int, b: float, depth_levels: int = 4) -> Dict[str, Any]:
    """
    Generate step-by-step table showing cost and subproblem count per level of a recursion tree.
    """
    levels = []
    total_nodes = 0

    for i in range(depth_levels):
        num_subproblems = int(a ** i)
        subproblem_size = f"n / ({b}^{i})"
        work_per_level = f"{num_subproblems} * f(n/{b}^{i})"
        total_nodes += num_subproblems

        levels.append({
            "level": i,
            "subproblems_count": num_subproblems,
            "subproblem_size": subproblem_size,
            "work_expression": work_per_level
        })

    return {
        "depth_inspected": depth_levels,
        "branching_factor_a": a,
        "shrink_factor_b": b,
        "tree_height": f"log_{b}(n)",
        "number_of_leaves": f"a^(log_{b}(n)) = n^(log_{b}({a}))",
        "level_breakdown": levels
    }


def solve_second_order_homogeneous(c1: float, c2: float) -> Dict[str, Any]:
    """
    Solve recurrence a_n = c1 * a_{n-1} + c2 * a_{n-2}.
    Characteristic equation: r^2 - c1*r - c2 = 0.
    """
    disc = c1 ** 2 + 4 * c2
    char_eq = f"r^2 - {c1}*r - {c2} = 0"

    if disc > 0:
        r1 = (c1 + math.sqrt(disc)) / 2.0
        r2 = (c1 - math.sqrt(disc)) / 2.0
        sol_form = f"a_n = C1 * ({round(r1, 3)})^n + C2 * ({round(r2, 3)})^n"
        nature = "Two distinct real roots"
    elif abs(disc) < 1e-9:
        r1 = c1 / 2.0
        r2 = r1
        sol_form = f"a_n = (C1 + C2 * n) * ({round(r1, 3)})^n"
        nature = "Repeated real root"
    else:
        real_part = c1 / 2.0
        imag_part = math.sqrt(-disc) / 2.0
        r_mod = math.sqrt(real_part**2 + imag_part**2)
        theta = math.atan2(imag_part, real_part)
        sol_form = f"a_n = ({round(r_mod, 3)})^n * [C1 * cos({round(theta, 3)}*n) + C2 * sin({round(theta, 3)}*n)]"
        nature = "Complex conjugate roots"

    return {
        "characteristic_equation": char_eq,
        "discriminant": round(disc, 4),
        "roots_nature": nature,
        "general_solution": sol_form
    }


def substitution_method_demonstration(recurrence_name: str = "MergeSort") -> Dict[str, Any]:
    """
    Walkthrough of the substitution method for verifying an asymptotic bound.
    Example: Prove T(n) = 2T(n/2) + n is O(n log n).
    """
    steps = [
        "1. Guess the form of the solution: T(n) <= c * n * log_2(n) for some positive constant c.",
        "2. Substitute inductive hypothesis into recurrence: T(n) <= 2 * [c * (n/2) * log_2(n/2)] + n",
        "3. Simplify: T(n) <= c * n * (log_2(n) - log_2(2)) + n = c * n * log_2(n) - c * n + n",
        "4. Bound the residual: c * n * log_2(n) - (c - 1) * n <= c * n * log_2(n) whenever (c - 1) >= 0, i.e., c >= 1.",
        "5. Base case: Check T(2) or T(3) for sufficiently large n0 to ensure initial boundary holds.",
        "6. Conclusion: By mathematical induction, T(n) = O(n log n) is proven rigorously."
    ]
    return {
        "recurrence": "T(n) = 2T(n/2) + n",
        "guessed_bound": "O(n log n)",
        "derivation_steps": steps
    }


def change_of_variable_demonstration() -> Dict[str, Any]:
    """
    Walkthrough of change of variable technique.
    Example: T(n) = 2T(sqrt(n)) + log_2(n).
    """
    steps = [
        "1. Given recurrence: T(n) = 2*T(sqrt(n)) + log(n).",
        "2. Let m = log_2(n), so n = 2^m and sqrt(n) = 2^(m/2).",
        "3. Rewrite: T(2^m) = 2*T(2^(m/2)) + m.",
        "4. Define S(m) = T(2^m): S(m) = 2*S(m/2) + m.",
        "5. Apply Master Theorem to S(m): a = 2, b = 2, d = 1 -> log_2(2) = 1 == d (Case 2).",
        "6. Therefore: S(m) = Θ(m * log_2(m)).",
        "7. Transform back to original variable n (m = log_2(n)): T(n) = Θ(log(n) * log(log(n)))."
    ]
    return {
        "original_recurrence": "T(n) = 2T(√n) + log(n)",
        "substitution": "m = log(n), S(m) = T(2^m)",
        "transformed_recurrence": "S(m) = 2S(m/2) + m",
        "final_complexity": "Θ(log(n) * log(log(n)))",
        "derivation_steps": steps
    }
