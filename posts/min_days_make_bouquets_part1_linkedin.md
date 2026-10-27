# Binary Search on the Answer: Greedy Flower Packing & Boundary Shortcuts (Part 1 of 2) 🌸

**The Problem**:
You have $n$ flowers planted in a row.
Flower $i$ blooms on day `bloomDay[i]`.
You need to make $m$ bouquets. Each bouquet requires $k$ adjacent bloomed flowers.
Each flower can only belong to one bouquet.
What is the minimum number of days needed to make $m$ bouquets? If impossible, return $-1$.

---

### 🧠 The Greedy Choice Property on the Timeline

Trying to compute the minimum day directly is difficult because bloomed clusters grow and merge continuously across time.

Instead of searching for combinations, invert the problem:
**"Can we form $m$ bouquets of $k$ adjacent flowers on or before day $T$?"**

Notice the monotonicity:
- If day $T$ allows $m$ bouquets, any later day $T' > T$ only has more bloomed flowers.
- If day $T$ fails, no earlier day could possibly work.

To verify candidate day $T$:
Walk through `bloomDay` from left to right.
Track consecutive bloomed flowers (`bloomDay[i] <= T`).
The moment consecutive count reaches $k$:
1. Form a bouquet immediately: $\text{bouquets} \leftarrow \text{bouquets} + 1$.
2. Reset consecutive flowers to $0$.

**Why is greedy packing optimal?**
Taking the earliest possible group of $k$ flowers leaves the maximum remaining array available for all future bouquets. Delaying a bouquet never creates a better grouping downstream.

---

### 💡 Two Instant $O(1)$ Shortcuts

Before starting any binary search, two boundary checks save unnecessary compute:

1. **Total Insufficiency ($n < m \times k$)**:
   Each bouquet consumes $k$ distinct flowers.
   If total flowers $n < m \times k$, making $m$ bouquets is mathematically impossible. Return $-1$ immediately.

2. **Exact Capacity ($n = m \times k$)**:
   When $n = m \times k$, every single flower in the entire garden must bloom.
   If even one flower has not bloomed, at most $n - 1 < m \times k$ flowers are ready.
   Therefore, the earliest day all $n$ flowers are bloomed is strictly day $\max(bloomDay)$.
   Checking `if n == m * k: return max(bloomDay)` avoids the entire binary search in $O(1)$!

---

### 📊 Complexity & Bottleneck

- **Time:** $O(N \log(\max - \min))$.
- For $N = 100,000$ and bloom days up to $10^9$, binary search takes $\approx 30$ iterations, totaling $3 \times 10^6$ operations ($185$ ms in Python).

In Part 2, we show how value-domain compression cuts search iterations nearly in half, and how an event sweep with $O(1)$ boundary merging bypasses binary search for a 3.4x speedup!

Have you used exact capacity shortcuts in other binary search problems? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
