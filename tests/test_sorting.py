"""
Unit tests for Sorting Algorithms (Bubble, Selection, Insertion, Heap, Counting, Bucket).
"""

import pytest
from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    counting_sort,
    bucket_sort
)


@pytest.fixture
def sample_numeric_arrays():
    return [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [42],
        [],
        [7, 7, 7, 7, 7],
        [15, -3, 0, 8, -12, 4]
    ]


def test_bubble_sort(sample_numeric_arrays):
    for arr in sample_numeric_arrays:
        res = bubble_sort(arr)
        assert res["sorted_list"] == sorted(arr)
        assert res["algorithm"] == "Bubble Sort"
        assert res["comparisons"] >= 0


def test_selection_sort(sample_numeric_arrays):
    for arr in sample_numeric_arrays:
        res = selection_sort(arr)
        assert res["sorted_list"] == sorted(arr)
        assert res["algorithm"] == "Selection Sort"


def test_insertion_sort(sample_numeric_arrays):
    for arr in sample_numeric_arrays:
        res = insertion_sort(arr)
        assert res["sorted_list"] == sorted(arr)
        assert res["algorithm"] == "Insertion Sort"


def test_heap_sort(sample_numeric_arrays):
    for arr in sample_numeric_arrays:
        res = heap_sort(arr)
        assert res["sorted_list"] == sorted(arr)
        assert res["algorithm"] == "Heap Sort"


def test_counting_sort():
    int_arrays = [
        [4, 2, 2, 8, 3, 3, 1],
        [10, 5, 2, 7, 10, 5],
        [0, 0, 0],
        [99],
        []
    ]
    for arr in int_arrays:
        res = counting_sort(arr)
        assert res["sorted_list"] == sorted(arr)

    # Test error handling on invalid non-integer inputs
    with pytest.raises(TypeError):
        counting_sort([1.5, 2.3, 4.0])


def test_bucket_sort():
    float_arrays = [
        [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434],
        [12.5, 4.2, 8.9, 1.1, 19.8, 12.5],
        [5.0, 5.0, 5.0],
        [3.14],
        []
    ]
    for arr in float_arrays:
        res = bucket_sort(arr)
        assert res["sorted_list"] == sorted(arr)
