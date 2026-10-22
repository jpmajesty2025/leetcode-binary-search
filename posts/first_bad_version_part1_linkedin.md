# First Bad Version: The Archetype of Binary Search (Part 1 of 2) 🐛

**The Problem**:
You have $n$ product versions ($1 \le n \le 2^{31} - 1 \approx 2.14 \text{ billion}$).
One version introduced a bug, and since each build relies on the previous, all subsequent versions are broken.
You have an API: `isBadVersion(version) -> bool`.
Find the **first bad version** while minimizing the number of API calls.

---

### 🧩 The Archetype of Lower-Bound Binary Search

This problem is the canonical definition of lower-bound binary search (`bisect_left`).
The versions form a monotonic boolean domain:
`[False, False, ..., False, True, True, True]`

We aren't looking for just any `True`; we are looking for the exact **transition point**—the very first `True`.

---

### 🔧 The Invariant-Driven Loop

1. **State Invariant**:
   - `left` is the smallest candidate that could be bad.
   - `right` is guaranteed to be a bad version (or the initial upper bound).
2. **Branching Logic**:
   - Calculate midpoint: `mid = left + (right - left) // 2`.
   - If `isBadVersion(mid)` is `True`: `mid` is bad. It might be the *first* bad version, or the first bad version could be earlier. So keep `mid` in our search range:
     `right = mid`
   - If `isBadVersion(mid)` is `False`: `mid` is good. The first bad version must be strictly to the right:
     `left = mid + 1`
3. **Termination**:
   - The loop runs `while left < right`.
   - When `left == right`, the search space has shrunk to a single element. That element is mathematically guaranteed to be the first bad version!

---

### 🛡️ The Integer Overflow Trap

In Python, integers have arbitrary precision and never overflow.
However, in statically-typed languages like C++, Java, or Go:
`(left + right) / 2`
When $n \approx 2^{31} - 1$, `left + right` exceeds the maximum 32-bit signed integer ($2,147,483,647$), overflowing into negative numbers and triggering infinite loops or segfaults!

The universal, portable formula:
`mid = left + (right - left) // 2`
guarantees you never overflow, regardless of programming language.

---

### 📊 Complexity

- **Time:** O(log2 n) — at most 31 API calls for 2.14 billion versions
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

`right = mid` (preserving the valid candidate) and `left = mid + 1` (advancing past the invalid candidate) is the bedrock pattern for finding transition boundaries in monotonic spaces.

In Part 2, we explore **Exponential (Galloping) Search**—how `git bisect` finds recent regressions in **9 queries instead of 31**!

Have you ever encountered a 32-bit integer overflow bug in production binary search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
