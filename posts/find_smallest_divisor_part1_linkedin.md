# Binary Search on Answer: Finding the Smallest Divisor (Part 1 of 2) ➗

**The Problem**:
You are given an integer array `nums` and an integer `threshold`.
Choose a positive integer `divisor`, divide each element by it, and round up to the nearest integer ($\lceil \text{num} / \text{divisor} \rceil$).
Return the **smallest divisor** such that the sum of all division results is $\le \text{threshold}$.

---

### 🧩 Why We Search the Answer Space

The array `nums` is unsorted, and sorting it doesn't give us the divisor.
Instead, we binary search over the **range of candidate divisors**:
$\text{divisor} \in [1, \max(\text{nums})]$.

---

### 🔧 Monotonicity: The Core Invariant

Why does binary search work on this problem?
Because the sum function is monotonic:
- Let $S(d) = \sum \lceil \text{nums}[i] / d \rceil$.
- As divisor $d$ increases, each term $\lceil \text{nums}[i] / d \rceil$ can only decrease or stay the same.
- Therefore, total sum $S(d)$ strictly non-increases.
- The feasibility test $S(d) \le \text{threshold}$ forms a monotonic boolean sequence:
  `[False, False, ..., False, True, True, True]`

We are finding the boundary: the **first `True`** in the feasibility domain!

---

### 🐛 Two Mathematical Bound Optimizations

1. **Tight Lower Bound**:
   Most solutions default to `left = 1`.
   Even if division had zero rounding-up overhead, the continuous sum would be $\sum \text{nums} / d \le \text{threshold}$.
   Thus, Koko/Divisor cannot be less than:
   $\text{left} = \lceil \sum \text{nums} / \text{threshold} \rceil = (\sum \text{nums} + \text{threshold} - 1) // \text{threshold}$
   This prunes useless small divisors before the loop starts.

2. **The O(1) Fast-Path When threshold == len(nums)**:
   Since every positive integer rounded up contributes at least $1$, the minimum possible sum across $n$ elements is $n$.
   If $\text{threshold} == n$, the ONLY way the sum can be $\le n$ is if **every single element contributes exactly 1**.
   That requires $\text{divisor} \ge \max(\text{nums})$.
   We can return `max(nums)` immediately in **O(1)** time ($115\times$ faster!), bypassing binary search entirely!

---

### 📊 Complexity

- **Time:** O(n log(max_num))
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Whenever division or rounding is involved, look for monotonic aggregate behavior. Establishing theoretical minimum bounds and boundary shortcuts eliminates binary search passes before you begin.

In Part 2, we benchmark standard binary search against frequency compression (`Counter`) and Python's `bisect`. The frequency approach runs up to 10x faster!

How often do you look for O(1) mathematical fast-paths before entering a binary search loop? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
