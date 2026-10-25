"""
LeetCode 540: Single Element in a Sorted Array (Even-Index Virtual Search)
https://leetcode.com/problems/single-element-in-a-sorted-array/

Strategy:
Why search over N indices when the array consists of N // 2 pairs plus 1 lone element?
We binary search directly over the pair indices:
0 <= pair_index <= N // 2

For each pair_index `mid`:
The expected pair starts at index `2 * mid` and ends at `2 * mid + 1`.
- If nums[2 * mid] == nums[2 * mid + 1]:
  The pair is intact. The single element is strictly to the right:
  low = mid + 1
- Else:
  The pair is broken. The single element is at or before this pair:
  high = mid

When low == high, the single element starts at index `2 * low`.

Advantages:
1. Search space is cut in half from the start (N // 2 iterations).
2. Completely eliminates parity branching and normalization.
3. Out-of-bounds access is impossible: 2 * mid + 1 < 2 * high + 1 <= len(nums).

Complexity:
- Time: O(log(n/2)) comparisons
- Space: O(1)
"""

from typing import List


def single_non_duplicate(nums: List[int]) -> int:
    """
    Find single element by binary searching over pair space [0, len(nums) // 2].
    """
    low, high = 0, len(nums) // 2

    while low < high:
        mid = low + (high - low) // 2
        if nums[2 * mid] == nums[2 * mid + 1]:
            low = mid + 1
        else:
            high = mid

    return nums[2 * low]


class Solution:
    """LeetCode submission interface."""
    singleNonDuplicate = staticmethod(single_non_duplicate)
