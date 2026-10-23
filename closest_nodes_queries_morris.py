"""
LeetCode 2476: Closest Nodes Queries in a Binary Search Tree (Morris Traversal)
https://leetcode.com/problems/closest-nodes-queries-in-a-binary-search-tree/

Strategy:
Uses Morris In-Order Traversal:
- Re-wires tree nodes using threaded binary tree pointers (connecting in-order
  predecessor to current node).
- Achieves in-order traversal in O(n) time and O(1) auxiliary traversal space
  (no recursion, no stack frames).
- Followed by bisect.bisect_left for query resolution in O(log n).

Complexity:
    Time: O(n + m log n) where n = number of nodes and m = len(queries)
    Space: O(n) for the output sorted values array (O(1) auxiliary traversal space)
"""

import bisect
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def closest_nodes(root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
    """
    Find closest nodes using Morris In-Order Traversal and bisect_left.
    """
    if not root:
        return [[-1, -1] for _ in queries]

    sorted_values: List[int] = []
    curr: Optional[TreeNode] = root

    # Morris in-order traversal (O(1) auxiliary traversal space)
    while curr:
        if not curr.left:
            sorted_values.append(curr.val)
            curr = curr.right
        else:
            # Find in-order predecessor
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right

            if not pred.right:
                # Thread predecessor to current node
                pred.right = curr
                curr = curr.left
            else:
                # Thread already exists: remove thread and visit current
                pred.right = None
                sorted_values.append(curr.val)
                curr = curr.right

    answer: List[List[int]] = []
    n = len(sorted_values)

    for q in queries:
        idx = bisect.bisect_left(sorted_values, q)
        if idx < n and sorted_values[idx] == q:
            answer.append([q, q])
        else:
            floor_val = sorted_values[idx - 1] if idx > 0 else -1
            ceil_val = sorted_values[idx] if idx < n else -1
            answer.append([floor_val, ceil_val])

    return answer


class Solution:
    """LeetCode submission interface."""
    closestNodes = staticmethod(closest_nodes)
