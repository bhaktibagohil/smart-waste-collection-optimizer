"""
Unit 2: Elementary and Advanced Sorting Algorithms.
Direct implementations of Bubble, Selection, Insertion, Heap, Counting, and Bucket sorts.
Instruments exact comparisons, swaps/movements, and time measurements.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Tuple


def bubble_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Bubble Sort: Repeatedly steps through list, compares adjacent elements and swaps them.
    Includes early-termination flag if no swaps occurred in a pass.
    Best: O(n), Average: O(n^2), Worst: O(n^2). Auxiliary Space: O(1). Stable: True.
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    start_t = time.perf_counter()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if key(a[j]) > key(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Bubble Sort",
        "sorted_list": a,
        "comparisons": comparisons,
        "swaps": swaps,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": True,
        "time_complexity": {"best": "O(n)", "average": "O(n^2)", "worst": "O(n^2)"},
        "space_complexity": "O(1) auxiliary",
        "assumptions": "General comparison sort. Inefficient for large arrays."
    }


def selection_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Selection Sort: Divides list into sorted and unsorted parts. Repeatedly finds minimum from unsorted.
    Best: O(n^2), Average: O(n^2), Worst: O(n^2). Auxiliary Space: O(1). Stable: False (standard swap).
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    start_t = time.perf_counter()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if key(a[j]) < key(a[min_idx]):
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Selection Sort",
        "sorted_list": a,
        "comparisons": comparisons,
        "swaps": swaps,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": False,
        "time_complexity": {"best": "O(n^2)", "average": "O(n^2)", "worst": "O(n^2)"},
        "space_complexity": "O(1) auxiliary",
        "assumptions": "Minimizes number of swaps (at most n-1 swaps), but comparison count is always n(n-1)/2."
    }


def insertion_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Insertion Sort: Builds sorted array one item at a time by shifting larger elements right.
    Best: O(n), Average: O(n^2), Worst: O(n^2). Auxiliary Space: O(1). Stable: True.
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0
    start_t = time.perf_counter()

    for i in range(1, n):
        cur = a[i]
        cur_val = key(cur)
        j = i - 1
        while j >= 0:
            comparisons += 1
            if key(a[j]) > cur_val:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = cur

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Insertion Sort",
        "sorted_list": a,
        "comparisons": comparisons,
        "swaps": shifts,  # shifts counted
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": True,
        "time_complexity": {"best": "O(n)", "average": "O(n^2)", "worst": "O(n^2)"},
        "space_complexity": "O(1) auxiliary",
        "assumptions": "Very fast for small or nearly sorted inputs. Adaptive."
    }


def heap_sort(arr: List[Any], key=lambda x: x) -> Dict[str, Any]:
    """
    Heap Sort: Builds max heap and repeatedly extracts maximum to the end.
    Best: O(n log n), Average: O(n log n), Worst: O(n log n). Auxiliary Space: O(1). Stable: False.
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    start_t = time.perf_counter()

    def heapify(length: int, i: int):
        nonlocal comparisons, swaps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < length:
            comparisons += 1
            if key(a[left]) > key(a[largest]):
                largest = left

        if right < length:
            comparisons += 1
            if key(a[right]) > key(a[largest]):
                largest = right

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps += 1
            heapify(length, largest)

    # 1. Build max heap: bottom-up from last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # 2. Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps += 1
        heapify(i, 0)

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Heap Sort",
        "sorted_list": a,
        "comparisons": comparisons,
        "swaps": swaps,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": False,
        "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)"},
        "space_complexity": "O(1) auxiliary",
        "assumptions": "In-place comparison sort with guaranteed O(n log n) worst case."
    }


def counting_sort(arr: List[int]) -> Dict[str, Any]:
    """
    Counting Sort: Non-comparison integer sort counting frequencies in range [min_val, max_val].
    Best: O(n + k), Average: O(n + k), Worst: O(n + k). Auxiliary Space: O(k). Stable: True.
    """
    if not arr:
        return {
            "algorithm": "Counting Sort",
            "sorted_list": [],
            "comparisons": 0,
            "swaps": 0,
            "execution_time_ms": 0.0,
            "is_stable": True,
            "time_complexity": {"best": "O(n+k)", "average": "O(n+k)", "worst": "O(n+k)"},
            "space_complexity": "O(k)",
            "assumptions": "Requires discrete integer keys with bounded range k = max - min."
        }

    # Verify input integer assumption
    if not all(isinstance(x, (int)) for x in arr):
        raise TypeError("Counting sort requires integer elements.")

    start_t = time.perf_counter()
    min_val = min(arr)
    max_val = max(arr)
    k = max_val - min_val + 1

    count = [0] * k
    output = [0] * len(arr)

    for x in arr:
        count[x - min_val] += 1

    # Prefix sums to maintain stability
    for i in range(1, k):
        count[i] += count[i - 1]

    for x in reversed(arr):
        output[count[x - min_val] - 1] = x
        count[x - min_val] -= 1

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Counting Sort",
        "sorted_list": output,
        "comparisons": 0,  # non-comparison sort
        "swaps": len(arr),  # elements placed
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": True,
        "time_complexity": {"best": "O(n+k)", "average": "O(n+k)", "worst": "O(n+k)"},
        "space_complexity": f"O(k) where k={k}",
        "assumptions": "Applicable strictly to integer keys where range k is not significantly larger than n."
    }


def bucket_sort(arr: List[float], bucket_count: int = 10) -> Dict[str, Any]:
    """
    Bucket Sort: Distributes elements across buckets, sorts each bucket (using insertion sort),
    and concatenates.
    Best: O(n + k), Average: O(n), Worst: O(n^2). Auxiliary Space: O(n + k). Stable: True.
    Assumes elements are uniformly distributed in a known numeric interval [min_val, max_val].
    """
    if not arr:
        return {
            "algorithm": "Bucket Sort",
            "sorted_list": [],
            "comparisons": 0,
            "swaps": 0,
            "execution_time_ms": 0.0,
            "is_stable": True,
            "time_complexity": {"best": "O(n+k)", "average": "O(n)", "worst": "O(n^2)"},
            "space_complexity": "O(n+k)",
            "assumptions": "Assumes input elements are drawn from a uniform continuous distribution."
        }

    start_t = time.perf_counter()
    min_v = min(arr)
    max_v = max(arr)

    if min_v == max_v:
        return {
            "algorithm": "Bucket Sort",
            "sorted_list": list(arr),
            "comparisons": 0,
            "swaps": 0,
            "execution_time_ms": 0.0,
            "is_stable": True,
            "time_complexity": {"best": "O(n)", "average": "O(n)", "worst": "O(n)"},
            "space_complexity": "O(n)",
            "assumptions": "All elements identical; trivial bucket sort."
        }

    # Create buckets
    buckets: List[List[float]] = [[] for _ in range(bucket_count)]
    val_range = max_v - min_v

    for x in arr:
        # Scale to [0, bucket_count - 1]
        norm = (x - min_v) / val_range
        idx = int(norm * bucket_count)
        if idx >= bucket_count:
            idx = bucket_count - 1
        buckets[idx].append(x)

    # Sort each bucket using insertion sort
    sorted_arr = []
    comparisons = 0
    swaps = 0

    for b in buckets:
        res = insertion_sort(b)
        sorted_arr.extend(res["sorted_list"])
        comparisons += res["comparisons"]
        swaps += res["swaps"]

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Bucket Sort",
        "sorted_list": sorted_arr,
        "comparisons": comparisons,
        "swaps": swaps,
        "execution_time_ms": round(elapsed_ms, 4),
        "is_stable": True,
        "time_complexity": {"best": "O(n+k)", "average": "O(n)", "worst": "O(n^2)"},
        "space_complexity": f"O(n+k) with {bucket_count} buckets",
        "assumptions": "Degrades to O(n^2) if all elements cluster into a single bucket (skewed distribution)."
    }
