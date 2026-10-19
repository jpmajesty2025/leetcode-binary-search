# Virtual 1D vs. Two-Pass vs. Bisect: The 2D Matrix Shootout (Part 2 of 2) ⚡

In Part 1, we solved Search a 2D Matrix by treating the grid as a virtual 1D sorted array using coordinate translation (`mid // n`, `mid % n`).

I benchmarked three distinct implementations:
1. **Virtual 1D**: Single binary search over `m * n` with coordinate math.
2. **Two-Pass Binary Search**: Binary search row bounds, then binary search within that row.
3. **Standard Library `bisect`**: Two-pass search pairing `bisect_right` on row starts with C-speed `bisect_left` on the row.

All three share the same asymptotic complexity: **O(log(m * n))** time and **O(1)** auxiliary space.

---

### 💥 The Benchmark (Average Time per Lookup)

| Workload | Virtual 1D | Two-Pass | Bisect (2-Pass) |
| :--- | :--- | :--- | :--- |
| 100 × 100 (Hit middle) | 1.78 µs | **1.14 µs** | 1.19 µs |
| 100 × 100 (Out-of-bounds) | 1.61 µs | **0.12 µs** | 0.13 µs |
| 1,000 × 1,000 (Hit) | 2.80 µs | 2.20 µs | **1.73 µs** |
| 1,000 × 1,000 (Miss inside) | 2.57 µs | **0.11 µs** | 0.13 µs |
| 10,000 × 10 (Tall, hit) | **1.92 µs** | 2.20 µs | 2.29 µs |
| 10 × 10,000 (Wide, hit) | 2.00 µs | 1.60 µs | **1.00 µs** |

---

### 🔍 What the Numbers Really Say

1️⃣ **Two-Pass beats Virtual 1D on square and wide matrices**:
In Virtual 1D, every step computes `mid // n`, `mid % n`, and performs a 2D lookup.
In Two-Pass, once the row is found, Pass 2 operates on a single contiguous row: **zero division, zero modulo**, and contiguous memory access.

2️⃣ **Standard library `bisect` in C is blazing fast**:
On wide matrices ($10 \times 10,000$), `bisect` runs the row search in optimized C code: **1.00 µs—2x faster** than Virtual 1D!

3️⃣ **The O(1) bounding guard yields up to 25x speedups**:
Out-of-bounds targets bypass the loop entirely, dropping latency from 2.57 µs down to 0.11 µs.

4️⃣ **Virtual 1D holds an edge on tall matrices**:
When $m \gg n$ ($10,000 \times 10$), Virtual 1D avoids the overhead of managing two separate loops.

---

### 🧪 Verification

Verified with pytest and Hypothesis (136 passed tests):
- **Brute-Force Oracle**: Every implementation matches an exhaustive search on random matrices.
- **Edge Cases**: Verified on $1 \times 1$ grids, single rows, single columns, inter-row gaps, negative numbers, and 32-bit limits.
- **Immutability**: Assertions confirm zero input mutation.
- **100% Agreement**: All variants return identical answers across hundreds of generated test cases.

---

### 🎯 Key Takeaway

Algorithmic complexity tells you how code scales; memory layout and bytecode tell you how it runs.
A single virtual 1D search is mathematically elegant, but separating row selection from column search lets the CPU work with contiguous cache lines and built-in C routines.

Have you benchmarked virtual indexing against two-pass searches? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Benchmarking #LeetCode #CodingInterview
