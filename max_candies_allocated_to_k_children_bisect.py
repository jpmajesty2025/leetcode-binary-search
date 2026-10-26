"""
LeetCode 2226: Maximum Candies Allocated to K Children (Monotonic Failure View + Bisect)
https://leetcode.com/problems/maximum-candies-allocated-to-k-children/

Strategy:
The allocation feasibility predicate can_allocate(c) is monotonically non-increasing:
    [True, True, ..., True, False, False, ..., False]
Inverting the predicate produces a monotonically non-decreasing boolean sequence:
    failure_view[c] = (not can_allocate(c))
    [False, False, ..., False, True, True, ..., True]

Finding the maximum feasible candies is equivalent to finding the FIRST True (first failure)
minus 1, which Python's C-accelerated `bisect.bisect_left` executes directly!

Complexity:
- Time: O(N log(sum(candies) // k))
- Space: O(1) auxiliary space (zero-allocation virtual view)
"""

import bisect
from typing import List


class AllocationFailureView:
    """Virtual monotonic sequence mapping candy allocation sizes to failure booleans."""

    __slots__ = ("candies", "k")

    def __init__(self, candies: List[int], k: int):
        self.candies = candies
        self.k = k

    def __getitem__(self, c: int) -> bool:
        if c == 0:
            return False

        allocated = 0
        for pile in self.candies:
            allocated += pile // c
            if allocated >= self.k:
                return False  # Allocation succeeded -> Failure is False

        return True  # Allocation failed -> Failure is True


def maximum_candies(candies: List[int], k: int) -> int:
    """
    Find maximum candies using monotonic failure sequence and bisect.bisect_left.
    """
    total = sum(candies)
    if total < k:
        return 0

    view = AllocationFailureView(candies, k)
    # Search range: [1, total // k + 1]
    first_failure = bisect.bisect_left(view, True, lo=1, hi=total // k + 1)
    return first_failure - 1


class Solution:
    """LeetCode submission interface."""
    maximumCandies = staticmethod(maximum_candies)
