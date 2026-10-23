"""
LeetCode 2250: Count Number of Rectangles Containing Each Point
https://leetcode.com/problems/count-number-of-rectangles-containing-each-point/

You are given a 2D integer array rectangles where rectangles[i] = [l_i, h_i] indicates that
the ith rectangle has length l_i and height h_i. You are also given a 2D integer array points
where points[j] = [x_j, y_j].

The ith rectangle has bottom-left corner at (0, 0) and top-right corner at (l_i, h_i).
A point (x, y) is contained if 0 <= x <= l_i and 0 <= y <= h_i.

Return an integer array count where count[j] is the number of rectangles containing points[j].
"""

import bisect
from typing import List


def count_rectangles(rectangles: List[List[int]], points: List[List[int]]) -> List[int]:
    """
    Count containing rectangles using Height-Bucketed Binary Search.

    Constraint Insight:
    - lengths can be up to 10^9, but heights are bounded by 1 <= h_i, y_j <= 100!
    - Group rectangle lengths by height into 100 buckets.
    - Sort each bucket in O(n log n) total time.
    - For each point (x, y), iterate over heights h in [y, 100] (at most 100 iterations)
      and binary search the number of rectangles with length >= x in O(log n).

    Complexity:
        Time: O(n log n + m * H log n) where H <= 100
        Space: O(n) for the buckets
    """
    if not rectangles or not points:
        return [0] * len(points)

    # Buckets for heights 1 to 100
    buckets: List[List[int]] = [[] for _ in range(101)]
    for l, h in rectangles:
        buckets[h].append(l)

    # Sort each height bucket
    for h in range(1, 101):
        if buckets[h]:
            buckets[h].sort()

    bucket_lens = [len(b) for b in buckets]
    counts: List[int] = []
    append = counts.append
    bisect_left = bisect.bisect_left

    for x, y in points:
        contained = 0
        for h in range(y, 101):
            total_at_h = bucket_lens[h]
            if total_at_h:
                contained += total_at_h - bisect_left(buckets[h], x)
        append(contained)

    return counts


class Solution:
    """LeetCode submission interface."""
    countRectangles = staticmethod(count_rectangles)
