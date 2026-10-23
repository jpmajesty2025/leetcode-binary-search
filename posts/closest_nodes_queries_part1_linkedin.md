# The Unbalanced Tree Trap: Closest Nodes in BST (Part 1 of 2) 🌲

**The Problem**:
You are given the root of a Binary Search Tree (BST) with up to $100,000$ nodes, and an array of up to $100,000$ queries.
For each query $q$, find:
1. **Floor**: The largest value in the tree $\le q$ (or `-1` if none).
2. **Ceiling**: The smallest value in the tree $\ge q$ (or `-1` if none).
Return the `[floor, ceiling]` pairs for all queries.

---

### 🧩 The Trap That Caught Thousands of Candidates

The immediate, intuitive approach sounds so simple:
*"It's a Binary Search Tree! Just traverse down from the root for each query. In a BST, finding floor and ceiling takes $O(\log n)$, so $m$ queries take $O(m \log n)$ time."*

**This intuition crashes into Time Limit Exceeded (TLE). Why?**
Look closely at the problem description:
It says you are given a *Binary Search Tree*.
It **never** says it is a *balanced* BST!

If the tree is skewed (e.g. $1 \to 2 \to 3 \to \dots \to 100,000$ in a single branch):
- Searching the tree for one query takes $O(n)$ time.
- For $m = 100,000$ queries, total operations reach $10^5 \times 10^5 = \mathbf{10^{10}\text{ operations}}$!
That will TLE in every programming language.

---

### 🔧 The Solution: Flatten Once, Search Forever

Never search an unverified BST directly when handling multiple queries!
1. **Flatten the BST into a sorted array**:
   An in-order traversal of any BST produces elements in strictly ascending order in **O(n)** time.
2. **Binary search the array**:
   Because the array is guaranteed to be flat and sorted, binary search runs in strictly **O(log n)** time per query, regardless of how skewed the tree was!

Total complexity drops from $O(m \cdot n)$ to **O(n + m log n)**!

---

### 🐛 The Silent RecursionError Bug

Many Python developers implement in-order traversal recursively.
On a skewed tree with $100,000$ nodes, recursive traversal crashes with:
`RecursionError: maximum recursion depth exceeded` (default limit is $1,000$).

**The Fix**:
Always use an **iterative in-order traversal with an explicit stack**. It runs entirely on the heap and handles $100,000$ depth without sweating.

---

### 📊 Complexity

- **Time:** O(n + m log n)
- **Space:** O(n) for the sorted values array and traversal stack

---

### 🎯 Key Takeaway

Never assume a BST is balanced unless explicitly stated. When an algorithm demands multiple queries on an arbitrary BST, flatten it to a sorted array first to decouple query performance from tree height.

In Part 2, we benchmark standard while-loops against Python's `bisect` and Morris Traversal for a **3.7x speedup**!

Have you ever fallen into the "unbalanced BST" time complexity trap? Let's discuss below! 👇

#LearningInPublic #Python #Algorithms #DataStructures #BinarySearch #BinarySearchTree #LeetCode #CodingInterview
