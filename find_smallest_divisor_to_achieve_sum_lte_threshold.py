"""
LeetCode 1283: Find the Smallest Divisor Given a Threshold
https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/

Given an array of integers nums and an integer threshold, we will choose a positive integer
divisor, divide all the array by it, and sum the division's result. Find the smallest
divisor such that the result mentioned above is less than or equal to threshold.

Each result of the division is rounded to the nearest integer greater than or equal to that
element. (For example: 7/3 = 3 and 10/2 = 5).

The test cases are generated so that there will be an answer (threshold >= len(nums)).
"""

from typing import List


def smallest_divisor(nums: List[int], threshold: int) -> int:
    """
    Compute smallest divisor using Binary Search on Answer.

    Optimizations:
    - If threshold == len(nums): each element must divide to at most 1.
      Thus, divisor must be max(nums) (O(1) after max).
    - Tight lower bound: divisor cannot be less than ceil(sum(nums) / threshold).
    - Monotonic feasibility predicate: sum(ceil(num / divisor)) decreases as divisor increases.

    Complexity:
        Time: O(n log(max_num - sum_nums//threshold + 1))
        Space: O(1) auxiliary space
    """
    if not nums:
        return 1

    n = len(nums)
    max_num = max(nums)

    # Fast-path: each element must contribute exactly 1
    if threshold == n:
        return max_num

    # Tight theoretical lower bound
    left = max(1, (sum(nums) + threshold - 1) // threshold)
    right = max_num

    def can_achieve_threshold(divisor: int) -> bool:
        total_sum = sum((num + divisor - 1) // divisor for num in nums)
        return total_sum <= threshold

    while left < right:
        mid = (left + right) // 2
        if can_achieve_threshold(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    smallestDivisor = staticmethod(smallest_divisor)
