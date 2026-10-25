"""
LeetCode 33: Search in Rotated Sorted Array (Two-Pass Pivot Finding + Bisect)
https://leetcode.com/problems/search-in-rotated-sorted-array/

Strategy:
Decouples inflection-point detection from target searching:
1. Pass 1: Find the pivot index (index of the minimum element, LeetCode 153 logic)
   using binary search in O(log n) time.
2. Segment Selection: Check whether target belongs to the left sorted segment
   [0, pivot - 1] or the right sorted segment [pivot, n - 1].
3. Pass 2: Run Python's C-accelerated `bisect.bisect_left` directly over the chosen
   strictly sorted subarray!

Complexity:
- Time: O(log n) comparisons (O(log n) to find pivot + O(log n) for bisect)
- Space: O(1) auxiliary space
"""

import bisect
from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search by first locating the pivot, then binary searching the active monotonic segment.
    """
    n = len(nums)
    if not nums:
        return -1

    # Pass 1: Find pivot (minimum element index)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    pivot = left

    # Pass 2: Select monotonic segment
    if pivot == 0:
        lo, hi = 0, n - 1
    elif target >= nums[0]:
        lo, hi = 0, pivot - 1
    else:
        lo, hi = pivot, n - 1

    idx = bisect.bisect_left(nums, target, lo=lo, hi=hi + 1)
    if idx <= hi and nums[idx] == target:
        return idx

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
