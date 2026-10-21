"""
LeetCode 1870: Minimum Speed to Arrive on Time (Pure Scaled Integer Arithmetic)
https://leetcode.com/problems/minimum-speed-to-arrive-on-time/

Strategy:
Because hour has at most two digits after the decimal point, we can scale
the inequality by 100 * speed to eliminate all floating-point math:
    sum(ceil(dist[i] / speed)) + dist[-1] / speed <= hour
Multiplying both sides by 100 * speed:
    100 * (sum_int_hours * speed + dist[-1]) <= round(hour * 100) * speed

This completely eliminates IEEE 754 floating-point roundoff errors.

Complexity:
    Time: O(n log(max_speed)) where max_speed = 10^7
    Space: O(1) auxiliary space
"""

from typing import List


def min_speed_on_time(dist: List[int], hour: float) -> int:
    """
    Compute minimum speed using pure scaled integer arithmetic.
    """
    if not dist:
        return -1

    n = len(dist)
    if hour <= n - 1:
        return -1

    first_trains = dist[:-1]
    last_train = dist[-1]
    hour_scaled = round(hour * 100)

    left = 1
    right = 10**7

    def can_reach_office(speed: int) -> bool:
        int_hours = sum((d + speed - 1) // speed for d in first_trains)
        return 100 * (int_hours * speed + last_train) <= hour_scaled * speed

    while left < right:
        mid = (left + right) // 2
        if can_reach_office(mid):
            right = mid
        else:
            left = mid + 1

    return left if can_reach_office(left) else -1


class Solution:
    """LeetCode submission interface."""
    minSpeedOnTime = staticmethod(min_speed_on_time)
