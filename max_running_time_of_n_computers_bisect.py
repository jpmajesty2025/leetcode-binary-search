"""
LeetCode 2141: Maximum Running Time of N Computers
https://leetcode.com/problems/maximum-running-time-of-n-computers/

Bisect + Prefix Sums Implementation:
Accelerates the predicate evaluation from O(M) linear scan to O(log M) binary search.

Complexity:
- Time: O(M log M + log(sum(batteries) // n) * log M)
  - Sorting: O(M log M)
  - Prefix Sum computation: O(M)
  - Binary search iterations: O(log(sum(batteries) // n)) (~47 iterations)
  - Predicate evaluation via bisect_left: O(log M)
- Space: O(M) for prefix sums and sorted array
"""

import bisect
from typing import List


def max_run_time(n: int, batteries: List[int]) -> int:
    """
    Find maximum runtime using binary search on answer with bisect and prefix sums.

    Predicate Acceleration:
    With sorted batteries and prefix sums:
    - Batteries < mid are located at indices [0, idx - 1] via bisect_left(batteries, mid).
      Their sum is prefix[idx].
    - Batteries >= mid are located at indices [idx, M - 1].
      Each battery contributes mid minutes, totaling (M - idx) * mid.
    - Total usable energy = prefix[idx] + (M - idx) * mid in O(log M) time!
    """
    sorted_batteries = sorted(batteries)
    m = len(sorted_batteries)

    prefix = [0] * (m + 1)
    for i, b in enumerate(sorted_batteries):
        prefix[i + 1] = prefix[i] + b

    total = prefix[m]
    left, right = 1, total // n

    while left < right:
        mid = (left + right + 1) // 2
        idx = bisect.bisect_left(sorted_batteries, mid)
        usable = prefix[idx] + (m - idx) * mid

        if usable >= mid * n:
            left = mid
        else:
            right = mid - 1

    return left


class Solution:
    """LeetCode submission interface."""
    maxRunTime = staticmethod(max_run_time)
