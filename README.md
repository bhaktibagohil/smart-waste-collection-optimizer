# Smart Waste Collection Route Optimizer with Complete DAA Coverage

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/tests-56%20passed-brightgreen.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end, algorithmic decision-support web application and educational laboratory built for third-year Computer Engineering students studying **Design and Analysis of Algorithms (DAA)**.

This project bridges theoretical algorithm engineering with a genuine municipal logistics problem: **Optimizing urban solid waste collection under truck capacity constraints over a weighted road network.**

---

## 🌟 Key Features

### 1. Smart Waste Collection System (Municipal Operations Mode)
- **Two Dedicated Application Areas**: Cleanly separated into **Municipal Operations Mode** for everyday sanitation workers and **Student & Project Details** for academic DAA examination.
- **Home Operations Dashboard**: Real-time operational situational awareness answering: Which bins need attention? Which are overflowing? Today's collection progress? What should the fleet do next?
- **Bin Management (CRUD)**: Create, inspect, update, and delete waste bins with plain language categories (*Overflowing*, *Nearly Full*, *Partly Full*, *Empty/Low*) and strict validation.
- **Transparent Multi-Criteria Priority Ranking**: Deterministic mathematical urgency scoring (NOT a black-box AI model):
  $$\text{Priority Score} = (\text{WasteLevel}\% \times 0.50) + \text{UrgencyPoints} + (\text{DaysElapsed} \times 2.0)$$
- **Road Network Representation**: Models urban street networks as a weighted directed graph (`NetworkX DiGraph`), supporting two-way boulevards, one-way alleys, and non-negative travel distances.
- **Capacity-Aware Bin Selection**: Solves subset selection using **0/1 Knapsack Dynamic Programming** to maximize collected priority points under truck capacity limits (with greedy ratio comparison).
- **Route Planning Engine**:
  - **Baseline Route**: Deterministic input-order collection route starting and ending at the Depot.
  - **Nearest-Neighbor Greedy Heuristic**: Fast polynomial-time approximation for larger instances.
  - **Exact Branch-and-Bound TSP**: Computes the provably optimal tour permutation for small sets ($\le 10$ bins).
  - **Shortest Paths**: Dijkstra's algorithm for traveling between consecutive collection stops.
- **Interactive Visualization**: Folium maps with color-coded urgency markers, waypoint sequence badges, road network overlays, and Matplotlib comparison charts.
- **Data Persistence**: SQLite database (`smart_waste.db`) stores bins, configuration, and audit logs of historical route optimization runs.

### 2. DAA Algorithm Lab (100% Syllabus Coverage)
An interactive educational laboratory covering Units 1 to 8:
- **Unit 1 (Basics & Mathematical Analysis)**: Sets, functions, relations, quantifiers ($\forall, \exists$), vectors, series, loop counter analysis, and amortized analysis of dynamic array table doubling.
- **Unit 2 (Recurrences & Sorting)**: Direct implementations of Bubble Sort, Selection Sort, Insertion Sort, Heap Sort, Counting Sort, Bucket Sort, Master Theorem solver, and recursion trees.
- **Unit 3 (Divide & Conquer)**: Binary Search, Merge Sort, Quick Sort, Max-Min tournament problem, Karatsuba large integer multiplication, and Strassen matrix multiplication.
- **Unit 4 (Greedy Algorithms)**: Greedy coin change (with canonical failure counterexample), Prim's MST, Kruskal's MST (with DSU), Dijkstra, Bellman-Ford (with negative cycle detection), Fractional Knapsack, Activity Selection, and Huffman coding.
- **Unit 5 (Dynamic Programming)**: Binomial coefficient $C(n, k)$, Coin Change DP, 0/1 Knapsack DP, Floyd-Warshall all-pairs shortest paths, Matrix Chain Multiplication, and Longest Common Subsequence (LCS).
- **Unit 6 (Graph Exploration, Backtracking, Branch & Bound)**: BFS, DFS (cycle detection), Kahn's topological sort, N-Queens puzzle, Backtracking Knapsack, Assignment problem (Branch & Bound), and Minimax with Alpha-Beta pruning.
- **Unit 7 (String Matching)**: Naive string matching, Rabin-Karp (rolling hash), Knuth-Morris-Pratt (KMP), and municipal complaint ticket keyword search.
- **Unit 8 (NP-Completeness)**: P vs NP hierarchy, polynomial-time reduction ($\text{Hamiltonian Cycle} \le_P \text{TSP}$), and empirical comparison between Exact TSP and Nearest-Neighbor Greedy heuristic.

---

## 📁 Project Structure

```
Smart-Waste-Collection-Optimizer/
├── app.py                      # Main Streamlit multi-view application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── data/
│   ├── sample_bins.csv         # 18 bundled municipal ward bins
│   └── sample_roads.csv        # Road network topology with distances & one-ways
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite schema, CRUD, and audit history
├── optimizer/
│   ├── __init__.py
│   ├── data_manager.py         # Schema validation, coordinates, graph builder
│   ├── priority.py             # Multi-factor priority scoring formula
│   ├── capacity.py             # Truck capacity validation & 0/1 Knapsack DP
│   ├── route_planner.py        # Baseline, Nearest-Neighbor, and Exact B&B TSP
│   └── route_metrics.py        # Operational metrics, travel time, savings
├── algorithms/
│   ├── __init__.py
│   ├── mathematical_analysis.py # Unit 1: Sets, quantifiers, series, loops, amortized
│   ├── complexity.py            # Unit 1: Asymptotic definitions, empirical profiler
│   ├── sorting.py               # Unit 2: 6 sorting algorithms
│   ├── recurrence_analysis.py   # Unit 2: Master Theorem, substitution, recursion tree
│   ├── divide_and_conquer.py    # Unit 3: Binary search, Merge, Quick, MaxMin, Karatsuba, Strassen
│   ├── greedy.py                # Unit 4: Prim, Kruskal, Dijkstra, Bellman-Ford, Huffman, etc.
│   ├── dynamic_programming.py   # Unit 5: 0/1 Knapsack, Coin Change, Floyd-Warshall, MCM, LCS
│   ├── graph_algorithms.py      # Unit 6: BFS, DFS, Topological sort
│   ├── backtracking.py          # Unit 6 & 8: N-Queens, Hamiltonian cycle, Exact TSP
│   ├── branch_and_bound.py      # Unit 6: Assignment problem, Knapsack B&B, Minimax
│   ├── string_matching.py       # Unit 7: Naive, Rabin-Karp, KMP, complaint search
│   └── np_completeness.py       # Unit 8: P vs NP, polynomial reduction walkthrough
├── visualization/
│   ├── __init__.py
│   ├── maps.py                  # Folium interactive map visualizer
│   └── charts.py                # Matplotlib charts for comparisons & benchmarks
├── tests/
│   ├── test_sorting.py          # Unit tests for sorting
│   ├── test_searching.py        # Unit tests for searching
│   ├── test_divide_and_conquer.py # Unit tests for divide and conquer
│   ├── test_greedy.py           # Unit tests for greedy
│   ├── test_dynamic_programming.py # Unit tests for DP
│   ├── test_graph_algorithms.py # Unit tests for graph traversals
│   ├── test_backtracking_bnb.py # Unit tests for backtracking and B&B
│   ├── test_string_matching.py  # Unit tests for string matching
│   ├── test_route_planner.py    # Unit tests for route optimization & capacity
│   └── test_database_and_data.py # Unit tests for DB and data validation
└── docs/
    ├── PROJECT_REPORT.md        # Comprehensive academic project report
    ├── DAA_SYLLABUS_MAPPING.md  # Detailed syllabus coverage matrix
    ├── VIVA_QUESTIONS.md        # 50+ viva voce examination questions & answers
    └── USER_GUIDE.md            # Operator and examiner instruction manual
```

---

## 🚀 Quickstart & Execution

### 1. Prerequisites
- Python 3.11 or higher installed on your system.
- Git (optional, for cloning).

### 2. Installation
Clone the repository or navigate to the workspace directory:
```bash
cd Smart-Waste-Collection-Optimizer
```

Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Automated Test Suite
Verify all algorithms, data managers, and databases pass tests:
```bash
pytest -v
```
*(All 56 tests will run and pass).*

### 4. Launch the Web Application
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your web browser at `http://localhost:8501`.

---

## 🔬 Design Decisions & Assumptions

1. **Offline Demonstration Mode**:
   - The application does not require internet access, API keys, or cloud routing servers to function.
   - It operates over the bundled `data/sample_roads.csv` graph with known road lengths in kilometers.
2. **Distance Model Clarity**:
   - The system distinguishes between **Road Network Distance** (Dijkstra shortest path over actual streets) and **Haversine Distance** (straight-line Euclidean distance as the crow flies).
3. **Combinatorial Safeguards**:
   - Exact Branch-and-Bound TSP search is restricted to subsets of size $\le 10$ bins. For inputs larger than 10, the application automatically uses the Nearest-Neighbor greedy heuristic to ensure sub-second UI responsiveness.
4. **Transparent Rules vs. AI**:
   - Bin priority ranking is calculated via an explicit, published linear formula rather than a black-box machine learning model.

---

## 📜 Academic Attribution
Developed for Computer Engineering students as a practical mini-project and examination demonstration for the **Design and Analysis of Algorithms (DAA)** curriculum.
