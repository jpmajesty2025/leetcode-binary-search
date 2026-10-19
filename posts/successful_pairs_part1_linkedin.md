# Sort Once, Search Often: Binary Search for Successful Pairs (Part 1 of 2) 🧪

**The Problem**:
You are given two positive integer arrays: `spells` (length $n$) and `potions` (length $m$), plus an integer `success`.
A pair is successful if `spell * potion >= success`.
For each spell, return how many potions form a successful pair.

---

### 🧩 Why Brute Force Fails

Checking every pair requires $n \times m$ multiplications.
With $n, m = 100,000$, that is $10^{10}$ operations—guaranteed Time Limit Exceeded (TLE).

---

### 🔧 The Binary Search Strategy

Notice that spells are queried independently. We don't need to reorder spells; we only need to query potions efficiently.

1. Sort `potions` ascending once in **O(m log m)**.
2. For any given `spell`, what is the minimum potion strength needed?
   - `min_potion = ceil(success / spell)`
   - In integer arithmetic: `(success + spell - 1) // spell`
3. Binary search for `min_potion` in `potions` in **O(log m)**.
4. Because `potions` is sorted, every potion from that insertion index to the end is $\ge \text{min\_potion}$.
5. Successful pairs for this spell = `m - index`.

Total time drops from $O(n \cdot m)$ to **O((m + n) log m)**.

---

### 🧠 Ceiling Division vs. Repeated Multiplication

Many implementations test `spell * potions[mid] >= success` inside the binary search loop.
Computing `min_potion = (success + spell - 1) // spell` **once** before the loop has two big advantages:
- It eliminates repeated multiplication inside the inner loop.
- In languages like C++ or Java, `spell * potion` can exceed $10^{10}$ and overflow 32-bit signed integers. Precomputing the threshold avoids overflow entirely.

---

### 📊 Complexity

- **Time:** O(m log m + n log m) = O((m + n) log m)
- **Space:** O(m) auxiliary space for the sorted copy of potions

---

### 🎯 Key Takeaway

When querying multiple inputs against static reference data: sort the reference data once, precompute the query boundary, and binary search.

In Part 2, we benchmark manual binary search against Python's C-level `bisect`, a two-pointer dual sort, and a suffix bucket array that queries in O(1). The winner is up to 11x faster!

How do you handle integer ceiling division in your favorite language? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
