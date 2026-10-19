"""
LeetCode 35: Search Insert Position
https://leetcode.com/problems/search-insert-position/

Given a sorted array of distinct integers and a target value, return the index
if the target is found. If not, return the index where it would be if it were
inserted in order.

You must write an algorithm with O(log n) runtime complexity and O(1) auxiliary space.
"""

from typing import List


def search_insert(nums: List[int], target: int) -> int:
    """
    Find insertion index of target in sorted distinct array nums in O(log n) time.

    Uses closed-interval [left, right] binary search.
    Invariant: nums[:left] < target and nums[right + 1:] >= target.
    Upon loop termination (left > right), left is the exact lower-bound index.
    """
    if not nums or target <= nums[0]:
        return 0
    if target > nums[-1]:
        return len(nums)

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left


class Solution:
    """LeetCode submission interface."""
    searchInsert = staticmethod(search_insert)
