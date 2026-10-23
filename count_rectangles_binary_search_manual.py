"""
LeetCode 2250: Count Number of Rectangles Containing Each Point (Manual Binary Search)
https://leetcode.com/problems/count-number-of-rectangles-containing-each-point/

Strategy:
Groups lengths by height into 100 buckets, sorts each bucket, and uses an explicit
manual binary search loop to find the count of rectangles with length >= x.

Complexity:
    Time: O(n log n + m * H log n) where H <= 100
    Space: O(n) for the height buckets
"""

from typing import List


def count_rectangles(rectangles: List[List[int]], points: List[List[int]]) -> List[int]:
    """
    Count containing rectangles using manual binary search on height buckets.
    """
    if not rectangles or not points:
        return [0] * len(points)

    buckets: List[List[int]] = [[] for _ in range(101)]
    for l, h in rectangles:
        buckets[h].append(l)

    for h in range(1, 101):
        if buckets[h]:
            buckets[h].sort()

    bucket_lens = [len(b) for b in buckets]
    counts: List[int] = []

    for x, y in points:
        contained = 0
        for h in range(y, 101):
            total_at_h = bucket_lens[h]
            if not total_at_h:
                continue

            arr = buckets[h]
            # Manual lower-bound binary search for first index with length >= x
            left, right = 0, total_at_h
            while left < right:
                mid = left + (right - left) // 2
                if arr[mid] < x:
                    left = mid + 1
                else:
                    right = mid

            contained += total_at_h - left

        counts.append(contained)

    return counts


class Solution:
    """LeetCode submission interface."""
    countRectangles = staticmethod(count_rectangles)
