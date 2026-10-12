"""
Data manager and validation module for bins and road network graph.
Handles schema verification, coordinates bounds, CSV parsing, and graph construction.
"""

from __future__ import annotations
import math
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Set, Tuple
import networkx as nx
import pandas as pd

DEFAULT_ROADS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_roads.csv")


@dataclass
class Depot:
    node_id: str = "DEPOT"
    name: str = "Central Sanitation Facility"
    latitude: float = 18.5200
    longitude: float = 73.8550


@dataclass
class Bin:
    bin_id: str
    name: str
    latitude: float
    longitude: float
    waste_level: float
    waste_kg: float
    urgency: str = "Medium"
    last_collection_days: int = 1
    status: str = "Pending"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def validate_bin_dict(data: Dict[str, Any], existing_ids: Optional[Set[str]] = None) -> Tuple[bool, str]:
    """
    Validate a single bin dictionary.
    Returns (is_valid, error_message).
    """
    # 1. Required keys
    req_keys = ["bin_id", "name", "latitude", "longitude", "waste_level", "waste_kg"]
    for k in req_keys:
        if k not in data or data[k] is None or str(data[k]).strip() == "":
            return False, f"Missing required field: '{k}'."

    bin_id = str(data["bin_id"]).strip()
    if existing_ids and bin_id in existing_ids:
        return False, f"Duplicate Bin ID '{bin_id}' detected."

    # 2. Coordinates validation
    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
    except (ValueError, TypeError):
        return False, "Latitude and Longitude must be valid numerical floating-point numbers."

    if not (-90.0 <= lat <= 90.0):
        return False, f"Latitude {lat} out of valid range [-90, +90]."
    if not (-180.0 <= lon <= 180.0):
        return False, f"Longitude {lon} out of valid range [-180, +180]."

    # 3. Waste level validation
    try:
        w_level = float(data["waste_level"])
    except (ValueError, TypeError):
        return False, "Waste level percentage must be a number."
    if not (0.0 <= w_level <= 100.0):
        return False, f"Waste level {w_level}% is invalid; must be between 0.0% and 100.0%."

    # 4. Waste kg validation
    try:
        w_kg = float(data["waste_kg"])
    except (ValueError, TypeError):
        return False, "Estimated waste quantity (kg) must be a number."
    if w_kg < 0.0:
        return False, f"Waste quantity {w_kg} kg cannot be negative."

    # 5. Urgency validation
    urgency = str(data.get("urgency", "Medium")).strip().capitalize()
    valid_urgencies = {"Low", "Medium", "High", "Critical"}
    if urgency not in valid_urgencies:
        return False, f"Urgency '{urgency}' is invalid. Allowed: {valid_urgencies}."

    # 6. Status validation
    status = str(data.get("status", "Pending")).strip().capitalize()
    valid_statuses = {"Pending", "Collected", "Skipped"}
    if status not in valid_statuses:
        return False, f"Status '{status}' is invalid. Allowed: {valid_statuses}."

    return True, ""


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle Euclidean/spherical distance between two coordinates in kilometers.
    Identified strictly as geometric straight-line distance, distinct from road distances.
    """
    R = 6371.0088  # Mean Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)


def load_road_network_graph(roads_csv_path: Optional[str] = None) -> nx.DiGraph:
    """
    Build and return a NetworkX DiGraph representing the road network.
    Edges contain 'distance_km', 'road_type', and 'road_name'.
    Supports one-way and two-way roads.
    """
    path = roads_csv_path or DEFAULT_ROADS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Road network dataset not found at {path}")

    df = pd.read_csv(path)
    required_cols = {"u", "v", "distance_km", "road_type"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Roads CSV missing required columns: {required_cols - set(df.columns)}")

    G = nx.DiGraph()

    for _, row in df.iterrows():
        u = str(row["u"]).strip()
        v = str(row["v"]).strip()
        dist = float(row["distance_km"])
        rtype = str(row["road_type"]).strip().lower()
        rname = str(row.get("road_name", f"{u}-{v}"))

        if dist < 0:
            raise ValueError(f"Negative road distance ({dist} km) on road {u}->{v} is not permitted.")

        # Add directed edge u -> v
        G.add_edge(u, v, weight=dist, distance_km=dist, road_type=rtype, road_name=rname)

        # If two-way, also add v -> u
        if rtype == "two_way":
            G.add_edge(v, u, weight=dist, distance_km=dist, road_type=rtype, road_name=rname)

    return G


def compute_all_pairs_shortest_distances(G: nx.DiGraph, nodes: List[str]) -> Dict[Tuple[str, str], float]:
    """
    Compute shortest road distances between every pair of given nodes using Dijkstra.
    If a pair is unreachable, distance is set to float('inf').
    """
    dist_matrix: Dict[Tuple[str, str], float] = {}

    for u in nodes:
        if u not in G:
            for v in nodes:
                dist_matrix[(u, v)] = 0.0 if u == v else float("inf")
            continue

        try:
            lengths = nx.single_source_dijkstra_path_length(G, u, weight="weight")
        except Exception:
            lengths = {}

        for v in nodes:
            if u == v:
                dist_matrix[(u, v)] = 0.0
            elif v in lengths:
                dist_matrix[(u, v)] = round(lengths[v], 3)
            else:
                dist_matrix[(u, v)] = float("inf")

    return dist_matrix
