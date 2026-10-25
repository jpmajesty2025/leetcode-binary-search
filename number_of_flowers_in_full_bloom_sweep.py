"""
LeetCode 2251: Number of Flowers in Full Bloom (Coordinate-Compressed Difference Array)
https://leetcode.com/problems/number-of-flowers-in-full-bloom/

Strategy:
Uses a sparse Difference Array over compressed time coordinates:
1. For each flower [start, end]:
   - Increment diff[start] by +1.
   - Decrement diff[end + 1] by -1.
2. Sort all unique boundary timestamps and calculate cumulative prefix sums.
   Each prefix sum represents the exact bloom count from timestamp times[i]
   up to times[i+1] - 1.
3. For each person arrival `t`:
   - Use `bisect_right(times, t) - 1` to locate the active interval and read the count.

Complexity:
- Time: O(N log N + M log N)
  - Sorting at most 2N unique timestamps: O(N log N)
  - Prefix sum accumulation: O(N)
  - M binary search queries: O(M log N)
- Space: O(N) auxiliary space
"""

from bisect import bisect_right
from collections import defaultdict
import itertools
from typing import List


def full_bloom_flowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    Count blooming flowers using coordinate-compressed difference array and prefix sums.
    """
    diff = defaultdict(int)
    for start, end in flowers:
        diff[start] += 1
        diff[end + 1] -= 1

    times = sorted(diff.keys())
    prefix = list(itertools.accumulate(diff[t] for t in times))

    ans = []
    for arrival in people:
        idx = bisect_right(times, arrival) - 1
        ans.append(prefix[idx] if idx >= 0 else 0)

    return ans


class Solution:
    """LeetCode submission interface."""
    fullBloomFlowers = staticmethod(full_bloom_flowers)
