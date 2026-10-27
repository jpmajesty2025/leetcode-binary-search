"""
LeetCode 1300: Sum of Mutated Array Closest to Target
https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/

Direct Mathematical Greedy Implementation:
Completely eliminates the outer binary search over the value range [0, max(arr)].
Solves for the exact integer cutoff in a single sorted pass using integer division.

Complexity:
- Time: O(N log N) dominated entirely by sorting, followed by an O(N) early-exit pass.
- Space: O(1) auxiliary space (or O(N) if preserving original array input).
"""

from typing import List


def find_best_value(arr: List[int], target: int) -> int:
    """
    Find best value using sort and single-pass mathematical greedy cutoff.

    Mathematical Derivation:
    Sort arr in ascending order: arr[0] <= arr[1] <= ... <= arr[N-1].
    Iterate through arr keeping a running prefix sum.
    At index i, suppose all remaining (N - i) elements are capped at arr[i].
    If prefix + arr[i] * (N - i) >= target:
      The ideal capping threshold MUST lie in [arr[i-1], arr[i]] (or [0, arr[0]] if i == 0).
      Every element before index i remains unchanged (summing to prefix).
      Every element from i to N-1 is capped to a candidate integer value 'v'.
      Thus: prefix + v * (N - i) ~ target
            v * (N - i) ~ target - prefix
      Let rem_target = target - prefix and k = N - i.
      The optimal integer candidate is either:
          q = rem_target // k
          or q + 1
      Comparing absolute differences:
          diff(q) = rem_target - q * k
          diff(q + 1) = (q + 1) * k - rem_target
      To satisfy the tie-breaking rule (smaller integer chosen in ties):
          Choose q + 1 if and only if diff(q + 1) < diff(q).
          Otherwise choose q.
    If the loop completes without exceeding target, sum(arr) <= target,
    so returning max(arr) (i.e. arr[-1]) is optimal.
    """
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    prefix = 0

    for i, a in enumerate(sorted_arr):
        rem_count = n - i
        # If capping all remaining elements at a reaches or exceeds target:
        if prefix + a * rem_count >= target:
            rem_target = target - prefix
            q = rem_target // rem_count
            diff_q = rem_target - q * rem_count
            diff_q1 = (q + 1) * rem_count - rem_target
            # Strict inequality ensures tie breaks to smaller integer q
            return q + 1 if diff_q1 < diff_q else q
        prefix += a

    return sorted_arr[-1]


class Solution:
    """LeetCode submission interface."""
    findBestValue = staticmethod(find_best_value)
