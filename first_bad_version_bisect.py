"""
LeetCode 278: First Bad Version (Standard Library bisect)
https://leetcode.com/problems/first-bad-version/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range of versions range(1, n + 1).
The key function evaluates:
    is_bad_version(v)
which produces a monotonic boolean sequence:
    [False, False, ..., False, True, True, True]
bisect_left locates the index of the first True in C speed.

Complexity:
    Time: O(log2 n), making at most 31 API calls for n = 2^31 - 1.
    Space: O(1) auxiliary space.
"""

import bisect
from typing import Callable, Optional

_DEFAULT_BAD = 4


def isBadVersion(version: int) -> bool:
    """Default mock isBadVersion API for testing."""
    return version >= _DEFAULT_BAD


def first_bad_version(n: int, is_bad_version: Optional[Callable[[int], bool]] = None) -> int:
    """
    Find first bad version using bisect_left with a monotonic boolean key.
    """
    api = is_bad_version if is_bad_version is not None else isBadVersion

    versions = range(1, n + 1)
    idx = bisect.bisect_left(versions, True, key=api)

    return versions[idx]


class Solution:
    """LeetCode submission interface."""

    def firstBadVersion(self, n: int) -> int:
        return first_bad_version(n)
