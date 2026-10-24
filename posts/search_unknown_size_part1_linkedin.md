# Searching an Infinite Horizon: Exponential Search in Unknown Arrays (Part 1 of 2) 🔭

**The Problem**:
You have a sorted array of unique integers, but its **size is completely unknown**.
You have no `.length()` method. Direct access is forbidden.
Instead, an API provides `reader.get(i)`:
- Returns `secret[i]` if `i` is within bounds.
- Returns $2^{31} - 1$ if `i` is out of bounds.
You are given an integer `target`. Find its index in $O(\log n)$ time, or return `-1` if absent.

---

### 🧩 The Fundamental Dilemma

Binary search is fundamentally an interpolation between two known walls: `left` and `right`.
You calculate `mid = (left + right) // 2` and discard half the elements.

**What happens when the right wall doesn't exist?**
If you guess an arbitrarily huge right wall (like $2^{31} - 1$), the first `mid` query lands near index $10^9$, returning out-of-bounds sentinel values for dozens of iterations before narrowing down to a modest array of size $10^4$.
If you guess too small, you might miss the target entirely!

---

### 💡 The Solution: Bentley-Yao Exponential Search (1976)

In 1976, computer scientists Jon Bentley and Andrew Yao proved how to search unbounded/infinite lists optimally: **Exponential Bounding**.

Instead of guessing a static right wall, we grow the wall exponentially:
1. Start at $[left, right] = [0, 1]$.
2. While `reader.get(right) < target`:
   - Tighten the left wall: `left = right + 1` (since `secret[right] < target`, the target cannot exist at or before `right`).
   - Double the right wall: `right *= 2` (or bit-shift `right <<= 1`).
3. Once `reader.get(right) >= target` (or hits the out-of-bounds sentinel $2^{31} - 1$), we have bracketed the target inside a finite interval $[left, right]$!
4. Run standard binary search on $[left, right]$!

---

### 🔬 The Magic of O(log k) vs O(log n)

Here lies the genius of Exponential Search:
Its time complexity is **$O(\log k)$**, where $k$ is the **index of the target**, NOT the size of the array $n$!

- **Phase 1 (Exponential expansion):** Takes $\lceil \log_2 k \rceil$ queries.
- **Phase 2 (Binary search):** The window $[k/2, k]$ has size $k/2$. Binary search takes $\lceil \log_2(k/2) \rceil \approx \log_2 k$ queries.
- **Total Cost:** At most $\mathbf{2 \log_2 k\text{ queries}}$!

Imagine an array of **1 billion elements**, but your target is sitting at index $k = 16$:
- Standard binary search on $10^9$: $\approx 30$ queries.
- Exponential search: $2 \log_2(16) = \mathbf{8\text{ queries}}$!
The closer the target is to the start, the faster it finishes!

In Part 2, we explore how Python's **Timsort** uses this exact algorithm (Galloping Search), and how to bridge interactive APIs with Python's C-accelerated `bisect` library using zero-memory virtual sequences.

Have you ever used exponential search outside LeetCode? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
