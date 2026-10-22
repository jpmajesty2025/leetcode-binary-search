"""
LeetCode 1231: Divide Chocolate (Prefix Sums + Binary Jump)
https://leetcode.com/problems/divide-chocolate/

Strategy:
When k is much smaller than n (k << n), scanning all n elements in every feasibility
check is wasteful.
Instead:
1. Precompute prefix sums of sweetness once in O(n).
2. For candidate sweetness target, use bisect.bisect_left on prefix_sums to jump directly
   to the next valid cut index in O(log n).
3. Repeating this k + 1 times verifies feasibility in O(k log n) time per check.

Complexity:
    Time: O(n + (k log n) * log(total // (k + 1)))
    Space: O(n) auxiliary space for prefix sums
"""

import bisect
import itertools
from typing import List


def maximize_sweetness(sweetness: List[int], k: int) -> int:
    """
    Compute maximum sweetness using prefix-sum binary jumping.
    Runs in O(k log n) per binary search step instead of O(n).
    """
    if not sweetness:
        return 0

    n = len(sweetness)
    if k == 0:
        return sum(sweetness)
    if k + 1 == n:
        return min(sweetness)

    prefix_sums = list(itertools.accumulate(sweetness))
    total_sweetness = prefix_sums[-1]

    left = min(sweetness)
    right = total_sweetness // (k + 1)
    needed_pieces = k + 1

    def can_divide(target: int) -> bool:
        pieces = 0
        curr_offset = 0

        while pieces < needed_pieces:
            target_sum = curr_offset + target
            idx = bisect.bisect_left(prefix_sums, target_sum)
            if idx == n:
                return False
            pieces += 1
            curr_offset = prefix_sums[idx]

        return True

    while left < right:
        mid = (left + right + 1) // 2
        if can_divide(mid):
            left = mid
        else:
            right = mid - 1

    return left


class Solution:
    """LeetCode submission interface."""
    maximizeSweetness = staticmethod(maximize_sweetness)
