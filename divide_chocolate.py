"""
LeetCode 1231: Divide Chocolate
https://leetcode.com/problems/divide-chocolate/

You have one chocolate bar that consists of some chunks. Each chunk has its own sweetness
given by the array sweetness.

You want to share the chocolate with your k friends so you start cutting the chocolate bar
into k + 1 pieces using k cuts, each piece consisting of some consecutive chunks.

Being generous, you will eat the piece with the minimum total sweetness and give the other
pieces to your friends. Return the maximum total sweetness of the piece you can get by
cutting the chocolate bar optimally.
"""

from typing import List


def maximize_sweetness(sweetness: List[int], k: int) -> int:
    """
    Compute maximum sweetness of the minimum piece using Maximin Binary Search.

    Optimizations:
    - If k == 0: you keep the whole chocolate, return sum(sweetness) in O(1).
    - If k + 1 == len(sweetness): each piece is a single chunk, return min(sweetness) in O(1).
    - Tight upper bound: by the pigeonhole principle, the minimum piece can never exceed
      the average piece size: sum(sweetness) // (k + 1).
    - Early exit in feasibility: return True as soon as k + 1 pieces are formed.
    - Upper-mid formula (left + right + 1) // 2 prevents infinite loops when left = mid.

    Complexity:
        Time: O(n log(sum(sweetness) // (k + 1) - min(sweetness) + 1))
        Space: O(1) auxiliary space
    """
    if not sweetness:
        return 0

    n = len(sweetness)
    total_sweetness = sum(sweetness)

    # Fast-paths
    if k == 0:
        return total_sweetness
    if k + 1 == n:
        return min(sweetness)

    left = min(sweetness)
    # The minimum piece can never exceed the average piece size
    right = total_sweetness // (k + 1)
    needed_pieces = k + 1

    def can_divide(min_sweetness: int) -> bool:
        current_sum = 0
        pieces = 0
        for s in sweetness:
            current_sum += s
            if current_sum >= min_sweetness:
                pieces += 1
                if pieces == needed_pieces:
                    return True
                current_sum = 0
        return False

    while left < right:
        mid = (left + right + 1) // 2
        if can_divide(mid):
            left = mid
        else:
            right = mid - 1

    return left


class Solution:
    """LeetCode submission interface."""
    maximizeSweetness = staticmethod(maximize_sweetness)
