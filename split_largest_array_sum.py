"""
LeetCode 410: Split Array Largest Sum
https://leetcode.com/problems/split-array-largest-sum/

Given an integer array nums and an integer k, split nums into k non-empty subarrays
such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.
"""

from typing import List


def split_array(nums: List[int], k: int) -> int:
    """
    Compute minimized largest subarray sum using Minimax Binary Search.

    Fixes:
    - Removes orphaned 'self' parameter from standalone function signature.
    - Fast-path for k == 1: returns sum(nums) in O(1).
    - Fast-path for k == len(nums): returns max(nums) in O(1).
    - Tight lower bound: by the pigeonhole principle, the largest subarray sum can
      never be less than ceil(sum(nums) / k).

    Complexity:
        Time: O(n log(sum(nums) - max(max(nums), sum(nums)//k) + 1))
        Space: O(1) auxiliary space
    """
    if not nums:
        return 0

    n = len(nums)
    total_sum = sum(nums)
    max_num = max(nums)

    # Fast-paths
    if k == 1:
        return total_sum
    if k == n:
        return max_num

    # Tight lower bound: max(max element, average subarray sum)
    left = max(max_num, (total_sum + k - 1) // k)
    right = total_sum

    def can_split(max_sum: int) -> bool:
        current_sum = 0
        subarrays = 1
        for num in nums:
            current_sum += num
            if current_sum > max_sum:
                subarrays += 1
                current_sum = num
                if subarrays > k:
                    return False
        return True

    while left < right:
        mid = (left + right) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    splitArray = staticmethod(split_array)
