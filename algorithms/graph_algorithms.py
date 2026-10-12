"""
Unit 6: Graph Exploration Algorithms.
Implements Adjacency List/Matrix representations, Breadth-First Search (BFS),
Depth-First Search (DFS) with discovery/finish times and cycle detection,
and Topological Sorting (Kahn's in-degree algorithm).
"""

from __future__ import annotations
import collections
import time
from typing import Any, Dict, List, Optional, Set, Tuple


class GraphRepresentation:
    """Represents directed or undirected graphs using both adjacency lists and matrices."""

    def __init__(self, num_vertices: int, directed: bool = False):
        self.v = num_vertices
        self.directed = directed
        self.adj_list: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}
        self.adj_matrix: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]
        self.edges: List[Tuple[int, int]] = []

    def add_edge(self, u: int, v: int) -> None:
        if 0 <= u < self.v and 0 <= v < self.v:
            self.adj_list[u].append(v)
            self.adj_matrix[u][v] = 1
            self.edges.append((u, v))
            if not self.directed:
                self.adj_list[v].append(u)
                self.adj_matrix[v][u] = 1


def breadth_first_search(graph: GraphRepresentation, start_vertex: int = 0) -> Dict[str, Any]:
    """
    Breadth-First Search (BFS): Explores graph level by level using a FIFO queue.
    Finds shortest paths in unweighted graphs.
    Time Complexity: O(V + E). Space: O(V).
    """
    if not (0 <= start_vertex < graph.v):
        raise ValueError("Start vertex out of bounds.")

    visited = {start_vertex}
    queue = collections.deque([start_vertex])
    traversal_order = []
    distances = {i: -1 for i in range(graph.v)}
    parents = {i: None for i in range(graph.v)}
    distances[start_vertex] = 0

    start_t = time.perf_counter()

    while queue:
        curr = queue.popleft()
        traversal_order.append(curr)

        for neighbor in sorted(graph.adj_list[curr]):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[curr] + 1
                parents[neighbor] = curr
                queue.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Breadth-First Search (BFS)",
        "start_vertex": start_vertex,
        "traversal_order": traversal_order,
        "distances_from_start": distances,
        "parents": parents,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)"
    }


def depth_first_search(graph: GraphRepresentation, start_vertex: int = 0) -> Dict[str, Any]:
    """
    Depth-First Search (DFS): Recursively explores as deeply as possible along each branch.
    Tracks discovery times, finish times, and detects cycles via back edges.
    Time Complexity: O(V + E). Space: O(V).
    """
    if not (0 <= start_vertex < graph.v):
        raise ValueError("Start vertex out of bounds.")

    visited: Set[int] = set()
    rec_stack: Set[int] = set()
    traversal_order: List[int] = []
    discovery_time: Dict[int, int] = {}
    finish_time: Dict[int, int] = {}
    has_cycle = False
    timer = 0

    start_t = time.perf_counter()

    def dfs_visit(u: int, parent_node: Optional[int] = None):
        nonlocal timer, has_cycle
        timer += 1
        discovery_time[u] = timer
        visited.add(u)
        rec_stack.add(u)
        traversal_order.append(u)

        for v in sorted(graph.adj_list[u]):
            if v not in visited:
                dfs_visit(v, u)
            elif graph.directed and v in rec_stack:
                has_cycle = True
            elif not graph.directed and v != parent_node and v in visited:
                has_cycle = True

        rec_stack.remove(u)
        timer += 1
        finish_time[u] = timer

    # Visit component of start_vertex first
    dfs_visit(start_vertex)

    # Visit any remaining unvisited components
    for v in range(graph.v):
        if v not in visited:
            dfs_visit(v)

    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Depth-First Search (DFS)",
        "start_vertex": start_vertex,
        "traversal_order": traversal_order,
        "discovery_times": discovery_time,
        "finish_times": finish_time,
        "has_cycle": has_cycle,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)"
    }


def topological_sort_kahns(num_vertices: int, directed_edges: List[Tuple[int, int]]) -> Dict[str, Any]:
    """
    Topological Sort using Kahn's algorithm (indegree reduction).
    Valid only for Directed Acyclic Graphs (DAGs).
    """
    adj = {i: [] for i in range(num_vertices)}
    indegree = {i: 0 for i in range(num_vertices)}

    for u, v in directed_edges:
        adj[u].append(v)
        indegree[v] += 1

    queue = collections.deque([i for i in range(num_vertices) if indegree[i] == 0])
    order = []
    start_t = time.perf_counter()

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    has_cycle = (len(order) != num_vertices)
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0

    return {
        "algorithm": "Topological Sort (Kahn's Algorithm)",
        "topological_order": order if not has_cycle else [],
        "has_cycle": has_cycle,
        "is_valid_dag": not has_cycle,
        "execution_time_ms": round(elapsed_ms, 4),
        "time_complexity": "O(V + E)"
    }
