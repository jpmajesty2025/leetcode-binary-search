"""
LeetCode 2300: Successful Pairs of Spells and Potions (Standard Library bisect)
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/

Strategy:
1. Sort potions ascending in O(m log m).
2. For each spell, compute required potion threshold min_potion = ceil(success / spell).
3. Use C-implemented bisect.bisect_left to locate the insertion index in O(log m).
4. All potions from this index to the end form successful pairs: m - index.

Complexity:
    Time: O((m + n) log m)
    Space: O(m) auxiliary space for sorted copy of potions
"""

import bisect
from typing import List


def successful_pairs(spells: List[int], potions: List[int], success: int) -> List[int]:
    """
    Compute successful pairs using C-speed bisect_left.
    """
    sorted_potions = sorted(potions)
    m = len(sorted_potions)

    return [
        m - bisect.bisect_left(sorted_potions, (success + spell - 1) // spell)
        for spell in spells
    ]


class Solution:
    """LeetCode submission interface."""
    successfulPairs = staticmethod(successful_pairs)
