# Comprehensive Viva Voce Questions & Answers Guide

This document prepares students for oral practical examinations (viva voce) on the **Smart Waste Collection Route Optimizer** project and **Design and Analysis of Algorithms (DAA)**.

---

## Category 1: Project Overview & Problem Formulation

### Q1: What is the high-level objective of this project?
**Answer**:  
The project aims to solve the municipal solid waste collection problem by replacing static collection beats with dynamic, algorithmic route planning. It selects bins based on fill level and urgency using 0/1 Knapsack Dynamic Programming under vehicle capacity constraints, calculates road driving distances using Dijkstra's algorithm, and generates optimized tours returning to the depot using Nearest-Neighbor and Branch-and-Bound TSP solvers.

### Q2: Why is waste collection modelled as a Travelling Salesperson Problem (TSP) rather than a simple shortest-path problem?
**Answer**:  
A shortest-path algorithm (such as Dijkstra) finds the minimum distance between a *single origin* and a *single destination*. In contrast, municipal waste collection requires visiting a *subset of multiple locations* and returning to the depot. Finding the order of visitation that minimizes total travel distance is a permutation problem — precisely the formulation of the Travelling Salesperson Problem (TSP).

### Q3: What is the difference between Haversine distance and Road Network distance?
**Answer**:  
- **Haversine Distance**: Calculates the great-circle Euclidean distance between two coordinate points on the surface of a sphere ("as the crow flies"). It ignores roads, obstacles, and terrain.
- **Road Network Distance**: The shortest path traversing actual physical streets, intersections, and one-way restrictions on a weighted road graph. Real driving distance is always greater than or equal to Haversine distance.

### Q4: How is bin collection priority calculated? Is it an AI model?
**Answer**:  
No, it is **not an AI model**. It is an explicit, transparent, and deterministic mathematical scoring formula:
$$\text{Priority Score} = (\text{WasteLevel}\% \times 0.50) + \text{UrgencyPoints} + (\text{DaysElapsed} \times 2.0)$$
Where Critical = 80 pts, High = 45 pts, Medium = 20 pts, and Low = 5 pts. This ensures transparency, reproducibility, and auditability without black-box machine learning dependencies.

---

## Category 2: Complexity & Mathematical Analysis (Unit 1)

### Q5: Define Big-O, Big-$\Omega$, and Big-$\Theta$ notations.
**Answer**:  
- **Big-O ($O$)**: Asymptotic upper bound. $f(n) \le c \cdot g(n)$ for all $n \ge n_0$. Represents the worst-case growth rate guarantee.
- **Big-Omega ($\Omega$)**: Asymptotic lower bound. $f(n) \ge c \cdot g(n)$ for all $n \ge n_0$. Represents the best-case growth rate guarantee.
- **Big-Theta ($\Theta$)**: Asymptotically tight bound. $c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$ for all $n \ge n_0$. The function is sandwiched between two constant multiples of $g(n)$.

### Q6: Can a single timing measurement prove an asymptotic complexity bound?
**Answer**:  
**No.** Wall-clock execution time is influenced by hardware architecture, operating system background processes, memory caching, and interpreter overhead. Asymptotic complexity ($O, \Theta$) is a mathematical property describing the growth rate of abstract operations as input size $n \to \infty$. Empirical timings can suggest or support theoretical expectations, but cannot prove an asymptotic bound.

### Q7: Explain Amortized Analysis and how Dynamic Array table doubling achieves $O(1)$ amortized cost.
**Answer**:  
Amortized analysis averages the running time of a sequence of operations over all operations in the sequence, ensuring that an occasional expensive operation is paid for by preceding cheap operations.  
When an array of capacity $N$ doubles to $2N$ upon filling:
- The resizing operation copies $N$ elements, taking $O(N)$ work.
- However, this resize occurs only after $N$ cheap $O(1)$ insertions have taken place.
- Using the **Aggregate Method**, the total cost for inserting $N$ elements is at most $N + \sum 2^i \le 3N$. Dividing by $N$ operations yields an amortized cost of $\le 3$ operations per append, which is $O(1)$ amortized time.

---

## Category 3: Recurrences & Sorting (Unit 2)

### Q8: What is the Master Theorem and what are its three cases?
**Answer**:  
The Master Theorem provides a cookbook solution for divide-and-conquer recurrences of the form:
$$T(n) = a \cdot T(n/b) + \Theta(n^d)$$
where $a \ge 1, b > 1, d \ge 0$. We compare $d$ with $\log_b a$:
1. **Case 1 ($d < \log_b a$)**: Work at leaves dominates $\implies T(n) = \Theta(n^{\log_b a})$.
2. **Case 2 ($d = \log_b a$)**: Work is evenly distributed across all tree levels $\implies T(n) = \Theta(n^d \log n)$.
3. **Case 3 ($d > \log_b a$)**: Work at the root dominates $\implies T(n) = \Theta(n^d)$ (provided regularity condition $a(n/b)^d \le c n^d$ holds for $c < 1$).

### Q9: Name one scenario where the Master Theorem cannot be applied.
**Answer**:  
The Master Theorem cannot be applied if:
1. $a < 1$ or $b \le 1$.
2. The subproblem size does not shrink by a constant factor (e.g. $T(n) = T(n-1) + n$).
3. The driving function $f(n)$ is not polynomial (e.g. $T(n) = 2T(n/2) + 2^n$ or $T(n) = 2T(n/2) + n \log n$).
4. The gap between $f(n)$ and $n^{\log_b a}$ is non-polynomial (e.g. $f(n) = n^{\log_b a} / \log n$).

### Q10: Compare Merge Sort, Quick Sort, and Heap Sort in terms of time and space complexity.
**Answer**:  
| Algorithm | Best Time | Average Time | Worst Time | Auxiliary Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | **Yes** |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ call stack | **No** |
| **Heap Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ in-place | **No** |

### Q11: What is the difference between Comparison Sorts and Non-Comparison Sorts?
**Answer**:  
- **Comparison Sorts** (e.g. Merge Sort, Quick Sort, Heap Sort) determine relative order by comparing elements against each other. Their theoretical lower bound is $\Omega(n \log n)$ comparisons.
- **Non-Comparison Sorts** (e.g. Counting Sort, Bucket Sort) use keys as indices or direct distributions. Counting Sort achieves $O(n + k)$ linear time by assuming keys are bounded integers in $[0, k]$.

---

## Category 4: Divide and Conquer (Unit 3)

### Q12: How does the Max-Min Divide-and-Conquer algorithm save comparisons over a naive linear scan?
**Answer**:  
- A naive linear scan finds the minimum in $n - 1$ comparisons and the maximum in another $n - 1$ comparisons, totaling $2n - 2$ comparisons.
- The divide-and-conquer tournament approach splits the array into two halves, recursively finds the min and max of each half, and combines them using 2 comparisons.
- Solving the recurrence $T(n) = 2T(n/2) + 2$ yields exactly $\lceil 3n/2 \rceil - 2$ comparisons, saving approximately $25\%$ of key comparisons.

### Q13: How does Karatsuba's algorithm multiply large integers faster than standard grade-school multiplication?
**Answer**:  
Standard multiplication divides two $n$-digit numbers into high and low halves and computes 4 sub-products: $z_2 = x_1 y_1$, $z_1 = x_1 y_0 + x_0 y_1$, and $z_0 = x_0 y_0$, resulting in $T(n) = 4T(n/2) + O(n) \implies O(n^2)$.  
Karatsuba computes only 3 multiplications: $z_0 = x_0 y_0$, $z_2 = x_1 y_1$, and $z_{mid} = (x_0 + x_1)(y_0 + y_1)$.  
Then $z_1 = z_{mid} - z_2 - z_0$.  
By Master Theorem: $T(n) = 3T(n/2) + O(n) \implies O(n^{\log_2 3}) \approx O(n^{1.585})$.

---

## Category 5: Greedy vs. Dynamic Programming (Units 4 & 5)

### Q14: What is the fundamental difference between the Greedy Approach and Dynamic Programming?
**Answer**:  
- **Greedy Method**: Makes the locally optimal choice at each step without ever reconsidering past choices or looking ahead at future subproblems. It works only when the problem exhibits the *Greedy Choice Property* and *Optimal Substructure*.
- **Dynamic Programming**: Solves overlapping subproblems systematically, stores their solutions in a table (memoization/tabulation), and guarantees global optimality by exploring all potential state transitions.

### Q15: Give a concrete counterexample where Greedy Coin Change fails, but DP succeeds.
**Answer**:  
- **Coin Denominations**: $\{1, 3, 4\}$
- **Target Amount**: $6$
- **Greedy Solution**: Greedily picks the largest coin $4$ first, leaving $2$. Then picks two $1$s. Total: $4 + 1 + 1$ (**3 coins**).
- **DP Solution**: Evaluates subproblems and finds $3 + 3 = 6$ (**2 coins**).  
This demonstrates that greedy local decisions fail on non-canonical currency systems.

### Q16: How do Fractional Knapsack and 0/1 Knapsack differ in algorithmic strategy?
**Answer**:  
- **Fractional Knapsack**: Items can be broken into fractional portions. Solved optimally using a **Greedy Algorithm** by sorting items by value-to-weight ratio $v_i / w_i$ descending in $O(n \log n)$ time.
- **0/1 Knapsack**: Items are discrete; each item must be taken whole ($1$) or left ($0$). Greedy ratio sorting fails because choosing a high-ratio heavy item may block a better combination of lighter items. Must be solved using **Dynamic Programming** in $O(n \cdot W)$ pseudo-polynomial time.

### Q17: Compare Prim's and Kruskal's algorithms for Minimum Spanning Trees (MST).
**Answer**:  
- **Prim's Algorithm**: Grows a single tree outward from an arbitrary start vertex by adding the minimum-weight incident edge using a min-heap priority queue. Time: $O(E \log V)$. Preferred for **dense graphs** ($E \approx V^2$).
- **Kruskal's Algorithm**: Sorts all edges globally by weight and adds edges that do not form cycles using a Disjoint Set Union (Union-Find) data structure. Time: $O(E \log E)$. Preferred for **sparse graphs** ($E \ll V^2$).

### Q18: Why can't Dijkstra's algorithm handle negative edge weights? Which algorithm can?
**Answer**:  
Dijkstra's algorithm assumes that once a vertex is extracted from the min-heap priority queue, its shortest distance is finalized and will never decrease (greedy choice property). Negative edge weights can create shorter paths through already-settled vertices, causing Dijkstra to produce incorrect distances.  
**Bellman-Ford algorithm** handles negative edge weights and detects negative-weight cycles by relaxing all edges $V - 1$ times in $O(V \cdot E)$ time.

---

## Category 6: Backtracking & Branch and Bound (Unit 6)

### Q19: What is the difference between Backtracking and Branch and Bound?
**Answer**:  
- **Backtracking**: Employs **Depth-First Search (DFS)** to explore a state-space tree. Used primarily for decision, constraint satisfaction, and enumeration problems (e.g. N-Queens, Hamiltonian Cycle). If a partial solution violates constraints, it immediately backtracks.
- **Branch and Bound**: Employs **Breadth-First Search (BFS)** or **Best-First Search (Least-Cost Search)** using a priority queue. Used exclusively for **optimization problems** (minimization/maximization). It computes mathematical lower/upper bounds at each node to prune entire subtrees that cannot beat the best solution found so far.

### Q20: How does Alpha-Beta pruning improve the Minimax algorithm?
**Answer**:  
Alpha-Beta pruning maintains two bounds during minimax game tree search:
- $\alpha$: The minimum score that the maximizing player is assured of.
- $\beta$: The maximum score that the minimizing player is assured of.
If at any node $\beta \le \alpha$, the opponent would never allow this state to be reached, so remaining sibling branches are pruned without evaluation, reducing the effective branching factor from $b$ to $\approx \sqrt{b}$ in optimal move ordering.

---

## Category 7: String Matching (Unit 7)

### Q21: How does the Knuth-Morris-Pratt (KMP) algorithm achieve $O(n + m)$ guaranteed linear time?
**Answer**:  
Naive matching backtracks the text pointer upon a mismatch, taking worst-case $O((n - m + 1)m)$.  
KMP preprocesses the pattern in $O(m)$ to build a prefix failure table $\pi$ (the longest proper prefix that is also a suffix). When a character mismatch occurs after matching $q$ characters, KMP uses $\pi[q-1]$ to slide the pattern without rolling back the text pointer. The text pointer advances monotonically from $0$ to $n-1$, guaranteeing $O(n + m)$ runtime.

### Q22: What is a spurious hit in the Rabin-Karp algorithm?
**Answer**:  
In Rabin-Karp, substring hashes are computed modulo a prime number $q$. A **spurious hit** occurs when the numerical hash value of the current text window matches the pattern hash ($hash(text) \equiv hash(pattern) \pmod q$), but the actual characters differ. Rabin-Karp resolves this by verifying the characters individually whenever a hash match occurs.

---

## Category 8: NP-Completeness & TSP (Unit 8)

### Q23: Explain the classes P, NP, NP-Complete, and NP-Hard.
**Answer**:  
- **P**: Problems solvable in polynomial time $O(n^k)$ by a deterministic Turing machine.
- **NP**: Decision problems whose positive solutions can be **verified** in polynomial time given a certificate.
- **NP-Complete**: The hardest problems in NP. A problem $X$ is NP-complete if $X \in NP$ and every problem $Y \in NP$ is polynomial-time reducible to $X$ ($Y \le_P X$).
- **NP-Hard**: Problems at least as hard as any problem in NP ($Y \le_P H$ for all $Y \in NP$). An NP-hard problem does not need to be in NP (e.g. optimization problems or the Halting Problem).

### Q24: How is Hamiltonian Cycle reduced to the Travelling Salesperson Problem (TSP)?
**Answer**:  
Given an unweighted graph $G = (V, E)$ for Hamiltonian Cycle, we construct a complete weighted graph $G' = (V, E')$ for TSP:
1. For each pair $(u, v)$, if $(u, v) \in E$, assign edge weight $w(u, v) = 1$.
2. If $(u, v) \notin E$, assign edge weight $w(u, v) = 2$.
3. Set the TSP cost budget $k = |V|$.  
$G$ has a Hamiltonian cycle if and only if $G'$ has a TSP tour of cost $\le |V|$. The transformation takes $O(V^2)$ polynomial time, proving Decision TSP is NP-Complete.

### Q25: Why is the exact TSP solver restricted to $N \le 10$ bins in this application?
**Answer**:  
For $N$ locations, the number of possible round-trip tours is $(N - 1)! / 2$.
- For $N = 10$, $(10 - 1)! / 2 = 9! / 2 = 181,440$ tours, which Branch-and-Bound evaluates in a few milliseconds.
- For $N = 20$, $19! / 2 \approx 6.08 \times 10^{16}$ tours. At 1 billion operations per second, exact evaluation would take **over 1.9 years**.  
To keep the application responsive, instances with $N > 10$ automatically fall back to the Nearest-Neighbor greedy heuristic ($O(N^2)$).
