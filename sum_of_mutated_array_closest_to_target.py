"""
LeetCode 1300: Sum of Mutated Array Closest to Target
https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/

Given an integer array arr and a target value target, return the integer value such that when we change 
all the integers larger than value in the given array to be equal to value, the sum of the array gets as 
close as possible (in absolute difference) to target.

In case of a tie, return the minimum such integer.

Notice that the answer is not necessarily a number from arr.

Constraints:
- 1 <= arr.length <= 10^4
- 1 <= arr[i] <= 10^5
- 1 <= target <= 10^5

Complexity:
- Time: O(N log(max(arr))) where N = len(arr)
- Space: O(1) auxiliary space
"""

from typing import List


def find_best_value(arr: List[int], target: int) -> int:
    """
    Find best value using binary search on answer.

    Bounds Analysis:
    - If total sum(arr) <= target:
      Any limit >= max(arr) produces the exact sum(arr).
      Because smaller limits only reduce the sum (increasing the difference from target),
      and larger limits tie with max(arr) (where the minimum integer wins ties),
      the optimal answer is strictly max(arr).
    - Lower Bound:
      When target is small relative to len(arr) (e.g. target = 1, arr = [2, 20, 11]),
      mutating all elements to 0 yields sum 0 (diff = target), whereas mutating to 1
      yields sum = len(arr) (diff = |len(arr) - target|). When diff(0) <= diff(1),
      value = 0 is optimal. Hence left MUST start at 0.
    - Upper Bound:
      Values strictly greater than max(arr) produce the exact same sum as max(arr),
      but tie-breaking favors the smaller integer. Hence right = max(arr).
    """
    total = sum(arr)
    if total <= target:
        return max(arr)

    left, right = 0, max(arr)
    ans = 0
    min_diff = float("inf")

    def get_sum_with_limit(limit: int) -> int:
        return sum(min(a, limit) for a in arr)

    while left <= right:
        mid = left + (right - left) // 2
        current_sum = get_sum_with_limit(mid)
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
