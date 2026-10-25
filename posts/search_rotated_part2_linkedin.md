# From Cyclic Modulo to Virtual Infinity: 3 Alternative Paradigms (Part 2 of 2) ⚡

In Part 1, we analyzed the classic one-pass decision tree for Search in Rotated Sorted Array (LeetCode 33).

Mastering alternative mental models reveals the deeper beauty of coordinate transformations and standard library design.

Here are **3 alternative paradigms** to solve this problem!

---

### 1️⃣ Two-Pass Decoupling: Separation of Concerns

Instead of intertwining pivot detection with target searching, decouple them:
1. **Pass 1:** Find pivot index $P$ (minimum element, identical to LeetCode 153) in $O(\log n)$.
2. **Segment Selection:** Check if `target >= nums[0]`:
   - If True: Target belongs to left segment $[0, P - 1]$.
   - If False: Target belongs to right segment $[P, n - 1]$.
3. **Pass 2:** Run Python's C-accelerated `bisect.bisect_left` directly over that sorted slice!

---

### 2️⃣ Cyclic Modulo Transformation: Coordinate Systems

Think of a rotated array as a circular ring!
1. Find pivot index $P$.
2. Virtual index $i$ in $[0, n - 1]$ maps to real index:
   $\text{real\_index} = (i + P) \pmod n$
3. Run **textbook binary search** over virtual indices $0 \dots n - 1$:
   Access `nums[(mid + P) % n]`.
   - If `nums[real_mid] < target`: `left = mid + 1`
   - If `nums[real_mid] > target`: `right = mid - 1`

**Advantage:** Zero nested if-else ladders! Binary search logic is completely unmodified.

---

### 3️⃣ Inflection Normalization: Virtual Infinity

Instead of modifying binary search logic, **modify data to fit standard binary search**!
If `mid` and `target` lie on opposite sides of `nums[0]`:
- Target on left, `mid` on right: Treat `nums[mid]` as $+\infty$.
- Target on right, `mid` on left: Treat `nums[mid]` as $-\infty$.

This virtually stitches the two disjoint pieces into a single continuous monotonic line!

---

### 💥 Benchmark Shootout (50,000 Iterations)

| Implementation | Technique | Time (50k runs) | Tradeoff |
| :--- | :--- | :--- | :--- |
| **One-Pass Modified** | Monotonic half checks | **120.69 ms** | **Fastest (zero extra passes)** |
| **Two-Pass Bisect** | Pivot find + `bisect_left` | 137.63 ms | Modular & clean |
| **Inflection Shift** | Virtual $\pm\infty$ mapping | 145.61 ms | Pure monotonic transformation |
| **Cyclic Modulo** | `(mid + P) % n` shift | 149.22 ms | Pure binary search logic |

---

### 🧪 Verification

Verified with pytest and Hypothesis (29 passing tests):
- All rotation offsets $k \in [0, n - 1]$.
- Small arrays (lengths 0, 1, 2) and negative numbers.
- Scale test with $N = 5,000$.
- Property fuzzing verifying 100% agreement across all 4 implementations.

---

### 🎯 Key Takeaway

A rotated array can be tackled as a piecewise partition, a decoupled two-pass pipeline, a circular modulo coordinate system, or a virtual continuous line.

Which paradigm speaks to you the most? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #CodingInterview
