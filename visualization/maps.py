"""
Interactive Map Visualization Module using Folium.
Renders municipal road network, bin status indicators, and planned collection routes.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import folium
from folium import plugins


COLOR_MAP = {
    "Critical": "#ef4444",  # Red
    "High": "#f97316",      # Orange
    "Medium": "#3b82f6",    # Blue
    "Low": "#10b981"        # Emerald
}


def build_collection_map(
    depot_info: Dict[str, Any],
    bins_list: List[Dict[str, Any]],
    route_sequence: Optional[List[str]] = None,
    road_edges: Optional[List[Dict[str, Any]]] = None,
    zoom_start: int = 14
) -> folium.Map:
    """
    Generate an interactive Folium map representing bins, road network, and active route.
    """
    depot_lat = float(depot_info.get("latitude", 18.5200))
    depot_lon = float(depot_info.get("longitude", 73.8550))

    # Base Folium Map centered on Depot
    m = folium.Map(
        location=[depot_lat, depot_lon],
        zoom_start=zoom_start,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # 1. Plot Depot
    depot_html = f"""
    <div style="font-family: sans-serif; font-size: 13px;">
        <h4 style="margin: 0 0 5px 0; color: #1e293b;">🏢 {depot_info.get('name', 'Depot')}</h4>
        <b>Node ID:</b> {depot_info.get('node_id', 'DEPOT')}<br>
        <b>Coordinates:</b> ({depot_lat:.4f}, {depot_lon:.4f})<br>
        <span style="color: #64748b;">Sanitation Fleet Starting & Termination Base</span>
    </div>
    """
    folium.Marker(
        location=[depot_lat, depot_lon],
        popup=folium.Popup(depot_html, max_width=300),
        tooltip="🏢 Depot (Start & Return Base)",
        icon=folium.Icon(color="black", icon="home", prefix="fa")
    ).add_to(m)

    # Lookup dict for quick coordinate access
    coords_lookup = {
        depot_info.get("node_id", "DEPOT"): (depot_lat, depot_lon)
    }

    # 2. Plot Waste Bins
    for b in bins_list:
        b_id = b["bin_id"]
        lat = float(b["latitude"])
        lon = float(b["longitude"])
        coords_lookup[b_id] = (lat, lon)

        urgency = b.get("urgency", "Medium")
        w_level = float(b.get("waste_level", 0.0))
        w_kg = float(b.get("waste_kg", 0.0))
        status = b.get("status", "Pending")
        color = COLOR_MAP.get(urgency, "#3b82f6")

        bin_html = f"""
        <div style="font-family: sans-serif; font-size: 13px; line-height: 1.4;">
            <h4 style="margin: 0 0 5px 0; color: {color};">🗑️ {b_id} — {b.get('name', '')}</h4>
            <b>Fill Level:</b> {w_level:.1f}%<br>
            <b>Estimated Waste:</b> {w_kg:.1f} kg<br>
            <b>Urgency:</b> <span style="font-weight: bold; color: {color};">{urgency}</span><br>
            <b>Status:</b> {status}<br>
            <b>Last Emptied:</b> {b.get('last_collection_days', 1)} days ago
        </div>
        """

        # Circle marker with radius proportional to fill level
        folium.CircleMarker(
            location=[lat, lon],
            radius=7 + int(w_level / 15.0),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(bin_html, max_width=300),
            tooltip=f"{b_id}: {b.get('name', '')} ({w_level}% fill)"
        ).add_to(m)

    # 3. Optional: Subtle Road Network Geometry Background
    if road_edges:
        for edge in road_edges:
            u, v = edge["u"], edge["v"]
            if u in coords_lookup and v in coords_lookup:
                pts = [coords_lookup[u], coords_lookup[v]]
                folium.PolyLine(
                    locations=pts,
                    color="#94a3b8",
                    weight=1.5,
                    opacity=0.45,
                    dash_array="4, 6"
                ).add_to(m)

    # 4. Draw Collection Route Sequence
    if route_sequence and len(route_sequence) >= 2:
        route_points = []
        for idx, node_id in enumerate(route_sequence):
            if node_id in coords_lookup:
                pt = coords_lookup[node_id]
                route_points.append(pt)

                # Add waypoint stop order badge (skip start/end depot duplicate)
                if node_id != depot_info.get("node_id", "DEPOT"):
                    folium.map.Marker(
                        location=pt,
                        icon=folium.DivIcon(
                            icon_size=(24, 24),
                            icon_anchor=(12, 12),
                            html=f"""<div style="background-color: #1e293b; color: #ffffff;
                                    border-radius: 50%; width: 22px; height: 22px;
                                    display: flex; align-items: center; justify-content: center;
                                    font-size: 11px; font-weight: bold; border: 2px solid #ffffff;
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{idx}</div>"""
                        )
                    ).add_to(m)

        if len(route_points) >= 2:
            folium.PolyLine(
                locations=route_points,
                color="#0284c7",
                weight=4.5,
                opacity=0.85,
                tooltip="Truck Collection Route"
            ).add_to(m)

    # Add HTML legend box
    legend_html = """
    <div style="position: fixed; bottom: 25px; right: 25px; z-index: 9999;
                background-color: rgba(255, 255, 255, 0.95); padding: 12px 16px;
                border-radius: 8px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                font-family: sans-serif; font-size: 12px; line-height: 1.5;">
        <b style="color: #0f172a; font-size: 13px;">Bin Urgency Legend</b><br>
        <span style="color: #ef4444;">●</span> Critical Urgency (>= 85%)<br>
        <span style="color: #f97316;">●</span> High Urgency<br>
        <span style="color: #3b82f6;">●</span> Medium Urgency<br>
        <span style="color: #10b981;">●</span> Low Urgency<br>
        <span style="color: #0284c7; font-weight: bold;">―</span> Planned Collection Route
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m
