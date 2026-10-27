# Bisect Acceleration & Direct Mathematical Greedy (Part 2 of 2) ⚡

In Part 1, we solved LeetCode 1300 with Binary Search on the Answer and fixed the zero-bound bug.

The standard binary search runs in $O(N \log(\max(arr)))$ time, running an $O(N)$ loop on each iteration to sum mutated elements.
Can we optimize this predicate or bypass the search loop entirely?

Here is how **Bisect Acceleration** and **Direct Mathematical Greedy** deliver a **17x speedup**.

---

### 🚀 Optimization 1: Sort + Prefix Sums + Bisect ($O(\log N)$ Predicate)

Instead of scanning unsorted elements in $O(N)$ on every step, sort `arr` and precompute prefix sums:
1. `bisect.bisect_right(arr, limit)` finds cutoff index $k$.
2. Elements to the left are $\le limit$, contributing `prefix[k]`.
3. Elements to the right are $> limit$, contributing $(N - k) \times limit$.

Total sum computation becomes:
$$\text{mutated\_sum} = prefix[k] + (N - k) \times limit$$

Predicate cost drops from $O(N)$ to $O(\log N)$, giving an immediate **13.5x speedup**.

---

### 💡 Optimization 2: Direct Mathematical Greedy ($O(N \log N)$ Solver)

Can we skip binary search over values entirely?

Sort `arr` in ascending order and track the running prefix sum.
At index $i$, test if capping all remaining $k = N - i$ elements at $arr[i]$ reaches `target`.
If $prefix + arr[i] \times k \ge \text{target}$, the optimal cutoff lies in $[arr[i-1], arr[i]]$.

We need:
$$v \times k \approx \text{target} - prefix$$

With $R = \text{target} - prefix$, the answer is either $q = \lfloor R / k \rfloor$ or $q + 1$.
- Error for $q$: $R - q \cdot k$
- Error for $q + 1$: $(q + 1) \cdot k - R$

Pick $q + 1$ only if its error is strictly smaller; otherwise pick $q$.
This solves the exact cutoff in $O(1)$ without any binary search iterations.

---

### 💥 Benchmark Shootout ($N = 10,000$, $\max = 100,000$)

| Implementation | Strategy | Runtime | Speedup |
| :--- | :--- | :--- | :--- |
| Standard Binary Search | $O(N)$ predicate scan | 25.66 ms | Baseline |
| **Bisect + Prefix Sums** | $O(\log N)$ predicate via bisect | **1.90 ms** | **13.5x** |
| **Direct Mathematical Greedy** | Single sorted pass + division | **1.48 ms** | **17.3x** |

---

### 🧪 Verification

Verified with pytest and Hypothesis (25 passing tests):
- Small target zero-bound edge cases where answer is $0$.
- Tie-breaking where lower integer wins.
- Array sums matching or exceeding target.
- Property fuzzing across 250 randomized inputs against an exhaustive oracle.

---

### 🎯 Key Takeaway

Binary search on the answer is a solid default. But sorting the data often uncovers structure that enables logarithmic lookups or direct closed-form division that bypasses the search entirely.

Have you replaced a binary search with a direct mathematical cutoff before? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
