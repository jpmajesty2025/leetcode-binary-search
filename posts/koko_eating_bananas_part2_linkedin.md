# Float Division vs. Pure Integer Math: Optimizing Koko (Part 2 of 2) ⚡

In Part 1, we established the Binary Search on Answer pattern for Koko Eating Bananas.

I benchmarked three distinct implementations:
1. **Standard `math.ceil`**: Traditional `sum(math.ceil(p / mid) for p in piles)`.
2. **Pure Integer Math + Early Exit**: Replaces float division with `(p + mid - 1) // mid` and breaks early when `total_hours > h`.
3. **Standard Library `bisect`**: Python 3.10+ `bisect.bisect_left` over a virtual `range(left, right + 1)` with a boolean feasibility key.

---

### 💥 The Benchmark (10,000 Piles, Values up to 10^9)

| Scenario | Standard (`math.ceil`) | Integer Math + Break | Bisect (`bisect_left`) |
| :--- | :--- | :--- | :--- |
| $N = 10,000, h = 20,000$ (Loose) | 25.65 ms | 33.93 ms | 26.33 ms |
| $N = 10,000, h = 10,000$ ($h = n$) | 25.36 ms | **0.11 ms** | **0.11 ms** |

---

### 🔍 What the Numbers Really Say

1️⃣ **The $h = n$ boundary check delivers a 225x speedup**:
When available hours equal the number of piles, Koko has exactly 1 hour per pile. She must finish the largest pile in 1 hour: $k = \max(\text{piles})$.
Skipping binary search drops latency from **25.36 ms down to 0.11 ms**.

2️⃣ **Float vs. Integer Ceiling Division**:
`math.ceil(p / mid)` is written in C and runs slightly faster in CPython than the Python bytecode required for `(p + mid - 1) // mid`.
However, float division is bound by 53-bit IEEE 754 precision ($\approx 9 \times 10^{15}$). In statically typed languages (C++, Java, Rust), or with huge 64-bit numbers, pure integer ceiling division is essential to avoid precision loss.

3️⃣ **`bisect` on a Virtual Range in Python 3.10+**:
`bisect.bisect_left(range(left, right + 1), True, key=can_finish)` matches manual loop performance (~26 ms) while writing declarative, idiomatic code with zero off-by-one pointer risk.

---

### 🧪 Verification

Verified with pytest and Hypothesis (56 passed tests):
- **Brute-Force Oracle**: Every implementation matches an independent linear search on random inputs.
- **Optimality Invariants**:
  - Speed $k$ finishes in $\le h$ hours.
  - Speed $k - 1$ strictly fails ($> h$ hours).
  - $k$ respects the theoretical lower bound: $k \ge \lceil \sum \text{piles} / h \rceil$.
- **Zero Mutation**: Assertions confirm `piles` remains untouched.
- **100% Agreement**: All variants produce identical results across hundreds of test cases.

---

### 🎯 Key Takeaway

For binary search on answer, algorithmic boundaries matter just as much as loop logic.
A tight theoretical lower bound and an $O(1)$ fast-path for $h = n$ eliminate iterations before the loop even starts. And in modern Python, `bisect` with a `key` function turns custom binary search into clean standard library code.

Do you prefer `math.ceil` or integer ceiling arithmetic in Python? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Benchmarking #LeetCode #CodingInterview
