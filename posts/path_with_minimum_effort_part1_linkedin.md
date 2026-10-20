# Minimax Paths: Binary Search + BFS for Minimum Effort (Part 1 of 2) 🏔️

**The Problem**:
You are a hiker traveling from $(0, 0)$ to the bottom-right cell $(m - 1, n - 1)$ in an $m \times n$ grid of heights.
You can move up, down, left, or right.
A route's **effort** is the **maximum absolute difference** between any two consecutive cells along the path.
Find the route requiring the **minimum effort**.

---

### 🧩 Why Standard Shortest Path Fails

In standard shortest path problems, you minimize the **sum** of edge weights ($\sum w_i$).
Here, the objective is **minimax**: minimize the single largest step along the path ($\max w_i$).

Taking twenty steps with an elevation jump of $1$ has an effort of $1$.
Taking a single step with a jump of $5$ has an effort of $5$.
Because total path length doesn't matter—only the bottleneck step does—standard BFS or unweighted pathfinding cannot solve this directly.

---

### 🔧 The Strategy: Binary Search on Answer + BFS

Instead of searching for a route, guess the effort threshold $E$ and test feasibility:
*Can we reach $(m - 1, n - 1)$ using only steps with height difference $\le E$?*

1. **Monotonicity**:
   If a path exists with maximum jump $\le E$, that exact same path remains valid for any threshold $E' > E$.
   The reachability function `can_reach(E)` is strictly monotonic:
   `[False, False, ..., False, True, True, True]`
2. **BFS Reachability**:
   For a candidate effort $E$, run a standard BFS from $(0, 0)$. Only traverse neighboring cells where `abs(heights[nr][nc] - heights[r][c]) <= E`.
   BFS runs in **O(m * n)** time.
3. **Binary Search**:
   Search over the range $[0, \max(\text{heights}) - \min(\text{heights})]$.
   Each iteration halves the effort range.

Total time: **O(m * n * log(max_diff))**.

---

### 🐛 Code Quality & Tight Bounds

1. **Tight Boundary Optimization**:
   Setting `right = max(heights) - min(heights)` rather than `max(heights)` tightens the range.
   On flat plateau grids, `max - min = 0`, allowing the function to return `0` in **O(1)** time without running a single BFS!
2. **Module-Level Imports**:
   Moving `from collections import deque` out of the inner helper function avoids re-import overhead on every binary search iteration.

---

### 📊 Complexity

- **Time:** O(m * n * log(max_diff))
- **Space:** O(m * n) for the BFS visited grid and queue

---

### 🎯 Key Takeaway

When a graph problem defines cost as the **bottleneck edge** rather than the sum of edges, convert optimization into decision: binary search on the answer, and verify reachability with BFS.

In Part 2, we benchmark Binary Search + BFS against modified Dijkstra and Kruskal's MST (Union-Find). The graph algorithms run up to 5.4x faster!

Have you tackled minimax path problems using binary search or priority queues? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #GraphAlgorithms #LeetCode #CodingInterview
