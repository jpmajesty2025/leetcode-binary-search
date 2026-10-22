"""
LeetCode 1231: Divide Chocolate (Standard Library bisect)
https://leetcode.com/problems/divide-chocolate/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of candidate sweetness levels:
    range(left, right + 1)
Because we want the MAXIMUM feasible sweetness, we invert the feasibility predicate:
    cannot_divide(target)
which transitions monotonically from False to True.
bisect_left finds the first infeasible target; the answer is the target right before it.

Complexity:
    Time: O(n log(total // (k + 1)))
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def maximize_sweetness(sweetness: List[int], k: int) -> int:
    """
    Find maximum sweetness using bisect_left with an inverted boolean key function.
    """
    if not sweetness:
        return 0

    n = len(sweetness)
    if k == 0:
        return sum(sweetness)
    if k + 1 == n:
        return min(sweetness)

    left = min(sweetness)
    right = sum(sweetness) // (k + 1)
    needed_pieces = k + 1

    def cannot_divide(target: int) -> bool:
        curr = 0
        pieces = 0
        for s in sweetness:
            curr += s
            if curr >= target:
                pieces += 1
                if pieces == needed_pieces:
                    return False
                curr = 0
        return True

    targets = range(left, right + 1)
    idx = bisect.bisect_left(targets, True, key=cannot_divide)

    return targets[idx - 1] if idx > 0 else left


class Solution:
    """LeetCode submission interface."""
    maximizeSweetness = staticmethod(maximize_sweetness)
