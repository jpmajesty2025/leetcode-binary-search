"""
LeetCode 1533: Find the Index of the Large Integer
https://leetcode.com/problems/find-the-index-of-the-large-integer/

We have an integer array arr, where all the integers in arr are equal except for one integer
which is larger than the rest of the integers. You will not be given direct access to the
array, instead, you will have an API ArrayReader:
- int compareSub(int l, int r, int x, int y): compares sum of arr[l..r] with arr[x..y]
  returns:
   1 if sum(arr[l..r]) > sum(arr[x..y])
   0 if sum(arr[l..r]) == sum(arr[x..y])
  -1 if sum(arr[l..r]) < sum(arr[x..y])
- int length(): returns the size of the array.

You are allowed to call compareSub() 20 times at most for arrays up to 500,000 elements.
Return the index of the largest integer.
"""

from typing import Protocol


class ArrayReader(object):
    """ArrayReader API specification."""

    def compareSub(self, l: int, r: int, x: int, y: int) -> int:
        pass

    def length(self) -> int:
        pass


def get_index(reader: "ArrayReader") -> int:
    """
    Find index of the larger integer using Parity-Aware Binary Search.

    The Critical Parity Invariant:
    - compareSub() compares SUMS of subarrays.
    - If the two subarrays have unequal lengths, the longer subarray can easily have
      a larger sum even if the large integer is in the shorter subarray!
    - Therefore, the two compared subarrays MUST always have identical lengths!

    Cases:
    1. Even length (2k):
       Compare left half [left, left + k - 1] with right half [left + k, right].
       If cmp == 1: target is in left half.
       If cmp == -1: target is in right half.
    2. Odd length (2k + 1):
       Set aside middle element at mid = left + k.
       Compare left slice [left, mid - 1] with right slice [mid + 1, right] (both length k).
       If cmp == 0: neither slice has the larger element -> target is mid!
       If cmp == 1: target is in left slice.
       If cmp == -1: target is in right slice.

    Complexity:
        Time: O(log2 n) calls, at most ceil(log2(500,000)) = 19 calls (strictly <= 20).
        Space: O(1) auxiliary space.
    """
    left, right = 0, reader.length() - 1

    while left < right:
        length = right - left + 1
        half = length // 2

        if length % 2 == 0:
            # Even length: two equal halves of size 'half'
            cmp = reader.compareSub(left, left + half - 1, left + half, right)
            if cmp == 1:
                right = left + half - 1
            else:
                left = left + half
        else:
            # Odd length: two equal slices of size 'half', leaving middle element at mid
            mid = left + half
            cmp = reader.compareSub(left, mid - 1, mid + 1, right)
            if cmp == 0:
                return mid
            elif cmp == 1:
                right = mid - 1
            else:
                left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    getIndex = staticmethod(get_index)
