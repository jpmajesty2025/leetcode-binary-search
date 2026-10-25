"""
LeetCode 33: Search in Rotated Sorted Array (Cyclic Modulo Transformation)
https://leetcode.com/problems/search-in-rotated-sorted-array/

Strategy:
Treats rotation as a circular shift in index space:
1. Locate the pivot index P (minimum element index) in O(log n).
2. In the virtual sorted space [0, n - 1], virtual index `i` maps to real index:
   real_index = (i + P) % n
3. Run unmodified standard binary search over virtual index space [0, n - 1]:
   Access nums[(mid + P) % n] as if the array were completely unrotated!

Complexity:
- Time: O(log n)
- Space: O(1)
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search using cyclic modulo index mapping.
    """
    n = len(nums)
    if not nums:
        return -1

    # Find pivot
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    pivot = left

    # Binary search in virtual sorted coordinate space
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        real_mid = (mid + pivot) % n

        if nums[real_mid] == target:
            return real_mid
        elif nums[real_mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
