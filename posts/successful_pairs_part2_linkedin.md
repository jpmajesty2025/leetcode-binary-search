# Manual Search vs. Bisect vs. Counting: 11x Faster Pairs (Part 2 of 2) ⚡

In Part 1, we solved Successful Pairs of Spells and Potions using binary search with ceiling division.

I benchmarked four distinct implementations:
1. **Manual Binary Search**: Non-mutating `while` loop with precomputed thresholds.
2. **Standard Library `bisect`**: Python's C-implemented `bisect_left` in a list comprehension.
3. **Monotonic Two-Pointer**: Dual sort; as spell strength grows, the potion pointer only moves left.
4. **Suffix Frequency Array**: Suffix sums over bounded potion values for O(1) queries.

---

### 💥 The Benchmark (Milliseconds)

| Workload | Manual BS | Bisect (`bisect_left`) | Two-Pointer | Suffix Bucket |
| :--- | :--- | :--- | :--- | :--- |
| 100k × 100k (LC Max) | 238.8 ms | 55.0 ms | 99.7 ms | **26.0 ms** |
| 100k spells × 1k potions | 113.5 ms | **19.7 ms** | 65.0 ms | 23.7 ms |
| 1k spells × 100k potions | 17.8 ms | **14.9 ms** | 20.8 ms | 15.4 ms |
| 50k × 50k (Already Sorted) | 95.9 ms | 13.1 ms | 13.4 ms | **12.7 ms** |

---

### 🔍 What the Numbers Really Say

1️⃣ **`bisect_left` in C is 4x to 6x faster than a Python loop**:
Both share O((m + n) log m) complexity, but `bisect_left` runs at C-speed, cutting out Python bytecode interpretation overhead.

2️⃣ **Suffix Frequency Array is the overall speed champion**:
At 100k × 100k, it finishes in **26 ms—11x faster** than the original code!
Because potion values are bounded ($K \le 100,000$), building a suffix array in O(m + K) allows each spell to query in **O(1)** time.
Trade-off: Requires O(K) memory, ideal for bounded values but impractical for sparse, massive numbers.

3️⃣ **Two-Pointer pays a sorting tax on spells**:
Two-pointer sorts both arrays: O(m log m + n log n). On random inputs, sorting `spells` adds cost.
When inputs arrive pre-sorted, its linear O(m + n) scan is blazingly fast (13.4 ms).

4️⃣ **General vs. Domain-Specific**:
`bisect_left` is the best general-purpose choice (handles huge numbers with O(m) space). Suffix counting is the domain-specific winner when values fit in RAM.

---

### 🧪 Verification

Verified with pytest and Hypothesis (74 passed tests):
- **Brute-Force Oracle**: Matches an exhaustive search on random inputs.
- **Monotonicity**: Stronger spells guarantee at least as many pairs.
- **Bounds**: Output counts are strictly in `[0, m]`.
- **Zero Mutation**: Caller inputs remain untouched.
- **100% Agreement**: All four algorithms return identical results.

---

### 🎯 Key Takeaway

Complexity sets the limits; runtime details and constraints reveal the fastest path.
For unbounded ranges, use standard library C routines (`bisect`). For bounded integer ranges, trading a small frequency array for O(1) lookups yields an order-of-magnitude speedup.

When do you prefer frequency arrays over binary search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Benchmarking #LeetCode #CodingInterview
