"""
Unit 3: Divide and Conquer Algorithms.
Direct implementations of Binary Search, Merge Sort, Quick Sort, Max-Min problem,
Karatsuba large integer multiplication, Strassen matrix multiplication, and exponential-time Fibonacci.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Tuple, Optional


# --- 1. Binary Search ---

def binary_search(arr: List[Any], target: Any) -> Dict[str, Any]:
    """
    Binary Search: Searches for target in a sorted list by repeatedly dividing search interval in half.
    Requires sorted input (validated upfront).
    Time Complexity: Best O(1), Average O(log n), Worst O(log n). Space: O(1) iterative.
    """
    # Validate sorted input requirement
    is_sorted = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    if not is_sorted:
        raise ValueError("Binary Search requires the input list to be sorted in ascending order.")

    comparisons = 0
    low = 0
    high = len(arr) - 1
    found_idx = -1
    trace = []

    start_t = time.perf_counter()

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        trace.append({"low": low, "mid": mid, "high": high, "mid_val": arr[mid]})

        if arr[mid] == target:
            found_idx = mid
            break
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Binary Search",
        "target": target,
        "found_index": found_idx,
        "comparisons": comparisons,
        "execution_time_ms": round(elapsed_ms, 4),
        "search_trace": trace,
        "time_complexity": {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)"},
        "space_complexity": "O(1) auxiliary"
    }


# --- 2. Merge Sort ---

def merge_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Merge Sort: Divide array into halves, recursively sort them, and merge.
    Time Complexity: Best O(n log n), Average O(n log n), Worst O(n log n). Space: O(n) auxiliary. Stable: True.
    """
    a = list(arr)
    comparisons = 0
    start_t = time.perf_counter()

    def sort_recursive(sub: List[Any]) -> List[Any]:
        nonlocal comparisons
        if len(sub) <= 1:
            return sub

        mid = len(sub) // 2
        left = sort_recursive(sub[:mid])
        right = sort_recursive(sub[mid:])

        # Merge step
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_result = sort_recursive(a)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Merge Sort",
        "sorted_list": sorted_result,
        "comparisons": comparisons,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": True,
        "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)"},
        "space_complexity": "O(n) auxiliary"
    }


# --- 3. Quick Sort ---

def quick_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Quick Sort: Partitions array around a pivot element and recursively sorts partitions.
    Using Lomuto partitioning scheme.
    Time Complexity: Best O(n log n), Average O(n log n), Worst O(n^2). Space: O(log n) call stack.
    """
    a = list(arr)
    comparisons = 0
    swaps = 0
    start_t = time.perf_counter()

    def partition(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot_val = key(a[high])
        i = low - 1

        for j in range(low, high):
            comparisons += 1
            if key(a[j]) <= pivot_val:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps += 1

        a[i + 1], a[high] = a[high], a[i + 1]
        swaps += 1
        return i + 1

    def sort_recursive(low: int, high: int):
        if low < high:
            pi = partition(low, high)
            sort_recursive(low, pi - 1)
            sort_recursive(pi + 1, high)

    sort_recursive(0, len(a) - 1)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Quick Sort",
        "sorted_list": a,
        "comparisons": comparisons,
        "swaps": swaps,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": False,
        "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n^2)"},
        "space_complexity": "O(log n) stack auxiliary"
    }


# --- 4. Max-Min Problem (Tournament Divide & Conquer) ---

def max_min_divide_and_conquer(arr: List[float]) -> Dict[str, Any]:
    """
    Find both maximum and minimum in an array using Divide and Conquer.
    Theoretical comparisons: 3n/2 - 2 (vs 2n - 2 naive linear scan).
    """
    if not arr:
        raise ValueError("Cannot find min/max of empty array.")

    comparisons = 0
    start_t = time.perf_counter()

    def helper(low: int, high: int) -> Tuple[float, float]:
        nonlocal comparisons
        if low == high:
            return arr[low], arr[low]

        if high == low + 1:
            comparisons += 1
            if arr[low] < arr[high]:
                return arr[low], arr[high]
            else:
                return arr[high], arr[low]

        mid = (low + high) // 2
        min1, max1 = helper(low, mid)
        min2, max2 = helper(mid + 1, high)

        comparisons += 2
        overall_min = min1 if min1 < min2 else min2
        overall_max = max1 if max1 > max2 else max2
        return overall_min, overall_max

    min_val, max_val = helper(0, len(arr) - 1)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    n = len(arr)
    naive_comparisons = 2 * (n - 1) if n > 0 else 0

    return {
        "algorithm": "Max-Min Divide and Conquer",
        "minimum": min_val,
        "maximum": max_val,
        "comparisons": comparisons,
        "naive_comparisons": naive_comparisons,
        "comparisons_saved": naive_comparisons - comparisons,
        "execution_time_ms": round(elapsed_ms, 4),
        "recurrence": "T(n) = 2T(n/2) + 2 with T(2)=1, T(1)=0 -> 3n/2 - 2 comparisons"
    }


# --- 5. Karatsuba Large Integer Multiplication ---

def karatsuba_multiplication(x: int, y: int) -> Dict[str, Any]:
    """
    Karatsuba Algorithm for multiplying two large integers.
    Divides integers into high and low halves and performs 3 multiplications instead of 4.
    Complexity: O(n^(log_2 3)) ≈ O(n^1.585) vs standard O(n^2).
    """
    recursive_multiplications = 0
    start_t = time.perf_counter()

    def multiply(num1: int, num2: int) -> int:
        nonlocal recursive_multiplications
        # Base case: small integers multiplied directly
        if num1 < 10 or num2 < 10:
            return num1 * num2

        n = max(len(str(num1)), len(str(num2)))
        m = n // 2

        high1, low1 = divmod(num1, 10 ** m)
        high2, low2 = divmod(num2, 10 ** m)

        recursive_multiplications += 3
        z0 = multiply(low1, low2)
        z1 = multiply(low1 + high1, low2 + high2)
        z2 = multiply(high1, high2)

        return (z2 * 10 ** (2 * m)) + ((z1 - z2 - z0) * 10 ** m) + z0

    product = multiply(x, y)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Karatsuba Large Integer Multiplication",
        "x": x,
        "y": y,
        "product": product,
        "verified_correct": (product == x * y),
        "recursive_calls": recursive_multiplications,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(n^log2(3)) ≈ O(n^1.585)"
    }


# --- 6. Matrix Multiplication (Standard vs Strassen) ---

def standard_matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Standard O(n^3) matrix multiplication."""
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def strassen_2x2_multiply(A: List[List[float]], B: List[List[float]]) -> Dict[str, Any]:
    """
    Strassen's Matrix Multiplication for 2x2 matrices using 7 scalar multiplications instead of 8.
    Recurrence: T(n) = 7*T(n/2) + O(n^2) -> O(n^(log_2 7)) ≈ O(n^2.807).
    """
    if len(A) != 2 or len(B) != 2 or len(A[0]) != 2 or len(B[0]) != 2:
        raise ValueError("Strassen demonstration currently configured for 2x2 matrices.")

    start_t = time.perf_counter()

    # Strassen's 7 sub-products
    M1 = (A[0][0] + A[1][1]) * (B[0][0] + B[1][1])
    M2 = (A[1][0] + A[1][1]) * B[0][0]
    M3 = A[0][0] * (B[0][1] - B[1][1])
    M4 = A[1][1] * (B[1][0] - B[0][0])
    M5 = (A[0][0] + A[0][1]) * B[1][1]
    M6 = (A[1][0] - A[0][0]) * (B[0][0] + B[0][1])
    M7 = (A[0][1] - A[1][1]) * (B[1][0] + B[1][1])

    # Reconstruct 2x2 result
    C00 = M1 + M4 - M5 + M7
    C01 = M3 + M5
    C10 = M2 + M4
    C11 = M1 - M2 + M3 + M6

    C = [[round(C00, 4), round(C01, 4)], [round(C10, 4), round(C11, 4)]]
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Strassen's Matrix Multiplication (2x2)",
        "result_matrix": C,
        "scalar_multiplications": 7,
        "standard_multiplications": 8,
        "multiplications_saved": 1,
        "execution_time_ms": round(elapsed_ms, 4),
        "recurrence": "T(n) = 7T(n/2) + Θ(n^2) -> Θ(n^log2(7)) ≈ Θ(n^2.807)"
    }


# --- 7. Exponential-Time Algorithm Demonstration ---

def naive_fibonacci(n: int) -> Dict[str, Any]:
    """
    Naive recursive Fibonacci: T(n) = T(n-1) + T(n-2) + O(1) -> O(2^n).
    Demonstrates exponential growth on small inputs (restricted to n <= 30 to prevent UI hangs).
    """
    if n > 30:
        raise ValueError("Input n exceeds safe limit (30) for exponential naive recursion.")

    calls_count = 0
    start_t = time.perf_counter()

    def fib(val: int) -> int:
        nonlocal calls_count
        calls_count += 1
        if val <= 1:
            return val
        return fib(val - 1) + fib(val - 2)

    ans = fib(n)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Naive Recursive Fibonacci",
        "n": n,
        "result": ans,
        "recursive_calls": calls_count,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(2^n) exponential",
        "contrast": "Iterative or DP alternative achieves O(n) using only n steps."
    }
