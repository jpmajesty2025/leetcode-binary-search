"""
LeetCode 1870: Minimum Speed to Arrive on Time (Standard Library bisect)
https://leetcode.com/problems/minimum-speed-to-arrive-on-time/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of speeds range(1, 10**7 + 1)
with a monotonic boolean feasibility key function.
Returns the smallest speed where can_reach(speed) evaluates to True, or -1.

Complexity:
    Time: O(n log(max_speed)) where max_speed = 10^7
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def min_speed_on_time(dist: List[int], hour: float) -> int:
    """
    Find minimum speed using bisect_left with a monotonic boolean key function.
    """
    if not dist:
        return -1

    n = len(dist)
    if hour <= n - 1:
        return -1

    first_trains = dist[:-1]
    last_train = dist[-1]

    speeds = range(1, 10**7 + 1)

    idx = bisect.bisect_left(
        speeds,
        True,
        key=lambda s: sum((d + s - 1) // s for d in first_trains) + last_train / s <= hour,
    )

    if idx < len(speeds):
        return speeds[idx]
    return -1


class Solution:
    """LeetCode submission interface."""
    minSpeedOnTime = staticmethod(min_speed_on_time)
