# The Constraint Goldmine: 2D Point Containment (Part 1 of 2) 📐

**The Problem**:
You are given $N$ rectangles with bottom-left corner at $(0, 0)$ and top-right corner at $(l_i, h_i)$.
You are also given $M$ query points $(x_j, y_j)$.
A rectangle contains a point if $x_j \le l_i$ and $y_j \le h_i$.
Return an array where each entry is the number of rectangles containing that point.

Constraints:
$N, M \le 50,000$.
Lengths up to $10^9$.

---

### 🧩 The Brute-Force TLE Trap

Checking each point against all rectangles with nested loops takes **O(N * M)** time:
$50,000 \times 50,000 = \mathbf{2.5 \times 10^9\text{ operations}}$!
That crashes directly into Time Limit Exceeded (TLE) in every language.

Usually, 2D range query problems require complex 2D Segment Trees or KD-Trees.
**Unless there is an asymmetry hidden in the constraints!**

---

### 🔍 The Constraint Goldmine: Height <= 100

Look at the constraints:
- Lengths $l_i, x_j \le 10^9$ (massive, continuous)
- Heights $h_i, y_j \le \mathbf{100}$ (tiny!)

The height coordinate space is strictly bounded between $1$ and $100$!
This asymmetrical constraint transforms an intractable 2D geometry problem into an elegant **Height-Bucketed Binary Search**.

---

### 🔧 The Height-Bucketed Binary Search Algorithm

1. **Bucket by Height**:
   Create 100 buckets (one for each height $1 \dots 100$).
   For each rectangle $(l, h)$, append its length $l$ to `buckets[h]`.
2. **Sort Each Bucket**:
   Sort each bucket's lengths in ascending order.
   Sorting all buckets takes strictly **O(N log N)** total time across the entire dataset.
3. **Query Resolution via Binary Search**:
   For each point $(x, y)$:
   A rectangle contains $(x, y)$ if $h \ge y$ and $l \ge x$.
   Iterate only through valid heights $h \in [y, 100]$ (at most $100$ iterations!).
   For each height $h$, binary search with `bisect_left` to count rectangles with length $\ge x$:
   $\text{count} += \text{len}(buckets[h]) - \text{bisect\_left}(buckets[h], x)$

Total query operations per point: at most $100 \times \log_2(50,000) \approx 1,600$.
For $50,000$ points, the entire search finishes in **502 ms**!

---

### 📊 Complexity

- **Time:** O(N log N + M * H log N) where $H \le 100$
- **Space:** O(N) for storing bucketed lengths

---

### 🎯 Key Takeaway

Always inspect problem constraints for dimensional asymmetry. When one dimension is bounded by a small constant ($H \le 100$), bucketing by that dimension reduces multidimensional geometry to simple 1D binary searches.

In Part 2, we benchmark Height Buckets against an **Offline Sweep-Line + Fenwick Tree** that runs **4.8x faster**!

How often do you check constraints for small dimensions before reaching for complex data structures? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
