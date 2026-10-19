"""
LeetCode 2300: Successful Pairs of Spells and Potions (Standard Library bisect)
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/

You are given two positive integer arrays spells and potions, of length n and m respectively,
where spells[i] represents the strength of the ith spell and potions[j] represents the strength
of the jth potion.

You are also given an integer success. A spell and potion pair is considered successful
if the product of their strengths is at least success.

Return an integer array pairs of length n where pairs[i] is the number of potions that
will form a successful pair with the ith spell.
"""

from typing import List


def successful_pairs(spells: List[int], potions: List[int], success: int) -> List[int]:
    """
    Compute number of successful potions for each spell using binary search.

    Fixes input mutation by using sorted() instead of potions.sort().
    Computes required potion strength via ceiling division: (success + spell - 1) // spell,
    avoiding multiplication in the inner binary search loop.

    Complexity:
        Time: O(m log m + n log m)
        Space: O(m) auxiliary space for sorted copy of potions
    """
    sorted_potions = sorted(potions)
    m = len(sorted_potions)
    result = [0] * len(spells)

    for i, spell in enumerate(spells):
        # Minimum potion strength needed: ceil(success / spell)
        min_potion = (success + spell - 1) // spell

        left, right = 0, m - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_potions[mid] >= min_potion:
                right = mid - 1
            else:
                left = mid + 1

        result[i] = m - left

    return result


class Solution:
    """LeetCode submission interface."""
    successfulPairs = staticmethod(successful_pairs)
