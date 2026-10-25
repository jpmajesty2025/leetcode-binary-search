"""
LeetCode 2187: Minimum Time to Complete Trips
https://leetcode.com/problems/minimum-time-to-complete-trips/

You are given an array time where time[i] denotes the time taken by the ith bus to complete
one trip. Each bus can make multiple trips successively and operates independently.
You are also given an integer totalTrips, which denotes the number of trips all buses
should make in total.

Return the minimum time required for all buses to complete at least totalTrips trips.

Constraints:
- 1 <= time.length <= 10^5
- 1 <= time[i], totalTrips <= 10^7

Complexity:
- Time: O(N log(min(time) * totalTrips))
  - Bounds range: [1, min(time) * totalTrips]
  - Early-exit loop avoids completing the full summation once totalTrips is met.
- Space: O(1) auxiliary space
"""

from typing import List


def minimum_time(time: List[int], totalTrips: int) -> int:
    """
    Find minimum time using binary search on answer with optimal bounds and early exit.

    Search Space Bounds:
    - Lower Bound: At least 1. If all buses were as fast as the fastest bus min(time),
      the fleet would need at least max(1, ((totalTrips - 1) // len(time)) * min_time).
    - Upper Bound: If only the fastest bus operated, it would complete all totalTrips
      alone in min(time) * totalTrips. All other buses only accelerate completion.
      (Note: using max(time) * totalTrips needlessly inflates the search range by up
      to 10^7 times!).
    """
    min_t = min(time)
    n = len(time)

    # Tightened search interval
    left = max(1, ((totalTrips - 1) // n) * min_t)
    right = min_t * totalTrips

    def can_complete_trips(t_limit: int) -> bool:
        completed = 0
        for t in time:
            completed += t_limit // t
            if completed >= totalTrips:
                return True
        return False

    while left < right:
        mid = left + (right - left) // 2
        if can_complete_trips(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    minimumTime = staticmethod(minimum_time)
