"""
LeetCode 540: Single Element in a Sorted Array
https://leetcode.com/problems/single-element-in-a-sorted-array/

You are given a sorted array consisting of only integers where every element appears exactly twice,
except for one element which appears exactly once.
Return the single element that appears only once.

Your solution must run in O(log n) time and O(1) space.

Complexity:
- Time: O(log n) comparisons
- Space: O(1) auxiliary space
"""

from typing import List


def single_non_duplicate(nums: List[int]) -> int:
    """
    Find the single non-duplicate element using Parity-Normalized Binary Search.

    The Parity Invariant:
    - Before the single element:
      Every pair begins at an EVEN index and ends at an ODD index:
      nums[2k] == nums[2k + 1]
    - After the single element:
      The disruption shifts every subsequent pair by 1, so pairs begin at an ODD index:
      nums[2k + 1] == nums[2k + 2]

    By normalizing mid to always be even (if mid % 2 == 1: mid -= 1):
    - If nums[mid] == nums[mid + 1]: the disruption has not occurred yet.
      The single element must be strictly to the right: left = mid + 2.
    - If nums[mid] != nums[mid + 1]: the disruption has already occurred.
      The single element is at mid or to the left: right = mid.
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        # Normalize mid to even index to test pair start
        if mid % 2 == 1:
            mid -= 1

        if nums[mid] == nums[mid + 1]:
            left = mid + 2
        else:
            right = mid

    return nums[left]


class Solution:
    """LeetCode submission interface."""
    singleNonDuplicate = staticmethod(single_non_duplicate)
