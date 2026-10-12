# Academic Project Report

**Project Title**: Smart Waste Collection Route Optimizer with Complete DAA Coverage  
**Degree**: Bachelor of Engineering (B.E.) in Computer Engineering  
**Subject**: Design and Analysis of Algorithms (DAA)  
**Academic Year**: 2026–2027  

---

## 1. Abstract
Municipal Solid Waste Management (MSWM) is one of the most critical operational challenges in modern urban administration. Inefficient, static collection schedules lead to overflowing bins, environmental hazards, wasted municipal fuel, and high vehicular carbon emissions. This project presents the **Smart Waste Collection Route Optimizer**, a decision-support system and educational laboratory developed in Python and Streamlit. The system models the municipal road network as a weighted directed graph, evaluates bin priority via a transparent multi-criteria formula, selects feasible collections under vehicle capacity limits using 0/1 Knapsack Dynamic Programming, and generates collection tours using shortest path calculations (Dijkstra), a Nearest-Neighbor greedy heuristic, and an exact Branch-and-Bound Traveling Salesperson Problem (TSP) solver. Additionally, the project features a dedicated **DAA Algorithm Lab** that implements, tests, and benchmarks every major algorithmic paradigm across Units 1 to 8 of the DAA curriculum.

---

## 2. Problem Statement
Municipal sanitation authorities must collect waste from multiple dispersed bins across urban wards while respecting vehicle load capacities, one-way road constraints, and urgency criteria. Current practices rely on static daily beats where trucks follow predetermined routes regardless of bin fill levels. This results in:
1. Unnecessary visits to bins with low waste fill.
2. Delayed collection at overflowing, hazardous locations.
3. Suboptimal travel sequences, increasing total distance, travel time, and diesel consumption.
4. Violations of vehicle weight capacities, requiring mid-route aborts.

The objective is to formulate and implement an algorithmic system that dynamically selects the optimal subset of bins and schedules an efficient collection route returning to the depot, while serving as a comprehensive demonstration platform for core algorithmic design techniques.

---

## 3. Objectives
- Implement a full-featured bin management system with SQLite persistence, validation, and CSV import/export.
- Represent urban road networks as directed, weighted graphs accounting for one-way roads.
- Formulate a transparent, deterministic priority scoring rule.
- Solve vehicle capacity constraints using 0/1 Knapsack Dynamic Programming.
- Implement baseline (input order), Nearest-Neighbor greedy heuristic, and exact Branch-and-Bound TSP route planners.
- Build an interactive Folium map visualization and performance comparison dashboard.
- Implement every topic in Units 1 to 8 of the DAA syllabus with direct source code, automated test verification, and educational explanations.

---

## 4. Existing Problem vs. Proposed Solution

| Feature | Existing Practice | Proposed Algorithmic Solution |
| :--- | :--- | :--- |
| **Collection Scheduling** | Fixed static routes regardless of fill level. | Dynamic collection triggered by fill level and priority scoring. |
| **Bin Selection** | Ad-hoc selection often exceeding truck limits. | 0/1 Knapsack Dynamic Programming maximizing priority within truck capacity. |
| **Road Distance Model** | Euclidean straight-line assumptions. | Directed road network shortest paths via Dijkstra's algorithm. |
| **Route Generation** | Driver intuition or arbitrary sequences. | Nearest-Neighbor heuristic and Exact Branch & Bound TSP search. |
| **Evaluation Metrics** | Rough odometer estimates. | Explicit calculation of distance, travel time, capacity utilization, fuel, and CO2 savings. |

---

## 5. Requirements Specification

### 5.1 Functional Requirements
- **FR1 (Bin CRUD)**: Allow users to create, view, update, and delete bin records with latitude, longitude, fill level (%), waste weight (kg), urgency, and status.
- **FR2 (Validation)**: Enforce coordinate boundaries ($-90 \le \text{lat} \le 90$), percentage ranges ($0-100\%$), non-negative weights, and unique bin identifiers.
- **FR3 (Road Graph)**: Construct a directed graph supporting two-way and one-way streets with non-negative edge weights.
- **FR4 (Capacity Enforcement)**: Ensure selected bins strictly respect the configured truck capacity.
- **FR5 (Route Planning)**: Generate a baseline tour, a nearest-neighbor tour, and an exact TSP tour returning to the depot.
- **FR6 (Map Rendering)**: Render an interactive map showing the depot, color-coded bin markers, road links, and route sequences.
- **FR7 (Audit Persistence)**: Record all executed routes into SQLite with timestamps, metrics, and sequences.
- **FR8 (Algorithm Lab)**: Provide runnable interactive modules for all syllabus topics across Units 1 to 8.

### 5.2 Non-Functional Requirements
- **NFR1 (Correctness)**: All algorithms must produce mathematically verified results validated by automated tests.
- **NFR2 (Responsiveness)**: The web UI must respond in under 1 second for standard operations; exact exponential searches must be bounded ($N \le 10$).
- **NFR3 (Explainability)**: Algorithms and priority formulas must be transparent and documented without black-box claims.
- **NFR4 (Portability)**: The system must run offline without requiring external API keys, IoT hardware, or internet connectivity.

---

## 6. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Web Frontend                    │
│   (9 Views: Overview, Bins, Graph, Optimizer, Maps, etc.)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌─────────────────────────────┐       ┌─────────────────────────────┐
│      Optimizer Module       │       │      DAA Algorithm Lab      │
│ - Data Manager & Validation │       │ - Units 1-8 Modular Engines │
│ - Priority Scoring Engine   │       │ - Complexity Profiler       │
│ - 0/1 Knapsack DP Selector  │       │ - Recurrence Solvers        │
│ - Route Planner (NN & B&B)  │       │ - String Matchers           │
│ - Route Metrics Evaluator   │       │ - NP-Completeness Proofs    │
└──────────────┬──────────────┘       └──────────────┬──────────────┘
               │                                     │
               ▼                                     ▼
┌─────────────────────────────┐       ┌─────────────────────────────┐
│      Database & Storage     │       │     Pytest Test Suite       │
│ - SQLite (smart_waste.db)   │       │ - 56 Automated Unit Tests   │
│ - CSV Datasets (Bins, Roads)│       │ - 100% Pass Rate            │
└─────────────────────────────┘       └─────────────────────────────┘
```

---

## 7. Data Model

### Database Schema (SQLite)
1. **`bins` Table**:
   - `bin_id` (TEXT PRIMARY KEY): Unique identifier (e.g. `BIN-01`).
   - `name` (TEXT NOT NULL): Landmark or area name.
   - `latitude` (REAL NOT NULL): Geographical latitude.
   - `longitude` (REAL NOT NULL): Geographical longitude.
   - `waste_level` (REAL NOT NULL): Fill percentage ($0.0 - 100.0$).
   - `waste_kg` (REAL NOT NULL): Estimated mass in kilograms.
   - `urgency` (TEXT NOT NULL): Category (`Low`, `Medium`, `High`, `Critical`).
   - `last_collection_days` (INTEGER): Days elapsed since last emptying.
   - `status` (TEXT NOT NULL): State (`Pending`, `Collected`).
   - `updated_at` (TEXT NOT NULL): Timestamp of last modification.

2. **`routes_history` Table**:
   - `run_id` (INTEGER PRIMARY KEY AUTOINCREMENT): Run identifier.
   - `timestamp` (TEXT NOT NULL): Date and time of optimization run.
   - `algorithm_name` (TEXT NOT NULL): Planner used.
   - `truck_capacity_kg` (REAL NOT NULL): Configured capacity limit.
   - `total_waste_collected_kg` (REAL NOT NULL): Actual mass collected.
   - `capacity_utilization_pct` (REAL NOT NULL): Percentage of capacity utilized.
   - `total_distance_km` (REAL NOT NULL): Total road distance.
   - `travel_time_min` (REAL NOT NULL): Estimated travel duration.
   - `bins_visited_count` (INTEGER NOT NULL): Count of serviced bins.
   - `uncollected_count` (INTEGER NOT NULL): Count of remaining bins.
   - `savings_pct` (REAL NOT NULL): Percentage distance saved over baseline.
   - `route_sequence_json` (TEXT NOT NULL): JSON serialized list of visited nodes.
   - `execution_time_ms` (REAL NOT NULL): Algorithm CPU runtime in milliseconds.

---

## 8. Algorithm Selection & Complexity Analysis

### 8.1 Waste Bin Selection: 0/1 Knapsack Dynamic Programming
- **Rationale**: When truck capacity is constrained, picking bins greedily by weight or urgency can lead to poor utilization or missed critical bins. Modeling bins as items where weight is $w_i = \text{waste\_kg}$ and value is $v_i = \text{priority\_score}$ allows us to find the globally optimal collection subset.
- **Recurrence**:
  $$dp[i][w] = \max(dp[i-1][w], dp[i-1][w - w_i] + v_i)$$
- **Time Complexity**: $O(N \cdot W)$ pseudo-polynomial time.
- **Space Complexity**: $O(N \cdot W)$ auxiliary space.

### 8.2 Shortest Road Paths: Dijkstra's Algorithm
- **Rationale**: Calculates the minimum road driving distance between consecutive stops on a graph with non-negative edge weights.
- **Data Structure**: Min-heap priority queue over adjacency list.
- **Time Complexity**: $O((V + E) \log V)$.
- **Space Complexity**: $O(V)$ for distance and predecessor maps.

### 8.3 Route Planning Heuristic: Nearest-Neighbor Greedy
- **Rationale**: The Traveling Salesperson Problem is NP-hard. For larger bin sets, calculating the exact permutation is computationally infeasible. The Nearest-Neighbor heuristic iteratively visits the closest unvisited location.
- **Time Complexity**: $O(K^2)$ where $K$ is the number of selected bins.
- **Optimality**: Polynomial-time heuristic; not guaranteed to find the global optimum.

### 8.4 Exact Route Planning: Branch-and-Bound TSP
- **Rationale**: For small instances ($K \le 10$), an exact search guarantees global optimality.
- **Bounding Strategy**: Prunes partial paths when the accumulated path cost exceeds the best completed tour cost found so far (initialized with the nearest-neighbor greedy tour upper bound).
- **Time Complexity**: $O(K!)$ worst-case; significantly reduced by branch pruning in practice.
- **Safeguard**: Automatically falls back to Nearest-Neighbor if $K > 10$.

---

## 9. Testing Methodology and Actual Results

Testing was conducted using `pytest` version 9.1.1 under Python 3.13. Every module was tested against edge cases, boundary values, and formal correctness conditions.

### Test Execution Summary
- **Total Test Cases**: 56 automated tests.
- **Passed**: 56.
- **Failed**: 0.
- **Pass Rate**: 100%.
- **Execution Duration**: 4.61 seconds.

### Test Breakdown by Module
1. `tests/test_sorting.py`: 6 tests covering Bubble, Selection, Insertion, Heap, Counting, and Bucket sorts across sorted, reverse, random, duplicate, and empty inputs.
2. `tests/test_searching.py`: 5 tests covering Binary Search hits, misses, boundaries, singletons, and exception throwing on unsorted inputs.
3. `tests/test_divide_and_conquer.py`: 6 tests verifying Merge Sort, Quick Sort, Max-Min tournament comparison savings, Karatsuba multiplication, Strassen matrix products, and Fibonacci limits.
4. `tests/test_greedy.py`: 8 tests covering Coin Change (including canonical counterexample), Prim's MST, Kruskal's MST (with DSU), Dijkstra, Bellman-Ford (negative cycle detection), Fractional Knapsack, Activity Selection, and Huffman coding.
5. `tests/test_dynamic_programming.py`: 7 tests verifying Binomial DP, Coin Change DP, 0/1 Knapsack DP, Floyd-Warshall, Matrix Chain Multiplication, LCS, and Greedy vs DP comparisons.
6. `tests/test_graph_algorithms.py`: 3 tests covering BFS, DFS cycle detection, and Kahn's topological sorting on DAGs and cyclic graphs.
7. `tests/test_backtracking_bnb.py`: 7 tests covering N-Queens (4-Queens = 2 solutions, 8-Queens = 92 solutions), Backtracking Knapsack, Hamiltonian cycle detection, Exact TSP, Assignment problem B&B, Knapsack B&B, and Minimax with Alpha-Beta pruning.
8. `tests/test_string_matching.py`: 6 tests covering Naive, Rabin-Karp, KMP matching with overlapping and empty patterns, prefix table computation, and complaint search.
9. `tests/test_route_planner.py`: 4 tests verifying priority scoring formula breakdowns, capacity knapsack selection, baseline/greedy/exact route planners, and comparison metrics.
10. `tests/test_database_and_data.py`: 4 tests validating SQLite CRUD, audit logging, bin schema rules, and Haversine distance calculations.

---

## 10. Limitations
1. **Static Sensor Assumption**: Bin fill percentages and weights are managed through simulated data and operator inputs rather than real-time hardware telemetry.
2. **Offline Network Boundaries**: The road network is currently represented as a bundled municipal graph with 19 nodes; full metropolitan networks with hundreds of thousands of edges require dedicated spatial database indexing.
3. **Single Vehicle Formulation**: The route planner currently models a single collection truck operating sequentially from a central depot, rather than a multi-vehicle fleet (VRP with Multiple Depots).

---

## 11. Future Scope
1. **IoT Sensor Integration**: Connecting ultrasonic fill-level sensors via MQTT or HTTP webhooks to update bin levels dynamically.
2. **Capacitated Multi-Vehicle Routing (CVRP)**: Extending the planner to partition bins across a fleet of trucks with differing capacities using Genetic Algorithms or Ant Colony Optimization.
3. **Live Traffic Incorporation**: Ingesting live traffic congestion data from open routing engines (e.g. OSRM or OpenRouteService) to compute dynamic time-dependent edge weights.

---

## 12. Conclusion
The **Smart Waste Collection Route Optimizer** successfully demonstrates how foundational concepts from Design and Analysis of Algorithms can be applied to solve an authentic municipal logistics challenge. By combining 0/1 Knapsack Dynamic Programming for capacity-constrained subset selection, Dijkstra's algorithm for road distance calculation, and Nearest-Neighbor/Branch-and-Bound algorithms for route optimization, the system achieves measurable reductions in travel distance, fuel consumption, and vehicle emissions. With complete coverage of Units 1 to 8, a comprehensive test suite with 56 passing tests, and an interactive Streamlit user interface, the project provides an exceptional practical and educational demonstration for computer engineering students.
