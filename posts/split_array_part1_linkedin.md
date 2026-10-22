# Minimax Binary Search: Mastering Split Array Largest Sum (Part 1 of 2) ⚖️

**The Problem**:
Given an integer array `nums` and an integer $k$, split `nums` into $k$ contiguous, non-empty subarrays such that the **largest sum among them is minimized**.
Return that minimized largest sum.

---

### 🧩 Why Dynamic Programming is Overkill

A classic DP state $dp[i][j]$ (splitting prefix of length $i$ into $j$ subarrays) takes **O(k * n^2)** time.
For $n = 1,000$ and $k = 50$, that is $5 \times 10^7$ operations!

Binary search on answer solves this in **O(n log(sum - max))** time.
For the same array, that is $\approx 30 \times 1,000 = 30,000$ operations—over **1,000x faster**!

---

### 🔧 The Minimax Invariant & Greedy Packing

Instead of searching for partition points, guess the maximum allowed subarray sum $S$:
*Can we split `nums` into $\le k$ subarrays where each subarray sum is $\le S$?*

1. **Greedy Packing**:
   Iterate through `nums` and add elements to the current subarray.
   The moment adding the next element would exceed $S$, cut the subarray and start a new one.
   **Why greedy works**: Packing each subarray as full as possible leaves the smallest remaining suffix, minimizing the total number of subarrays needed.
2. **Monotonicity**:
   As threshold $S$ increases, the number of required subarrays strictly non-increases.
   Feasibility `can_split(S)` forms a monotonic boolean sequence:
   `[False, False, ..., False, True, True, True]`
   Binary search finds the first `True` in $O(n \log(\sum \text{nums}))$.

---

### 🐛 Two Mathematical Bounds & Fast-Paths

1. **Tight Lower Bound via Average**:
   Most solutions set `left = max(nums)`.
   By the Pigeonhole Principle, the largest subarray sum can **never be less than the average**:
   `left = max(max(nums), ceil(sum(nums) / k))`
   This prunes candidate sums before the loop begins.

2. **O(1) Boundary Fast-Paths**:
   - If $k == 1$: Return `sum(nums)` in **O(1)** time ($126\times$ faster!).
   - If $k == n$: Every element is its own subarray. Return `max(nums)` in **O(1)** time.

---

### 📊 Complexity

- **Time:** O(n log(sum(nums) - max(nums)))
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Whenever asked to minimize the maximum contiguous subarray partition, reach for Binary Search on Answer + Greedy Packing instead of Dynamic Programming.

In Part 2, we benchmark standard greedy search against a **Prefix-Sum Binary Jump** optimization that runs **24x faster** when $k \ll n$!

Do you reach for DP or Binary Search first when partitioning arrays? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
