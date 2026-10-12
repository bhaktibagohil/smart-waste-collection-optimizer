"""
Unit 7: String Matching Algorithms.
Direct educational implementations of Naive String Matching,
Rabin-Karp (Rolling Hash), and Knuth-Morris-Pratt (KMP) algorithms.
Includes municipal complaint description keyword search demonstration.
"""

from __future__ import annotations
import time
from typing import Any, Dict, List, Tuple


# --- 1. Naive String Matching ---

def naive_string_match(text: str, pattern: str) -> Dict[str, Any]:
    """
    Naive String Matching: Checks for pattern occurrence at every text shift 0 <= s <= n - m.
    Time Complexity: Best O(n), Worst O((n - m + 1) * m). Auxiliary Space: O(1).
    Convention: Empty pattern returns [] (empty list).
    """
    if not pattern:
        return {
            "algorithm": "Naive String Matching",
            "matches": [],
            "character_comparisons": 0,
            "execution_time_ms": 0.0,
            "convention": "Empty pattern yields empty list of matches."
        }

    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0
    start_t = time.perf_counter()

    for s in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[s + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(s)

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Naive String Matching",
        "text_length": n,
        "pattern_length": m,
        "matches": matches,
        "match_count": len(matches),
        "character_comparisons": comparisons,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O((n - m + 1) * m)"
    }


# --- 2. Rabin-Karp Algorithm ---

def rabin_karp_match(text: str, pattern: str, prime_q: int = 101, radix_d: int = 256) -> Dict[str, Any]:
    """
    Rabin-Karp String Matching using Rolling Hash.
    Computes hash values of pattern and sliding text window modulo prime_q.
    Resolves hash collisions by character verification.
    Time Complexity: Average O(n + m), Worst O((n - m + 1) * m).
    """
    if not pattern:
        return {
            "algorithm": "Rabin-Karp",
            "matches": [],
            "character_comparisons": 0,
            "spurious_hits": 0,
            "execution_time_ms": 0.0
        }

    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0
    spurious_hits = 0
    start_t = time.perf_counter()

    if m > n:
        return {
            "algorithm": "Rabin-Karp",
            "matches": [],
            "character_comparisons": 0,
            "spurious_hits": 0,
            "execution_time_ms": 0.0
        }

    # h = (radix_d^(m-1)) % prime_q
    h = pow(radix_d, m - 1, prime_q)

    p_hash = 0
    t_hash = 0

    # Initial hash computation for pattern and first window
    for i in range(m):
        p_hash = (radix_d * p_hash + ord(pattern[i])) % prime_q
        t_hash = (radix_d * t_hash + ord(text[i])) % prime_q

    # Slide window over text
    for s in range(n - m + 1):
        if p_hash == t_hash:
            # Hash match -> verify characters
            match = True
            for j in range(m):
                comparisons += 1
                if text[s + j] != pattern[j]:
                    match = False
                    spurious_hits += 1
                    break
            if match:
                matches.append(s)

        # Compute next hash value using rolling hash formula
        if s < n - m:
            t_hash = (radix_d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % prime_q
            if t_hash < 0:
                t_hash += prime_q

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Rabin-Karp (Rolling Hash)",
        "matches": matches,
        "match_count": len(matches),
        "character_comparisons": comparisons,
        "spurious_hits": spurious_hits,
        "execution_time_ms": round(elapsed_ms, 4),
        "prime_modulus": prime_q,
        "time_complexity": "Average O(n + m), Worst O(n * m)"
    }


# --- 3. Knuth-Morris-Pratt (KMP) Algorithm ---

def compute_kmp_prefix_function(pattern: str) -> Tuple[List[int], int]:
    """
    Computes the prefix failure function (pi table) for KMP.
    pi[q] is the length of the longest proper prefix of pattern[0..q] that is also a suffix.
    """
    m = len(pattern)
    pi = [0] * m
    k = 0
    comparisons = 0

    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            comparisons += 1
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            comparisons += 1
            k += 1
        pi[q] = k

    return pi, comparisons


def kmp_string_match(text: str, pattern: str) -> Dict[str, Any]:
    """
    Knuth-Morris-Pratt (KMP) String Matching:
    Preprocesses pattern to construct pi array. Advances text pointer monotonically without backtracking.
    Time Complexity: O(n + m) guaranteed. Space: O(m).
    """
    if not pattern:
        return {
            "algorithm": "Knuth-Morris-Pratt (KMP)",
            "matches": [],
            "character_comparisons": 0,
            "prefix_table": [],
            "execution_time_ms": 0.0
        }

    n = len(text)
    m = len(pattern)
    matches = []
    start_t = time.perf_counter()

    pi, pi_comparisons = compute_kmp_prefix_function(pattern)
    comparisons = pi_comparisons
    q = 0  # Number of characters matched

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            comparisons += 1
            q = pi[q - 1]
        comparisons += 1
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q - 1]

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Knuth-Morris-Pratt (KMP)",
        "matches": matches,
        "match_count": len(matches),
        "character_comparisons": comparisons,
        "prefix_table": pi,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "Guaranteed O(n + m)",
        "space_complexity": "O(m) for prefix table"
    }


# --- 4. Municipal Complaint Search Application ---

SAMPLE_MUNICIPAL_COMPLAINTS = [
    {"ticket_id": "CMP-101", "bin_id": "BIN-02", "text": "Severe garbage overflow near Central Market South with foul smell."},
    {"ticket_id": "CMP-102", "bin_id": "BIN-05", "text": "Hospital waste bin is completely full and biomedical bags are spilling."},
    {"ticket_id": "CMP-103", "bin_id": "BIN-11", "text": "Industrial scrap and chemical containers overflowing on roadside."},
    {"ticket_id": "CMP-104", "bin_id": "BIN-01", "text": "Civic plaza bin lid broken and plastic waste blowing into street."},
    {"ticket_id": "CMP-105", "bin_id": "BIN-03", "text": "Garden bin full after festival event, urgent collection required."}
]


def search_complaint_tickets(
    query_pattern: str,
    complaints: Optional[List[Dict[str, str]]] = None,
    method: str = "kmp"
) -> Dict[str, Any]:
    """
    Search citizen municipal complaints using chosen string matching algorithm.
    """
    data = complaints or SAMPLE_MUNICIPAL_COMPLAINTS
    results = []
    total_comparisons = 0

    matcher_fn = {
        "naive": naive_string_match,
        "rabin_karp": rabin_karp_match,
        "kmp": kmp_string_match
    }.get(method.lower(), kmp_string_match)

    for item in data:
        # Case-insensitive search on ticket text
        t_lower = item["text"].lower()
        p_lower = query_pattern.lower()
        res = matcher_fn(t_lower, p_lower)
        total_comparisons += res["character_comparisons"]
        if res["matches"]:
            results.append({
                "ticket_id": item["ticket_id"],
                "bin_id": item["bin_id"],
                "text": item["text"],
                "match_indices": res["matches"]
            })

    return {
        "query": query_pattern,
        "method_used": method,
        "matched_tickets_count": len(results),
        "matched_tickets": results,
        "total_character_comparisons": total_comparisons
    }
