"""
LeetCode 2226: Maximum Candies Allocated to K Children
https://leetcode.com/problems/maximum-candies-allocated-to-k-children/

You are given a 0-indexed integer array candies where candies[i] denotes a pile of candies.
You can divide each pile into any number of sub-piles, but cannot merge two piles together.
You are also given an integer k. Allocate piles to k children such that each child gets the
same number of candies. Each child can receive candies from only one pile.

Return the maximum number of candies each child can get, or 0 if impossible.

Constraints:
- 1 <= candies.length <= 10^5
- 1 <= candies[i] <= 10^7
- 1 <= k <= 10^12

Complexity:
- Time: O(N log(sum(candies) // k)) comparisons
- Space: O(1) auxiliary space
"""

from typing import List


def maximum_candies(candies: List[int], k: int) -> int:
    """
    Find maximum candies per child using binary search on answer with tight pigeonhole bounds.

    Bounds Analysis:
    - If total candies sum(candies) < k, it is impossible to give even 1 candy to each child -> return 0.
    - Upper Bound (Pigeonhole Principle):
      Even if all piles could be merged, k children could receive at most sum(candies) // k candies.
      Since merging is prohibited, the answer is strictly bounded by:
          right = sum(candies) // k
      This is strictly tighter than max(candies), drastically cutting the search range when k is large.
    """
    total = sum(candies)
    if total < k:
        return 0

    left, right = 1, total // k
    ans = 0

    def can_allocate_candies(c_limit: int) -> bool:
        allocated = 0
        for c in candies:
            allocated += c // c_limit
            if allocated >= k:
                return True
        return False

    while left <= right:
        mid = left + (right - left) // 2
        if can_allocate_candies(mid):
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    return ans


class Solution:
    """LeetCode submission interface."""
    maximumCandies = staticmethod(maximum_candies)
