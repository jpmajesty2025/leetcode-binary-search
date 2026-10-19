"""
LeetCode 2389: Longest Subsequence With Limited Sum (Two-Pointer / Dual Sort)
https://leetcode.com/problems/longest-subsequence-with-limited-sum/

Strategy:
1. Sort nums ascending and compute prefix sums.
2. Sort queries ascending along with their original indices in O(m log m).
3. Monotonic property: As the query budget Q increases, the maximum subsequence size
   can only increase or stay the same.
4. A single pointer idx walks forward across prefix_sums. Across all m queries,
   idx advances at most n times total!
5. The query scan runs in O(n + m) time.

Complexity:
    Time: O(n log n + m log m)
    Space: O(n + m) auxiliary space for prefix sums and sorted queries
"""

import itertools
from typing import List


def answer_queries(nums: List[int], queries: List[int]) -> List[int]:
    """
    Compute maximum subsequence sizes using dual sorting and a monotonic two-pointer scan.
    """
    if not nums:
        return [0] * len(queries)

    prefix_sums = list(itertools.accumulate(sorted(nums)))
    n = len(prefix_sums)

    sorted_queries = sorted(enumerate(queries), key=lambda x: x[1])
    result = [0] * len(queries)

    idx = 0
    for orig_idx, query in sorted_queries:
        while idx < n and prefix_sums[idx] <= query:
            idx += 1
        result[orig_idx] = idx

    return result


class Solution:
    """LeetCode submission interface."""
    answerQueries = staticmethod(answer_queries)
