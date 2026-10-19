"""
LeetCode 875: Koko Eating Bananas
https://leetcode.com/problems/koko-eating-bananas/

Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas.
The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile
of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats
all of them instead and will not eat any more bananas during this hour.

Return the minimum integer k such that she can eat all the bananas within h hours.
"""

import math
from typing import List


def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Compute minimum eating speed k using Binary Search on Answer.

    Optimizations:
    - If len(piles) == h: Koko has exactly 1 hour per pile, so she must eat at
      max(piles) bananas per hour (O(1) after finding max).
    - Tight lower bound: Koko cannot finish if speed < ceil(sum(piles) / h).
    - Monotonic feasibility predicate: hours(k) is non-increasing as k increases.

    Complexity:
        Time: O(n log(max(piles) - sum(piles)//h + 1))
        Space: O(1) auxiliary space
    """
    if not piles:
        return 0

    n = len(piles)
    max_pile = max(piles)

    # Fast-path: exactly 1 hour available per pile
    if n == h:
        return max_pile

    # Tight lower bound based on total bananas
    left = max(1, (sum(piles) + h - 1) // h)
    right = max_pile

    while left < right:
        mid = (left + right) // 2
        total_hours = sum(math.ceil(p / mid) for p in piles)

        if total_hours <= h:
            right = mid  # mid is feasible; try smaller speeds
        else:
            left = mid + 1  # mid is too slow; increase speed

    return left


class Solution:
    """LeetCode submission interface."""
    minEatingSpeed = staticmethod(min_eating_speed)
