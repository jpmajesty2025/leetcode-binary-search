"""
LeetCode 2517: Maximum Tastiness of Candy Basket (Monotonic Failure View + Bisect)
https://leetcode.com/problems/maximum-tastiness-of-candy-basket/

Strategy:
The predicate can_form_basket(t) is monotonically non-increasing:
    [True, True, ..., True, False, False, ..., False]
Inverting the predicate produces a monotonically non-decreasing boolean sequence:
    failure_view[t] = (not can_form_basket(t))
    [False, False, ..., False, True, True, ..., True]

Finding the maximum tastiness is equivalent to finding the FIRST True (first failure)
minus 1, which Python's C-accelerated `bisect.bisect_left` executes directly!

Complexity:
- Time: O(N log N + N log((max - min) / (k - 1)))
- Space: O(1) auxiliary space (zero-allocation virtual view)
"""

import bisect
from typing import List


class TastinessFailureView:
    """Virtual monotonic sequence mapping candidate tastiness to failure booleans."""

    __slots__ = ("price", "k", "n")

    def __init__(self, price: List[int], k: int):
        self.price = price
        self.k = k
        self.n = len(price)

    def __getitem__(self, t_limit: int) -> bool:
        if t_limit <= 0:
            return False

        count = 1
        last_price = self.price[0]
        for p in self.price[1:]:
            if p - last_price >= t_limit:
                count += 1
                last_price = p
                if count >= self.k:
                    return False  # Succeeded -> Failure is False

        return True  # Failed -> Failure is True


def maximum_tastiness(price: List[int], k: int) -> int:
    """
    Find maximum tastiness using monotonic failure view and bisect.bisect_left.
    """
    price.sort()
    right = (price[-1] - price[0]) // (k - 1)

    view = TastinessFailureView(price, k)
    # Search range: [0, right + 1]
    first_failure = bisect.bisect_left(view, True, lo=0, hi=right + 1)
    return first_failure - 1


class Solution:
    """LeetCode submission interface."""
    maximumTastiness = staticmethod(maximum_tastiness)
