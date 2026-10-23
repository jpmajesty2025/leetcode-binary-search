"""
LeetCode 1855: Maximum Distance Between a Pair of Values (Standard Library bisect)
https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of indices range(i, len(nums2)).
Because nums2 is non-increasing, the condition:
    nums2[j] < nums1[i]
transitions monotonically from False to True:
    [False, False, ..., False, True, True, True]
bisect_left finds the first index where nums2[j] < nums1[i]; the element immediately
preceding it (idx - 1) is the rightmost valid index where nums2[j] >= nums1[i].

Complexity:
    Time: O(n log m)
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def max_distance(nums1: List[int], nums2: List[int]) -> int:
    """
    Find maximum distance using bisect_left with an inverted boolean key.
    """
    if not nums1 or not nums2:
        return 0

    max_dist = 0
    n1, n2 = len(nums1), len(nums2)

    for i in range(n1):
        if i + max_dist >= n2:
            break

        candidates = range(i, n2)
        idx = bisect.bisect_left(candidates, True, key=lambda j: nums2[j] < nums1[i])
        best_j = candidates[idx - 1] if idx > 0 else -1

        if best_j >= i and nums2[best_j] >= nums1[i]:
            max_dist = max(max_dist, best_j - i)

    return max_dist


class Solution:
    """LeetCode submission interface."""
    maxDistance = staticmethod(max_distance)
