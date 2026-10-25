"""
LeetCode 33: Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array nums sorted in ascending order (with distinct values).
Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k.
Given the array nums after the possible rotation and an integer target, return the index of
target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity and O(1) space complexity.

Complexity:
- Time: O(log n) comparisons
- Space: O(1) auxiliary space
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search for target in a rotated sorted array using One-Pass Modified Binary Search.

    The Monotonic Half Invariant:
    In any rotated sorted array with distinct values, dividing the array at `mid` guarantees
    that at least ONE half ([left, mid] or [mid, right]) is strictly sorted and monotonic:
    1. If nums[left] <= nums[mid]:
       The left half [left, mid] is strictly sorted.
       - If nums[left] <= target < nums[mid]: target is inside the left half -> search left.
       - Otherwise: target must be in the right half -> search right.
    2. Else (nums[left] > nums[mid]):
       The right half [mid, right] is strictly sorted.
       - If nums[mid] < target <= nums[right]: target is inside the right half -> search right.
       - Otherwise: target must be in the left half -> search left.
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Check if left half is strictly sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Otherwise, right half is strictly sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
