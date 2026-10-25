"""
LeetCode 2251: Number of Flowers in Full Bloom
https://leetcode.com/problems/number-of-flowers-in-full-bloom/

You are given a 0-indexed 2D integer array flowers, where flowers[i] = [start_i, end_i]
means the ith flower will be in full bloom from start_i to end_i (inclusive).
You are also given a 0-indexed integer array people, where people[i] is the arrival time
of the ith person.

Return an integer array answer of size len(people), where answer[i] is the number of
flowers in full bloom when the ith person arrives.

Constraints:
- 1 <= flowers.length <= 5 * 10^4
- flowers[i].length == 2
- 1 <= start_i <= end_i <= 10^9
- 1 <= people.length <= 5 * 10^4
- 1 <= people[i] <= 10^9

Complexity:
- Time: O(N log N + M log N) where N = len(flowers), M = len(people)
  - Sorting starts and ends: O(N log N)
  - M queries of 2 binary searches each: O(M log N)
  - Does NOT require sorting people!
- Space: O(N) auxiliary space for sorted starts and ends
"""

from bisect import bisect_left, bisect_right
from typing import List


def full_bloom_flowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    Count blooming flowers at each person's arrival time using Dual Binary Search.

    The Mathematical Invariant:
    A flower [start, end] is in bloom at time t if and only if:
        start <= t <= end
    Equivalently:
        (start <= t) AND NOT (end < t)

    Therefore:
        blooming(t) = count(flowers with start <= t) - count(flowers with end < t)

    By decoupling start and end times into two independent sorted arrays:
    - bisect_right(starts, t): flowers that have started blooming by time t.
    - bisect_left(ends, t): flowers that have finished blooming strictly before time t.
    The difference directly yields the exact count in O(log N) per query.
    """
    starts = sorted(f[0] for f in flowers)
    ends = sorted(f[1] for f in flowers)

    return [bisect_right(starts, t) - bisect_left(ends, t) for t in people]


class Solution:
    """LeetCode submission interface."""
    fullBloomFlowers = staticmethod(full_bloom_flowers)
