# Pruned Binary Search: Beating O(N) by 3x (Part 2 of 2) ⚡

In Part 1, we derived the linear $O(n + m)$ Two-Pointer solution for Maximum Distance Between a Pair of Values.

In standard algorithm theory, $O(n + m)$ should beat $O(n \log m)$ Binary Search.
**Yet on 100,000 elements, Pruned Binary Search ran in 9.55 ms vs. 28.51 ms—beating Two Pointers by 3x!**

How does an $O(n \log m)$ algorithm beat an $O(n)$ linear scan?

---

### 💥 The Benchmark (100,000 Elements)

| Implementation | 100k Elements Time | Relative Speed |
| :--- | :--- | :--- |
| Naive Binary Search | 173.96 ms | Baseline |
| Standard Bisect | 242.70 ms | 0.7x |
| Two Pointers | 28.51 ms | 6.1x faster |
| **Pruned Binary Search** | **9.55 ms** | **18x faster than BS, 3x faster than Two Pointers!** |

---

### 🔍 The Pruning Secret: O(1) Candidate Filtering

Why does naive binary search take 174 ms?
Searching $[i, \text{len}(nums2) - 1]$ for every index $i$ runs $100,000$ independent binary searches!

We eliminate 99% of those searches with **three mathematical prunings**:

1️⃣ **Global Early Exit**:
If $i + \text{max\_dist} \ge \text{len}(nums2)$, index $i$ and all following indices cannot beat `max_dist`. Break the outer loop immediately!

2️⃣ **O(1) Candidate Filter**:
Before launching binary search, test a single value:
`nums2[i + max_dist] >= nums1[i]`
Because `nums2` is descending: if the element at $i + \text{max\_dist}$ is already $< nums1[i]$, then **every element after it is also strictly smaller**!
Index $i$ has zero chance of improving `max_dist`. We skip binary search entirely in **O(1)**!

3️⃣ **Narrowed Search Range**:
When a candidate passes the filter, we search only $[i + \text{max\_dist}, \text{len}(nums2) - 1]$.

---

### 💡 Binary Search with `bisect` on Descending Arrays

Can Python's standard library `bisect` search descending arrays?
Yes! Invert the condition:
`nums2[j] < nums1[i]` is strictly monotonic (`False -> True`)!
`idx = bisect.bisect_left(range(i, len(nums2)), True, key=lambda j: nums2[j] < nums1[i])`
The target right before `idx` is your furthest valid index.

---

### 🧪 Verification

Verified with pytest and Hypothesis (50 passed tests):
- **Deterministic Cases**: LeetCode examples, empty lists, diagonal matches ($i == j$), singletons, and maximum stretch distances.
- **Invariants**: $d \ge 0$, $d < \text{len}(nums2)$, and exact pair validation.
- **100% Agreement**: All variants return identical answers across randomized descending inputs.

---

### 🎯 Key Takeaway

Asymptotic big-O tells only part of the story.
By filtering candidate states in $O(1)$ before entering search, an $O(n \log m)$ algorithm can eliminate almost all iterations, outrunning an $O(n)$ scan in production!

Have you ever used early candidate filtering to beat a theoretical big-O bound? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #TwoPointers #LeetCode #CodingInterview
