"""
LeetCode 1631: Path With Minimum Effort
https://leetcode.com/problems/path-with-minimum-effort/

You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size
rows x columns, where heights[row][col] represents the height of cell (row, col).
You are situated in the top-left cell (0, 0), and you hope to travel to the bottom-right
cell (rows-1, columns-1). You can move up, down, left, or right, and you wish to find
a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two consecutive
cells of the route. Return the minimum effort required.
"""

from collections import deque
from typing import List


def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    Compute minimum effort path using Binary Search on Answer + BFS reachability.

    The feasibility predicate can_reach(limit) checks whether a path from (0, 0)
    to (rows-1, cols-1) exists where every step has height difference <= limit.
    Because can_reach(limit) is monotonic with respect to limit, we binary search
    the effort range [0, max(heights) - min(heights)].

    Complexity:
        Time: O(rows * cols * log(max_diff))
        Space: O(rows * cols) for BFS visited matrix and queue
    """
    if not heights or not heights[0]:
        return 0

    rows, cols = len(heights), len(heights[0])
    if rows == 1 and cols == 1:
        return 0

    min_h = min(min(row) for row in heights)
    max_h = max(max(row) for row in heights)

    # Tight bounds: effort cannot exceed the global maximum height difference
    left, right = 0, max_h - min_h

    def can_reach_destination(max_effort: int) -> bool:
        visited = [[False] * cols for _ in range(rows)]
        queue = deque([(0, 0)])
        visited[0][0] = True

        while queue:
            r, c = queue.popleft()
            if r == rows - 1 and c == cols - 1:
                return True

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    if abs(heights[nr][nc] - heights[r][c]) <= max_effort:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return False

    while left < right:
        mid = (left + right) // 2
        if can_reach_destination(mid):
            right = mid
        else:
            left = mid + 1

    return left


class Solution:
    """LeetCode submission interface."""
    minimumEffortPath = staticmethod(minimum_effort_path)
