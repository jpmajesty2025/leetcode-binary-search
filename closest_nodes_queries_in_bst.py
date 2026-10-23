"""
LeetCode 2476: Closest Nodes Queries in a Binary Search Tree
https://leetcode.com/problems/closest-nodes-queries-in-a-binary-search-tree/

You are given the root of a binary search tree and an array queries of size n consisting
of positive integers.

Find a 2D array answer of size n where answer[i] = [min_i, max_i]:
- min_i is the largest value in the tree that is <= queries[i]. If none exists, -1.
- max_i is the smallest value in the tree that is >= queries[i]. If none exists, -1.

Return the array answer.
"""

from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def closest_nodes(root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
    """
    Find closest nodes (floor and ceiling) for each query in O(n + m log n) time.

    Why direct BST traversal causes TLE:
    - The problem does NOT guarantee a balanced BST.
    - Searching a skewed tree directly takes O(m * n) = 10^10 operations (TLE).
    - Solution: Flatten the BST into a sorted array in O(n), then binary search
      each query in O(log n).

    Why iterative traversal is used:
    - Recursive traversal on skewed trees with 10^5 nodes raises RecursionError.
    - Iterative stack traversal avoids Python's recursion limit entirely.

    Complexity:
        Time: O(n + m log n) where n = number of nodes and m = len(queries)
        Space: O(n) for the sorted values and traversal stack
    """
    if not root:
        return [[-1, -1] for _ in queries]

    # Iterative in-order traversal using an explicit stack
    sorted_values: List[int] = []
    stack: List[TreeNode] = []
    curr: Optional[TreeNode] = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        sorted_values.append(curr.val)
        curr = curr.right

    answer: List[List[int]] = []
    n = len(sorted_values)

    for query in queries:
        left, right = 0, n - 1
        floor_val, ceil_val = -1, -1

        while left <= right:
            mid = left + (right - left) // 2
            if sorted_values[mid] < query:
                floor_val = sorted_values[mid]
                left = mid + 1
            elif sorted_values[mid] > query:
                ceil_val = sorted_values[mid]
                right = mid - 1
            else:
                floor_val = ceil_val = sorted_values[mid]
                break

        answer.append([floor_val, ceil_val])

    return answer


class Solution:
    """LeetCode submission interface."""
    closestNodes = staticmethod(closest_nodes)
