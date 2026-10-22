"""
LeetCode 374: Guess Number Higher or Lower (Ternary Search)
https://leetcode.com/problems/guess-number-higher-or-lower/

Strategy:
Splits the search interval into 3 equal parts using two midpoints:
    m1 = left + (right - left) // 3
    m2 = right - (right - left) // 3

Why Ternary Search makes MORE queries than Binary Search:
- Ternary search reduces the interval by a factor of 3, taking log3(n) iterations.
- However, each iteration requires up to 2 calls to guess(): guess(m1) and guess(m2).
- Total API calls in the worst case: 2 * log3(n) = 2 * (ln n / ln 3) ≈ 1.82 ln n.
- Binary search makes at most log2(n) = ln n / ln 2 ≈ 1.44 ln n calls.
- Ratio: (2 * ln 2) / ln 3 ≈ 1.262 -> Ternary search makes 26.2% MORE comparisons!

Complexity:
    Time: O(log3 n) iterations, O(log n) total calls
    Space: O(1) auxiliary space
"""

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
    Find picked number using ternary search.
    """
    api = guess_api if guess_api is not None else guess

    left, right = 1, n
    while left <= right:
        m1 = left + (right - left) // 3
        m2 = right - (right - left) // 3

        res1 = api(m1)
        if res1 == 0:
            return m1
        if res1 < 0:
            right = m1 - 1
            continue

        res2 = api(m2)
        if res2 == 0:
            return m2
        if res2 < 0:
            left = m1 + 1
            right = m2 - 1
        else:
            left = m2 + 1

    return -1


class Solution:
    """LeetCode submission interface."""

    def guessNumber(self, n: int) -> int:
        return guess_number(n)
