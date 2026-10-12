"""
Charts and Plotting Visualization Module using Matplotlib.
Renders route comparison metrics, sorting benchmarks, asymptotic curves, and bin histograms.
"""

from __future__ import annotations
from typing import Any, Dict, List
import matplotlib.pyplot as plt
import numpy as np


def plot_route_comparison(baseline: Dict[str, Any], optimized: Dict[str, Any]) -> plt.Figure:
    """
    Generate side-by-side bar charts comparing Baseline vs Optimized route metrics.
    """
    labels = ["Distance (km)", "Travel Time (min)", "Fuel Est (L)", "CO2 Est (kg)"]
    b_vals = [
        baseline["total_distance_km"],
        baseline["travel_time_min"],
        baseline["estimated_fuel_liters"],
        baseline["estimated_co2_kg"]
    ]
    o_vals = [
        optimized["total_distance_km"],
        optimized["travel_time_min"],
        optimized["estimated_fuel_liters"],
        optimized["estimated_co2_kg"]
    ]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    rects1 = ax.bar(x - width/2, b_vals, width, label="Baseline (Input Order)", color="#94a3b8")
    rects2 = ax.bar(x + width/2, o_vals, width, label="Optimized Route", color="#0284c7")

    ax.set_ylabel("Metric Value")
    ax.set_title("Operational Route Comparison: Baseline vs. Optimized", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontweight="semibold")
    ax.legend(frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Bar value labels
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f"{height:.1f}", xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f"{height:.1f}", xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    fig.tight_layout()
    return fig


def plot_sorting_comparison(results: List[Dict[str, Any]]) -> plt.Figure:
    """
    Plot comparisons and execution times across sorting algorithms on identical test inputs.
    """
    names = [r["algorithm"].replace(" Sort", "") for r in results]
    times_ms = [r["execution_time_ms"] for r in results]
    comparisons = [r.get("comparisons", 0) for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=100)

    # Subplot 1: Execution Time
    y_pos = np.arange(len(names))
    ax1.barh(y_pos, times_ms, color="#38bdf8")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontweight="semibold")
    ax1.invert_yaxis()
    ax1.set_xlabel("Time (milliseconds)")
    ax1.set_title("Execution Time (ms)", fontweight="bold")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)

    # Subplot 2: Comparisons Count
    ax2.barh(y_pos, comparisons, color="#818cf8")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([])
    ax2.invert_yaxis()
    ax2.set_xlabel("Comparison Count")
    ax2.set_title("Key Comparisons", fontweight="bold")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig


def plot_complexity_curves(bench_data: List[Dict[str, Any]]) -> plt.Figure:
    """
    Plot empirical execution time across input sizes alongside theoretical growth rates.
    """
    sizes = [d["size"] for d in bench_data]
    times = [d["avg_time_ms"] for d in bench_data]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    ax.plot(sizes, times, marker="o", linewidth=2.5, color="#2563eb", label="Observed Runtime (ms)")

    ax.set_xlabel("Input Size N", fontweight="bold")
    ax.set_ylabel("Execution Time (ms)", fontweight="bold")
    ax.set_title("Empirical Growth Rate vs Input Size", fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="#f8fafc")

    fig.tight_layout()
    return fig


def plot_bin_waste_distribution(bins: List[Dict[str, Any]]) -> plt.Figure:
    """
    Plot histogram of waste fill percentage and counts by urgency.
    """
    levels = [float(b.get("waste_level", 0.0)) for b in bins]
    urgencies = [b.get("urgency", "Medium") for b in bins]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), dpi=100)

    # Fill percentage histogram
    ax1.hist(levels, bins=6, color="#0ea5e9", edgecolor="#0284c7", alpha=0.85)
    ax1.set_xlabel("Fill Level (%)")
    ax1.set_ylabel("Number of Bins")
    ax1.set_title("Bin Fill Level Distribution", fontweight="bold")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Urgency breakdown
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for u in urgencies:
        counts[u] = counts.get(u, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())
    colors = ["#ef4444", "#f97316", "#3b82f6", "#10b981"]

    ax2.bar(labels, values, color=colors, edgecolor="#475569")
    ax2.set_ylabel("Number of Bins")
    ax2.set_title("Bins by Urgency Category", fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig
