"""
LeetCode 35: Search Insert Position (Standard Library bisect)
https://leetcode.com/problems/search-insert-position/

Strategy:
Uses Python's standard library bisect.bisect_left.
Since bisect_left returns the leftmost insertion point for target to maintain
sorted order, it directly solves LeetCode 35 in a single compiled-C function call.

Complexity:
    Time: O(log n)
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def search_insert(nums: List[int], target: int) -> int:
    """
    Find insertion position using C-speed bisect_left.
    """
    return bisect.bisect_left(nums, target)


class Solution:
    """LeetCode submission interface."""
    searchInsert = staticmethod(search_insert)
