"""
Unit tests for Divide and Conquer Algorithms.
"""

import pytest
from algorithms.divide_and_conquer import (
    merge_sort,
    quick_sort,
    max_min_divide_and_conquer,
    karatsuba_multiplication,
    strassen_2x2_multiply,
    naive_fibonacci
)


def test_merge_sort():
    arrays = [
        [38, 27, 43, 3, 9, 82, 10],
        [5, 4, 3, 2, 1],
        [],
        [1],
        [2, 2, 2]
    ]
    for arr in arrays:
        res = merge_sort(arr)
        assert res["sorted_list"] == sorted(arr)


def test_quick_sort():
    arrays = [
        [10, 80, 30, 90, 40, 50, 70],
        [5, 4, 3, 2, 1],
        [],
        [100],
        [4, 4, 4, 4]
    ]
    for arr in arrays:
        res = quick_sort(arr)
        assert res["sorted_list"] == sorted(arr)


def test_max_min_divide_and_conquer():
    arr = [1000, 11, 445, 1, 330, 3000]
    res = max_min_divide_and_conquer(arr)
    assert res["minimum"] == 1
    assert res["maximum"] == 3000
    assert res["comparisons"] <= res["naive_comparisons"]

    # Single element
    res_single = max_min_divide_and_conquer([42])
    assert res_single["minimum"] == 42
    assert res_single["maximum"] == 42

    with pytest.raises(ValueError):
        max_min_divide_and_conquer([])


def test_karatsuba_multiplication():
    test_cases = [
        (1234, 5678),
        (9999, 9999),
        (1024, 2048),
        (5, 7),
        (12345678, 87654321)
    ]
    for x, y in test_cases:
        res = karatsuba_multiplication(x, y)
        assert res["product"] == x * y
        assert res["verified_correct"] is True


def test_strassen_2x2_multiply():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    res = strassen_2x2_multiply(A, B)
    expected = [[19, 22], [43, 50]]
    assert res["result_matrix"] == expected
    assert res["scalar_multiplications"] == 7


def test_naive_fibonacci():
    res = naive_fibonacci(10)
    assert res["result"] == 55

    # Safe limit enforcement
    with pytest.raises(ValueError):
        naive_fibonacci(35)
