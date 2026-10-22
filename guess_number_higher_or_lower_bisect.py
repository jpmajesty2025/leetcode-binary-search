"""
LeetCode 374: Guess Number Higher or Lower (Standard Library bisect)
https://leetcode.com/problems/guess-number-higher-or-lower/

Strategy:
Uses Python 3.10+ bisect.bisect_left over a virtual range range(1, n + 1).
The key function evaluates:
    guess_api(x) <= 0
Because guess(x) returns:
    1 if x < pick
    0 if x == pick
   -1 if x > pick
The condition (guess(x) <= 0) produces a monotonic boolean sequence:
    [False, False, ..., False, True, True, True]
where the first True is precisely the picked number!

Complexity:
    Time: O(log2 n)
    Space: O(1) auxiliary space
"""

import bisect
from typing import Callable, Optional

_DEFAULT_PICK = 42


def guess(num: int) -> int:
    """Default mock guess API for testing."""
    if num > _DEFAULT_PICK:
        return -1
    elif num < _DEFAULT_PICK:
        return 1
    return 0


def guess_number(n: int, guess_api: Optional[Callable[[int], int]] = None) -> int:
    """
    Find picked number using bisect_left with a monotonic boolean key function.
    """
    api = guess_api if guess_api is not None else guess

    candidates = range(1, n + 1)
    idx = bisect.bisect_left(candidates, True, key=lambda x: api(x) <= 0)

    if idx < len(candidates):
        return candidates[idx]
    return -1


class Solution:
    """LeetCode submission interface."""

    def guessNumber(self, n: int) -> int:
        return guess_number(n)
