# The Sneaky Edge Case: Beating Minimum Speed to Arrive on Time (Part 1 of 2) 🚆

**The Problem**:
You have $h$ hours to reach the office by taking $n$ sequential trains with distances `dist`.
Each train can only depart at an integer hour mark, meaning you must wait after each ride—**except for the final train**, which arrives directly at your destination.
Find the minimum positive integer speed (up to $10^7$) to arrive on time, or return `-1` if impossible.

---

### 🧩 The Fatal Bug in Many Solutions

Look at this seemingly intuitive check:
`if len(dist) > hour: return -1`

At first glance, it feels correct: if you have $3$ trains and only $2.7$ hours, how could you possibly make it if trains depart on the hour?
**This fails LeetCode's own Example 2!**
`dist = [1, 3, 2], hour = 2.7`
Here $n = 3$, and $3 > 2.7$. Yet the correct answer is **speed = 3**:
- Train 1: $1 / 3 = 0.33$ hrs $\to$ wait until hour $1$
- Train 2: $3 / 3 = 1.00$ hrs $\to$ wait until hour $2$
- Train 3: $2 / 3 \approx 0.67$ hrs $\to$ **no waiting!** Arrive at $2.67 \le 2.7$ hours!

The true mathematical impossibility threshold is:
`if hour <= n - 1: return -1`
Only the first $n - 1$ trains require at least $1$ hour each. The last train can take a tiny fraction of an hour if your speed is high enough!

---

### 🔧 The Binary Search on Answer Strategy

We cannot sort `dist` (train sequence is fixed). Instead, we binary search over the **speed domain**: $[1, 10^7]$.
- Let $T(s)$ be the total travel time at speed $s$:
  $T(s) = \sum_{i=0}^{n-2} \lceil \text{dist}[i] / s \rceil + \frac{\text{dist}[n-1]}{s}$
- As speed $s$ increases, total commute time $T(s)$ strictly decreases or stays flat.
- Feasibility $T(s) \le \text{hour}$ is monotonic:
  `[False, False, ..., False, True, True, True]`
- Standard binary search finds the transition point in $O(n \log(\text{max\_speed}))$ time.

---

### 🧠 Integer Ceiling Division vs. Float Modulo

Avoid checking `dist[i] / speed % 1 > 0`. Floating-point modulo introduces subtle rounding bugs in IEEE 754 arithmetic.
Instead, use exact integer ceiling division for the first $n - 1$ trains:
`(dist[i] + speed - 1) // speed`

---

### 📊 Complexity

- **Time:** O(n log(max_speed)) where max_speed = $10^7$, taking at most $\approx 24$ iterations
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Always verify problem constraints on boundary elements. The final step in a multi-stage process often follows different rules than the intermediate stages.

In Part 2, we benchmark floating-point comparisons against pure scaled integer arithmetic (scaling by 100 to eliminate floats completely) and Python's `bisect`. The precision insights are eye-opening!

Have you ever been caught by an edge case where the last item breaks the pattern? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
