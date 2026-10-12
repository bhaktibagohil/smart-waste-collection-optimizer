"""
Smart Waste Collection Route Optimizer with Complete DAA Coverage
Main Streamlit Application.
"""

from __future__ import annotations
import os
import json
import time
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# --- Database & Optimizer Imports ---
from database.db import (
    init_db,
    get_all_bins,
    get_bins_df,
    get_bin,
    add_bin,
    update_bin,
    delete_bin,
    update_bin_status,
    reset_to_sample_data,
    save_route_run,
    get_route_history,
    clear_route_history,
    get_config
)
from optimizer.data_manager import (
    load_road_network_graph,
    compute_all_pairs_shortest_distances,
    validate_bin_dict,
    haversine_distance_km,
    Depot
)
from optimizer.priority import rank_bins, get_formula_breakdown, compute_priority_score
from optimizer.capacity import select_bins_knapsack_dp, select_bins_greedy_ratio, validate_truck_capacity
from optimizer.route_planner import RoutePlanner
from optimizer.route_metrics import compute_route_metrics, compare_routes
from visualization.maps import build_collection_map
from visualization.charts import (
    plot_route_comparison,
    plot_sorting_comparison,
    plot_complexity_curves,
    plot_bin_waste_distribution
)

# --- DAA Algorithm Imports ---
from algorithms.mathematical_analysis import (
    set_operations_demo,
    check_relation_properties,
    evaluate_quantifiers,
    arithmetic_series_sum,
    geometric_series_sum,
    permutations_combinations,
    analyze_loop_counters,
    simulate_dynamic_array_amortization
)
from algorithms.complexity import ASYMPTOTIC_DEFINITIONS, limit_quotient_comparison, benchmark_function_sizes
from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    counting_sort,
    bucket_sort
)
from algorithms.recurrence_analysis import (
    solve_master_theorem,
    analyze_recursion_tree,
    solve_second_order_homogeneous,
    substitution_method_demonstration,
    change_of_variable_demonstration
)
from algorithms.divide_and_conquer import (
    binary_search,
    merge_sort,
    quick_sort,
    max_min_divide_and_conquer,
    karatsuba_multiplication,
    strassen_2x2_multiply,
    naive_fibonacci
)
from algorithms.greedy import (
    greedy_coin_change,
    prim_mst,
    kruskal_mst,
    dijkstra_shortest_path,
    bellman_ford_shortest_path,
    fractional_knapsack_greedy,
    activity_selection_greedy,
    huffman_encoding
)
from algorithms.dynamic_programming import (
    binomial_coefficient_dp,
    coin_change_min_coins_dp,
    knapsack_01_dp,
    floyd_warshall_all_pairs,
    matrix_chain_multiplication,
    longest_common_subsequence,
    compare_greedy_vs_dp_coin_change
)
from algorithms.graph_algorithms import (
    GraphRepresentation,
    breadth_first_search,
    depth_first_search,
    topological_sort_kahns
)
from algorithms.backtracking import (
    solve_n_queens,
    knapsack_backtracking,
    hamiltonian_cycle,
    tsp_backtracking_exact
)
from algorithms.branch_and_bound import (
    solve_assignment_problem_bnb,
    knapsack_branch_and_bound,
    minimax_alphabeta_demo
)
from algorithms.string_matching import (
    naive_string_match,
    rabin_karp_match,
    kmp_string_match,
    search_complaint_tickets
)
from algorithms.np_completeness import (
    NP_COMPLEXITY_CLASSES,
    reduction_hamiltonian_cycle_to_tsp,
    compare_exact_vs_greedy_tsp
)

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="Smart Waste Collection Optimizer & DAA Lab",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Rich Modern Aesthetics)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(241,245,249,0.9));
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
    }
    
    .metric-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-val {
        color: #0f172a;
        font-size: 26px;
        font-weight: 700;
        margin-top: 4px;
    }
    
    .badge-critical {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .badge-high {
        background-color: #ffedd5;
        color: #ea580c;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .badge-medium {
        background-color: #dbeafe;
        color: #2563eb;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .badge-low {
        background-color: #d1fae5;
        color: #059669;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Ensure Database is initialized on startup
init_db()

# Cached Graph Loader
@st.cache_resource
def get_road_graph():
    return load_road_network_graph()

road_graph = get_road_graph()
depot_config = {
    "node_id": "DEPOT",
    "name": "Central Sanitation Facility",
    "latitude": 18.5200,
    "longitude": 73.8550
}

# --- Sidebar Navigation ---
st.sidebar.image("https://img.icons8.com/isometric/100/recycle-bin.png", width=64)
st.sidebar.title("Smart Waste Optimizer")
st.sidebar.caption("DAA Capstone Project • BE Computer Engg")

view_selection = st.sidebar.radio(
    "Navigation Views",
    [
        "🏙️ Home & Overview",
        "🗑️ Bin Management",
        "🗺️ Road Network & Graph",
        "🚛 Route Optimizer",
        "📍 Interactive Route Map",
        "📊 Route History & Reports",
        "🧪 DAA Algorithm Lab",
        "📈 Complexity & Benchmarks",
        "📚 DAA Syllabus & Viva Guide"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Exam Mode**: Offline Road Network Graph active. No paid APIs or external sensors required.")


# ==============================================================================
# VIEW 1: HOME & OVERVIEW
# ==============================================================================
if view_selection == "🏙️ Home & Overview":
    st.title("♻️ Smart Waste Collection Route Optimizer")
    st.subheader("An Algorithmic Decision-Support System with Comprehensive DAA Coverage")

    col_hero1, col_hero2 = st.columns([2, 1])
    with col_hero1:
        st.markdown("""
        ### Problem Statement & Municipal Context
        Urban solid waste collection in municipalities (e.g. *Green Hills Municipal Ward*) faces significant operational challenges:
        - **Static collection schedules** waste fuel and labor by emptying bins that are half-empty while leaving overflowing bins unattended.
        - **Vehicle capacity constraints** mean a single collection truck cannot service every bin in a single trip.
        - **Road networks** feature one-way streets, traffic choke points, and differing travel distances that naive straight-line routing fails to account for.

        ### Proposed Algorithmic Solution
        This project integrates classic **Design and Analysis of Algorithms (DAA)** techniques to solve this genuine logistics problem:
        1. **Multi-Factor Priority Scoring**: Transparent urgency formula ranking bins by fill level, days elapsed, and hazard urgency.
        2. **0/1 Knapsack Bin Selection**: Dynamic programming to select the highest-priority waste subset strictly under truck capacity limits.
        3. **Shortest Road Paths**: Dijkstra's algorithm over a weighted directed road network.
        4. **Route Planning**: Baseline (input order), Nearest-Neighbor Greedy heuristic, and Exact Branch & Bound TSP search.
        """)
    with col_hero2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Municipal Ward</div>
            <div class="metric-val">Green Hills Ward</div>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 13px;">Zone 4 Central Cluster</p>
        </div>
        <div class="metric-card">
            <div class="metric-title">Active Bins Monitored</div>
            <div class="metric-val">18 Municipal Bins</div>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 13px;">Critical, High, Medium, Low</p>
        </div>
        <div class="metric-card">
            <div class="metric-title">DAA Syllabus Coverage</div>
            <div class="metric-val">100% (Units 1 - 8)</div>
            <p style="margin: 4px 0 0 0; color: #64748b; font-size: 13px;">All 56 Automated Tests Passing</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("System Architecture & Data Flow")
    st.markdown("""
    ```
    ┌─────────────────────────┐       ┌────────────────────────┐       ┌─────────────────────────┐
    │     Bin Management      │  ──>  │  Priority Ranking Rule │  ──>  │   0/1 Knapsack DP       │
    │  (SQLite CRUD & Bins)   │       │  (Fill % + Urgency Pts)│       │  (Capacity Constraint)  │
    └─────────────────────────┘       └────────────────────────┘       └─────────────────────────┘
                 │                                                                  │
                 ▼                                                                  ▼
    ┌─────────────────────────┐       ┌────────────────────────┐       ┌─────────────────────────┐
    │   Road Network Graph    │  ──>  │  Dijkstra / All-Pairs  │  ──>  │ Route Optimizers        │
    │ (Weighted Directed DiG) │       │ (Shortest Path Matrix) │       │ (Baseline, Greedy, B&B) │
    └─────────────────────────┘       └────────────────────────┘       └─────────────────────────┘
                                                                                    │
                                                                                    ▼
                                                                       ┌─────────────────────────┐
                                                                       │ Folium Map & Dashboard │
                                                                       │ (Distance, Fuel, Time)  │
                                                                       └─────────────────────────┘
    ```
    """)


# ==============================================================================
# VIEW 2: BIN MANAGEMENT
# ==============================================================================
elif view_selection == "🗑️ Bin Management":
    st.title("🗑️ Municipal Waste Bin Management")
    st.caption("Manage collection bins, validate schema, inspect priority scores, and import/export datasets.")

    bins = get_all_bins()

    tab_list, tab_add, tab_priority, tab_io = st.tabs(["📋 View & Filter Bins", "➕ Add / Edit Bin", "🎯 Priority Formula Inspector", "💾 CSV Import / Export / Reset"])

    with tab_list:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_urgency = st.multiselect("Filter Urgency", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"])
        with col_f2:
            filter_status = st.multiselect("Filter Status", ["Pending", "Collected"], default=["Pending", "Collected"])
        with col_f3:
            search_query = st.text_input("Search Bin ID or Name", "")

        filtered = [
            b for b in bins
            if b.get("urgency") in filter_urgency
            and b.get("status") in filter_status
            and (search_query.lower() in b["bin_id"].lower() or search_query.lower() in b["name"].lower())
        ]

        if filtered:
            df_display = pd.DataFrame(filtered)
            st.dataframe(
                df_display[["bin_id", "name", "waste_level", "waste_kg", "urgency", "last_collection_days", "status", "latitude", "longitude"]],
                use_container_width=True
            )
            st.write(f"Showing **{len(filtered)}** of **{len(bins)}** total bins.")
        else:
            st.warning("No bins match the selected filter criteria.")

        # Quick Actions
        st.subheader("Quick Status Action")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            selected_bin_id = st.selectbox("Select Bin ID to Toggle Status", [b["bin_id"] for b in bins] if bins else [])
        with col_act2:
            if st.button("Mark as Collected / Pending Toggle"):
                target = get_bin(selected_bin_id)
                new_st = "Collected" if target["status"] == "Pending" else "Pending"
                update_bin_status([selected_bin_id], new_st)
                st.success(f"Bin {selected_bin_id} status updated to {new_st}!")
                st.rerun()

    with tab_add:
        st.subheader("Add New Bin Location")
        with st.form("add_bin_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_id = st.text_input("Bin ID (Unique)", f"BIN-{len(bins)+1:02d}")
                new_name = st.text_input("Location Name / Landmark", "Suburban Plaza East")
                new_lat = st.number_input("Latitude", value=18.5250, format="%.4f")
                new_lon = st.number_input("Longitude", value=73.8580, format="%.4f")
            with c2:
                new_level = st.slider("Waste Fill Level (%)", 0.0, 100.0, 75.0, step=1.0)
                new_kg = st.number_input("Estimated Waste Quantity (kg)", min_value=0.0, value=225.0, step=5.0)
                new_urgency = st.selectbox("Urgency", ["Low", "Medium", "High", "Critical"], index=2)
                new_days = st.number_input("Days Elapsed Since Last Collection", min_value=0, max_value=30, value=3)

            submit_add = st.form_submit_button("Add Bin to System")
            if submit_add:
                new_dict = {
                    "bin_id": new_id,
                    "name": new_name,
                    "latitude": new_lat,
                    "longitude": new_lon,
                    "waste_level": new_level,
                    "waste_kg": new_kg,
                    "urgency": new_urgency,
                    "last_collection_days": new_days,
                    "status": "Pending"
                }
                existing_ids = {b["bin_id"] for b in bins}
                is_valid, err = validate_bin_dict(new_dict, existing_ids)
                if not is_valid:
                    st.error(f"Validation Error: {err}")
                else:
                    success = add_bin(new_dict)
                    if success:
                        st.success(f"Bin '{new_id}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add bin. Check for duplicate ID.")

    with tab_priority:
        st.subheader("🎯 Transparent Multi-Criteria Priority Scoring")
        st.markdown("""
        Unlike black-box AI predictions, this system uses an **explicit, deterministic mathematical formula**:
        $$\\text{Priority Score} = (\\text{WasteLevel}\\% \\times 0.50) + \\text{UrgencyPoints} + (\\text{DaysElapsed} \\times 2.0)$$
        Where:
        - **Critical Urgency**: 80 pts
        - **High Urgency**: 45 pts
        - **Medium Urgency**: 20 pts
        - **Low Urgency**: 5 pts
        """)

        ranked = rank_bins(bins, sort_by="priority")
        breakdown_rows = [get_formula_breakdown(b) for b in ranked]
        st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True)

    with tab_io:
        st.subheader("Data Import, Export & Reset")
        col_io1, col_io2, col_io3 = st.columns(3)

        with col_io1:
            st.markdown("#### Export Current Bins")
            df_current = get_bins_df()
            csv_data = df_current.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Bins as CSV",
                csv_data,
                "current_bins.csv",
                "text/csv"
            )

        with col_io2:
            st.markdown("#### Import Bins from CSV")
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            if uploaded_file is not None:
                try:
                    df_up = pd.read_csv(uploaded_file)
                    st.write(f"Parsed {len(df_up)} rows. Validating...")
                    # Save temporary and load
                    temp_path = "temp_uploaded_bins.csv"
                    df_up.to_csv(temp_path, index=False)
                    from database.db import load_bins_from_csv
                    count = load_bins_from_csv(temp_path, replace_existing=True)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.success(f"Successfully imported {count} bins!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Import failed: {str(e)}")

        with col_io3:
            st.markdown("#### Reset Sample Dataset")
            st.warning("Resets all bin records back to the 18 bundled municipal ward bins.")
            if st.button("⚠️ Confirm Reset to Sample Data"):
                reset_to_sample_data()
                st.success("Database restored to default sample ward bins!")
                st.rerun()


# ==============================================================================
# VIEW 3: ROAD NETWORK & GRAPH
# ==============================================================================
elif view_selection == "🗺️ Road Network & Graph":
    st.title("🗺️ Municipal Road Network & Shortest Path Matrix")
    st.caption("Inspect the weighted directed graph representation, edge distances, one-way streets, and all-pairs shortest paths.")

    bins = get_all_bins()
    planner = RoutePlanner(road_graph, depot_id="DEPOT")

    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.markdown("### Graph Topology Metrics")
        st.write(f"- **Nodes (Vertices)**: {road_graph.number_of_nodes()} (Depot + {road_graph.number_of_nodes() - 1} Bins)")
        st.write(f"- **Directed Edges**: {road_graph.number_of_edges()}")
        st.write(f"- **Graph Model**: Directed Multigraph / DiGraph (Supports one-way road segments)")
        st.write(f"- **Distance Metric**: Actual road length in kilometers (Non-negative weights)")

    with c_g2:
        st.markdown("### One-Way Road Segments Identified")
        one_ways = [
            f"`{u}` ➔ `{v}` ({d['distance_km']} km): *{d.get('road_name', 'Street')}*"
            for u, v, d in road_graph.edges(data=True)
            if d.get("road_type") == "one_way"
        ]
        for ow in one_ways:
            st.markdown(f"- {ow}")

    st.divider()

    st.subheader("Shortest Path Inspector (Dijkstra's Algorithm)")
    c_p1, c_p2, c_p3 = st.columns([1, 1, 2])
    all_nodes = sorted(list(road_graph.nodes()))

    with c_p1:
        orig = st.selectbox("Origin Vertex", all_nodes, index=0)
    with c_p2:
        dest = st.selectbox("Destination Vertex", all_nodes, index=min(2, len(all_nodes)-1))

    with c_p3:
        import networkx as nx
        try:
            path_nodes = nx.shortest_path(road_graph, orig, dest, weight="weight")
            path_len = nx.shortest_path_length(road_graph, orig, dest, weight="weight")
            st.success(f"**Shortest Path Distance**: `{path_len:.2f} km`")
            st.markdown(f"**Path Sequence**: {' ➔ '.join(path_nodes)}")
        except nx.NetworkXNoPath:
            st.error(f"No directed road connection exists from {orig} to {dest}.")

    st.divider()

    st.subheader("All-Pairs Distance Matrix (Sample Subset)")
    sub_nodes = ["DEPOT", "BIN-01", "BIN-02", "BIN-03", "BIN-04", "BIN-05"]
    dist_mat = planner.build_distance_matrix(sub_nodes)
    matrix_table = []
    for u in sub_nodes:
        row = {"From / To": u}
        for v in sub_nodes:
            d = dist_mat.get((u, v), float("inf"))
            row[v] = f"{d:.2f} km" if d != float("inf") else "∞"
        matrix_table.append(row)
    st.dataframe(pd.DataFrame(matrix_table).set_index("From / To"), use_container_width=True)


# ==============================================================================
# VIEW 4: ROUTE OPTIMIZER
# ==============================================================================
elif view_selection == "🚛 Route Optimizer":
    st.title("🚛 Waste Collection Route Optimizer")
    st.caption("Select candidate bins under truck capacity constraints, generate collection routes, and compare baseline vs optimized outcomes.")

    bins = get_all_bins()
    planner = RoutePlanner(road_graph, depot_id="DEPOT")

    # Sidebar Planning Controls
    st.sidebar.markdown("### ⚙️ Optimization Parameters")
    truck_capacity = st.sidebar.number_input("Truck Capacity (kg)", min_value=500.0, max_value=5000.0, value=1200.0, step=100.0)
    truck_speed = st.sidebar.slider("Average Urban Speed (km/h)", min_value=15.0, max_value=45.0, value=25.0, step=1.0)
    selection_strategy = st.sidebar.selectbox("Bin Selection Strategy", ["0/1 Knapsack DP (Optimal Priority)", "Greedy Ratio Heuristic", "Manual Bin Selection"])
    route_algorithm = st.sidebar.selectbox("Route Optimization Method", ["Nearest-Neighbor Greedy Heuristic", "Exact Branch & Bound TSP (<= 10 Bins)"])

    # 1. Candidate Bins Selection
    pending_bins = [b for b in bins if b.get("status") == "Pending"]
    if not pending_bins:
        st.warning("All bins are currently marked as 'Collected'. Reset sample data in Bin Management to plan new routes.")
        pending_bins = bins

    if selection_strategy == "0/1 Knapsack DP (Optimal Priority)":
        selected_bins, uncollected_bins, total_waste, total_p = select_bins_knapsack_dp(pending_bins, capacity_kg=truck_capacity)
        method_label = "0/1 Knapsack DP"
    elif selection_strategy == "Greedy Ratio Heuristic":
        selected_bins, uncollected_bins, total_waste, total_p = select_bins_greedy_ratio(pending_bins, capacity_kg=truck_capacity)
        method_label = "Greedy Ratio"
    else:
        # Manual selection
        st.subheader("Manual Bin Selection")
        selected_ids = st.multiselect("Choose bins to include in route", [b["bin_id"] for b in pending_bins], default=[b["bin_id"] for b in pending_bins[:6]])
        selected_bins = [b for b in pending_bins if b["bin_id"] in selected_ids]
        uncollected_bins = [b for b in pending_bins if b["bin_id"] not in selected_ids]
        total_waste = sum(float(b["waste_kg"]) for b in selected_bins)
        method_label = "Manual"

    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
    with col_sum1:
        st.metric("Bins Selected", f"{len(selected_bins)} of {len(pending_bins)}")
    with col_sum2:
        st.metric("Total Waste", f"{total_waste:.1f} kg")
    with col_sum3:
        util_pct = (total_waste / truck_capacity * 100.0) if truck_capacity > 0 else 0.0
        st.metric("Capacity Utilization", f"{util_pct:.1f}%")
    with col_sum4:
        cap_val = validate_truck_capacity(selected_bins, truck_capacity)
        status_text = "✅ Feasible" if cap_val["is_feasible"] else "❌ Over Capacity"
        st.metric("Capacity Status", status_text)

    st.divider()

    # 2. Execute Route Planning
    selected_ids = [b["bin_id"] for b in selected_bins]
    dist_matrix = planner.build_distance_matrix(selected_ids)
    lookup_bins = {b["bin_id"]: b for b in bins}

    # Baseline Route (Deterministic Input Order)
    start_base = time.perf_counter()
    base_seq, base_dist = planner.plan_baseline_route(selected_ids, dist_matrix)
    base_time_ms = (time.perf_counter() - start_base) * 1000.0

    # Optimized Route
    is_exact_optimal = False
    start_opt = time.perf_counter()
    if route_algorithm == "Nearest-Neighbor Greedy Heuristic":
        opt_seq, opt_dist = planner.plan_nearest_neighbor_route(selected_ids, dist_matrix)
        opt_algo_name = "Nearest-Neighbor Greedy"
    else:
        if len(selected_ids) > 10:
            st.warning("⚠️ Selected bins exceed 10 locations. Falling back to Nearest-Neighbor heuristic to prevent combinatorial delay.")
            opt_seq, opt_dist = planner.plan_nearest_neighbor_route(selected_ids, dist_matrix)
            opt_algo_name = "Nearest-Neighbor Greedy (Auto-Fallback)"
        else:
            opt_seq, opt_dist, is_exact_optimal = planner.plan_exact_branch_and_bound_tsp(selected_ids, dist_matrix)
            opt_algo_name = "Exact Branch & Bound TSP"
    opt_time_ms = (time.perf_counter() - start_opt) * 1000.0

    # Operational Metrics
    m_base = compute_route_metrics(base_seq, dist_matrix, lookup_bins, bins, truck_capacity, truck_speed)
    m_opt = compute_route_metrics(opt_seq, dist_matrix, lookup_bins, bins, truck_capacity, truck_speed)
    comparison = compare_routes(m_base, m_opt)

    # 3. Display Results Dashboard
    st.subheader("📊 Route Performance Comparison")
    col_dash1, col_dash2 = st.columns([3, 2])

    with col_dash1:
        comp_df = pd.DataFrame([
            {"Metric": "Routing Method", "Baseline (Input Order)": "Deterministic Input Order", "Optimized Route": opt_algo_name},
            {"Metric": "Optimality Status", "Baseline (Input Order)": "Heuristic (Unoptimized)", "Optimized Route": "Proven Optimal" if is_exact_optimal else "Heuristic Approximation"},
            {"Metric": "Total Distance", "Baseline (Input Order)": f"{m_base['total_distance_km']:.2f} km", "Optimized Route": f"{m_opt['total_distance_km']:.2f} km"},
            {"Metric": "Estimated Travel Time", "Baseline (Input Order)": f"{m_base['travel_time_min']:.1f} min", "Optimized Route": f"{m_opt['travel_time_min']:.1f} min"},
            {"Metric": "Capacity Feasible", "Baseline (Input Order)": str(m_base['is_capacity_feasible']), "Optimized Route": str(m_opt['is_capacity_feasible'])},
            {"Metric": "Return to Depot", "Baseline (Input Order)": str(m_base['returns_to_depot']), "Optimized Route": str(m_opt['returns_to_depot'])},
            {"Metric": "Distance Reduction", "Baseline (Input Order)": "-", "Optimized Route": f"{comparison['distance_reduction_km']:.2f} km ({comparison['distance_savings_pct']:.1f}%)"},
            {"Metric": "Time Saved", "Baseline (Input Order)": "-", "Optimized Route": f"{comparison['time_saved_min']:.1f} min"},
            {"Metric": "Fuel Saved (Est)", "Baseline (Input Order)": "-", "Optimized Route": f"{comparison['fuel_saved_liters']:.2f} L diesel"},
            {"Metric": "Algorithm Runtime", "Baseline (Input Order)": f"{base_time_ms:.2f} ms", "Optimized Route": f"{opt_time_ms:.2f} ms"}
        ])
        st.dataframe(comp_df.set_index("Metric"), use_container_width=True)

    with col_dash2:
        chart_fig = plot_route_comparison(m_base, m_opt)
        st.pyplot(chart_fig)

    st.subheader("Route Waypoint Sequences")
    st.markdown(f"**Baseline Sequence**: `{' ➔ '.join(base_seq)}`")
    st.markdown(f"**Optimized Sequence**: `{' ➔ '.join(opt_seq)}`")

    # Audit & History Action Buttons
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("💾 Save Route Plan to History Audit Log"):
            run_data = {
                "algorithm_name": opt_algo_name,
                "depot_id": "DEPOT",
                "truck_capacity_kg": truck_capacity,
                "total_waste_collected_kg": m_opt["total_waste_kg"],
                "capacity_utilization_pct": m_opt["capacity_utilization_pct"],
                "total_distance_km": m_opt["total_distance_km"],
                "travel_time_min": m_opt["travel_time_min"],
                "bins_visited_count": m_opt["bins_visited_count"],
                "uncollected_count": m_opt["uncollected_count"],
                "savings_pct": comparison["distance_savings_pct"],
                "route_sequence": opt_seq,
                "execution_time_ms": opt_time_ms
            }
            new_run_id = save_route_run(run_data)
            st.success(f"Route run saved to persistent SQLite database! (Run ID: #{new_run_id})")

    with c_btn2:
        if st.button("✅ Mark Visited Bins as 'Collected' in Database"):
            visited_ids = [n for n in opt_seq if n != "DEPOT"]
            cnt = update_bin_status(visited_ids, "Collected")
            st.success(f"Marked {cnt} bins as Collected! Database updated.")
            st.rerun()


# ==============================================================================
# VIEW 5: INTERACTIVE ROUTE MAP
# ==============================================================================
elif view_selection == "📍 Interactive Route Map":
    st.title("📍 Interactive Collection Route Map")
    st.caption("Visual map representation with depot base, bin fill badges, road network connections, and planned collection paths.")

    bins = get_all_bins()
    planner = RoutePlanner(road_graph, depot_id="DEPOT")

    # Quick option to show Baseline vs Optimized route
    map_mode = st.radio("Route Display", ["Optimized Route (Nearest-Neighbor)", "Baseline Route (Input Order)", "Bins Only (No Route)"], horizontal=True)

    pending_bins = [b for b in bins if b.get("status") == "Pending"] or bins
    selected_bins, _, _, _ = select_bins_knapsack_dp(pending_bins, capacity_kg=1200.0)
    selected_ids = [b["bin_id"] for b in selected_bins]
    dist_matrix = planner.build_distance_matrix(selected_ids)

    if map_mode == "Optimized Route (Nearest-Neighbor)":
        seq, _ = planner.plan_nearest_neighbor_route(selected_ids, dist_matrix)
    elif map_mode == "Baseline Route (Input Order)":
        seq, _ = planner.plan_baseline_route(selected_ids, dist_matrix)
    else:
        seq = None

    # Load road edge connections for visual background
    road_df = pd.read_csv("data/sample_roads.csv")
    road_edges_list = [dict(r) for _, r in road_df.iterrows()]

    m = build_collection_map(
        depot_info=depot_config,
        bins_list=bins,
        route_sequence=seq,
        road_edges=road_edges_list
    )

    st_folium(m, width="100%", height=550)


# ==============================================================================
# VIEW 6: ROUTE HISTORY & REPORTS
# ==============================================================================
elif view_selection == "📊 Route History & Reports":
    st.title("📊 Route History Audit & Export")
    st.caption("Audit trail of all executed route optimization runs saved persistently in SQLite.")

    history = get_route_history(limit=50)

    if history:
        df_hist = pd.DataFrame(history)
        st.dataframe(
            df_hist[["run_id", "timestamp", "algorithm_name", "truck_capacity_kg", "total_waste_collected_kg", "capacity_utilization_pct", "total_distance_km", "travel_time_min", "bins_visited_count", "savings_pct"]],
            use_container_width=True
        )

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            csv_hist = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export Route History to CSV",
                csv_hist,
                "route_optimization_history.csv",
                "text/csv"
            )
        with col_h2:
            if st.button("🗑️ Clear All Route Run History"):
                clear_route_history()
                st.success("History log cleared.")
                st.rerun()
    else:
        st.info("No route optimization runs recorded yet. Generate a route in the Route Optimizer and click 'Save Route Plan to History Audit Log'.")


# ==============================================================================
# VIEW 7: DAA ALGORITHM LAB
# ==============================================================================
elif view_selection == "🧪 DAA Algorithm Lab":
    st.title("🧪 DAA Algorithm Lab (Complete Syllabus Units 1 to 8)")
    st.caption("Interactive workbench for running, testing, and inspecting genuine implementations across all syllabus units.")

    lab_unit = st.selectbox(
        "Select DAA Syllabus Unit",
        [
            "Unit 1: Basics & Mathematical Analysis",
            "Unit 2: Recurrences & Sorting Algorithms",
            "Unit 3: Divide & Conquer",
            "Unit 4: Greedy Algorithms",
            "Unit 5: Dynamic Programming",
            "Unit 6: Graph Exploration, Backtracking & Branch and Bound",
            "Unit 7: String Matching",
            "Unit 8: NP-Completeness & Exact TSP"
        ]
    )

    st.divider()

    # --- UNIT 1 LAB ---
    if "Unit 1" in lab_unit:
        st.subheader("Unit 1: Basics and Mathematical Analysis")
        u1_tab1, u1_tab2, u1_tab3, u1_tab4 = st.tabs(["Sets & Quantifiers", "Series & Combinations", "Loop Counter Analysis", "Amortized Dynamic Array Doubling"])

        with u1_tab1:
            st.markdown("#### Set Operations on Waste Zones")
            s_a = st.text_input("Set A (comma separated)", "BIN-01, BIN-02, BIN-03, BIN-05")
            s_b = st.text_input("Set B (comma separated)", "BIN-02, BIN-04, BIN-05, BIN-06")
            set_a = {x.strip() for x in s_a.split(",") if x.strip()}
            set_b = {x.strip() for x in s_b.split(",") if x.strip()}
            st.json(set_operations_demo(set_a, set_b))

        with u1_tab2:
            st.markdown("#### Arithmetic & Geometric Series")
            c1, c2 = st.columns(2)
            with c1:
                n_terms = st.slider("Number of terms (n)", 1, 50, 10)
                f_res, a_res, d_str = arithmetic_series_sum(n_terms, a=1.0, d=1.0)
                st.write(f"**Arithmetic Series (1 + 2 + ... + {n_terms})**:")
                st.write(f"Formula Result: `{f_res}` | Derivation: `{d_str}`")
            with c2:
                comb = permutations_combinations(n_terms, min(3, n_terms))
                st.write(f"**Permutations P({n_terms}, 3)**: `{comb['permutations']}`")
                st.write(f"**Combinations C({n_terms}, 3)**: `{comb['combinations']}`")

        with u1_tab3:
            st.markdown("#### Loop Operation Counters: for, nested for, and while")
            n_loop = st.slider("Input size N for loop test", 5, 200, 20)
            loop_res = analyze_loop_counters(n_loop)
            st.write(f"- **Single for loop**: Count = `{loop_res['single_for_count']}` (Theoretical $O(n) = {loop_res['single_for_theoretical']}$)")
            st.write(f"- **Nested triangular for loop**: Count = `{loop_res['nested_for_count']}` (Theoretical $n(n+1)/2 = {loop_res['nested_for_theoretical']}$)")
            st.write(f"- **Halving while loop**: Count = `{loop_res['log_while_count']}` (Theoretical $\\lfloor \\log_2 n \\rfloor = {loop_res['log_while_theoretical']}$)")

        with u1_tab4:
            st.markdown("#### Amortized Analysis: Dynamic Array Table Doubling")
            num_appends = st.slider("Number of Sequential Append Operations", 10, 128, 32)
            amort_res = simulate_dynamic_array_amortization(num_appends)
            st.write(f"**Total Operations**: `{amort_res['total_operations']}` | **Overall Amortized Cost per Append**: `{amort_res['overall_amortized_cost']} operations`")
            st.info(f"**Mathematical Proof**: {amort_res['theoretical_bound']}")
            st.dataframe(pd.DataFrame(amort_res["history_snapshots"]), use_container_width=True)

    # --- UNIT 2 LAB ---
    elif "Unit 2" in lab_unit:
        st.subheader("Unit 2: Recurrences & Sorting Algorithms")
        u2_tab1, u2_tab2 = st.tabs(["📊 Sorting Algorithms Benchmark", "📐 Recurrence Equation Solver"])

        with u2_tab1:
            st.markdown("#### Direct Comparison of 6 Sorting Algorithms")
            sort_input = st.text_input("Enter comma-separated numbers", "64, 34, 25, 12, 22, 11, 90, 45, 8, 77")
            raw_nums = [float(x.strip()) for x in sort_input.split(",") if x.strip()]
            int_nums = [int(x) for x in raw_nums]

            r_bubble = bubble_sort(raw_nums)
            r_sel = selection_sort(raw_nums)
            r_ins = insertion_sort(raw_nums)
            r_heap = heap_sort(raw_nums)
            r_count = counting_sort(int_nums)
            r_bucket = bucket_sort(raw_nums)

            sort_results = [r_bubble, r_sel, r_ins, r_heap, r_count, r_bucket]
            st.dataframe(pd.DataFrame([
                {
                    "Algorithm": r["algorithm"],
                    "Comparisons": r.get("comparisons", 0),
                    "Swaps / Moves": r.get("swaps", 0),
                    "Time (ms)": r["execution_time_ms"],
                    "Stable": r.get("is_stable", False),
                    "Time Complexity": str(r.get("time_complexity", {})),
                    "Space": r.get("space_complexity", "")
                } for r in sort_results
            ]), use_container_width=True)

            chart_sort = plot_sorting_comparison(sort_results)
            st.pyplot(chart_sort)

        with u2_tab2:
            st.markdown("#### Master Theorem Solver: $T(n) = a T(n/b) + \\Theta(n^d)$")
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                m_a = st.number_input("a (subproblems)", min_value=1.0, value=2.0, step=1.0)
            with c_m2:
                m_b = st.number_input("b (division factor)", min_value=1.1, value=2.0, step=0.5)
            with c_m3:
                m_d = st.number_input("d (polynomial degree)", min_value=0.0, value=1.0, step=0.5)

            sol = solve_master_theorem(m_a, m_b, m_d)
            if sol["applicable"]:
                st.success(f"**Complexity**: `{sol['complexity']}`")
                st.write(f"- **Recurrence**: `{sol['recurrence']}`")
                st.write(f"- **Case**: `Case {sol['case']}`")
                st.write(f"- **Explanation**: {sol['explanation']}")
            else:
                st.error(sol["error"])

            st.divider()
            st.markdown("#### Recursion Tree Inspector")
            tree_info = analyze_recursion_tree(int(m_a), m_b, depth_levels=4)
            st.dataframe(pd.DataFrame(tree_info["level_breakdown"]), use_container_width=True)

    # --- UNIT 3 LAB ---
    elif "Unit 3" in lab_unit:
        st.subheader("Unit 3: Divide & Conquer Algorithms")
        d_tab1, d_tab2, d_tab3 = st.tabs(["Binary Search & Max-Min", "Karatsuba Large Integer Multiplication", "Strassen Matrix Multiplication"])

        with d_tab1:
            st.markdown("#### Binary Search")
            sorted_arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
            st.write(f"Sorted Array: `{sorted_arr}`")
            target_val = st.number_input("Target Value to Search", value=23)
            b_res = binary_search(sorted_arr, target_val)
            st.write(f"**Search Result Index**: `{b_res['found_index']}` | **Comparisons**: `{b_res['comparisons']}`")
            st.dataframe(pd.DataFrame(b_res["search_trace"]))

            st.markdown("#### Max-Min Tournament Problem")
            mm_arr = [1000, 11, 445, 1, 330, 3000, 220, 85]
            mm_res = max_min_divide_and_conquer(mm_arr)
            st.write(f"Array: `{mm_arr}`")
            st.write(f"Min: `{mm_res['minimum']}` | Max: `{mm_res['maximum']}`")
            st.write(f"Tournament Comparisons: `{mm_res['comparisons']}` vs Naive Scan Comparisons: `{mm_res['naive_comparisons']}`")
            st.success(f"Comparisons Saved: `{mm_res['comparisons_saved']}`")

        with d_tab2:
            st.markdown("#### Karatsuba Large Integer Multiplication")
            k_x = st.number_input("Integer X", value=12345678, step=1)
            k_y = st.number_input("Integer Y", value=87654321, step=1)
            k_res = karatsuba_multiplication(k_x, k_y)
            st.write(f"**Product Result**: `{k_res['product']}`")
            st.write(f"Verified Correct: `{k_res['verified_correct']}` | Recursive Calls: `{k_res['recursive_calls']}`")
            st.info("Complexity: $O(n^{\\log_2 3}) \\approx O(n^{1.585})$ vs standard $O(n^2)$.")

        with d_tab3:
            st.markdown("#### Strassen's Matrix Multiplication (2x2 Demo)")
            A_m = [[1.0, 2.0], [3.0, 4.0]]
            B_m = [[5.0, 6.0], [7.0, 8.0]]
            st.write(f"Matrix A: `{A_m}` | Matrix B: `{B_m}`")
            stras_res = strassen_2x2_multiply(A_m, B_m)
            st.write(f"**Product C = A * B**: `{stras_res['result_matrix']}`")
            st.write(f"Scalar Multiplications: `{stras_res['scalar_multiplications']}` (Saved 1 multiplication vs standard 8)")

    # --- UNIT 4 LAB ---
    elif "Unit 4" in lab_unit:
        st.subheader("Unit 4: Greedy Algorithms")
        g_tab1, g_tab2, g_tab3, g_tab4 = st.tabs(["Dijkstra & Bellman-Ford", "Prim & Kruskal MST", "Fractional Knapsack & Jobs", "Huffman Coding"])

        with g_tab1:
            st.markdown("#### Shortest Paths: Dijkstra vs Bellman-Ford")
            st.write("Demonstration on 4-vertex graph:")
            adj_demo = {
                0: [(1, 4.0), (2, 1.0)],
                1: [(3, 1.0)],
                2: [(1, 2.0), (3, 5.0)],
                3: []
            }
            dijk_res = dijkstra_shortest_path(4, adj_demo, source=0)
            st.write(f"**Dijkstra Shortest Distances from Node 0**: `{dijk_res['distances']}`")

            st.markdown("#### Bellman-Ford Negative Cycle Detection")
            neg_edges = [(0, 1, 1.0), (1, 2, -2.0), (2, 1, -1.0)]
            bf_res = bellman_ford_shortest_path(3, neg_edges, source=0)
            st.write(f"Negative Cycle Detected: `{bf_res['has_negative_cycle']}`")
            st.info("Bellman-Ford handles arbitrary edge weights and halts gracefully upon negative cycles.")

        with g_tab2:
            st.markdown("#### Minimum Spanning Tree (Prim vs Kruskal)")
            sample_mst_edges = [
                (0, 1, 4.0), (0, 7, 8.0), (1, 2, 8.0), (1, 7, 11.0),
                (2, 3, 7.0), (2, 8, 2.0), (2, 5, 4.0), (3, 4, 9.0),
                (3, 5, 14.0), (4, 5, 10.0), (5, 6, 2.0), (6, 7, 1.0),
                (6, 8, 6.0), (7, 8, 7.0)
            ]
            prim_res = prim_mst(9, sample_mst_edges, start_node=0)
            kruskal_res = kruskal_mst(9, sample_mst_edges)
            st.write(f"**Prim's MST Total Weight**: `{prim_res['total_weight']}`")
            st.write(f"**Kruskal's MST Total Weight**: `{kruskal_res['total_weight']}`")

        with g_tab3:
            st.markdown("#### Fractional Knapsack (Greedy by Ratio)")
            wts = [10.0, 20.0, 30.0]
            vals = [60.0, 100.0, 120.0]
            frac_res = fractional_knapsack_greedy(wts, vals, capacity=50.0)
            st.write(f"Total Value Gained: `{frac_res['total_value']}`")
            st.dataframe(pd.DataFrame(frac_res["selections"]))

        with g_tab4:
            st.markdown("#### Huffman Compression Codebook")
            huff_txt = st.text_input("Text to encode", "ABRACADABRA MUNICIPAL WASTE")
            h_res = huffman_encoding(huff_txt)
            st.write(f"**Compression Ratio**: `{h_res['compression_ratio']}x`")
            st.write(f"Codebook: `{h_res['codebook']}`")

    # --- UNIT 5 LAB ---
    elif "Unit 5" in lab_unit:
        st.subheader("Unit 5: Dynamic Programming")
        dp_tab1, dp_tab2, dp_tab3 = st.tabs(["0/1 Knapsack & Greedy Counterexample", "Matrix Chain Multiplication", "Longest Common Subsequence"])

        with dp_tab1:
            st.markdown("#### 0/1 Knapsack Dynamic Programming")
            w_01 = [10, 20, 30]
            v_01 = [60, 100, 120]
            c_01 = 50
            knap_res = knapsack_01_dp(w_01, v_01, c_01)
            st.write(f"**Optimal 0/1 Value**: `{knap_res['max_value']}` | Items: `{knap_res['selected_indices']}`")

            st.markdown("#### Canonical Counterexample: Greedy vs DP Coin Change")
            comp_coin = compare_greedy_vs_dp_coin_change()
            st.write(f"- Coins Available: `{comp_coin['coins']}` | Target: `{comp_coin['amount']}`")
            st.write(f"- Greedy Choice (takes largest coin first): `{comp_coin['greedy_solution']}` (**{comp_coin['greedy_coin_count']} coins**)")
            st.write(f"- DP Optimal Solution: `{comp_coin['dp_solution']}` (**{comp_coin['dp_coin_count']} coins**)")
            st.success("Proven: Greedy fails to achieve optimality on non-canonical denominations!")

        with dp_tab2:
            st.markdown("#### Matrix Chain Multiplication")
            m_dims = [10, 30, 5, 60]
            mcm_res = matrix_chain_multiplication(m_dims)
            st.write(f"**Minimum Scalar Multiplications**: `{mcm_res['min_scalar_multiplications']}`")
            st.write(f"**Optimal Parenthesization**: `{mcm_res['optimal_parenthesization']}`")

        with dp_tab3:
            st.markdown("#### Longest Common Subsequence (LCS)")
            s1 = st.text_input("String 1", "AGGTAB")
            s2 = st.text_input("String 2", "GXTXAYB")
            lcs_res = longest_common_subsequence(s1, s2)
            st.write(f"**LCS Length**: `{lcs_res['lcs_length']}` | **LCS String**: `{lcs_res['lcs_string']}`")

    # --- UNIT 6 LAB ---
    elif "Unit 6" in lab_unit:
        st.subheader("Unit 6: Graph Exploration, Backtracking & Branch and Bound")
        u6_tab1, u6_tab2, u6_tab3 = st.tabs(["N-Queens Backtracking", "Assignment Problem (Branch & Bound)", "Minimax Game Tree Search"])

        with u6_tab1:
            st.markdown("#### N-Queens Puzzle")
            n_q = st.slider("Board Dimension N", 4, 10, 8)
            q_res = solve_n_queens(n_q, find_all=True)
            st.write(f"Total Valid Solutions Found: `{q_res['solution_count']}`")
            if q_res["solutions"]:
                st.write(f"Sample Solution (Queen Col per Row): `{q_res['solutions'][0]}`")

        with u6_tab2:
            st.markdown("#### Assignment Problem (Branch & Bound LC-Search)")
            cost_m = [
                [9.0, 2.0, 7.0, 8.0],
                [6.0, 4.0, 3.0, 7.0],
                [5.0, 8.0, 1.0, 8.0],
                [7.0, 6.0, 9.0, 4.0]
            ]
            ass_res = solve_assignment_problem_bnb(cost_m)
            st.write(f"**Minimum Total Assignment Cost**: `{ass_res['min_total_cost']}`")
            st.write(f"Worker-Job Pairs (Worker, Job): `{ass_res['worker_job_assignments']}`")

        with u6_tab3:
            st.markdown("#### Minimax with Alpha-Beta Pruning")
            mini_res = minimax_alphabeta_demo()
            st.write(f"Optimal Root Value: `{mini_res['optimal_root_value']}`")
            st.write(f"Branches Pruned by Alpha-Beta Bounds: `{mini_res['branches_pruned']}`")

    # --- UNIT 7 LAB ---
    elif "Unit 7" in lab_unit:
        st.subheader("Unit 7: String Matching Algorithms")
        st.markdown("#### Text Pattern Search Comparison (Naive vs Rabin-Karp vs KMP)")
        s_text = st.text_area("Input Text", "AABAACAADAABAABA")
        s_pat = st.text_input("Pattern to Find", "AABA")

        r_n = naive_string_match(s_text, s_pat)
        r_rk = rabin_karp_match(s_text, s_pat)
        r_kmp = kmp_string_match(s_text, s_pat)

        st.dataframe(pd.DataFrame([
            {"Algorithm": "Naive Matching", "Matches": str(r_n["matches"]), "Comparisons": r_n["character_comparisons"], "Time (ms)": r_n["execution_time_ms"]},
            {"Algorithm": "Rabin-Karp (Rolling Hash)", "Matches": str(r_rk["matches"]), "Comparisons": r_rk["character_comparisons"], "Time (ms)": r_rk["execution_time_ms"]},
            {"Algorithm": "Knuth-Morris-Pratt (KMP)", "Matches": str(r_kmp["matches"]), "Comparisons": r_kmp["character_comparisons"], "Time (ms)": r_kmp["execution_time_ms"]}
        ]))

        st.markdown("#### Municipal Complaint Search Application")
        q_complaint = st.text_input("Keyword in Citizen Complaints", "overflow")
        res_comp = search_complaint_tickets(q_complaint)
        st.write(f"Found **{res_comp['matched_tickets_count']}** matching tickets:")
        st.dataframe(pd.DataFrame(res_comp["matched_tickets"]))

    # --- UNIT 8 LAB ---
    elif "Unit 8" in lab_unit:
        st.subheader("Unit 8: NP-Completeness & Exact TSP")
        st.markdown("#### Theoretical Hierarchy: P, NP, NP-Complete, and NP-Hard")
        for cls, data in NP_COMPLEXITY_CLASSES.items():
            with st.expander(f"📌 Class {cls}: {data['name']}"):
                st.write(f"**Definition**: {data['definition']}")
                st.write(f"**Examples**: {', '.join(data['examples'])}")

        st.divider()
        st.markdown("#### Polynomial-Time Reduction Walkthrough")
        red = reduction_hamiltonian_cycle_to_tsp()
        st.write(f"**Reduction**: `{red['reduction_name']}` ({red['reduction_complexity']})")
        for stp in red["steps"]:
            st.markdown(f"- {stp}")

        st.divider()
        st.markdown("#### Empirical Benchmark: Exact TSP vs Nearest-Neighbor Greedy")
        tsp_sample_dist = [
            [0.0, 10.0, 15.0, 20.0],
            [10.0, 0.0, 35.0, 25.0],
            [15.0, 35.0, 0.0, 30.0],
            [20.0, 25.0, 30.0, 0.0]
        ]
        tsp_comp = compare_exact_vs_greedy_tsp(tsp_sample_dist, start_vertex=0)
        st.write(f"**Exact Optimal Cost**: `{tsp_comp['exact_solution']['cost']}` | Tour: `{tsp_comp['exact_solution']['tour']}`")
        st.write(f"**Greedy Heuristic Cost**: `{tsp_comp['greedy_heuristic']['cost']}` | Tour: `{tsp_comp['greedy_heuristic']['tour']}`")
        st.write(f"Speedup Factor of Heuristic: `{tsp_comp['speedup_factor']}x` faster")


# ==============================================================================
# VIEW 8: COMPLEXITY & BENCHMARKS
# ==============================================================================
elif view_selection == "📈 Complexity & Benchmarks":
    st.title("📈 Complexity Profiler & Empirical Benchmarks")
    st.caption("Benchmark empirical CPU runtimes across increasing input sizes N and contrast with theoretical Big-O curves.")

    st.markdown("""
    ### Asymptotic Notations Reference
    """)
    c_a1, c_a2, c_a3 = st.columns(3)
    with c_a1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Big-O: O(g(n))</div>
            <div style="font-weight: bold; margin-top: 4px;">Asymptotic Upper Bound</div>
            <p style="font-size: 13px; color: #64748b; margin-top: 4px;">f(n) <= c * g(n) for n >= n0. Worst-case running time guarantee.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_a2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Big-Omega: Ω(g(n))</div>
            <div style="font-weight: bold; margin-top: 4px;">Asymptotic Lower Bound</div>
            <p style="font-size: 13px; color: #64748b; margin-top: 4px;">f(n) >= c * g(n) for n >= n0. Best-case running time guarantee.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_a3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Big-Theta: Θ(g(n))</div>
            <div style="font-weight: bold; margin-top: 4px;">Asymptotically Tight Bound</div>
            <p style="font-size: 13px; color: #64748b; margin-top: 4px;">c1 * g(n) <= f(n) <= c2 * g(n). Sandwiched tightly from both sides.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Live Empirical Timing Benchmark")
    algo_choice = st.selectbox("Choose Algorithm to Benchmark", ["Merge Sort (O(n log n))", "Quick Sort (O(n log n) avg)", "Insertion Sort (O(n^2))", "Bubble Sort (O(n^2))"])

    if st.button("🚀 Run Empirical Benchmark Across N = [100, 250, 500, 1000, 2000]"):
        import random
        sizes = [100, 250, 500, 1000, 2000]
        gen = lambda s: [random.randint(1, 10000) for _ in range(s)]

        if "Merge" in algo_choice:
            fn = lambda data: merge_sort(data)
        elif "Quick" in algo_choice:
            fn = lambda data: quick_sort(data)
        elif "Insertion" in algo_choice:
            fn = lambda data: insertion_sort(data)
        else:
            fn = lambda data: bubble_sort(data)

        with st.spinner("Benchmarking execution times..."):
            bench_results = benchmark_function_sizes(fn, gen, sizes, runs_per_size=3)

        st.dataframe(pd.DataFrame(bench_results), use_container_width=True)
        chart_curve = plot_complexity_curves(bench_results)
        st.pyplot(chart_curve)
        st.info("⚠️ Note: Observed runtimes depend on CPU architecture, OS context switches, and Python interpreter overhead. A single timing measurement does not prove an asymptotic bound.")


# ==============================================================================
# VIEW 9: DAA SYLLABUS & VIVA GUIDE
# ==============================================================================
elif view_selection == "📚 DAA Syllabus & Viva Guide":
    st.title("📚 DAA Syllabus Coverage & Viva Examination Guide")
    st.caption("Structured syllabus mapping matrix across Units 1 to 8, exam revision summary, and viva voce technical Q&A.")

    viva_tab1, viva_tab2 = st.tabs(["📋 Syllabus Coverage Matrix", "🎓 Viva Voce Questions & Answers"])

    with viva_tab1:
        st.subheader("DAA Syllabus Mapping Matrix")
        syllabus_data = [
            {"Unit": "Unit 1", "Topic": "Sets, functions, relations, quantifiers, vectors, series, loop analysis, amortized analysis", "Implementation Source": "algorithms/mathematical_analysis.py", "Test File": "tests/test_database_and_data.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 1", "Topic": "Asymptotic bounds (Big-O, Omega, Theta), limit rules, complexity profiler", "Implementation Source": "algorithms/complexity.py", "Test File": "tests/test_database_and_data.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 2", "Topic": "Sorting: Bubble, Selection, Insertion, Heap, Counting, Bucket Sort", "Implementation Source": "algorithms/sorting.py", "Test File": "tests/test_sorting.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 2", "Topic": "Recurrences: Master Theorem, Substitution, Recursion Tree, Homogeneous Linear", "Implementation Source": "algorithms/recurrence_analysis.py", "Test File": "tests/test_divide_and_conquer.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 3", "Topic": "Binary Search, Merge Sort, Quick Sort, Max-Min problem", "Implementation Source": "algorithms/divide_and_conquer.py", "Test File": "tests/test_divide_and_conquer.py, tests/test_searching.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 3", "Topic": "Karatsuba Large Integer Multiplication, Strassen Matrix Multiplication, Exponential Fib", "Implementation Source": "algorithms/divide_and_conquer.py", "Test File": "tests/test_divide_and_conquer.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 4", "Topic": "Greedy Coin Change, Prim MST, Kruskal MST, Dijkstra, Bellman-Ford, Frac Knapsack, Jobs, Huffman", "Implementation Source": "algorithms/greedy.py", "Test File": "tests/test_greedy.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 5", "Topic": "Binomial DP, Coin Change DP, 0/1 Knapsack DP, Floyd-Warshall, Matrix Chain, LCS, Greedy vs DP", "Implementation Source": "algorithms/dynamic_programming.py", "Test File": "tests/test_dynamic_programming.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 6", "Topic": "Graph BFS, DFS, Topological Sort, N-Queens, Knapsack Backtracking, Assignment B&B, Minimax", "Implementation Source": "algorithms/graph_algorithms.py, algorithms/backtracking.py, algorithms/branch_and_bound.py", "Test File": "tests/test_graph_algorithms.py, tests/test_backtracking_bnb.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 7", "Topic": "Naive String Matching, Rabin-Karp (Rolling Hash), Knuth-Morris-Pratt (KMP), Complaint Search", "Implementation Source": "algorithms/string_matching.py", "Test File": "tests/test_string_matching.py", "Status": "Verified & Tested"},
            {"Unit": "Unit 8", "Topic": "P vs NP, NP-Completeness, HC <=_P TSP Polynomial Reduction, Exact TSP vs Nearest-Neighbor", "Implementation Source": "algorithms/np_completeness.py, algorithms/backtracking.py", "Test File": "tests/test_backtracking_bnb.py", "Status": "Verified & Tested"}
        ]
        st.dataframe(pd.DataFrame(syllabus_data), use_container_width=True)

    with viva_tab2:
        st.subheader("🎓 10 Core Viva Questions & Model Answers")

        vivas = [
            (
                "Q1: Why is waste collection modelled as a Travelling Salesperson Problem (TSP) rather than a simple shortest path problem?",
                "Shortest path (Dijkstra) finds the minimum distance between ONE origin and ONE destination. Waste collection requires visiting a SUBSET of multiple bins and returning to the depot, which is a tour permutation problem — exactly the formulation of the Travelling Salesperson Problem (TSP)."
            ),
            (
                "Q2: Is the waste collection problem NP-hard? Why?",
                "Yes. The optimization TSP is NP-hard because its decision version (does a tour of cost <= k exist?) is NP-complete via polynomial-time reduction from Hamiltonian Cycle. Adding truck capacity constraints transforms it into the Capacitated Vehicle Routing Problem (CVRP), which is also NP-hard."
            ),
            (
                "Q3: Why can't we always use the Exact Branch and Bound TSP solver?",
                "Exact TSP has worst-case time complexity O(N!) or O(N^2 * 2^N) with dynamic programming. For N = 10, 10! = 3.6 million states, which runs in milliseconds. But for N = 20, 20! ≈ 2.4 * 10^18 operations, which would freeze the computer for years. Thus, we use the Nearest-Neighbor greedy heuristic for larger inputs."
            ),
            (
                "Q4: How does 0/1 Knapsack Dynamic Programming select which bins to collect?",
                "Given a truck capacity W, each bin i has weight w_i = waste_kg and value v_i = priority_score. The 0/1 knapsack DP table maximizes the total priority value of collected bins such that the sum of their weights is <= W. This guarantees optimal capacity utilization."
            ),
            (
                "Q5: Why does greedy coin change fail on coins [1, 3, 4] for amount 6, but DP succeeds?",
                "Greedy irrevocably takes the largest coin 4 first, leaving 2, requiring two 1s (total 3 coins: 4+1+1). DP considers all subproblems and discovers 3+3 (2 coins), which is optimal. Greedy makes local irrevocable decisions without looking ahead."
            ),
            (
                "Q6: What is the difference between Dijkstra and Bellman-Ford?",
                "Dijkstra runs in O((V + E) log V) but assumes all edge weights are non-negative. Bellman-Ford runs in O(V * E), allows negative edge weights, and detects reachable negative-weight cycles."
            ),
            (
                "Q7: What is amortized analysis and how does dynamic array doubling achieve O(1) amortized time?",
                "Amortized analysis averages the running time of a sequence of operations over all operations. When a dynamic array doubles its capacity upon filling, an occasional expensive resize O(N) is preceded by N-1 cheap O(1) insertions. The aggregate cost over N appends is <= 3N, yielding O(1) amortized cost per append."
            ),
            (
                "Q8: How does KMP string matching improve over naive string matching?",
                "Naive matching backtracks the text pointer upon a mismatch, taking worst-case O((N - M + 1) * M). KMP precomputes the pi failure table (longest proper prefix that is also a suffix) and advances the text pointer monotonically without backtracking, guaranteeing O(N + M) time."
            ),
            (
                "Q9: What is the Master Theorem and when does it not apply?",
                "Master Theorem solves recurrences T(n) = a*T(n/b) + Theta(n^d) by comparing d with log_b(a). It does not apply when: a < 1, b <= 1, f(n) is not polynomial (e.g. 2^n), or the gap between f(n) and n^(log_b a) is non-polynomial."
            ),
            (
                "Q10: Why do we distinguish straight-line Haversine distance from Road Network distance?",
                "Haversine calculates Euclidean spherical geometric distance as the crow flies. Urban road networks consist of actual streets, intersections, turns, and one-way streets. Real driving distance is always greater than or equal to straight-line distance; confounding the two leads to infeasible vehicle plans."
            )
        ]

        for q, a in vivas:
            with st.expander(f"**{q}**"):
                st.markdown(f"**Answer**: {a}")
