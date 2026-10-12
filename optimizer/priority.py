"""
Transparent Priority Ranking Module.
Calculates deterministic urgency and collection priority scores for waste bins.
Note: This is an explicit mathematical multi-criteria evaluation, NOT an AI/ML prediction.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# Default weights and points
URGENCY_POINTS = {
    "Low": 5.0,
    "Medium": 20.0,
    "High": 45.0,
    "Critical": 80.0
}


def compute_priority_score(
    bin_data: Dict[str, Any],
    fill_weight: float = 0.5,
    urgency_weight: float = 1.0,
    days_weight: float = 2.0
) -> float:
    """
    Compute a transparent multi-criteria priority score.
    Formula:
      Priority Score = (waste_level * fill_weight) + (UrgencyPoints * urgency_weight) + (days * days_weight)
    
    A higher score indicates greater necessity for collection.
    """
    waste_level = float(bin_data.get("waste_level", 0.0))
    urgency_str = str(bin_data.get("urgency", "Medium")).strip().capitalize()
    days = float(bin_data.get("last_collection_days", 1))

    urgency_pts = URGENCY_POINTS.get(urgency_str, 20.0)

    score = (waste_level * fill_weight) + (urgency_pts * urgency_weight) + (days * days_weight)
    return round(score, 2)


def get_formula_breakdown(
    bin_data: Dict[str, Any],
    fill_weight: float = 0.5,
    urgency_weight: float = 1.0,
    days_weight: float = 2.0
) -> Dict[str, Any]:
    """Return explicit breakdown of each component contributing to the final score."""
    waste_level = float(bin_data.get("waste_level", 0.0))
    urgency_str = str(bin_data.get("urgency", "Medium")).strip().capitalize()
    days = float(bin_data.get("last_collection_days", 1))
    urgency_pts = URGENCY_POINTS.get(urgency_str, 20.0)

    fill_component = round(waste_level * fill_weight, 2)
    urgency_component = round(urgency_pts * urgency_weight, 2)
    days_component = round(days * days_weight, 2)
    total_score = round(fill_component + urgency_component + days_component, 2)

    return {
        "bin_id": bin_data.get("bin_id"),
        "waste_level_pct": waste_level,
        "fill_component": fill_component,
        "urgency_label": urgency_str,
        "urgency_component": urgency_component,
        "days_elapsed": days,
        "days_component": days_component,
        "total_score": total_score,
        "formula": f"({waste_level} * {fill_weight}) + ({urgency_pts} * {urgency_weight}) + ({days} * {days_weight})"
    }


def rank_bins(
    bins: List[Dict[str, Any]],
    sort_by: str = "priority",
    min_priority_threshold: float = 0.0,
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Filter and rank bins by chosen criteria: 'priority', 'waste_level', 'waste_kg', or 'bin_id'.
    Adds 'priority_score' attribute to each bin dictionary.
    """
    enriched = []
    for b in bins:
        b_copy = dict(b)
        score = compute_priority_score(b_copy)
        b_copy["priority_score"] = score
        if score >= min_priority_threshold:
            enriched.append(b_copy)

    if sort_by == "priority":
        enriched.sort(key=lambda x: x["priority_score"], reverse=reverse)
    elif sort_by == "waste_level":
        enriched.sort(key=lambda x: float(x.get("waste_level", 0.0)), reverse=reverse)
    elif sort_by == "waste_kg":
        enriched.sort(key=lambda x: float(x.get("waste_kg", 0.0)), reverse=reverse)
    elif sort_by == "bin_id":
        enriched.sort(key=lambda x: str(x.get("bin_id", "")), reverse=not reverse)

    return enriched
