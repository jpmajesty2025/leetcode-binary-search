"""
LeetCode 278: First Bad Version
https://leetcode.com/problems/first-bad-version/

You are a product manager and currently leading a team to develop a new product.
Unfortunately, the latest version of your product fails the quality check. Since each
version is developed based on the previous version, all the versions after a bad version
are also bad.

Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one,
which causes all the following ones to be bad.

You are given an API bool isBadVersion(version) which returns whether version is bad.
Implement a function to find the first bad version. You should minimize the number of calls
to the API.
"""

from typing import Callable, Optional

# Default placeholder for module-level compatibility
_DEFAULT_BAD = 4


def isBadVersion(version: int) -> bool:
    """Default mock isBadVersion API for testing."""
    return version >= _DEFAULT_BAD


def first_bad_version(n: int, is_bad_version: Optional[Callable[[int], bool]] = None) -> int:
    """
    Find first bad version using lower-bound binary search in O(log n) time.

    Supports dependency injection for is_bad_version to enable thread-safe testing
    without mutating global state.

    Complexity:
        Time: O(log2 n), making at most 31 API calls for n = 2^31 - 1.
        Space: O(1) auxiliary space.
    """
    api = is_bad_version if is_bad_version is not None else isBadVersion

    left, right = 1, n
    while left < right:
        # Prevents integer overflow in statically-typed languages
        mid = left + (right - left) // 2
        if api(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""

    def firstBadVersion(self, n: int) -> int:
        return first_bad_version(n)
