"""
LeetCode 278: First Bad Version (Exponential / Galloping Search)
https://leetcode.com/problems/first-bad-version/

Strategy:
Emulates the behavior of git bisect on large codebases:
1. Probe versions at exponentially growing boundaries (1, 2, 4, 8, 16, ...) until
   is_bad_version(bound) returns True.
2. Binary search within [bound // 2, min(bound, n)].

Advantage:
If the regression was introduced recently at version k (where k << n), Exponential Search
finds the bad version in O(log k) API calls instead of O(log n).
For example, if bad = 10 and n = 2^31 - 1, Exponential Search requires only 9 queries
compared to 31 queries for standard binary search (3.4x fewer API calls)!

Complexity:
    Time: O(log k) where k is the index of the first bad version (bounded by O(log n)).
    Space: O(1) auxiliary space.
"""

from typing import Callable, Optional

_DEFAULT_BAD = 4


def isBadVersion(version: int) -> bool:
    """Default mock isBadVersion API for testing."""
    return version >= _DEFAULT_BAD


def first_bad_version(n: int, is_bad_version: Optional[Callable[[int], bool]] = None) -> int:
    """
    Find first bad version using Exponential (Galloping) Search.
    """
    api = is_bad_version if is_bad_version is not None else isBadVersion

    if api(1):
        return 1

    bound = 1
    while bound < n:
        if api(min(bound, n)):
            break
        bound *= 2

    left = bound // 2
    right = min(bound, n)

    while left < right:
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
