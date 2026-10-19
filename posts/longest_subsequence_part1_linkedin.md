# Greedy + Binary Search: Maximizing Subsequences Under a Budget (Part 1 of 2) 🎒

**The Problem**:
You are given an integer array `nums` of length $n$, and an array `queries` of length $m$.
For each query $Q$, find the maximum size of a **subsequence** taken from `nums` whose sum is $\le Q$.
Return an array of answers for all $m$ queries.

---

### 🧩 The Greedy Foundation: Subsequence vs. Subarray

A common trap is confusing subsequences with contiguous subarrays.
Subarrays force elements to be adjacent, requiring sliding windows or prefix hash maps.
A **subsequence**, however, lets you pick any subset of elements.

To maximize the **count** of items under a fixed sum budget $Q$, which items should you pick?
The smallest ones!
- An exchange argument proves optimality: if any valid subsequence includes a larger element instead of an available smaller element, swapping it reduces the total sum without changing the count.
- Thus, the $k$ smallest elements yield the absolute minimum possible sum for any subsequence of size $k$.

---

### 🔧 The Strategy: Prefix Sums + Binary Search

1. Sort `nums` ascending in **O(n log n)**.
2. Build `prefix_sums` where `prefix_sums[i]` is the sum of the first $i + 1$ elements.
   Because all elements are positive, `prefix_sums` is strictly increasing.
3. For each query $Q$, binary search for the largest index where `prefix_sums[mid] <= Q`.
4. The maximum count of elements is `mid + 1`. This is precisely an **upper-bound search** (`bisect_right`).

Total time drops to **O((n + m) log n)** with **O(n)** auxiliary space.

---

### 🐛 Two Quality Issues in the Initial Draft

1. **Empty Array Crash**:
   Writing `prefix_sums[0] = nums[0]` without checking `nums` raises `IndexError` when `nums = []`.
   Defensive guards should return `[0] * len(queries)` immediately.

2. **Silent Caller Mutation**:
   Calling `nums.sort()` rearranges the caller's array in place.
   A read-only query function must never mutate input arguments. Replacing it with `sorted(nums)` guarantees thread safety and immutability.

---

### 📊 Complexity

- **Time:** O(n log n + m log n) = O((n + m) log n)
- **Space:** O(n) auxiliary space for sorted elements and prefix sums

---

### 🎯 Key Takeaway

When optimizing subset size under a cumulative constraint, sort greedily. Prefix sums transform a combinatorial selection problem into standard binary search.

In Part 2, we benchmark manual binary search against `itertools.accumulate` + `bisect_right` and a monotonic two-pointer approach. The C-speed version runs up to 7x faster!

How often do you catch in-place `.sort()` calls during code review? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #Greedy #LeetCode #CodingInterview
