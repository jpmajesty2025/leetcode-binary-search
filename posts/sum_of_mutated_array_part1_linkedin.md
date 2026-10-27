# Binary Search on the Answer: The Truncation Dilemma & Zero-Bound Trap (Part 1 of 2) 🎯

**The Problem**:
You are given an integer array `arr` and an integer `target` (LeetCode 1300).
Pick an integer `value` such that changing all numbers in `arr` larger than `value` to equal `value` makes the mutated sum as close as possible to `target`.
In case of a tie, return the minimum such integer.

---

### 🧠 Non-Monotonic Distance vs Monotonic Sum

The objective function:
$$\text{Difference}(v) = |\text{mutated\_sum}(v) - \text{target}|$$
is non-monotonic. It forms a V-shape, dropping to a minimum and rising again.

However, the mutated sum itself:
$$f(v) = \sum_{i=1}^N \min(arr[i], v)$$
is strictly monotonic. As $v$ increases from $0$, each element either stays constant or increases. The sum $f(v)$ never decreases.
Because $f(v)$ is monotonically non-decreasing, we can binary search across candidate values $v$ to locate where $f(v)$ crosses `target`.

---

### ⚠️ The Zero-Bound Trap

A frequent mistake is initializing the binary search range as:
`left = 1, right = max(arr)`

This introduces a silent bug on valid inputs.

Consider:
`arr = [2, 20, 11]` and `target = 1`.
- At $v = 0$: mutated sum is $0$, distance = $|0 - 1| = 1$.
- At $v = 1$: mutated sum is $3$, distance = $|3 - 1| = 2$.
The optimal value is $0$. Starting at `left = 1` skips $0$ completely.

Another case:
`arr = [1, 1]` and `target = 1`.
- $v = 0 \implies \text{sum} = 0$, distance = $1$.
- $v = 1 \implies \text{sum} = 2$, distance = $1$.
Both values tie on distance. The tie-breaker picks the smaller integer, so $0$ is correct.
The search range must start at `left = 0`.

---

### 💡 Search Space Bounds & Early Exit

1. **Lower Bound ($left = 0$)**: Required whenever small targets make $0$ optimal.
2. **Upper Bound ($right = \max(arr)$)**: Candidate values $v > \max(arr)$ truncate no elements and yield the exact same sum as $\max(arr)$, but are larger integers. They always lose ties to $\max(arr)$, so values above $\max(arr)$ are never needed.
3. **Early Exit**: If $\text{sum}(arr) \le \text{target}$, setting $v = \max(arr)$ is immediately optimal. Any smaller value lowers the sum further away from target.

---

### 📊 Complexity

- **Time:** $O(N \log(\max(arr)))$ where $N = \text{len}(arr)$.
- **Space:** $O(1)$ auxiliary space.

In Part 2, we eliminate the repeated $O(N)$ inner loop using prefix sums with bisect, then show a direct $O(N \log N)$ mathematical greedy approach that removes the value search loop entirely.

Have you ever hit an off-by-one lower bound bug in binary search? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
