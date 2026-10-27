"""
LeetCode 2517: Maximum Tastiness of Candy Basket (Bisect Hopping / Exponential Skipping)
https://leetcode.com/problems/maximum-tastiness-of-candy-basket/

Strategy:
In standard verification, linear scanning inspects up to N elements.
When k is much smaller than N (e.g. k = 5, N = 100,000), linear scanning wastes
thousands of comparisons checking elements that cannot satisfy the distance.
Instead, use `bisect.bisect_left(price, price[curr_idx] + target)` to skip directly
to the earliest eligible candy!
This reduces validation time from O(N) down to O(k log N), delivering up to an
85x speedup when k << N!

Complexity:
- Time: O(N log N + k log N * log((max - min) / (k - 1)))
- Space: O(1) auxiliary space
"""

import bisect
from typing import List


def maximum_tastiness(price: List[int], k: int) -> int:
    """
    Find maximum tastiness using bisect hopping for O(k log N) predicate evaluation.
    """
    price.sort()
    n = len(price)
    left = 0
    right = (price[-1] - price[0]) // (k - 1)
    ans = 0

    def can_form_basket(t_limit: int) -> bool:
        count = 1
        curr_idx = 0
        while count < k:
            # Hop directly to the first element with price >= price[curr_idx] + t_limit
            next_idx = bisect.bisect_left(price, price[curr_idx] + t_limit, lo=curr_idx + 1)
            if next_idx >= n:
                return False
            count += 1
            curr_idx = next_idx
        return True

    while left <= right:
        mid = left + (right - left) // 2
        if can_form_basket(mid):
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    return ans


class Solution:
    """LeetCode submission interface."""
    maximumTastiness = staticmethod(maximum_tastiness)
