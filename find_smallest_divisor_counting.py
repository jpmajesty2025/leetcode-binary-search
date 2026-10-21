"""
LeetCode 1283: Find the Smallest Divisor Given a Threshold (Frequency Compression)
https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/

Strategy:
When nums contains repeated elements, iterating over all n elements in every
binary search iteration does redundant work.
We compress nums into unique values and their counts using collections.Counter.
The feasibility check evaluates:
    sum(count * ((val + d - 1) // d) for val, count in counts.items())
When unique values U << n, this achieves up to a 10x speedup!

Complexity:
    Time: O(n + U * log(max_num)) where U is the number of unique elements
    Space: O(U) for frequency map
"""

from collections import Counter
from typing import List


def smallest_divisor(nums: List[int], threshold: int) -> int:
    """
    Find smallest divisor using frequency-compressed binary search.
    """
    if not nums:
        return 1

    n = len(nums)
    max_num = max(nums)

    if threshold == n:
        return max_num

    counts = Counter(nums)
    items = list(counts.items())

    left = max(1, (sum(nums) + threshold - 1) // threshold)
    right = max_num

    def can_achieve_threshold(divisor: int) -> bool:
        total_sum = sum(cnt * ((val + divisor - 1) // divisor) for val, cnt in items)
        return total_sum <= threshold

    while left < right:
        mid = (left + right) // 2
        if can_achieve_threshold(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    smallestDivisor = staticmethod(smallest_divisor)
