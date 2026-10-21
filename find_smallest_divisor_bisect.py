"""
LeetCode 1283: Find the Smallest Divisor Given a Threshold (Standard Library bisect)
https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of candidate divisors:
    range(left, right + 1)
with a monotonic boolean feasibility key:
    lambda d: sum((x + d - 1) // d for x in nums) <= threshold

Complexity:
    Time: O(n log(max_num))
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def smallest_divisor(nums: List[int], threshold: int) -> int:
    """
    Find smallest divisor using bisect_left with a monotonic boolean key function.
    """
    if not nums:
        return 1

    n = len(nums)
    max_num = max(nums)

    if threshold == n:
        return max_num

    left = max(1, (sum(nums) + threshold - 1) // threshold)
    right = max_num

    divisors = range(left, right + 1)
    idx = bisect.bisect_left(
        divisors,
        True,
        key=lambda d: sum((x + d - 1) // d for x in nums) <= threshold,
    )

    return divisors[idx]


class Solution:
    """LeetCode submission interface."""
    smallestDivisor = staticmethod(smallest_divisor)
