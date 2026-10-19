"""
You are given an m x n integer matrix matrix with the following two properties:
1. Each row is sorted in non-decreasing order.
2. The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return True if target is in matrix or False otherwise.
You must write a solution in O(log(m * n)) time complexity and O(1) auxiliary space.
"""

from typing import List


def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Search for target in an m x n matrix using virtual 1D binary search.

    Because row i + 1 starts strictly after row i ends, the entire 2D matrix
    maps directly to a single monotonically sorted 1D array of length m * n.
    Index k in [0, m * n - 1] maps to 2D coordinates:
        row = k // n
        col = k % n

    Complexity:
        Time: O(log(m * n))
        Space: O(1) auxiliary space
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    # O(1) boundary check: reject targets outside the matrix's value range
    if target < matrix[0][0] or target > matrix[-1][-1]:
        return False

    left, right = 0, m * n - 1

    while left <= right:
        mid = (left + right) // 2
        # Translate 1D virtual index to 2D coordinates
        mid_value = matrix[mid // n][mid % n]

        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


class Solution:
    """LeetCode submission interface."""
    searchMatrix = staticmethod(search_matrix)
