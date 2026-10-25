"""
LeetCode 2187: Minimum Time to Complete Trips (Frequency-Compressed Evaluation)
https://leetcode.com/problems/minimum-time-to-complete-trips/

Strategy:
In many practical workloads with N = 10^5 buses, bus durations repeat frequently
(e.g., small integer durations).
By compressing duplicate durations into frequency counts:
    counts = Counter(time).items()
Each verification step calculates:
    completed += (mid // t) * count
This reduces inner-loop iterations from N down to the number of UNIQUE durations,
yielding up to an order-of-magnitude speedup!

Complexity:
- Time: O(N + U * log(min(time) * totalTrips)), where U is the number of unique durations (U <= N)
- Space: O(U) auxiliary space
"""

from collections import Counter
from typing import List


def minimum_time(time: List[int], totalTrips: int) -> int:
    """
    Find minimum time using frequency-compressed binary search on answer.
    """
    min_t = min(time)
    n = len(time)

    # Pre-aggregate bus durations
    counts = list(Counter(time).items())

    left = max(1, ((totalTrips - 1) // n) * min_t)
    right = min_t * totalTrips

    while left < right:
        mid = left + (right - left) // 2

        completed = 0
        for t, cnt in counts:
            completed += (mid // t) * cnt
            if completed >= totalTrips:
                break

        if completed >= totalTrips:
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    minimumTime = staticmethod(minimum_time)
