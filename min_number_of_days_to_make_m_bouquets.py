"""
LeetCode 1482: Minimum Number of Days to Make m Bouquets
https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/

You are given an integer array bloomDay, an integer m and an integer k.

You want to make m bouquets. To make a bouquet, you need to use k adjacent flowers from the garden.

The garden consists of n flowers, the ith flower will bloom in the bloomDay[i] and then can be used in 
exactly one bouquet.

Return the minimum number of days you need to wait to be able to make m bouquets from the garden. If it 
is impossible to make m bouquets return -1.

Constraints:
- bloomDay.length == n
- 1 <= n <= 10^5
- 1 <= bloomDay[i] <= 10^9
- 1 <= m <= 10^6
- 1 <= k <= n

Complexity:
- Time: O(N log(max(bloomDay) - min(bloomDay))) comparisons
- Space: O(1) auxiliary space
"""

from typing import List


def min_days(bloomDay: List[int], m: int, k: int) -> int:
    """
    Find minimum days to make m bouquets using binary search on answer.

    Mathematical Feasibility & Early Exits:
    - If n < m * k, we don't have enough flowers in total -> return -1 immediately.
    - If n == m * k, every single flower in the garden must be used.
      The only day all n flowers are bloomed is day max(bloomDay) -> return max(bloomDay) in O(1).
    - Otherwise, binary search for the minimal day T in [min(bloomDay), max(bloomDay)].

    Greedy Choice Property:
    To count achievable bouquets by day T, greedily take the first k bloomed adjacent flowers.
    Taking an earlier group of k never diminishes future bouquet opportunities.
    """
    n = len(bloomDay)
    if n < m * k:
        return -1
    if n == m * k:
        return max(bloomDay)

    left, right = min(bloomDay), max(bloomDay)

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
        if can_make_bouquets(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    minDays = staticmethod(min_days)
