"""
LeetCode 374: Guess Number Higher or Lower
https://leetcode.com/problems/guess-number-higher-or-lower/

We are playing the Guess Game. The game is as follows:
I pick a number from 1 to n. You have to guess which number I picked.

Every time you guess wrong, I will tell you whether the number I picked is higher or lower
than your guess.

You call a pre-defined API int guess(int num), which returns three possible results:
-1: Your guess is higher than the number I picked (num > pick).
 1: Your guess is lower than the number I picked (num < pick).
 0: Your guess is equal to the number I picked (num == pick).

Return the number that I picked.
"""

from typing import Callable, Optional

# Default placeholder for module-level compatibility
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
    Find picked number using binary search in O(log n) time.

    Supports dependency injection for guess_api to enable thread-safe testing
    without mutating global state.

    Complexity:
        Time: O(log2 n), making at most 31 API calls for n = 2^31 - 1.
        Space: O(1) auxiliary space.
    """
    api = guess_api if guess_api is not None else guess

    left, right = 1, n
    while left <= right:
        mid = (left + right) // 2
        res = api(mid)
        if res == 0:
            return mid
        elif res < 0:
            right = mid - 1
        else:
            left = mid + 1

    return -1


class Solution:
    """LeetCode submission interface."""

    def guessNumber(self, n: int) -> int:
        return guess_number(n)
