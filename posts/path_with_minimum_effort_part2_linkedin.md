# Binary Search vs. Dijkstra vs. Kruskal: Up to 5.4x Faster (Part 2 of 2) ⚡

In Part 1, we solved Path With Minimum Effort using Binary Search on Answer + BFS.

I benchmarked three distinct algorithmic paradigms:
1. **Binary Search + BFS**: Guess bottleneck effort, verify reachability via queue.
2. **Modified Dijkstra**: Minimax relaxation using a min-heap priority queue; returns the instant the destination is popped.
3. **Kruskal's MST (Union-Find)**: Sort all grid edges; add them until $(0, 0)$ and $(m - 1, n - 1)$ connect.

---

### 💥 The Benchmark (Execution Time in Milliseconds)

| Workload | BS + BFS | Modified Dijkstra | Kruskal (DSU) |
| :--- | :--- | :--- | :--- |
| $100 \times 100$ Random Grid | 92.94 ms | 23.03 ms | **17.24 ms** |
| $100 \times 100$ Smooth Gradient | 42.89 ms | **15.94 ms** | 19.21 ms |
| $50 \times 50$ Plateau (Zero effort) | **0.07 ms** | 4.18 ms | 4.58 ms |

---

### 🔍 What the Numbers Really Say

1️⃣ **Kruskal's algorithm is 5.4x faster on random terrain**:
Sorting all grid edges in $O(E \log E)$ allows Disjoint Set Union (DSU) to connect cells from lowest effort to highest.
On random terrain, a connecting path emerges early, terminating the algorithm before high-effort edges are ever touched!

2️⃣ **Dijkstra dominates on smooth gradients**:
When elevation changes smoothly, Dijkstra's priority queue guides exploration along the lowest-effort contours directly to the destination. It beats BS+BFS by **2.7x**.

3️⃣ **Binary Search pays a multi-pass traversal tax**:
BS+BFS executes $\approx 14$ separate BFS passes on a $100 \times 100$ grid, repeatedly resetting the visited grid and traversing thousands of nodes.
However, on flat plateau grids, its $O(1)$ boundary guard (`max_h - min_h = 0`) wins outright in **0.07 ms**!

---

### 🧪 Verification

Verified with pytest and Hypothesis (46 passed tests):
- **Deterministic Edge Cases**: LeetCode examples, $1 \times 1$ singleton grids, single rows, single columns, flat plateaus, winding paths, and $10^6$ elevation differences.
- **Hypothesis Property Tests**: All three algorithms return 100% identical answers across randomized grids.
- **Bound Guarantees**: Effort is mathematically proven to be $\le \max(\text{heights}) - \min(\text{heights})$.
- **Zero Mutation**: Caller inputs remain untouched.

---

### 🎯 Key Takeaway

Three different perspectives solve the exact same minimax path:
- **Decision problem**: Binary Search + BFS
- **Shortest path**: Modified Dijkstra
- **Spanning tree**: Kruskal's algorithm + Disjoint Set Union

Graph algorithms (Dijkstra and Kruskal) typically beat multi-pass binary search because they inspect edges once and terminate the moment the target is reached.

Which of these three paradigms do you reach for first? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #GraphAlgorithms #Dijkstra #LeetCode #CodingInterview
