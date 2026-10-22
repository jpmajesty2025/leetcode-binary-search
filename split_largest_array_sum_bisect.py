"""
LeetCode 410: Split Array Largest Sum (Standard Library bisect)
https://leetcode.com/problems/split-array-largest-sum/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of candidate max sums:
    range(left, right + 1)
with a monotonic boolean feasibility key:
    can_split(max_sum) -> bool
which transitions monotonically from False to True.
bisect_left locates the minimum feasible largest sum in C speed.

Complexity:
    Time: O(n log(sum(nums) - max(nums)))
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def split_array(nums: List[int], k: int) -> int:
    """
    Find minimized largest sum using bisect_left with a monotonic boolean key function.
    """
    if not nums:
        return 0

    n = len(nums)
    if k == 1:
        return sum(nums)
    if k == n:
        return max(nums)

    total_sum = sum(nums)
    left = max(max(nums), (total_sum + k - 1) // k)
    right = total_sum

    def can_split(max_sum: int) -> bool:
        current_sum = 0
        subarrays = 1
        for num in nums:
            current_sum += num
            if current_sum > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
        return True

    candidates = range(left, right + 1)
    idx = bisect.bisect_left(candidates, True, key=can_split)

    return candidates[idx]


class Solution:
    """LeetCode submission interface."""
    splitArray = staticmethod(split_array)
