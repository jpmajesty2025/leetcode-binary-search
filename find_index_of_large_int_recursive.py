"""
LeetCode 1533: Find the Index of the Large Integer (Recursive Divide-and-Conquer)
https://leetcode.com/problems/find-the-index-of-the-large-integer/

Strategy:
Formulates parity-aware binary search as a recursive divide-and-conquer function.
Call depth is at most 19 frames for N = 500,000, well within Python's recursion limit.

Complexity:
    Time: O(log2 n) calls, at most 19 calls
    Space: O(log n) call stack frames
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
    Find index of the larger integer using recursive divide-and-conquer.
    """
    def search(left: int, right: int) -> int:
        if left >= right:
            return left

        length = right - left + 1
        half = length // 2

        if length % 2 == 0:
            cmp = reader.compareSub(left, left + half - 1, left + half, right)
            if cmp == 1:
                return search(left, left + half - 1)
            else:
                return search(left + half, right)
        else:
            mid = left + half
            cmp = reader.compareSub(left, mid - 1, mid + 1, right)
            if cmp == 0:
                return mid
            elif cmp == 1:
                return search(left, mid - 1)
            else:
                return search(mid + 1, right)

    return search(0, reader.length() - 1)


class Solution:
    """LeetCode submission interface."""
    getIndex = staticmethod(get_index)
