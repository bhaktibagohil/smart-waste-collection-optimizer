"""
Route Planner Module for Smart Waste Collection System.
Implements Baseline (Input-Order), Nearest-Neighbor Greedy Heuristic,
and Exact Branch-and-Bound TSP route optimizers over the road network graph.
"""

from __future__ import annotations
import itertools
import time
from typing import Any, Dict, List, Optional, Tuple
import networkx as nx

from optimizer.data_manager import compute_all_pairs_shortest_distances
from optimizer.capacity import select_bins_knapsack_dp
from optimizer.route_metrics import compute_route_metrics


class RoutePlanner:
    """
    Orchestrates collection route generation over a weighted road graph.
    """

    def __init__(self, road_graph: nx.DiGraph, depot_id: str = "DEPOT"):
        self.road_graph = road_graph
        self.depot_id = depot_id

    def build_distance_matrix(self, nodes: List[str]) -> Dict[Tuple[str, str], float]:
        """Compute all-pairs shortest path road distances for the requested nodes."""
        all_nodes = list(set([self.depot_id] + nodes))
        return compute_all_pairs_shortest_distances(self.road_graph, all_nodes)

    def plan_baseline_route(
        self,
        selected_bin_ids: List[str],
        dist_matrix: Dict[Tuple[str, str], float]
    ) -> Tuple[List[str], float]:
        """
        Baseline route: Visits bins in deterministic order (e.g. sorted by ID or input order),
        starting at DEPOT and returning to DEPOT.
        """
        if not selected_bin_ids:
            return [self.depot_id, self.depot_id], 0.0

        ordered = sorted(selected_bin_ids)
        sequence = [self.depot_id] + ordered + [self.depot_id]

        total_dist = 0.0
        for i in range(len(sequence) - 1):
            u, v = sequence[i], sequence[i + 1]
            total_dist += dist_matrix.get((u, v), float("inf"))

        return sequence, round(total_dist, 3)

    def plan_nearest_neighbor_route(
        self,
        selected_bin_ids: List[str],
        dist_matrix: Dict[Tuple[str, str], float]
    ) -> Tuple[List[str], float]:
        """
        Nearest-Neighbor Greedy Heuristic:
        Starts at DEPOT, greedily moves to the nearest reachable unvisited bin,
        and finally returns to DEPOT.
        Optimality: Heuristic (polynomial-time approximation, NOT guaranteed globally optimal).
        """
        if not selected_bin_ids:
            return [self.depot_id, self.depot_id], 0.0

        unvisited = set(selected_bin_ids)
        current = self.depot_id
        sequence = [current]
        total_dist = 0.0

        while unvisited:
            next_node = None
            min_dist = float("inf")

            for candidate in sorted(unvisited):  # deterministic tie-breaking
                d = dist_matrix.get((current, candidate), float("inf"))
                if d < min_dist:
                    min_dist = d
                    next_node = candidate

            if next_node is None or min_dist == float("inf"):
                # No reachable remaining nodes
                break

            sequence.append(next_node)
            total_dist += min_dist
            unvisited.remove(next_node)
            current = next_node

        # Return to depot
        return_dist = dist_matrix.get((current, self.depot_id), float("inf"))
        sequence.append(self.depot_id)
        total_dist += return_dist

        return sequence, round(total_dist, 3)

    def plan_exact_branch_and_bound_tsp(
        self,
        selected_bin_ids: List[str],
        dist_matrix: Dict[Tuple[str, str], float],
        max_locations_limit: int = 10
    ) -> Tuple[List[str], float, bool]:
        """
        Exact TSP route optimization via Branch-and-Bound / state-space search.
        Guarantee: Provably optimal for the given subset.
        Constraint: Limited to max_locations_limit (default 10) to prevent exponential explosion.
        Returns: (sequence, total_dist, is_proven_optimal)
        """
        n = len(selected_bin_ids)
        if n == 0:
            return [self.depot_id, self.depot_id], 0.0, True

        if n > max_locations_limit:
            # Fallback to nearest neighbor if size exceeds safe limit
            seq, dist = self.plan_nearest_neighbor_route(selected_bin_ids, dist_matrix)
            return seq, dist, False

        # Exact Branch-and-Bound search
        best_cost = float("inf")
        best_path: List[str] = []

        # Find greedy solution first to establish a tight initial upper bound
        greedy_seq, greedy_dist = self.plan_nearest_neighbor_route(selected_bin_ids, dist_matrix)
        best_cost = greedy_dist
        best_path = greedy_seq

        def branch(current_node: str, unvisited_set: set, current_cost: float, path_so_far: List[str]):
            nonlocal best_cost, best_path

            if not unvisited_set:
                return_cost = dist_matrix.get((current_node, self.depot_id), float("inf"))
                total = current_cost + return_cost
                if total < best_cost:
                    best_cost = total
                    best_path = path_so_far + [self.depot_id]
                return

            # Lower bound pruning: current_cost + min return to depot
            # Even in the most optimistic case, we must eventually reach depot
            if current_cost >= best_cost:
                return

            # Branch to unvisited neighbors sorted by edge weight (Best-First branching heuristic)
            neighbors = sorted(list(unvisited_set), key=lambda x: dist_matrix.get((current_node, x), float("inf")))

            for nxt in neighbors:
                step_dist = dist_matrix.get((current_node, nxt), float("inf"))
                if current_cost + step_dist >= best_cost:
                    continue  # Prune branch

                unvisited_set.remove(nxt)
                branch(nxt, unvisited_set, current_cost + step_dist, path_so_far + [nxt])
                unvisited_set.add(nxt)

        initial_unvisited = set(selected_bin_ids)
        branch(self.depot_id, initial_unvisited, 0.0, [self.depot_id])

        return best_path, round(best_cost, 3), True

    def get_detailed_path_nodes(self, sequence: List[str]) -> List[str]:
        """
        Expand a route sequence (e.g. ['DEPOT', 'BIN-01', 'BIN-03', 'DEPOT'])
        into full road-by-road intermediate graph node steps using Dijkstra paths.
        """
        full_path = []
        for i in range(len(sequence) - 1):
            u, v = sequence[i], sequence[i + 1]
            if u == v:
                continue
            try:
                sub_path = nx.shortest_path(self.road_graph, u, v, weight="weight")
                if full_path:
                    full_path.extend(sub_path[1:])
                else:
                    full_path.extend(sub_path)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                if full_path:
                    full_path.append(v)
                else:
                    full_path.extend([u, v])

        return full_path
