"""
LeetCode 1533: Find the Index of the Large Integer (Ternary Balance-Scale Search)
https://leetcode.com/problems/find-the-index-of-the-large-integer/

Strategy:
Based on the classic Counterfeit Coin Balance-Scale Puzzle:
Given an interval of length L:
- If L == 1: return left.
- If L == 2: compare left with right using 1 call.
- If L >= 3: split into 3 parts:
    Part A: [left, left + k - 1]           (length k = L // 3)
    Part B: [left + k, left + 2 * k - 1]   (length k = L // 3)
    Part C: [left + 2 * k, right]          (length L - 2 * k)

Compare Part A and Part B using compareSub:
- If A > B (cmp == 1): the heavier integer is in Part A!
- If A < B (cmp == -1): the heavier integer is in Part B!
- If A == B (cmp == 0): neither A nor B has the heavier integer.
  It MUST be in Part C!

Why this beats Binary Search:
- In standard ternary search, each iteration needs 2 comparisons (2 * log3 n > log2 n).
- But here, because all other elements are IDENTICAL, a single comparison of A and B
  distinguishes between ALL THREE PARTS!
- Maximum calls for N = 500,000 drops from 19 calls (binary) to at most 13 calls (32% reduction!).

Complexity:
    Time: O(log3 n) calls, at most ceil(log3(500,000)) = 13 calls.
    Space: O(1) auxiliary space.
"""

from typing import Protocol


class ArrayReader(object):
    """ArrayReader API specification."""

    def compareSub(self, l: int, r: int, x: int, y: int) -> int:
        pass

    def length(self) -> int:
        pass


def get_index(reader: "ArrayReader") -> int:
    """
    Find index of the larger integer using 3-way balance scale search.
    """
    left, right = 0, reader.length() - 1

    while left < right:
        length = right - left + 1

        if length == 2:
            cmp = reader.compareSub(left, left, right, right)
            return left if cmp == 1 else right

        k = length // 3
        # Subarray A: [left, left + k - 1]
        # Subarray B: [left + k, left + 2 * k - 1]
        cmp = reader.compareSub(left, left + k - 1, left + k, left + 2 * k - 1)

        if cmp == 1:
            right = left + k - 1
        elif cmp == -1:
            left = left + k
            right = left + k - 1
        else:
            left = left + 2 * k

    return left


class Solution:
    """LeetCode submission interface."""
    getIndex = staticmethod(get_index)
