# The Monotonic Half Invariant: Searching Rotated Arrays in One Pass (Part 1 of 2) 🔄

**The Problem**:
You are given an integer array with unique values, sorted in ascending order, but rotated at an unknown pivot index $k$.
For example: `[0, 1, 2, 4, 5, 6, 7]` might become `[4, 5, 6, 7, 0, 1, 2]`.
Given a `target`, return its index if found, or `-1` if absent.
Your solution must run in **O(log n) time and O(1) space**.

---

### 🧩 The Dilemma: Broken Global Monotonicity

Standard binary search relies on **global monotonicity**: every element is greater than or equal to the preceding one.
When an array is rotated, the inflection point (where $7$ drops to $0$) breaks global monotonicity.
If `target = 0` and you query `mid = 7`:
- $7 > 0$. In a standard sorted array, you would search left.
- But in this rotated array, $0$ is sitting to the **right** of $7$!
Naive binary search fails immediately.

---

### 💡 The Solution: The Monotonic Half Invariant

How do we restore the power of binary search?
By recognizing a fundamental geometric truth:

**Whenever you split a rotated sorted array at ANY index `mid`, at least ONE of the two halves is GUARANTEED to be strictly sorted and monotonic!**

Consider `[4, 5, 6, 7, 0, 1, 2]`, where `mid` points to $7$:
- Left half `[4, 5, 6, 7]` is strictly sorted!
- Right half `[7, 0, 1, 2]` contains the inflection drop.

---

### 🧭 The 1-Pass Decision Tree

Because one half is always sorted, we can test whether `target` falls cleanly within the sorted half's known boundaries:

1. **Identify the Sorted Half**:
   Compare `nums[left]` with `nums[mid]`:
   - If `nums[left] <= nums[mid]`: The **Left Half** $[left, mid]$ is strictly sorted.
   - Else: The **Right Half** $[mid, right]$ is strictly sorted.

2. **Check Target Containment**:
   - **If Left Half is Sorted**:
     Check if `target` lies within `[nums[left], nums[mid])`:
     - If `nums[left] <= target < nums[mid]`: Target is trapped in the left half! Search left: `right = mid - 1`.
     - Else: Target must be in the right half! Search right: `left = mid + 1`.
   - **If Right Half is Sorted**:
     Check if `target` lies within `(nums[mid], nums[right]]`:
     - If `nums[mid] < target <= nums[right]`: Target is trapped in the right half! Search right: `left = mid + 1`.
     - Else: Target must be in the left half! Search left: `right = mid - 1`.

Every iteration cuts the search space exactly in half!

---

### 📊 Complexity

- **Time:** $O(\log n)$ comparisons.
- **Space:** $O(1)$ auxiliary space.

In Part 2, we explore 3 fascinating alternative paradigms:
1. Two-pass decoupling with Python's C-accelerated `bisect`.
2. Cyclic Modulo Coordinate Transformation.
3. Inflection Normalization with Virtual Infinity ($\pm\infty$)!

What was your biggest stumbling block when first tackling rotated binary search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
