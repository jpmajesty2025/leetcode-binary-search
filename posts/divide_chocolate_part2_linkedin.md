# Linear Greedy vs. Prefix Jumps: The 23x Speedup (Part 2 of 2) ⚡

In Part 1, we analyzed the Maximin Binary Search pattern for Divide Chocolate.

Here we benchmark three implementations:
1. **Standard Linear Greedy**: Scans the array chunk by chunk on every binary search pass.
2. **Prefix-Sum Binary Jump**: Precomputes prefix sums and uses `bisect_left` to jump to cut points.
3. **Standard Library `bisect`**: Python 3.10+ `bisect.bisect_left` with an inverted feasibility key.

---

### 💥 The Benchmark (Execution Time on 50,000 Chunks)

| Workload | Linear Greedy | Prefix Jump | Standard Bisect |
| :--- | :--- | :--- | :--- |
| 50k chunks, $k = 3$ | 55.90 ms | **2.18 ms** (23x faster!) | 47.97 ms |
| 50k chunks, $k = 500$ | 51.08 ms | 40.23 ms | 48.50 ms |
| 50k chunks, $k = 0$ | 59.39 ms | **0.31 ms** (188x faster!) | **0.31 ms** |

---

### 🔍 What the Numbers Really Say

1️⃣ **Prefix Jumping is 23x faster when $k \ll n$**:
When $k = 3$, scanning all $50,000$ elements across 16 binary search steps requires $\approx 800,000$ loop operations.
Instead:
- Precompute prefix sums once in $O(n)$.
- To find the next cut, search `bisect_left(prefix_sums, curr_offset + target)`.
- Verification takes strictly **O(k log n)** time!
$4 \times \log_2(50,000) \approx 64$ operations per check. Across 16 iterations, that's just $\approx 1,000$ operations! Runtime plummets from **55.9 ms down to 2.18 ms**!

2️⃣ **The $k = 0$ shortcut is 188x faster**:
Recognizing that $0$ cuts means keeping the entire bar lets us return `sum(sweetness)` in **0.31 ms vs 59.39 ms**, eliminating the binary search loop entirely.

3️⃣ **Declarative `bisect` with Inverted Predicates**:
Standard `bisect_left` looks for the first `True`.
Because feasibility transitions from `True` to `False`, inverting the predicate to `cannot_divide(target)` creates a monotonic `False -> True` function, finding the maximal answer cleanly.

---

### 🧪 Verification

Verified with pytest and Hypothesis (44 passed tests):
- **Deterministic Cases**: LeetCode examples, $k = 0$, $k + 1 = n$, single chunks, identical pieces, and values up to $10^5$.
- **Maximin Invariants**:
  - Can achieve at least $k + 1$ pieces with sweetness $\ge w$.
  - Cannot achieve $k + 1$ pieces with sweetness $\ge w + 1$.
  - Sweetness $w$ respects $\min(\text{sweetness}) \le w \le \lfloor \sum / (k + 1) \rfloor$.
- **Zero Mutation**: Caller inputs remain untouched.
- **100% Agreement**: All variants return identical answers across hundreds of test cases.

---

### 🎯 Key Takeaway

Algorithmic innovation lives inside the inner feasibility check.
When partition counts are small ($k \ll n$), switching from a linear $O(n)$ greedy scan to $O(k \log n)$ prefix binary jumping yields an order-of-magnitude leap in performance.

Have you ever used binary jumping on prefix sums to accelerate a greedy check? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Benchmarking #LeetCode #CodingInterview
