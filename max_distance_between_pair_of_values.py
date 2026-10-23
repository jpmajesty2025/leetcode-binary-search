"""
LeetCode 1855: Maximum Distance Between a Pair of Values
https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/

You are given two non-increasing 0-indexed integer arrays nums1 and nums2.

A pair of indices (i, j), where 0 <= i < nums1.length and 0 <= j < nums2.length,
is valid if both i <= j and nums1[i] <= nums2[j]. The distance of the pair is j - i.

Return the maximum distance of any valid pair (i, j). If there are no valid pairs, return 0.
"""

from typing import List


def max_distance(nums1: List[int], nums2: List[int]) -> int:
    """
    Find the maximum distance of any valid pair (i, j) using Two Pointers.

    Because both nums1 and nums2 are non-increasing:
    As i increases, nums1[i] decreases. Any j that satisfied nums1[i_prev] <= nums2[j]
    will automatically satisfy nums1[i_curr] <= nums2[j]. Therefore, j never needs
    to backtrack.

    Complexity:
        Time: O(n + m) where n = len(nums1) and m = len(nums2)
        Space: O(1) auxiliary space
    """
    if not nums1 or not nums2:
        return 0

    max_dist = 0
    j = 0
    n2 = len(nums2)

    for i in range(len(nums1)):
        while j < n2 and nums1[i] <= nums2[j]:
            j += 1
        max_dist = max(max_dist, j - i - 1)

    return max_dist


class Solution:
    """LeetCode submission interface."""
    maxDistance = staticmethod(max_distance)
