"""
Unit tests for Searching Algorithms (Binary Search).
"""

import pytest
from algorithms.divide_and_conquer import binary_search


def test_binary_search_found():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    res = binary_search(arr, 23)
    assert res["found_index"] == 5
    assert res["comparisons"] > 0


def test_binary_search_boundaries():
    arr = [10, 20, 30, 40, 50]
    res_first = binary_search(arr, 10)
    assert res_first["found_index"] == 0

    res_last = binary_search(arr, 50)
    assert res_last["found_index"] == 4


def test_binary_search_not_found():
    arr = [3, 9, 15, 21, 27]
    res = binary_search(arr, 100)
    assert res["found_index"] == -1

    res_low = binary_search(arr, 1)
    assert res_low["found_index"] == -1


def test_binary_search_single_element():
    res_present = binary_search([42], 42)
    assert res_present["found_index"] == 0

    res_absent = binary_search([42], 7)
    assert res_absent["found_index"] == -1


def test_binary_search_unsorted_exception():
    unsorted = [10, 5, 20, 8]
    with pytest.raises(ValueError, match="Binary Search requires the input list to be sorted"):
        binary_search(unsorted, 5)
