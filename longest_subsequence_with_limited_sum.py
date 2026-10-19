"""
LeetCode 2389: Longest Subsequence With Limited Sum
https://leetcode.com/problems/longest-subsequence-with-limited-sum/

You are given an integer array nums of length n, and an integer array queries of length m.

Return an array answer of length m where answer[i] is the maximum size of a subsequence
that you can take from nums such that the sum of its elements is less than or equal to queries[i].

A subsequence is an array that can be derived from another array by deleting some or no
elements without changing the order of the remaining elements.
"""

from typing import List


def answer_queries(nums: List[int], queries: List[int]) -> List[int]:
    """
    Compute maximum subsequence size for each query using prefix sums and binary search.

    Greedy principle: To maximize the number of elements whose sum is <= Q, we must greedily
    pick the smallest elements. Sorting nums and building prefix sums turns each query
    into an upper-bound binary search (bisect_right).

    Fixes:
    - Handles empty nums defensively (returns [0] * len(queries)).
    - Avoids mutating caller's nums by using sorted(nums).

    Complexity:
        Time: O((n + m) log n)
        Space: O(n) auxiliary space for sorted copy and prefix sums
    """
    if not nums:
        return [0] * len(queries)

    sorted_nums = sorted(nums)
    n = len(sorted_nums)

    prefix_sums = [0] * n
    prefix_sums[0] = sorted_nums[0]
    for i in range(1, n):
        prefix_sums[i] = prefix_sums[i - 1] + sorted_nums[i]

    result = [0] * len(queries)

    for i, query in enumerate(queries):
        left, right = 0, n - 1
        while left <= right:
            mid = (left + right) // 2
            if prefix_sums[mid] <= query:
                left = mid + 1
            else:
                right = mid - 1
        result[i] = left

    return result


class Solution:
    """LeetCode submission interface."""
    answerQueries = staticmethod(answer_queries)
