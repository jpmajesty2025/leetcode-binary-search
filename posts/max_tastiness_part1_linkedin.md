# Binary Search on the Answer: Maximizing Minimum Distance (Part 1 of 2) 🍬

**The Problem**:
You are given an array `price` of $N$ candy prices (up to $100,000$) and an integer $k$.
A basket consists of $k$ distinct candies.
The **tastiness** of a basket is defined as the **smallest absolute difference** between any two candy prices in the basket:
$$\text{Tastiness} = \min_{i \ne j} |price[i] - price[j]|$$
What is the **maximum possible tastiness** you can achieve?

---

### 🧠 The "Maximize the Minimum" Archetype

Whenever you encounter a problem asking to **maximize a minimum** (or minimize a maximum), your algorithmic intuition should immediately scream:
**Binary Search on the Answer!**

Why?
Trying to construct the optimal basket directly via dynamic programming or greedy choices fails because spacing choices are globally coupled across all $k$ items.

Instead, we invert the question:
**"Given a candidate tastiness $T$, is it possible to choose $k$ candies such that every adjacent pair is separated by at least $T$?"**

---

### 🔍 Monotonicity & The Greedy Choice Property

Notice the monotonicity of this predicate:
- If spacing $T$ is possible, any smaller spacing $T' < T$ is trivially possible.
- If spacing $T$ is impossible, no larger spacing $T' > T$ can ever work.

To test if candidate tastiness $T$ is achievable:
1. Sort `price` in ascending order.
2. **Greedy Choice**: Always pick `price[0]`! Choosing the smallest available price leaves the maximum possible room for all remaining $k - 1$ candies.
3. Traverse the array and greedily select the earliest candy whose price is $\ge \text{last\_chosen} + T$.
4. If you successfully collect at least $k$ candies, then $T$ is achievable!

---

### 💡 The Pigeonhole Principle Upper Bound

What should the upper bound of your binary search range be?
Many developers lazily write:
$\text{right} = price[-1] - price[0]$

Can we tighten this?
Consider: When you select $k$ sorted candies between $price[0]$ and $price[-1]$, you create exactly $k - 1$ gaps between them.
The sum of those $k - 1$ gaps cannot exceed $price[-1] - price[0]$.

By the **Pigeonhole Principle** (or average spacing bound), the smallest gap can **never exceed**:
$$\text{Upper Bound} = \left\lfloor \frac{price[-1] - price[0]}{k - 1} \right\rfloor$$

For $k = 100$ and a price span of $1,000$, this bound cuts your initial search range from $1,000$ down to just $10$, eliminating unnecessary binary search cycles!

---

### 📊 Complexity

- **Time:** $O(N \log N + N \log(\frac{\max - \min}{k - 1}))$.
- **Space:** $O(1)$ auxiliary space.

In Part 2, we uncover a hidden bottleneck in this linear greedy check and reveal how **Bisect Hopping** delivers an incredible **85x speedup**!

Have you seen the "maximize the minimum" pattern in other problems like Aggressive Cows or Magnetic Force? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
