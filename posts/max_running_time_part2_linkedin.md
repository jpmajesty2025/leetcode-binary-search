# From Bisect Acceleration to Greedy Reverse Elimination: 31x Faster (Part 2 of 2) ⚡

In Part 1, we formulated LeetCode 2141 using Binary Search on the Answer.
Standard binary search re-scans all batteries on each step, taking $436$ ms in Python.

Here is how **Bisect Acceleration** and **Greedy Reverse Elimination** deliver a **31x speedup**.

---

### 🚀 Optimization 1: Sort + Prefix Sums + Bisect ($O(\log M)$ Predicate)

Instead of linear scanning on each step, sort `batteries` and precalculate prefix sums:
1. `bisect.bisect_left(batteries, T)` finds cutoff index $k$.
2. Batteries to the left are $< T$, contributing `prefix[k]`.
3. Batteries to the right are $\ge T$, contributing $(M - k) \times T$.

Total usable energy:
$$\text{Usable Energy} = prefix[k] + (M - k) \times T$$

Predicate evaluation drops to $O(\log M)$, giving an **18.4x speedup** ($23.7$ ms).

---

### 💡 Optimization 2: Greedy Reverse Elimination ($O(M \log M)$ Solver)

Can we eliminate binary search across runtimes completely?

Sort `batteries` ascending and let $total = \sum batteries$.
If the largest battery has capacity $B > \lfloor total / n \rfloor$:
The average possible runtime cannot exceed $total / n$. Battery $B$ has excess capacity that would be capped, so we dedicate it to power one computer for the full duration:
- $n \leftarrow n - 1$
- $total \leftarrow total - B$

Repeat from largest to smallest.
The moment the largest remaining battery has $B \le \lfloor total / n \rfloor$:
Every remaining battery can be fully consumed without capping.
By McNaughton's theorem, they run the remaining $n$ computers for exactly $\lfloor total / n \rfloor$ minutes.
Return `total // n` immediately in $O(1)$.

---

### 💥 Benchmark Shootout ($M = 100,000$ batteries, $n = 40,000$)

| Implementation | Strategy | Runtime | Speedup |
| :--- | :--- | :--- | :--- |
| Naive Generator BS | $O(M)$ generator scan | 436.21 ms | Baseline |
| Early-Exit BS | $O(M)$ early-exit loop | 177.75 ms | 2.5x |
| **Bisect + Prefix Sums** | $O(\log M)$ bisect lookup | **23.70 ms** | **18.4x** |
| **Greedy Reverse Elimination** | Single sorted pass + pop | **14.03 ms** | **31.1x** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (25 passing tests):
- Extreme cases where $n = \text{len}(batteries)$ and $n = 1$.
- Dominant massive batteries combined with small batteries.
- 64-bit integer values up to $10^9$.
- Property fuzzing over 150 randomized inputs against an independent scheduling oracle.

---

### 🎯 Key Takeaway

When individual capacity constraints cap contributions, check the largest elements. If an element exceeds the collective average, dedicating it eliminates both the element and the machine, collapsing the problem into direct division.

Have you used reverse greedy elimination to bypass a binary search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
