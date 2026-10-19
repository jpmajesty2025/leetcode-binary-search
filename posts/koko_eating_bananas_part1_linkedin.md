# Binary Search on Answer: The Secret to Koko Eating Bananas (Part 1 of 2) 🍌

**The Problem**:
Koko has $n$ banana piles and $h$ hours before the guards return.
She eats at an integer speed of $k$ bananas per hour.
Each hour, she chooses one pile. If the pile has fewer than $k$ bananas, she finishes it and waits out the rest of the hour.
Find the **minimum integer speed $k$** that lets her eat all bananas within $h$ hours.

---

### 🧩 Why We Search the Answer, Not the Array

In standard binary search, you search elements or indices in a sorted array.
Here, `piles` is not sorted—and sorting it doesn't give you $k$.

Instead, we binary search over the **solution space**: the range of possible eating speeds $k \in [1, \max(\text{piles})]$.

---

### 🔧 Monotonicity: The Engine of Feasibility

Why does binary search work on an unsorted problem?
Because the feasibility function is strictly monotonic:
- Let $H(k)$ be the hours needed to finish all piles at speed $k$:
  $H(k) = \sum \lceil p / k \rceil$
- As speed $k$ increases, $H(k)$ can only decrease or stay the same.
- The condition $H(k) \le h$ forms a monotonic boolean sequence:
  `[False, False, ..., False, True, True, True]`

We aren't searching for a specific number in `piles`; we are finding the **first `True`** in the feasibility sequence!

---

### 🐛 Two Mathematical Bound Optimizations

1. **Tight Lower Bound**:
   Most solutions set `left = 1`.
   Even if Koko could eat continuously with zero hour waste, she needs at least:
   $\text{left} = \lceil \sum \text{piles} / h \rceil = (\sum \text{piles} + h - 1) // h$
   Starting at this mathematical lower bound tightens the search space.

2. **The O(1) Shortcut When $h = n$**:
   If $h == \text{len}(\text{piles})$, Koko has exactly 1 hour per pile!
   She must finish each pile in $\le 1$ hour, which means she must be fast enough to eat the largest pile: $k = \max(\text{piles})$.
   Returning `max(piles)` bypasses the binary search loop completely!

---

### 📊 Complexity

- **Time:** O(n log(max(piles) - sum(piles)//h + 1))
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Whenever a problem asks for the "minimum X to satisfy condition Y" or "maximum X under budget Y", ask: **Is the feasibility function monotonic?**
If yes, you don't need a sorted dataset—you binary search on the answer space.

In Part 2, we benchmark floating-point `math.ceil` against pure integer arithmetic, early summation breaks, and Python's `bisect` with boolean keys. One optimization runs 225x faster!

What is your favorite "binary search on answer" problem? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
