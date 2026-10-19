"""
LeetCode 2300: Successful Pairs of Spells and Potions (Suffix Frequency Array)
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/

Strategy:
When potion values are bounded (e.g., max(potions) <= 10^5):
1. Build a frequency array count[v] recording occurrences of each potion value.
2. Accumulate suffix sums in-place from right to left so that
   count[v] becomes the number of potions with strength >= v.
3. For each spell, calculate min_potion = ceil(success / spell).
   Lookup count[min_potion] in O(1) time.

Complexity:
    Time: O(m + K + n), where K = max(potions)
    Space: O(K) auxiliary space for the frequency/suffix array
"""

from typing import List


def successful_pairs(spells: List[int], potions: List[int], success: int) -> List[int]:
    """
    Compute successful pairs using a suffix-sum frequency array.
    Provides O(1) lookup per spell query when potion strengths are bounded.
    """
    if not potions:
        return [0] * len(spells)

    max_potion = max(potions)
    # freq[v] will store the number of potions with strength >= v
    freq = [0] * (max_potion + 2)

    for p in potions:
        freq[p] += 1

    # Accumulate suffix sums backwards
    for v in range(max_potion, 0, -1):
        freq[v] += freq[v + 1]

    result = [0] * len(spells)
    for i, spell in enumerate(spells):
        min_potion = (success + spell - 1) // spell
        if min_potion <= max_potion:
            result[i] = freq[min_potion]

    return result


class Solution:
    """LeetCode submission interface."""
    successfulPairs = staticmethod(successful_pairs)
