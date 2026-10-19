"""
LeetCode 35: Search Insert Position (Half-Open Interval Lower Bound)
https://leetcode.com/problems/search-insert-position/

Strategy:
Uses the canonical half-open interval [left, right) lower-bound pattern:
- Initial bounds: left = 0, right = len(nums)
- Invariant: nums[:left] < target and nums[right:] >= target
- Search space length: right - left
- Loop condition: while left < right
- Each iteration performs exactly ONE comparison (nums[mid] < target),
  halving the search range until left == right.

This is the exact algorithm underlying C++ std::lower_bound and Python bisect.bisect_left.

Complexity:
    Time: O(log n)
    Space: O(1) auxiliary space
"""

from typing import List


def search_insert(nums: List[int], target: int) -> int:
    """
    Find insertion position using half-open interval [left, right) lower-bound search.
    """
    left, right = 0, len(nums)

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


class Solution:
    """LeetCode submission interface."""
    searchInsert = staticmethod(search_insert)
