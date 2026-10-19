# Flatten Without Flattening: The Virtual 1D Binary Search (Part 1 of 2) 🔍

**The Problem**:
You are given an `m x n` integer matrix with two strict rules:
1. Each row is sorted in non-decreasing order.
2. The first integer of each row is strictly greater than the last integer of the previous row.

Given a target integer, return whether it exists in the matrix.
The catch? Your algorithm must run in strictly **O(log(m * n))** time.

---

### 🧩 Why Linear & Staircase Searches Fall Short

- A full scan inspects up to $m \times n$ items: **O(m * n)**.
- A staircase search (stepping from top-right down or left) runs in **O(m + n)**. That is optimal for the scenario where rows and columns are sorted independently.
- But this problem guarantees that row transitions are strictly sorted.
- On a $1,000 \times 1,000$ matrix, $m + n = 2,000$ steps, while $\log_2(m \cdot n) \approx 20$ comparisons. $O(m + n)$ leaves massive performance on the table!

---

### 🔧 The Virtual 1D Array Insight

Because the end of row $i$ is smaller than the start of row $i+1$, the entire matrix behaves as a single sorted array of length $N = m \times n$.

No need to flatten the matrix in memory—that wastes O(m * n) time and space.
Instead, flatten **the coordinate math**:

1. Treat the search space as indices from `0` to `m * n - 1`.
2. Compute `mid = (left + right) // 2`.
3. Map `mid` back to matrix coordinates in O(1):
   - `row = mid // n`
   - `col = mid % n`
4. Compare `matrix[row][col]` to target and adjust `left` or `right`.

---

### 🧠 Why the Coordinate Mapping Works

Think of base-$n$ arithmetic:
- Every row has exactly $n$ elements.
- The index `mid` represents the number of elements preceding it.
- Integer division `mid // n` gives how many full rows fit before `mid` (the row).
- Modulo `mid % n` gives the remaining offset into that row (the column).

Monotonicity is preserved across the entire virtual array, making binary search 100% sound.

---

### 🐛 Quality Optimization: O(1) Bounding Guard

Before entering the loop, check the outer bounds:
If `target < matrix[0][0]` or `target > matrix[-1][-1]`, return `False` immediately.
This rejects out-of-range queries in sub-microsecond time.

---

### 📊 Complexity

- **Time:** O(log(m * n)) = O(log m + log n), halving search space each step
- **Space:** O(1) auxiliary space, storing only integer pointers

---

### 🎯 Key Takeaway

When multidimensional data has a global monotonic order, don't reshape data—reshape your index mapping.

In Part 2, we benchmark this against Two-Pass Binary Search and Python's `bisect`. The numbers reveal unexpected cache and bytecode trade-offs!

Do you prefer virtual 1D indexing or a two-pass row-then-column search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #CodingInterview
