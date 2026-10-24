"""
LeetCode 702: Search in a Sorted Array of Unknown Size (Bentley-Yao Galloping Search)
https://leetcode.com/problems/search-in-a-sorted-array-of-unknown-size/

Strategy:
Uses the classic Bentley-Yao Galloping Search (the same galloping strategy used
in Python's Timsort):
- Instead of doubling the absolute right boundary, maintain a base index `curr`
  and an exponential jump stride `step = 1, 2, 4, 8, ...`.
- Advance `curr += step` while reader.get(curr + step) < target.
- Once an overshoot occurs, binary search the bracketed segment [curr, curr + step].

Complexity:
- Time: O(log k), at most 2 * ceil(log2 k) calls.
- Space: O(1) auxiliary space.
"""

from typing import Protocol


class ArrayReader:
    """ArrayReader API specification."""

    def get(self, index: int) -> int:
        return -1


def search(reader: "ArrayReader", target: int) -> int:
    """
    Search using Bentley-Yao Galloping Jump Search.
    """
    curr = 0
    step = 1

    # Galloping phase
    while reader.get(curr + step) < target:
        curr += step
        step <<= 1

    # Binary search phase in [curr, curr + step]
    left = curr
    right = curr + step

    while left <= right:
        mid = left + (right - left) // 2
        mid_val = reader.get(mid)

        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
