"""
LeetCode 2226: Maximum Candies Allocated to K Children (Frequency Compression)
https://leetcode.com/problems/maximum-candies-allocated-to-k-children/

Strategy:
When candies array contains many duplicate pile sizes (common in large allocations),
evaluating every pile individually is redundant.
Pre-aggregating piles into a frequency list:
    counts = Counter(candies).items()
allows evaluating all identical piles in a single multiplication:
    allocated += (c // mid) * freq
This reduces inner loop iterations from N down to the number of unique pile sizes (U <= N),
achieving significant performance gains.

Complexity:
- Time: O(N + U log(sum(candies) // k))
- Space: O(U) auxiliary space
"""

from collections import Counter
from typing import List


def maximum_candies(candies: List[int], k: int) -> int:
    """
    Find maximum candies using frequency-compressed binary search on answer.
    """
    total = sum(candies)
    if total < k:
        return 0

    counts = list(Counter(candies).items())
    left, right = 1, total // k
    ans = 0

    while left <= right:
        mid = left + (right - left) // 2

        allocated = 0
        for c, freq in counts:
            allocated += (c // mid) * freq
            if allocated >= k:
                break

        if allocated >= k:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    return ans


class Solution:
    """LeetCode submission interface."""
    maximumCandies = staticmethod(maximum_candies)
