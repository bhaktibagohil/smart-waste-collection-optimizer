"""
Unit 4: Greedy Algorithms.
Direct educational implementations of Coin Change (Greedy), Prim's MST, Kruskal's MST,
Dijkstra's Shortest Path, Bellman-Ford Shortest Path, Fractional Knapsack,
Activity Selection (Job Scheduling), and Huffman Coding.
"""

from __future__ import annotations
import heapq
import time
from typing import Any, Dict, List, Optional, Set, Tuple


# --- 1. Greedy Making-Change Problem ---

def greedy_coin_change(coins: List[int], amount: int) -> Dict[str, Any]:
    """
    Greedy Coin Change: Always picks the largest coin value <= remaining amount.
    Note: For non-canonical coin systems (e.g. [1, 3, 4] for amount 6), greedy picks 4 + 1 + 1 (3 coins)
    instead of the optimal DP solution 3 + 3 (2 coins)!
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if not coins or any(c <= 0 for c in coins):
        raise ValueError("Coins must be positive integers.")

    sorted_coins = sorted(coins, reverse=True)
    rem = amount
    chosen = []
    start_t = time.perf_counter()

    for c in sorted_coins:
        count = rem // c
        if count > 0:
            chosen.extend([c] * count)
            rem -= count * c

    success = (rem == 0)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Greedy Coin Change",
        "coins_provided": sorted_coins,
        "amount": amount,
        "success": success,
        "coin_count": len(chosen) if success else -1,
        "coins_chosen": chosen if success else [],
        "remaining_uncovered": rem,
        "execution_time_ms": round(elapsed_ms, 4),
        "optimality_note": "Greedy is optimal for canonical currencies (e.g., standard US/Indian coins), but can fail on arbitrary denominations."
    }


# --- 2. Prim's Minimum Spanning Tree ---

def prim_mst(num_vertices: int, edges: List[Tuple[int, int, float]], start_node: int = 0) -> Dict[str, Any]:
    """
    Prim's Algorithm for Minimum Spanning Tree (MST).
    Grows a single tree from a starting vertex by greedily adding minimum weight incident edge.
    Time Complexity: O(E log V) with min-heap.
    """
    adj: Dict[int, List[Tuple[float, int]]] = {i: [] for i in range(num_vertices)}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    visited = set([start_node])
    min_heap: List[Tuple[float, int, int]] = []  # (weight, from_u, to_v)
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0

    start_t = time.perf_counter()

    for w, neighbor in adj[start_node]:
        heapq.heappush(min_heap, (w, start_node, neighbor))

    while min_heap and len(visited) < num_vertices:
        w, u, v = heapq.heappop(min_heap)
        if v in visited:
            continue

        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w

        for nxt_w, nxt_node in adj[v]:
            if nxt_node not in visited:
                heapq.heappush(min_heap, (nxt_w, v, nxt_node))

    is_spanning = (len(visited) == num_vertices)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Prim's MST",
        "is_connected_mst": is_spanning,
        "total_weight": round(total_weight, 3),
        "mst_edges": mst_edges,
        "vertices_covered": len(visited),
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(E log V)"
    }


# --- 3. Kruskal's Minimum Spanning Tree ---

class DisjointSetUnion:
    """Disjoint Set Union (Union-Find) with path compression and union by rank."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False

        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True


def kruskal_mst(num_vertices: int, edges: List[Tuple[int, int, float]]) -> Dict[str, Any]:
    """
    Kruskal's Algorithm for Minimum Spanning Tree (MST).
    Sorts all edges by non-decreasing weight and adds an edge if it doesn't create a cycle (DSU).
    Time Complexity: O(E log E).
    """
    start_t = time.perf_counter()
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DisjointSetUnion(num_vertices)
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0

    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == num_vertices - 1:
                break

    is_spanning = (len(mst_edges) == num_vertices - 1) if num_vertices > 1 else True
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Kruskal's MST",
        "is_connected_mst": is_spanning,
        "total_weight": round(total_weight, 3),
        "mst_edges": mst_edges,
        "edge_count": len(mst_edges),
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(E log E)"
    }


# --- 4. Dijkstra's Shortest Path Algorithm ---

def dijkstra_shortest_path(
    num_vertices: int,
    adj_list: Dict[int, List[Tuple[int, float]]],
    source: int
) -> Dict[str, Any]:
    """
    Dijkstra's Single-Source Shortest Path algorithm using a min-heap priority queue.
    Assumption: Edge weights MUST be non-negative.
    Time Complexity: O((V + E) log V).
    """
    # Verify non-negative weights
    for u, neighbors in adj_list.items():
        for v, w in neighbors:
            if w < 0:
                raise ValueError(f"Dijkstra cannot handle negative edge weight: edge ({u}, {v}) has weight {w}.")

    dist = {i: float("inf") for i in range(num_vertices)}
    parent = {i: None for i in range(num_vertices)}
    dist[source] = 0.0

    min_heap = [(0.0, source)]
    visited = set()
    start_t = time.perf_counter()

    while min_heap:
        d, u = heapq.heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)

        for v, w in adj_list.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = round(dist[u] + w, 4)
                parent[v] = u
                heapq.heappush(min_heap, (dist[v], v))

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Dijkstra's Shortest Path",
        "source": source,
        "distances": dist,
        "parents": parent,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O((V + E) log V)",
        "limitation": "Cannot handle negative edge weights. Greedy relaxation assumes explored nodes are finalized."
    }


# --- 5. Bellman-Ford Shortest Path Algorithm ---

def bellman_ford_shortest_path(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int
) -> Dict[str, Any]:
    """
    Bellman-Ford Single-Source Shortest Path Algorithm.
    Relaxes all edges V - 1 times. Detects reachable negative-weight cycles on V-th iteration.
    Time Complexity: O(V * E).
    """
    dist = {i: float("inf") for i in range(num_vertices)}
    parent = {i: None for i in range(num_vertices)}
    dist[source] = 0.0

    start_t = time.perf_counter()

    # Relax edges V - 1 times
    for _ in range(num_vertices - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = round(dist[u] + w, 4)
                parent[v] = u
                updated = True
        if not updated:
            break

    # Check for negative-weight cycles
    has_negative_cycle = False
    cycle_edge = None
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            has_negative_cycle = True
            cycle_edge = (u, v, w)
            break

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Bellman-Ford Shortest Path",
        "source": source,
        "has_negative_cycle": has_negative_cycle,
        "negative_cycle_edge": cycle_edge,
        "distances": dist if not has_negative_cycle else "Undefined due to negative-weight cycle",
        "parents": parent if not has_negative_cycle else {},
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(V * E)",
        "advantage": "Handles arbitrary edge weights and reliably detects negative-weight cycles."
    }


# --- 6. Fractional Greedy Knapsack ---

def fractional_knapsack_greedy(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Dict[str, Any]:
    """
    Fractional Knapsack: Allows taking fractional portions of items.
    Greedy strategy: Sort items by value/weight ratio descending.
    Guaranteed optimal for continuous/fractional items (NOT discrete 0/1 knapsack).
    """
    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal length.")

    n = len(weights)
    items = []
    for i in range(n):
        w = weights[i]
        v = values[i]
        ratio = v / w if w > 0 else 0.0
        items.append({"item_id": i, "weight": w, "value": v, "ratio": ratio})

    # Sort descending by ratio
    items.sort(key=lambda x: x["ratio"], reverse=True)

    rem_cap = capacity
    total_val = 0.0
    selections = []
    start_t = time.perf_counter()

    for it in items:
        if rem_cap <= 0:
            break
        if it["weight"] <= rem_cap:
            selections.append({"item_id": it["item_id"], "fraction": 1.0, "taken_weight": it["weight"], "value_gained": it["value"]})
            total_val += it["value"]
            rem_cap -= it["weight"]
        else:
            fraction = rem_cap / it["weight"]
            gain = fraction * it["value"]
            selections.append({"item_id": it["item_id"], "fraction": round(fraction, 4), "taken_weight": rem_cap, "value_gained": round(gain, 4)})
            total_val += gain
            rem_cap = 0.0

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Fractional Knapsack (Greedy)",
        "capacity": capacity,
        "total_value": round(total_val, 3),
        "selections": selections,
        "execution_time_ms": round(elapsed_ms, 4),
        "optimality_proof": "Greedy choice property holds for fractional items, but fails for 0/1 integer items."
    }


# --- 7. Activity Selection / Job Scheduling ---

def activity_selection_greedy(start_times: List[float], finish_times: List[float]) -> Dict[str, Any]:
    """
    Activity Selection / Job Scheduling: Select maximum number of mutually compatible activities.
    Greedy Choice: Always select the activity with the earliest finish time.
    Time Complexity: O(n log n) for sorting.
    """
    if len(start_times) != len(finish_times):
        raise ValueError("Start times and finish times must have identical length.")

    activities = []
    for i in range(len(start_times)):
        activities.append({"id": i, "start": start_times[i], "finish": finish_times[i]})

    # Sort by finish time ascending
    activities.sort(key=lambda x: x["finish"])

    selected = []
    last_finish = -float("inf")
    start_t = time.perf_counter()

    for act in activities:
        if act["start"] >= last_finish:
            selected.append(act)
            last_finish = act["finish"]

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Activity Selection (Job Scheduling)",
        "total_activities": len(start_times),
        "selected_count": len(selected),
        "selected_activities": selected,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(n log n)"
    }


# --- 8. Huffman Coding ---

class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_encoding(text: str) -> Dict[str, Any]:
    """
    Huffman Coding: Optimal prefix code construction for lossless data compression.
    Builds min-heap of character frequencies and merges lowest frequency nodes.
    Time Complexity: O(k log k) where k is the number of distinct characters.
    """
    if not text:
        return {"algorithm": "Huffman Coding", "encoded_bitstring": "", "codebook": {}, "compression_ratio": 0.0}

    start_t = time.perf_counter()

    # Calculate frequencies
    freq_map: Dict[str, int] = {}
    for ch in text:
        freq_map[ch] = freq_map.get(ch, 0) + 1

    # Single distinct character edge case
    if len(freq_map) == 1:
        ch = next(iter(freq_map.keys()))
        codebook = {ch: "0"}
        encoded = "0" * len(text)
        return {
            "algorithm": "Huffman Coding",
            "codebook": codebook,
            "encoded_bitstring": encoded,
            "original_bits": len(text) * 8,
            "compressed_bits": len(encoded),
            "compression_ratio": round((len(text) * 8) / max(1, len(encoded)), 2),
            "execution_time_ms": 0.0
        }

    # Min-heap
    heap = [HuffmanNode(ch, freq) for ch, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(None, n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)

    root = heap[0]
    codebook: Dict[str, str] = {}

    def build_codes(node: HuffmanNode, current_code: str):
        if node is None:
            return
        if node.char is not None:
            codebook[node.char] = current_code
            return
        build_codes(node.left, current_code + "0")
        build_codes(node.right, current_code + "1")

    build_codes(root, "")

    encoded_bitstring = "".join(codebook[ch] for ch in text)
    orig_bits = len(text) * 8
    comp_bits = len(encoded_bitstring)
    comp_ratio = round(orig_bits / max(1, comp_bits), 2)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Huffman Coding",
        "frequencies": freq_map,
        "codebook": codebook,
        "encoded_bitstring": encoded_bitstring[:100] + ("..." if len(encoded_bitstring) > 100 else ""),
        "original_bits": orig_bits,
        "compressed_bits": comp_bits,
        "compression_ratio": comp_ratio,
        "execution_time_ms": round(elapsed_ms, 4)
    }
