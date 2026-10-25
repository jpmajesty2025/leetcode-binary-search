"""
LeetCode 33: Search in Rotated Sorted Array (Inflection Shift / Virtual Infinity)
https://leetcode.com/problems/search-in-rotated-sorted-array/

Strategy:
Transforms the piecewise-monotonic rotated array into an infinitely extended monotonic line:
1. Determine if `target` resides on the left sorted segment (target >= nums[0])
   or the right segment (target < nums[0]).
2. At each step, test if `nums[mid]` is on the same segment as `target`:
   - If YES: compare `nums[mid]` directly against `target`.
   - If NO:
     - If target is on the left segment, but mid is on the right segment:
       mid is ahead in index space, but smaller in value -> treat mid as +inf
       so binary search branches left (right = mid - 1).
     - If target is on the right segment, but mid is on the left segment:
       mid is behind in index space, but larger in value -> treat mid as -inf
       so binary search branches right (left = mid + 1).

This maps the disjoint rotated intervals into a single continuous monotonic sequence!

Complexity:
- Time: O(log n)
- Space: O(1)
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search using inflection-shifted virtual infinity mapping.
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1
    v0 = nums[0]
    is_target_left = (target >= v0)

    while left <= right:
        mid = left + (right - left) // 2
        v_mid = nums[mid]
        is_mid_left = (v_mid >= v0)

        if is_mid_left == is_target_left:
            comp = v_mid
        else:
            comp = float("inf") if is_target_left else float("-inf")

        if comp == target:
            return mid
        elif comp < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
