"""
Unit 1: Asymptotic Analysis and Complexity Profiler.
Provides definitions, limit quotient rules for Big-O / Big-Theta / Big-Omega,
and an empirical benchmark runner comparing theoretical growth rates against observed runtimes.
"""

from __future__ import annotations
import time
import math
from typing import Any, Callable, Dict, List, Tuple


ASYMPTOTIC_DEFINITIONS = {
    "Big-O": {
        "symbol": "O(g(n))",
        "name": "Asymptotic Upper Bound",
        "formal_definition": "f(n) <= c * g(n) for all n >= n0, where c > 0 and n0 >= 1",
        "meaning": "Worst-case running time guarantee. The algorithm will never grow faster than g(n)."
    },
    "Big-Omega": {
        "symbol": "Ω(g(n))",
        "name": "Asymptotic Lower Bound",
        "formal_definition": "f(n) >= c * g(n) for all n >= n0, where c > 0 and n0 >= 1",
        "meaning": "Best-case running time guarantee. The algorithm takes at least c * g(n) operations."
    },
    "Big-Theta": {
        "symbol": "Θ(g(n))",
        "name": "Asymptotically Tight Bound",
        "formal_definition": "c1 * g(n) <= f(n) <= c2 * g(n) for all n >= n0, where c1, c2 > 0 and n0 >= 1",
        "meaning": "The algorithm's growth rate is sandwiched tightly between two positive multiples of g(n)."
    }
}


def limit_quotient_comparison(fn_name_1: str, fn_name_2: str) -> Dict[str, str]:
    """
    Explain the limit rule for comparing two functions f(n) and g(n):
    L = lim_{n -> inf} [f(n) / g(n)].
    """
    return {
        "L_equals_zero": "If L = 0, then f(n) grows strictly slower than g(n); f(n) ∈ o(g(n)) ⊂ O(g(n)).",
        "L_equals_constant": "If 0 < L < ∞, then f(n) and g(n) have identical growth rates; f(n) ∈ Θ(g(n)).",
        "L_equals_infinity": "If L = ∞, then f(n) grows strictly faster than g(n); f(n) ∈ ω(g(n)) ⊂ Ω(g(n)).",
        "note": "Useful for functions where the formal definition constant 'c' is difficult to determine algebraically."
    }


def benchmark_function_sizes(
    func: Callable[[List[int]], Any],
    generator: Callable[[int], List[int]],
    sizes: List[int],
    runs_per_size: int = 3
) -> List[Dict[str, Any]]:
    """
    Empirically measure average execution time for a function across increasing input sizes.
    Important caveat: A single timing measurement does not prove an asymptotic complexity bound;
    it measures wall-clock time subject to interpreter, cache, and OS noise.
    """
    results = []

    for size in sizes:
        durations = []
        for _ in range(runs_per_size):
            data = generator(size)
            start_t = time.perf_counter()
            func(data)
            durations.append((time.perf_counter() - start_t) * 1000.0)  # ms

        avg_ms = sum(durations) / len(durations)
        results.append({
            "size": size,
            "avg_time_ms": round(avg_ms, 4),
            "min_time_ms": round(min(durations), 4),
            "max_time_ms": round(max(durations), 4),
            "theoretical_n": size,
            "theoretical_n_log_n": round(size * math.log2(size), 2) if size > 1 else size,
            "theoretical_n_squared": size * size
        })

    return results
