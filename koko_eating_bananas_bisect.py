"""
LeetCode 875: Koko Eating Bananas (Standard Library bisect)
https://leetcode.com/problems/koko-eating-bananas/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual speed range range(left, right + 1).
The feasibility predicate can_finish(k) evaluates to False for speeds that are too slow,
and True once the speed is sufficient.
Because False < True in Python booleans, the sequence is monotonically sorted.
bisect_left searches for True to find the minimal viable speed in C speed.

Complexity:
    Time: O(n log(max(piles)))
    Space: O(1) auxiliary space
"""

import bisect
import math
from typing import List


def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Find minimum speed using bisect_left with a monotonic boolean key function.
    """
    if not piles:
        return 0

    n = len(piles)
    max_pile = max(piles)

    if n == h:
        return max_pile

    left = max(1, (sum(piles) + h - 1) // h)
    right = max_pile

    speeds = range(left, right + 1)
    idx = bisect.bisect_left(
        speeds,
        True,
        key=lambda k: sum(math.ceil(p / k) for p in piles) <= h,
    )

    return speeds[idx]


class Solution:
    """LeetCode submission interface."""
    minEatingSpeed = staticmethod(min_eating_speed)
