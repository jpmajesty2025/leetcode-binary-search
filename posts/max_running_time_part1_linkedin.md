# Binary Search on the Answer: The Computer Scheduling Paradox (Part 1 of 2) 💻

**The Problem**:
You have $n$ computers and an array of battery runtimes (LeetCode 2141).
You want to run all $n$ computers simultaneously for as long as possible.
At any moment, you can swap batteries instantaneously between computers with zero downtime.
Batteries cannot be recharged. What is the maximum simultaneous runtime $T$?

---

### 🧠 The Scheduling Trap vs Search Inversion

Constructing an explicit battery schedule directly is complicated because batteries can be swapped and split across machines in many combinations.

Instead of asking how to schedule the batteries, invert the question:
**"Can we run all $n$ computers simultaneously for candidate time $T$?"**

Notice the monotonicity:
- If running for $T$ minutes is possible, any smaller time $T' < T$ is trivial.
- If $T$ minutes is impossible, no larger time $T' > T$ can work.

This allows us to binary search directly across the timeline for the optimal runtime $T$.

---

### 🔬 The Feasibility Condition & McNaughton's Theorem

How do we check if candidate runtime $T$ is achievable?

Consider the physical constraint:
**No single battery can power two computers at the same time.**
During a window of $T$ minutes, a battery of capacity $b$ can provide at most $\min(b, T)$ minutes of useful power. Any excess capacity above $T$ sits idle.

Summing across all batteries, the total usable energy is:
$$\text{Usable Energy} = \sum_{i=1}^M \min(batteries[i], T)$$

To keep $n$ computers running for $T$ minutes, the fleet requires at least $n \times T$ total energy:
$$\sum_{i=1}^M \min(batteries[i], T) \ge n \times T$$

Is this condition sufficient?
**Yes.**
By McNaughton's wrap-around rule from parallel machine scheduling, whenever each task is $\le T$ and total load $\le n \times T$, an overlap-free schedule is guaranteed to exist.

---

### 💡 Search Space Bounds

- **Lower Bound ($left = 1$)**: Since $M \ge n$ and every battery has at least $1$ minute, $1$ minute is always achievable.
- **Upper Bound ($right = \lfloor \sum batteries / n \rfloor$)**: Even with zero waste, $n$ computers can never exceed the total energy divided by $n$.

---

### 📊 Complexity & Bottleneck

- **Time:** $O(M \log(\sum batteries / n))$.
- For $M = 100,000$ and values up to $10^{14}$, binary search takes $\approx 47$ iterations, totaling $4.7 \times 10^6$ operations.

In Part 2, we show how prefix sums with bisect deliver an 18x speedup, and how greedy reverse elimination skips the search entirely for a 31x boost!

Have you ever used scheduling theory to prove a binary search predicate? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
