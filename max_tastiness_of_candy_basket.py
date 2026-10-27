"""
LeetCode 2517: Maximum Tastiness of Candy Basket
https://leetcode.com/problems/maximum-tastiness-of-candy-basket/

You are given an array of positive integers price where price[i] denotes the price of the ith
candy and a positive integer k.
The store sells baskets of k distinct candies. The tastiness of a candy basket is the smallest
absolute difference of the prices of any two candies in the basket.

Return the maximum tastiness of a candy basket.

Constraints:
- 2 <= k <= price.length <= 10^5
- 1 <= price[i] <= 10^9

Complexity:
- Time: O(N log N + N log((max(price) - min(price)) / (k - 1)))
  - Sorting: O(N log N)
  - Binary search range: [0, (price[-1] - price[0]) // (k - 1)]
  - Greedy validation per step: O(N)
- Space: O(1) auxiliary space (or O(N) if preserving original array)
"""

from typing import List


def maximum_tastiness(price: List[int], k: int) -> int:
    """
    Find maximum tastiness using binary search on answer with tight pigeonhole bounds.

    The Pigeonhole Upper Bound:
    When selecting k elements from sorted range [price[0], price[-1]], there are k - 1
    adjacent intervals between them. The total distance is at most price[-1] - price[0].
    By the Pigeonhole Principle, the minimum interval (tastiness) can never exceed:
        upper_bound = (price[-1] - price[0]) // (k - 1)
    This drastically tightens the search space compared to price[-1] - price[0].

    Greedy Choice Property:
    To test if tastiness T is achievable, always pick price[0], then greedily pick the
    earliest subsequent candy with price >= prev + T.
    """
    price.sort()
    left = 0
    right = (price[-1] - price[0]) // (k - 1)
    ans = 0

    def can_form_basket(t_limit: int) -> bool:
        count = 1
        last_price = price[0]
        for p in price[1:]:
            if p - last_price >= t_limit:
                count += 1
                last_price = p
                if count >= k:
                    return True
        return False

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
