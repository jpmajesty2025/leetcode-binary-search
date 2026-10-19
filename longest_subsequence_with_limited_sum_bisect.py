"""
LeetCode 2389: Longest Subsequence With Limited Sum (Standard Library bisect + itertools)
https://leetcode.com/problems/longest-subsequence-with-limited-sum/

Strategy:
1. Greedily sort nums ascending in O(n log n).
2. Generate prefix sums in C speed using itertools.accumulate in O(n).
3. For each query, locate the upper bound using C-speed bisect.bisect_right in O(log n).
   bisect_right returns the count of prefix sums <= query, which is directly
   the maximum subsequence length!

Complexity:
    Time: O((n + m) log n)
    Space: O(n) auxiliary space for prefix sums
"""

import bisect
import itertools
from typing import List


def answer_queries(nums: List[int], queries: List[int]) -> List[int]:
    """
    Compute maximum subsequence sizes using itertools.accumulate and bisect_right.
    """
    if not nums:
        return [0] * len(queries)

    prefix_sums = list(itertools.accumulate(sorted(nums)))
    return [bisect.bisect_right(prefix_sums, q) for q in queries]


class Solution:
    """LeetCode submission interface."""
    answerQueries = staticmethod(answer_queries)
