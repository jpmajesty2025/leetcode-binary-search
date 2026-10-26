# Binary Search on the Answer: Resource Allocation & The Pigeonhole Bound (Part 1 of 2) 🍬

**The Problem**:
You have $N$ piles of candies (up to $100,000$ piles).
You can divide each pile into smaller sub-piles, but you **cannot merge** two piles together.
You have $k$ children (where $k$ can be up to $10^{12}$!).
You must allocate sub-piles to all $k$ children such that every child receives the exact same number of candies.
What is the **maximum number of candies** each child can get? (Return $0$ if impossible).

---

### 🧠 The Paradigm Shift: Binary Search on the Answer Space

Notice that the input array `candies` is not sorted, and we aren't looking for a pile inside `candies`.
Instead, we are searching for an unknown integer $C$ (candies per child).

Why does binary search work here?
Because the allocation capacity function is **strictly monotonic**!

At a candidate rate of $C$ candies per child, a pile of size $P$ can satisfy:
$$\text{children served from pile } P = \lfloor P / C \rfloor$$

The total children that can be served across all piles is:
$$g(C) = \sum_{i=1}^N \lfloor \text{candies}[i] / C \rfloor$$

Notice the monotonicity:
- If we give each child **fewer** candies, we can serve **more** children.
- If we give each child **more** candies, we can serve **fewer** children.
As $C$ increases, $g(C)$ is monotonically non-increasing.
Our goal is to find the **maximum $C$** such that $g(C) \ge k$!

---

### ⚠️ The Critical Edge Case & The Pigeonhole Upper Bound

1. **The Zero Edge Case**:
   What if $\sum \text{candies} < k$?
   If the total number of candies across all piles is strictly less than $k$, you cannot give even $1$ candy to each child!
   You must return $0$ immediately.

2. **The Pigeonhole Upper Bound**:
   Most candidates lazily set the binary search upper bound to:
   $\text{right} = \max(\text{candies})$
   
   Can we do better? Absolutely!
   Think about the physical theoretical limit:
   Even if you were allowed to melt and merge every single candy into one gigantic pile, $k$ children could receive at most:
   $$\text{Maximum Theoretical Limit} = \lfloor \sum \text{candies} / k \rfloor$$
   Since merging piles is strictly forbidden, the real answer can **never exceed** $\lfloor \sum \text{candies} / k \rfloor$!
   
   Setting $\text{right} = \sum \text{candies} // k$ provides a mathematically tight bound.
   When $k$ is large (e.g. $k = 10^7$ or $10^{12}$), this collapses the search range to a tiny interval before binary search even begins!

---

### 📊 Complexity

- **Time:** $O(N \log(\sum \text{candies} // k))$ comparisons.
- **Space:** $O(1)$ auxiliary space.

In Part 2, we explore how **Frequency Compression** and **Monotonic Failure Views** take performance to the next level!

Have you ever used the Pigeonhole Principle to bound your binary search range? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
