# Operator & Student User Guide

**Smart Waste Collection Route Optimizer & DAA Laboratory**  
A step-by-step practical manual for municipal operators, examiners, and students demonstrating the application.

---

## 1. System Setup & Launch

### 1.1 Prerequisites
Ensure Python 3.11 or higher is installed:
```bash
python --version
```

### 1.2 Installation
Open a terminal (PowerShell, Command Prompt, or bash) in the project root:
```bash
cd Smart-Waste-Collection-Optimizer
pip install -r requirements.txt
```

### 1.3 Running the Automated Test Suite
Before launching the user interface, verify the algorithm library:
```bash
pytest -v
```
You should observe **56 passed tests** in under 5 seconds.

### 1.4 Launching the Application
Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```
The browser will automatically open to `http://localhost:8501`.

---

## 2. Application Architecture: Two Dedicated Areas

The application is cleanly organized into two dedicated areas using a switcher at the top of the sidebar:

### A. 🚛 Waste Collection Management (Municipal Operations - Default Mode)
Designed for everyday municipal workers, route supervisors, and sanitation administrators:
1. **Home Dashboard**: Immediate situational awareness (bins needing attention, overflowing count, today's completion progress, recommended action, and quick map preview).
2. **Manage Waste Bins**: Tabular bin management, plain language fill categories, add/edit forms, CSV backup/restore.
3. **Plan Collection Route**: Guided 4-step workflow (settings, route generation, plain-language results, alternatives comparison).
4. **Collection Map**: Interactive street map with depot base, color-coded markers, and stop sequence badges.
5. **Collection History**: Historical audit trail of saved routes with performance metrics and CSV export.
6. **Reports**: Operational analytics (waste distribution, collection completion donut chart, fleet summary statistics).

### B. 🎓 Student & Project Details (DAA Academic Area)
Designed for examiners, professors, and students evaluating algorithm engineering:
1. **DAA Algorithm Lab**: Interactive runnable workbench for Units 1 to 8.
2. **Algorithm Complexity & Benchmarks**: Live empirical execution timing profiler and Big-O growth curves.
3. **Road Network Graph Inspector**: Graph topology metrics, one-way road segments, and Dijkstra path inspector.
4. **DAA Syllabus Coverage Matrix**: Detailed syllabus alignment table across all 8 units.
5. **Project Academic Report**: Complete documentation report with problem formulation, data models, and methodology.
6. **Viva Preparation Guide**: 25+ high-yield oral examination questions with model answers.

---

## 3. Bin Management Workflow

1. Navigate to **🗑️ Bin Management**.
2. **View & Filter**:
   - Filter bins by urgency level (`Critical`, `High`, `Medium`, `Low`) or collection status (`Pending`, `Collected`).
   - Use the search bar to locate specific areas (e.g. "Hospital" or "BIN-05").
   - Click "Mark as Collected / Pending Toggle" to change status.
3. **Add New Bin**:
   - Switch to the **➕ Add / Edit Bin** tab.
   - Enter a unique Bin ID (e.g. `BIN-19`), location name, coordinates (within Pune municipality, e.g. Lat 18.5200, Lon 73.8550), fill percentage ($0-100\%$), estimated weight (kg), and urgency.
   - Click **Add Bin to System**. The record is validated and written to SQLite.
4. **Priority Scoring**:
   - Switch to the **🎯 Priority Formula Inspector** tab.
   - Inspect the exact mathematical breakdown of each bin's score:
     $$\text{Score} = (\text{WasteLevel}\% \times 0.5) + \text{UrgencyPoints} + (\text{DaysElapsed} \times 2.0)$$
5. **CSV Import / Export & Reset**:
   - Click **Download Bins as CSV** to export the current database.
   - Upload a new CSV file to import custom bins.
   - Click **⚠️ Confirm Reset to Sample Data** to restore the default 18 municipal ward bins.

---

## 4. Road Network & Shortest Paths

1. Navigate to **🗺️ Road Network & Graph**.
2. Inspect the road network graph metrics:
   - 19 vertices (Depot + 18 bins) and directed road connections.
   - Review one-way street segments (e.g. `BIN-02 -> BIN-05` Hospital one-way slip).
3. Use the **Shortest Path Inspector**:
   - Select an Origin node (e.g. `DEPOT`) and a Destination node (e.g. `BIN-11`).
   - The system executes **Dijkstra's Algorithm** and displays the exact driving distance in kilometers along with the sequence of intermediate road nodes.

---

## 5. Route Optimizer Workflow

1. Navigate to **🚛 Route Optimizer**.
2. In the sidebar:
   - Set **Truck Capacity** (default: `1200.0 kg`).
   - Choose **Bin Selection Strategy**:
     - `0/1 Knapsack DP`: Solves integer knapsack DP to maximize total priority score within truck capacity.
     - `Greedy Ratio`: Greedily selects bins sorted by priority-to-weight ratio.
     - `Manual`: Pick specific bins from a multi-select list.
   - Choose **Route Optimization Method**:
     - `Nearest-Neighbor Greedy Heuristic`: Fast polynomial routing.
     - `Exact Branch & Bound TSP`: Provably optimal tour (safeguarded for $\le 10$ bins).
3. Inspect the Dashboard:
   - **Summary Cards**: Bins selected, total waste collected, capacity utilization %, feasibility check.
   - **Comparison Table**: Compares Baseline (deterministic input order) with the Optimized Route.
   - **Savings Indicators**: Distance reduction (km), percentage savings (%), travel time saved (min), and diesel fuel/carbon emissions saved.
   - **Bar Chart**: Visualizes distance, travel time, fuel, and emissions side-by-side.
4. Save & Update:
   - Click **💾 Save Route Plan to History Audit Log** to persist the run to the database.
   - Click **✅ Mark Visited Bins as 'Collected'** to update bin statuses in the database.

---

## 6. Interactive Route Map

1. Navigate to **📍 Interactive Route Map**.
2. Switch between view modes:
   - **Optimized Route**: Displays the polyline tour with numbered waypoint badges ($1, 2, 3 \dots$).
   - **Baseline Route**: Displays the unoptimized tour order.
   - **Bins Only**: Shows only markers without polylines.
3. Click any bin marker on the map to open an informative popup with area name, fill level %, weight, and urgency.

---

## 7. Route History & Reports

1. Navigate to **📊 Route History & Reports**.
2. Review past optimization runs stored in SQLite with timestamps and performance metrics.
3. Click **📥 Export Route History to CSV** to generate a spreadsheet report.
4. Use **🗑️ Clear All Route Run History** to reset the audit trail.

---

## 8. DAA Algorithm Lab

1. Navigate to **🧪 DAA Algorithm Lab**.
2. Choose any syllabus unit from the dropdown:
   - **Unit 1**: Sets, quantifiers, series, loop counter analysis, and dynamic array table doubling simulation.
   - **Unit 2**: Interactive 6-sorting algorithm benchmark (Bubble, Selection, Insertion, Heap, Counting, Bucket) and Master Theorem solver.
   - **Unit 3**: Divide-and-Conquer workbench (Binary search, Max-Min tournament problem, Karatsuba integer multiplication, Strassen matrix multiplication).
   - **Unit 4**: Greedy workbench (Coin change, Prim MST, Kruskal MST, Dijkstra, Bellman-Ford negative cycles, Fractional knapsack, Huffman encoding).
   - **Unit 5**: Dynamic Programming (0/1 Knapsack, Coin change DP with greedy counterexample, Matrix Chain Multiplication, LCS).
   - **Unit 6**: Backtracking and Branch-and-Bound (N-Queens, Backtracking Knapsack, Assignment problem, Minimax with Alpha-Beta pruning).
   - **Unit 7**: String Matching (Naive, Rabin-Karp, KMP comparison, municipal complaint ticket search).
   - **Unit 8**: NP-Completeness (P vs NP hierarchy, polynomial reduction walkthrough, exact TSP vs greedy comparison).

---

## 9. Troubleshooting & FAQ

- **Q: What if port 8501 is already in use?**  
  Run Streamlit on an alternate port:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Q: Are live GPS sensors or external internet needed?**  
  No. The application is completely self-contained and runs in **Offline Demonstration Mode** using bundled local CSV datasets.
- **Q: What if I accidentally delete bins?**  
  Go to **🗑️ Bin Management** ➔ **💾 CSV Import / Export / Reset** ➔ Click **⚠️ Confirm Reset to Sample Data**.
