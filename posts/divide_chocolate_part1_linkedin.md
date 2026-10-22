# Maximin Binary Search: Conquering Divide Chocolate (Part 1 of 2) 🍫

**The Problem**:
You have a chocolate bar with $n$ chunks, each with a sweetness value.
You want to share it with $k$ friends by cutting it into $k + 1$ contiguous pieces.
Being generous, you eat the piece with the **minimum total sweetness**.
Find the **maximum sweetness** you can guarantee for yourself by cutting optimally.

---

### 🧩 The Maximin Duality

Most binary search on answer problems are "Minimax" (minimize the maximum, like Koko or ship capacity).
Here the goal is flipped: **maximize the minimum** piece (Maximin).

This inversion changes two critical implementation mechanics:
1. **Upper-Mid Formula**:
   When moving the lower bound (`left = mid`), standard `(left + right) // 2` rounds down, causing an **infinite loop** when `left + 1 == right`.
   We must use the upper-mid formula:
   `mid = (left + right + 1) // 2`
2. **Search Direction**:
   If candidate sweetness is feasible, we search higher: `left = mid`.
   If infeasible, we pull back: `right = mid - 1`.

---

### 🔧 Greedy Piece Formation & Monotonicity

Can we form at least $k + 1$ pieces where every piece has sweetness $\ge T$?
- We iterate through `sweetness`, accumulating chunk values.
- The moment the running sum reaches $T$, we **cut immediately** and reset the sum.
- **Why greedy works**: Cutting as early as possible preserves maximum sweetness for remaining pieces. If greedy cannot find $k + 1$ pieces of size $\ge T$, no partition can.
- As target sweetness $T$ increases, achievable pieces monotonically decrease:
  `[True, True, ..., True, False, False]`

---

### 🐛 Two Mathematical Bounds & Fast-Paths

1. **Tight Upper Bound via Average**:
   Most solutions write `right = sum(sweetness)`.
   By the Pigeonhole Principle, the minimum piece can **never exceed the average**:
   `right = sum(sweetness) // (k + 1)`
   If $k = 100$, this bound is **100x tighter**, pruning ~7 binary search iterations!

2. **O(1) Boundary Fast-Paths**:
   - If $k == 0$: You keep the entire bar. Return `sum(sweetness)` in **O(1)** time ($188\times$ faster!).
   - If $k + 1 == n$: Each chunk is its own piece. Return `min(sweetness)` in **O(1)** time.

---

### 📊 Complexity

- **Time:** O(n log(sum(sweetness) // (k + 1) - min(sweetness) + 1))
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Maximin problems require upper-mid calculation `(left + right + 1) // 2` to advance the lower bound safely. Capping search at the theoretical average $\lfloor \sum / (k + 1) \rfloor$ eliminates redundant iterations up front.

In Part 2, we benchmark standard greedy search against a **Prefix-Sum Binary Jump** optimization that runs **23x faster** when $k \ll n$!

Have you ever hit an infinite loop in binary search from rounding down? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
