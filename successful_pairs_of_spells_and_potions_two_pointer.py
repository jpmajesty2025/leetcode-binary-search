"""
LeetCode 2300: Successful Pairs of Spells and Potions (Standard Library bisect)
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/

Strategy:
1. Sort potions ascending in O(m log m).
2. Sort spells ascending along with their original indices in O(n log n).
3. Monotonic property: As spell strength increases, the required potion strength
   decreases. A pointer j starting at the end of potions only moves backward.
   Across all n spells, the pointer j moves at most m times total!
4. The two-pointer pass runs in O(m + n).

Complexity:
    Time: O(m log m + n log n)
    Space: O(m + n) auxiliary space for sorted arrays and output
"""

from typing import List


def successful_pairs(spells: List[int], potions: List[int], success: int) -> List[int]:
    """
    Compute successful pairs using dual sorting and a monotonic two-pointer scan.
    """
    sorted_potions = sorted(potions)
    sorted_spells = sorted(enumerate(spells), key=lambda x: x[1])

    m = len(sorted_potions)
    result = [0] * len(spells)

    # j represents the leftmost index of successful potions
    j = m
    for orig_idx, spell in sorted_spells:
        while j > 0 and spell * sorted_potions[j - 1] >= success:
            j -= 1
        result[orig_idx] = m - j

    return result


class Solution:
    """LeetCode submission interface."""
    successfulPairs = staticmethod(successful_pairs)
