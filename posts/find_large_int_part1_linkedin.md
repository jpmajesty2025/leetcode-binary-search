# The Parity Trap: Finding the Heavy Element with Binary Search (Part 1 of 2) ⚖️

**The Problem**:
All elements in an array are equal, except for **one larger integer**.
You cannot inspect the array directly. Instead, you have an API:
`compareSub(l, r, x, y)`: Compares the **sum** of `arr[l..r]` with `arr[x..y]`, returning `1` if left is greater, `0` if equal, and `-1` if right is greater.
For arrays up to $500,000$ elements, you get **at most 20 calls** to find the index of the large integer!

---

### 🧩 The Fatal Trap in Naive Binary Search

Perhaps you are tempted to write this intuitive loop:
`mid = (left + right) // 2`
`if reader.compareSub(left, mid, mid + 1, right) < 0: left = mid + 1`
`else: right = mid`

**This code fails completely. Why?**
`compareSub` compares the **sum** of two subarrays.
When interval length is **odd**, splitting at `mid` creates subarrays of **unequal lengths**!

Consider: `arr = [10, 10, 11]` (where the heavy element is at index 2).
`left = 0, right = 2, mid = 1`.
We call `compareSub(0, 1, 2, 2)`:
- Left slice `arr[0..1]` has **2 elements**: $10 + 10 = \mathbf{20}$.
- Right slice `arr[2..2]` has **1 element**: $\mathbf{11}$.

Because $20 > 11$, `compareSub` returns `1`!
The naive code concludes the heavy element is on the left, missing the target at index 2!
**You can never compare sums to find an outlier unless slices have identical lengths!**

---

### 🔧 The Parity-Aware Binary Search Solution

To guarantee valid sum comparisons, divide based on parity:

1. **Even Length ($2k$)**:
   Split into two equal halves of size $k$:
   `cmp = reader.compareSub(left, left + k - 1, left + k, right)`
   - If `cmp == 1`: Target is in left half (`right = left + k - 1`).
   - If `cmp == -1`: Target is in right half (`left = left + k`).

2. **Odd Length ($2k + 1$)**:
   Isolate the middle element at $mid = left + k$.
   Compare the two equal slices on either side:
   `cmp = reader.compareSub(left, mid - 1, mid + 1, right)` (both length $k$)
   - If `cmp == 0`: Both sides have equal sums! Neither slice contains the outlier. Therefore, **$mid$ is the large integer!** Return `mid` immediately!
   - If `cmp == 1`: Outlier is in left slice (`right = mid - 1`).
   - If `cmp == -1`: Outlier is in right slice (`left = mid + 1`).

---

### 📊 Complexity

Each step cuts the search space in half:
- **Calls:** At most $\lceil \log_2(500,000) \rceil = \mathbf{19\text{ calls}}$ (strictly $\le 20$).
- **Space:** $O(1)$ auxiliary space.

---

### 🎯 Key Takeaway

When using sum comparisons as a proxy for value comparisons, slice parity is everything. Setting aside the middle element on odd lengths guarantees symmetrical weighings.

In Part 2, we show how the classic **Counterfeit Coin Puzzle** cuts queries down to **13 calls (a 32% reduction)**!

Have you ever had an algorithm fail because odd-length slices weren't symmetrical? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #CodingInterview
