"""
LeetCode 875: Koko Eating Bananas (Pure Integer Math & Early Termination)
https://leetcode.com/problems/koko-eating-bananas/

Strategy:
1. Replaces floating-point math.ceil(p / k) with pure integer ceiling division:
   (p + k - 1) // k
   This eliminates float conversion overhead and avoids potential floating-point
   precision limits on huge integers.
2. Short-circuits the hours sum early: as soon as running_hours exceeds h,
   we immediately break out of the loop without checking remaining piles.

Complexity:
    Time: O(n log(max(piles)))
    Space: O(1) auxiliary space
"""

from typing import List


def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Compute minimum speed using pure integer arithmetic and early loop break.
    """
    if not piles:
        return 0

    n = len(piles)
    max_pile = max(piles)

    if n == h:
        return max_pile

    left = max(1, (sum(piles) + h - 1) // h)
    right = max_pile

    while left < right:
        mid = (left + right) // 2

        # Accumulate hours with early termination
        total_hours = 0
        for p in piles:
            total_hours += (p + mid - 1) // mid
            if total_hours > h:
                break

        if total_hours <= h:
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    minEatingSpeed = staticmethod(min_eating_speed)
