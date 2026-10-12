"""
Unit tests for String Matching Algorithms (Naive, Rabin-Karp, KMP).
"""

import pytest
from algorithms.string_matching import (
    naive_string_match,
    rabin_karp_match,
    kmp_string_match,
    compute_kmp_prefix_function,
    search_complaint_tickets
)


def test_string_matching_standard_pattern():
    text = "AABAACAADAABAABA"
    pattern = "AABA"

    res_naive = naive_string_match(text, pattern)
    res_rk = rabin_karp_match(text, pattern)
    res_kmp = kmp_string_match(text, pattern)

    expected = [0, 9, 12]
    assert res_naive["matches"] == expected
    assert res_rk["matches"] == expected
    assert res_kmp["matches"] == expected


def test_string_matching_overlapping():
    text = "AAAAAA"
    pattern = "AAA"
    expected = [0, 1, 2, 3]

    assert naive_string_match(text, pattern)["matches"] == expected
    assert rabin_karp_match(text, pattern)["matches"] == expected
    assert kmp_string_match(text, pattern)["matches"] == expected


def test_string_matching_not_found():
    text = "HELLO WORLD"
    pattern = "XYZ"

    assert naive_string_match(text, pattern)["matches"] == []
    assert rabin_karp_match(text, pattern)["matches"] == []
    assert kmp_string_match(text, pattern)["matches"] == []


def test_string_matching_empty_pattern_convention():
    text = "TEST"
    pattern = ""

    assert naive_string_match(text, pattern)["matches"] == []
    assert rabin_karp_match(text, pattern)["matches"] == []
    assert kmp_string_match(text, pattern)["matches"] == []


def test_kmp_prefix_table():
    pattern = "ABABCABAB"
    pi, _ = compute_kmp_prefix_function(pattern)
    assert pi == [0, 0, 1, 2, 0, 1, 2, 3, 4]


def test_search_complaint_tickets():
    res = search_complaint_tickets("overflow", method="kmp")
    assert res["matched_tickets_count"] >= 2
    for t in res["matched_tickets"]:
        assert "overflow" in t["text"].lower()
