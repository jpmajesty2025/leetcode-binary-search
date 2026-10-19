"""
Alternative Strategy: Two-Pass Binary Search
1. Pass 1 (Row Search): Binary search over row boundaries to locate the unique candidate row.
   A row r is a candidate if matrix[r][0] <= target <= matrix[r][-1].
2. Pass 2 (Column Search): Standard binary search within that single 1D row.

Advantages:
- Cache locality: Pass 2 operates on a single contiguous row list in memory.
- No coordinate arithmetic (div/mod) inside the inner search loop of pass 2.
- Cleanly decomposes the 2D search into two independent 1D binary searches.

Complexity:
    Time: O(log m + log n) = O(log(m * n))
    Space: O(1) auxiliary space
"""

from typing import List


def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Search for target using two sequential binary searches:
    find candidate row in O(log m), then search within that row in O(log n).
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    # O(1) boundary check: reject targets outside the matrix's value range
    if target < matrix[0][0] or target > matrix[-1][-1]:
        return False

    # Pass 1: Binary search to find candidate row
    top, bottom = 0, m - 1
    target_row = -1

    while top <= bottom:
        mid_row = (top + bottom) // 2
        if matrix[mid_row][0] <= target <= matrix[mid_row][-1]:
            target_row = mid_row
            break
        elif matrix[mid_row][0] > target:
            bottom = mid_row - 1
        else:
            top = mid_row + 1

    if target_row == -1:
        return False

    # Pass 2: Binary search within the identified row
    row = matrix[target_row]
    left, right = 0, n - 1

    while left <= right:
        mid = (left + right) // 2
        if row[mid] == target:
            return True
        elif row[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


class Solution:
    """LeetCode submission interface."""
    searchMatrix = staticmethod(search_matrix)
