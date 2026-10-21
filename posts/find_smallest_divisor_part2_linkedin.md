# Frequency Compression vs. Standard Bisect: Up to 10x Faster Divisors (Part 2 of 2) ⚡

In Part 1, we analyzed Binary Search on Answer for Smallest Divisor.

Here we benchmark three implementations:
1. **Standard Binary Search**: Manual loop with theoretical lower bounds.
2. **Frequency-Compressed Binary Search**: Pre-aggregates duplicate values with `Counter`.
3. **Standard Library `bisect`**: Python 3.10+ `bisect.bisect_left` over a virtual divisor range.

---

### 💥 The Benchmark (Execution Time on 50,000 Elements)

| Workload | Standard BS | Frequency Counter | Standard Bisect |
| :--- | :--- | :--- | :--- |
| 50k nums (2,000 unique values) | 44.45 ms | **4.56 ms** (9.8x faster!) | 45.10 ms |
| 50k nums (Distinct values) | 63.45 ms | 73.09 ms | 72.04 ms |
| 50k nums (Threshold == n) | 67.34 ms | **0.58 ms** (115x faster!) | **0.58 ms** |

---

### 🔍 What the Numbers Really Say

1️⃣ **Frequency Compression delivers a 10x speedup on duplicates**:
In real-world data, values frequently repeat.
Instead of evaluating all $50,000$ numbers across every binary search step, compress `nums` into unique pairs `(value, count)`.
Each check evaluates:
`sum(cnt * ((val + d - 1) // d) for val, cnt in items)`
When unique items $U = 2,000 \ll 50,000$, runtime plummets from **44.45 ms down to 4.56 ms**!

2️⃣ **The `threshold == n` boundary guard is 115x faster**:
Recognizing that $\text{threshold} = n$ requires every element to round to $1$ lets us return `max(nums)` immediately.
It collapses runtime from **67.34 ms down to 0.58 ms**.

3️⃣ **Declarative `bisect` on Virtual Ranges**:
`bisect.bisect_left(range(left, right + 1), True, key=can_achieve)` matches manual loop performance while eliminating pointer updates and off-by-one errors.

4️⃣ **Memory vs. Speed**:
Frequency compression uses $O(U)$ memory. For distinct arrays, building Counter adds slight overhead; for duplicated datasets, it is an overwhelming win.

---

### 🧪 Verification

Verified with pytest and Hypothesis (53 passed tests):
- **Deterministic Cases**: LeetCode examples, threshold equals length, single elements, identical arrays, and values up to $10^6$.
- **Optimality Invariants**:
  - Divisor $d$ achieves sum $\le \text{threshold}$.
  - Divisor $d - 1$ strictly fails ($> \text{threshold}$).
  - $d$ respects theoretical bounds: $\lceil \sum \text{nums} / \text{threshold} \rceil \le d \le \max(\text{nums})$.
- **Zero Mutation**: Caller inputs remain untouched.
- **100% Agreement**: All variants return identical answers across hundreds of test cases.

---

### 🎯 Key Takeaway

Algorithmic scalability is just the beginning. Compressing repeated inputs transforms inner-loop complexity from $O(n)$ to $O(U)$, yielding massive real-world performance gains.

Have you ever used frequency compression to accelerate an inner-loop search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Benchmarking #LeetCode #CodingInterview
