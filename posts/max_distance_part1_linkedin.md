# Dual Monotonicity: Maximum Distance Between Values (Part 1 of 2) 📏

**The Problem**:
You are given two **non-increasing** (descending) integer arrays: `nums1` and `nums2`.
A pair of indices $(i, j)$ is valid if:
1. $i \le j$
2. $nums1[i] \le nums2[j]$
The distance of the pair is $j - i$.
Find the **maximum distance** of any valid pair, or return `0` if none exists.

---

### 🧩 The Dual Monotonicity Invariant

Both arrays are sorted in descending order:
- $nums1[0] \ge nums1[1] \ge nums1[2] \ge \dots$
- $nums2[0] \ge nums2[1] \ge nums2[2] \ge \dots$

This dual monotonicity creates an invariant that makes a **linear Two-Pointer** approach possible:
1. As index $i$ advances, $nums1[i]$ decreases (or stays the same).
2. If an element $nums2[j]$ was greater than or equal to an earlier (larger) $nums1[i_{\text{prev}}]$, it is **guaranteed to be greater than or equal to** the current (smaller) $nums1[i_{\text{curr}}]$!
3. Therefore, pointer $j$ **never needs to backtrack**! It only ever moves forward.

---

### 🔧 The Two-Pointer Algorithm

- Initialize `j = 0` and `max_dist = 0`.
- Iterate $i$ from $0$ to $\text{len}(nums1) - 1$:
  - While $j < \text{len}(nums2)$ and $nums1[i] \le nums2[j]$, increment $j$.
  - When the loop stops, index $j - 1$ was the furthest valid target for index $i$.
  - Candidate distance: $(j - 1) - i = j - i - 1$.
  - Update: `max_dist = max(max_dist, j - i - 1)`.
- If $j \le i$, the distance expression $j - i - 1 \le -1$, naturally preventing invalid pairs ($i > j$) from contributing positive distances.

Both pointers traverse their respective arrays at most once.

---

### 📊 Complexity

- **Time:** O(n + m) where $n = \text{len}(nums1)$ and $m = \text{len}(nums2)$
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

When two arrays both share a monotonic property, look for coupling invariants. Here, because $nums1[i]$ non-increases, valid targets in $nums2$ only expand to the right, enabling an optimal single-pass traversal.

In Part 2, we explore an unexpected twist: how **Pruned Binary Search** actually beats Two Pointers by **3x** on 100,000 elements!

Have you ever seen an $O(n \log m)$ binary search outperform an $O(n + m)$ two-pointer scan? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #TwoPointers #LeetCode #CodingInterview
