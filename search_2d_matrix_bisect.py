"""
Alternative Strategy: Utilizing Python's Standard Library bisect
1. Two-pass bisect (search_matrix_bisect_twopass):
   - Locate the candidate row using bisect_right on row head elements.
   - Run C-speed bisect_left on the candidate row.
2. Virtual 1D bisect (search_matrix):
   - Binary search over virtual range(m * n) with a key function translating
     1D indices into matrix values.

Complexity:
    Time: O(log(m * n))
    Space: O(1) auxiliary space
"""

import bisect
from typing import List


def search_matrix_bisect_twopass(matrix: List[List[int]], target: int) -> bool:
    """
    Search matrix using standard library bisect in two passes:
    C-level binary search on row heads, then C-level binary search within candidate row.
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    if target < matrix[0][0] or target > matrix[-1][-1]:
        return False

    # Find the row whose first element is <= target
    row_idx = bisect.bisect_right(range(m), target, key=lambda r: matrix[r][0]) - 1
    if row_idx < 0:
        return False

    row = matrix[row_idx]
    col_idx = bisect.bisect_left(row, target)
    return col_idx < n and row[col_idx] == target


def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Search matrix using bisect_left over a virtual 1D index space range(m * n).
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    if target < matrix[0][0] or target > matrix[-1][-1]:
        return False

    total = m * n
    idx = bisect.bisect_left(range(total), target, key=lambda i: matrix[i // n][i % n])
    return idx < total and matrix[idx // n][idx % n] == target


class Solution:
    """LeetCode submission interface."""
    searchMatrix = staticmethod(search_matrix)
