# Binary vs. Ternary Search: Why 2 Halves Beat 3 Thirds (Part 1 of 2) 🎯

**The Problem**:
I pick a secret number from $1$ to $n$ (where $n \le 2^{31} - 1 \approx 2.14 \text{ billion}$).
You have an interactive API: `guess(num)`:
- `-1`: My number is lower than your guess.
- `1`: My number is higher than your guess.
- `0`: Bingo! You found it.
Find the secret number with the fewest possible API calls.

---

### 🧩 The Binary Search Solution

In a range of $2.14$ billion numbers, linear guessing is impossible.
With binary search:
- Check the midpoint: `mid = (left + right) // 2`.
- Query `guess(mid)`.
- If `0`, return `mid`.
- If `-1`, search the left half: `right = mid - 1`.
- If `1`, search the right half: `left = mid + 1`.

Because each query cuts the search range in half, binary search guarantees finding the answer in at most:
$\lceil \log_2(2^{31} - 1) \rceil = \mathbf{31\text{ queries}}$!

---

### 🔬 The Ternary Search Trap

A classic interview debate:
*If dividing into 2 parts is fast, wouldn't dividing into 3 parts (Ternary Search) be faster?*

In Ternary Search:
- Pick two midpoints: $m_1$ and $m_2$ at the $1/3$ and $2/3$ marks.
- It shrinks the search space by a factor of $3$ on each round: $\log_3(n)$ rounds instead of $\log_2(n)$.

**Here is the catch:**
To choose which of the 3 segments holds the number, you must make **two API calls** per round (`guess(m1)` and `guess(m2)`).

The math reveals the truth:
- Binary Search worst-case calls: $\log_2(n) = \frac{\ln n}{\ln 2} \approx \mathbf{1.44 \ln n}$
- Ternary Search worst-case calls: $2 \log_3(n) = \frac{2 \ln n}{\ln 3} \approx \mathbf{1.82 \ln n}$

Ratio: $\frac{2 \ln 2}{\ln 3} \approx 1.262$.
**Ternary search makes 26.2% MORE API calls in the worst case!**

When API calls represent costly RPCs, network hops, or database lookups, Binary Search is strictly superior.

---

### 🐛 Engineering Quality: Dependency Injection

In early prototypes, developers often hardcode a global variable for testing `guess()`.
This breaks concurrent testing and pollutes state.
Adding dependency injection:
`def guess_number(n: int, guess_api: Callable[[int], int] = guess) -> int`
allows unit tests and property testing suites to pass custom oracles seamlessly.

---

### 📊 Complexity

- **Time:** O(log2 n) — at most 31 queries for a 32-bit integer
- **Space:** O(1) auxiliary space

---

### 🎯 Key Takeaway

Reducing a search range into more slices is only beneficial if the cost of slicing doesn't outpace the reduction. Binary search achieves the optimal balance between comparison cost and range reduction.

In Part 2, we explore the information-theoretic proof of why $k = 2$ is optimal and wrap interactive APIs with Python's `bisect`!

Have you ever encountered a problem where Ternary Search was actually optimal? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #LeetCode #SoftwareEngineering #CodingInterview
