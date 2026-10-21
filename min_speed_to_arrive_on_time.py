"""
LeetCode 1870: Minimum Speed to Arrive on Time
https://leetcode.com/problems/minimum-speed-to-arrive-on-time/

You are given a floating-point number hour, representing the amount of time you have to reach
the office. To commute to the office, you must take n trains in sequential order. You are also
given an integer array dist of length n, where dist[i] describes the distance (in kilometers)
of the ith train ride.

Each train can only depart at an integer hour, so you may need to wait in between each train
ride (except the final train, which arrives at the destination).

Return the minimum positive integer speed (in kilometers per hour) that all the trains must
travel at for you to reach the office on time, or -1 if it is impossible to be on time.
"""

from typing import List


def min_speed_on_time(dist: List[int], hour: float) -> int:
    """
    Compute minimum speed using Binary Search on Answer.

    Crucial Edge Case:
    - The first n - 1 trains each take at least 1 hour (due to integer departure times).
    - The last train requires > 0 time.
    - Therefore, if hour <= n - 1, it is mathematically impossible; return -1.
    - Note: hour can be strictly between n - 1 and n (e.g., n = 3, hour = 2.7 is solvable).

    Complexity:
        Time: O(n log(max_speed)) where max_speed = 10^7
        Space: O(1) auxiliary space
    """
    if not dist:
        return -1

    n = len(dist)
    # The first n - 1 trains take at least n - 1 hours.
    if hour <= n - 1:
        return -1

    first_trains = dist[:-1]
    last_train = dist[-1]

    left = 1
    right = 10**7

    def can_reach_office(speed: int) -> bool:
        # First n - 1 trains use exact integer ceiling division
        time_taken = sum((d + speed - 1) // speed for d in first_trains) + last_train / speed
        return time_taken <= hour

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
