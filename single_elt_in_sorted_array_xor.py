"""
LeetCode 540: Single Element in a Sorted Array (XOR Partner Symmetry Search)
https://leetcode.com/problems/single-element-in-a-sorted-array/

Strategy:
Uses the bitwise identity `k ^ 1` to find an index's expected partner:
- If k is even: k ^ 1 == k + 1 (its right partner)
- If k is odd:  k ^ 1 == k - 1 (its left partner)

Therefore:
`nums[mid] == nums[mid ^ 1]`
simultaneously checks whether an even mid is paired with its right neighbor,
OR an odd mid is paired with its left neighbor!

- If True: the pair is intact; the disruption lies strictly to the right:
  left = mid + 1
- If False: the pair is broken; the disruption lies at mid or to the left:
  right = mid

Complexity:
- Time: O(log n)
- Space: O(1)
"""

from typing import List


def single_non_duplicate(nums: List[int]) -> int:
    """
    Find single element using branchless XOR partner checking.
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] == nums[mid ^ 1]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


class Solution:
    """LeetCode submission interface."""
    singleNonDuplicate = staticmethod(single_non_duplicate)
