"""
LeetCode 1482: Minimum Number of Days to Make m Bouquets
https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/

Unique Bloom Days Binary Search Implementation:
Compresses the search range from [min, max] (up to 10^9) to the sorted set of unique
bloom days (at most 10^5 elements), cutting iterations nearly in half (from ~30 down to ~17).

Complexity:
- Time: O(N log(unique_days) + N log N)
  - Sorting unique days: O(U log U) where U <= N
  - Binary search iterations: O(log U) (at most 17 iterations)
  - Predicate check per iteration: O(N)
- Space: O(U) for unique sorted days
"""

from typing import List


def min_days(bloomDay: List[int], m: int, k: int) -> int:
    """
    Find minimum days using binary search over sorted unique bloom days.

    Domain Compression Invariant:
    The minimal day on which m bouquets can be formed must be an actual bloom day
    from the array. If no flower blooms between day D - 1 and day D, the state of
    the garden is identical. Thus, searching non-existent days is redundant.
    """
    n = len(bloomDay)
    if n < m * k:
        return -1
    if n == m * k:
        return max(bloomDay)

    unique_days = sorted(set(bloomDay))
    left, right = 0, len(unique_days) - 1

    def can_make_bouquets(days: int) -> bool:
        bouquets = 0
        flowers = 0
        for bloom in bloomDay:
            if bloom <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
            if bouquets >= m:
                return True
        return False

    while left < right:
        mid = (left + right) // 2
        if can_make_bouquets(unique_days[mid]):
            right = mid
        else:
            left = mid + 1

    return unique_days[left]


class Solution:
    """LeetCode submission interface."""
    minDays = staticmethod(min_days)
