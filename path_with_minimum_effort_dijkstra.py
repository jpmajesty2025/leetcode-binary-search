"""
LeetCode 1631: Path With Minimum Effort (Modified Dijkstra)
https://leetcode.com/problems/path-with-minimum-effort/

Strategy:
Models the grid as a graph where the distance to a cell is the minimax effort
required to reach it from (0, 0).
Uses Dijkstra's algorithm with a min-heap:
- dist[r][c] stores the minimum effort required to reach (r, c).
- At each step, pop the cell with smallest effort.
- Relaxation: next_effort = max(curr_effort, abs(heights[nr][nc] - heights[r][c]))
- Early exit: return immediately as soon as (rows-1, cols-1) is popped from the heap.

Complexity:
    Time: O(rows * cols * log(rows * cols))
    Space: O(rows * cols) for priority queue and distance matrix
"""

import heapq
from typing import List


def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    Find minimum effort path using modified Dijkstra's algorithm.
    """
    if not heights or not heights[0]:
        return 0

    rows, cols = len(heights), len(heights[0])
    if rows == 1 and cols == 1:
        return 0

    # dist[r][c] records the minimum effort to reach cell (r, c)
    dist = [[float("inf")] * cols for _ in range(rows)]
    dist[0][0] = 0

    # Min-heap stores tuples of (effort, row, col)
    pq = [(0, 0, 0)]

    while pq:
        eff, r, c = heapq.heappop(pq)

        # Early exit: first time we pop destination is guaranteed to be minimal effort
        if r == rows - 1 and c == cols - 1:
            return eff

        if eff > dist[r][c]:
            continue

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                step_effort = max(eff, abs(heights[nr][nc] - heights[r][c]))
                if step_effort < dist[nr][nc]:
                    dist[nr][nc] = step_effort
                    heapq.heappush(pq, (step_effort, nr, nc))

    return int(dist[rows - 1][cols - 1])


class Solution:
    """LeetCode submission interface."""
    minimumEffortPath = staticmethod(minimum_effort_path)
