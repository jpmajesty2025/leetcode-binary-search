"""
LeetCode 1631: Path With Minimum Effort (Kruskal's Algorithm / Union-Find)
https://leetcode.com/problems/path-with-minimum-effort/

Strategy:
Models the problem as finding a bottleneck edge in a spanning tree (Kruskal's algorithm):
1. Extract all grid edges: weight = abs(heights[r1][c1] - heights[r2][c2]).
2. Sort all edges ascending by weight.
3. Union connected cells using Disjoint Set Union (DSU) with path compression and union by rank.
4. Stop and return the edge weight the moment (0, 0) and (rows-1, cols-1) belong to
   the same connected component.

Complexity:
    Time: O(E log E) = O(rows * cols * log(rows * cols)), dominated by sorting edges
    Space: O(rows * cols) for DSU structures and edge list
"""

from typing import List


def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    Find minimum effort path using Kruskal's algorithm and Union-Find.
    """
    if not heights or not heights[0]:
        return 0

    rows, cols = len(heights), len(heights[0])
    if rows == 1 and cols == 1:
        return 0

    total_cells = rows * cols
    parent = list(range(total_cells))
    rank = [0] * total_cells

    def find(i: int) -> int:
        root = i
        while parent[root] != root:
            root = parent[root]
        # Path compression
        while i != root:
            parent[i], i = root, parent[i]
        return root

    def union(i: int, j: int) -> bool:
        root_i, root_j = find(i), find(j)
        if root_i == root_j:
            return False
        if rank[root_i] < rank[root_j]:
            root_i, root_j = root_j, root_i
        parent[root_j] = root_i
        if rank[root_i] == rank[root_j]:
            rank[root_i] += 1
        return True

    edges = []
    for r in range(rows):
        for c in range(cols):
            curr = r * cols + c
            if r + 1 < rows:
                diff = abs(heights[r][c] - heights[r + 1][c])
                edges.append((diff, curr, (r + 1) * cols + c))
            if c + 1 < cols:
                diff = abs(heights[r][c] - heights[r][c + 1])
                edges.append((diff, curr, r * cols + (c + 1)))

    edges.sort(key=lambda x: x[0])
    target = total_cells - 1

    for diff, u, v in edges:
        union(u, v)
        if find(0) == find(target):
            return diff

    return 0


class Solution:
    """LeetCode submission interface."""
    minimumEffortPath = staticmethod(minimum_effort_path)
