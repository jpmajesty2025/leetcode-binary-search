"""
LeetCode 1300: Sum of Mutated Array Closest to Target
https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/

Bisect + Prefix Sums Implementation:
Accelerates the predicate evaluation from O(N) linear scan to O(log N) binary search.

Complexity:
- Time: O(N log N + log(max(arr)) * log N)
  - Sorting: O(N log N)
  - Prefix Sum computation: O(N)
  - Binary search iterations: O(log(max(arr)))
  - Predicate evaluation via bisect_right: O(log N)
- Space: O(N) for prefix sums and sorted array
"""

import bisect
from typing import List


def find_best_value(arr: List[int], target: int) -> int:
    """
    Find best value using binary search on answer with bisect and prefix sums.

    Predicate Acceleration:
    In the standard approach, computing sum(min(a, limit) for a in arr) requires
    O(N) operations per binary search step.
    With sorted arr and prefix sums:
    - Elements <= limit are located at indices [0, idx - 1] via bisect_right(arr, limit).
      Their sum is prefix[idx].
    - Elements > limit are located at indices [idx, N - 1].
      Each element is truncated to limit, yielding (N - idx) * limit.
    - Total mutated sum = prefix[idx] + (N - idx) * limit in O(log N) time!
    """
    sorted_arr = sorted(arr)
    n = len(sorted_arr)

    # Prefix sums where prefix[i] = sum(sorted_arr[:i])
    prefix = [0] * (n + 1)
    for i, val in enumerate(sorted_arr):
        prefix[i + 1] = prefix[i] + val

    total = prefix[n]
    if total <= target:
        return sorted_arr[-1]

    left, right = 0, sorted_arr[-1]
    ans = 0
    min_diff = float("inf")

    while left <= right:
        mid = left + (right - left) // 2

        # O(log N) predicate
        idx = bisect.bisect_right(sorted_arr, mid)
        current_sum = prefix[idx] + (n - idx) * mid
        current_diff = abs(current_sum - target)

        if current_diff < min_diff or (current_diff == min_diff and mid < ans):
            ans = mid
            min_diff = current_diff

        if current_sum < target:
            left = mid + 1
        else:
            right = mid - 1

    return ans


class Solution:
    """LeetCode submission interface."""
    findBestValue = staticmethod(find_best_value)
