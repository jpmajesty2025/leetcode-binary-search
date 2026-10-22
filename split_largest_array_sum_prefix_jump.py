"""
LeetCode 410: Split Array Largest Sum (Prefix Sums + Binary Jump)
https://leetcode.com/problems/split-array-largest-sum/

Strategy:
When k is much smaller than n (k << n), scanning all n elements in every feasibility
check is wasteful.
Instead:
1. Precompute prefix sums of nums in O(n).
2. For candidate max_sum, use bisect.bisect_right on prefix_sums to find the furthest
   element that fits in the current subarray in O(log n).
3. Repeating this at most k times verifies feasibility in O(k log n) time per check.

Complexity:
    Time: O(n + (k log n) * log(sum(nums) - max(nums)))
    Space: O(n) auxiliary space for prefix sums
"""

import bisect
import itertools
from typing import List


def split_array(nums: List[int], k: int) -> int:
    """
    Compute minimized largest subarray sum using prefix-sum binary jumping.
    Runs in O(k log n) per binary search step instead of O(n).
    """
    if not nums:
        return 0

    n = len(nums)
    if k == 1:
        return sum(nums)
    if k == n:
        return max(nums)

    prefix_sums = list(itertools.accumulate(nums))
    total_sum = prefix_sums[-1]
    max_num = max(nums)

    left = max(max_num, (total_sum + k - 1) // k)
    right = total_sum

    def can_split(max_sum: int) -> bool:
        subarrays = 0
        curr_offset = 0

        while curr_offset < total_sum:
            subarrays += 1
            if subarrays > k:
                return False

            target = curr_offset + max_sum
            idx = bisect.bisect_right(prefix_sums, target)
            if idx == 0 or prefix_sums[idx - 1] <= curr_offset:
                return False
            curr_offset = prefix_sums[idx - 1]

        return True

    while left < right:
        mid = (left + right) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    splitArray = staticmethod(split_array)
