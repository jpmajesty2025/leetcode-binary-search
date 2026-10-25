"""
LeetCode 540: Single Element in a Sorted Array (Monotonic Boolean Disruption View)
https://leetcode.com/problems/single-element-in-a-sorted-array/

Strategy:
Defines a virtual sequence over pair indices 0 <= i < len(nums) // 2:
    view[i] = (nums[2 * i] != nums[2 * i + 1])

Notice that this boolean sequence is monotonically non-decreasing:
[False, False, ..., False, True, True, ..., True]
- Before the single element: nums[2i] == nums[2i+1] -> False
- After the single element:  nums[2i] != nums[2i+1] -> True

Finding the single element is equivalent to finding the FIRST `True` in this sequence,
which Python's C-accelerated `bisect.bisect_left` solves in O(log(n/2)) steps!

Complexity:
- Time: O(log(n/2)) comparisons
- Space: O(1) auxiliary space (zero array allocations)
"""

import bisect
from typing import List


class DisruptionView:
    """Zero-allocation lazy view mapping pair indices to disruption booleans."""

    __slots__ = ("nums", "num_pairs")

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.num_pairs = len(nums) // 2

    def __len__(self) -> int:
        return self.num_pairs

    def __getitem__(self, i: int) -> bool:
        return self.nums[2 * i] != self.nums[2 * i + 1]


def single_non_duplicate(nums: List[int]) -> int:
    """
    Find single element using monotonic boolean disruption view and bisect.bisect_left.
    """
    if len(nums) == 1:
        return nums[0]

    view = DisruptionView(nums)
    idx = bisect.bisect_left(view, True)
    return nums[2 * idx]


class Solution:
    """LeetCode submission interface."""
    singleNonDuplicate = staticmethod(single_non_duplicate)
