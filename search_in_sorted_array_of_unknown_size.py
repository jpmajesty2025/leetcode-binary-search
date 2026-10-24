"""
LeetCode 702: Search in a Sorted Array of Unknown Size
https://leetcode.com/problems/search-in-a-sorted-array-of-unknown-size/

This is an interactive problem.
You have a sorted array of unique elements and an unknown size. You do not have direct
access to the array, but you can use the ArrayReader interface to access it:
- reader.get(i): returns the value at index i (0-indexed), or 2^31 - 1 if i is out of bounds.

Constraints:
- 1 <= secret.length <= 10^4
- -10^4 <= secret[i], target <= 10^4
- secret is sorted in strictly ascending order.

Complexity:
- Time: O(log k), where k is the index of the target (strictly O(log n) worst case).
  - Exponential expansion takes ceil(log2 k) calls.
  - Binary search takes ceil(log2 k) calls.
  - Total calls: ~2 * log2(k) <= 28 calls for k <= 10,000.
- Space: O(1) auxiliary space.
"""

class ArrayReader:
    """ArrayReader API specification."""

    def get(self, index: int) -> int:
        return -1


def search(reader: "ArrayReader", target: int) -> int:
    """
    Search for target in a sorted array of unknown size using Exponential Search.

    Phase 1: Exponential Range Bounding (Galloping)
      Start with [left, right] = [0, 1].
      While reader.get(right) < target:
        left = right + 1
        right <<= 1
      Because array elements are sorted and reader.get(right) < target,
      no index <= right can hold target, so left can strictly be right + 1.

    Phase 2: Standard Binary Search
      Search within the identified interval [left, right].
      If reader.get(mid) lands out of bounds (returning 2^31 - 1),
      it is strictly greater than target (since target <= 10^4 < 2^31 - 1),
      naturally directing the search to the left half.
    """
    left, right = 0, 1

    # Phase 1: Exponential bounding
    while reader.get(right) < target:
        left = right + 1
        right <<= 1

    # Phase 2: Binary search within [left, right]
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = reader.get(mid)

        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
