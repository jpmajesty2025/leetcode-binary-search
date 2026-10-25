# From Interval Heaps to Difference Sweeps: 3 Architectural Patterns (Part 2 of 2) ⚡

In Part 1, we saw how decomposing interval containment into independent start and end counts unlocks an elegant Dual Binary Search.

How does this mathematical approach compare against classic patterns like **Active Min-Heaps** and **Coordinate-Compressed Sweep-Lines**?

Here is a breakdown of the 3 major paradigms!

---

### 1️⃣ Pattern 1: Dual Binary Search (Cumulative Distribution)

- **The Idea:** Sort `starts` and `ends` into two 1D arrays.
- Calculate: $\text{active} = \text{bisect\_right}(\text{starts}, T) - \text{bisect\_left}(\text{ends}, T)$.
- **Advantage:** Preserves query order! Zero visitor sorting or tuple allocations.

---

### 2️⃣ Pattern 2: Active Min-Heap Simulation (Interval Scheduling)

- **The Idea:** Classic pattern from Meeting Rooms II!
  1. Sort flowers by start time.
  2. Sort visitors by arrival: `(time, original_index)`.
  3. Min-heap tracks active flower end times.
  4. For each visitor: push started flowers, pop expired ones, record `len(heap)`.
- **Advantage:** Mirrors physical time progression. Ideal for streaming events.

---

### 3️⃣ Pattern 3: Coordinate-Compressed Difference Array (Sweep-Line)

- **The Idea:**
  1. Sparse difference map: `diff[start] += 1`, `diff[end + 1] -= 1`.
  2. Sort unique timestamps and compute prefix sums.
  3. Binary search with `bisect_right` to find the active bucket.
- **Advantage:** Precomputes a piecewise step function across active spans.

---

### 💥 Benchmark Shootout (50,000 Flowers, 50,000 Visitors)

| Pattern | Core Technique | Runtime | Speedup |
| :--- | :--- | :--- | :--- |
| **Dual Bisect** | Cumulative Decomposition | **49.78 ms** | **2.12x** |
| **Diff Array + Bisect** | Coordinate Compression | 89.87 ms | 1.18x |
| **Min-Heap Simulation** | Active Event Queue | 95.44 ms | 1.11x |
| **Two-Pointer Sweep** | Event Sweep-Line | 105.75 ms | Baseline |

---

### 🔬 Why Dual Bisect Dominates

Why is Dual Bisect **over 2x faster** than Min-Heap and Sweep-Line?

1. **Zero Query Sorting**: Min-Heap and Sweep-Line must allocate and sort $50,000$ tuples `(arrival, original_index)`. Dual Bisect answers visitors in natural order!
2. **C-Speed Execution**: Dual Bisect operates on flat integer arrays inside Python's C-implemented `bisect` with zero heap or dictionary overhead.

---

### 🧪 Verification

Verified with pytest and Hypothesis (19 passing tests):
- Single-day blooms and boundary arrivals.
- Large scale tests ($N = 5,000, M = 5,000$).
- Property fuzzing verifying 100% agreement against brute force.

---

### 🎯 Key Takeaway

Before reaching for heaps or sweep loops, ask: **Can the problem be decomposed into independent cumulative counts?** Mathematical simplification often beats complex algorithmic machinery.

Which pattern is your go-to for interval problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #CodingInterview
