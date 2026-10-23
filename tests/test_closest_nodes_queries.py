import copy
from typing import List, Optional
import pytest
from hypothesis import given, settings, strategies as st

import closest_nodes_queries_in_bst as orig_module
import closest_nodes_queries_bisect as bisect_module
import closest_nodes_queries_morris as morris_module

TreeNode = orig_module.TreeNode

IMPLS = [
    orig_module.closest_nodes,
    bisect_module.closest_nodes,
    morris_module.closest_nodes,
]


def build_bst(arr: List[int]) -> Optional[TreeNode]:
    """Construct a height-balanced BST from a sorted array."""
    if not arr:
        return None
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    root.left = build_bst(arr[:mid])
    root.right = build_bst(arr[mid + 1 :])
    return root


def build_skewed_bst(n: int) -> TreeNode:
    """Construct a right-skewed degenerate BST of depth n."""
    root = TreeNode(1)
    curr = root
    for i in range(2, n + 1):
        curr.right = TreeNode(i)
        curr = curr.right
    return root


def brute_force_oracle(sorted_vals: List[int], queries: List[int]) -> List[List[int]]:
    ans = []
    for q in queries:
        floors = [x for x in sorted_vals if x <= q]
        ceils = [x for x in sorted_vals if x >= q]
        floor_val = max(floors) if floors else -1
        ceil_val = min(ceils) if ceils else -1
        ans.append([floor_val, ceil_val])
    return ans


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_1(impl):
    # Tree: [6,2,13,1,4,9,15,null,null,null,null,null,null,14]
    # Sorted: [1, 2, 4, 6, 9, 13, 14, 15]
    root = TreeNode(6)
    root.left = TreeNode(2, TreeNode(1), TreeNode(4))
    root.right = TreeNode(13, TreeNode(9), TreeNode(15, TreeNode(14)))

    queries = [2, 5, 16]
    expected = [[2, 2], [4, 6], [15, -1]]
    assert impl(root, queries) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_example_2(impl):
    # Tree: [4, null, 9]
    root = TreeNode(4, None, TreeNode(9))
    queries = [3]
    expected = [[-1, 4]]
    assert impl(root, queries) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_boundary_and_edge_cases(impl):
    root = build_bst([10, 20, 30])

    # Query below all elements
    assert impl(root, [5]) == [[-1, 10]]
    # Query above all elements
    assert impl(root, [35]) == [[30, -1]]
    # Query exact matches
    assert impl(root, [10, 20, 30]) == [[10, 10], [20, 20], [30, 30]]
    # Query in gaps
    assert impl(root, [15, 25]) == [[10, 20], [20, 30]]
    # Empty tree
    assert impl(None, [10, 20]) == [[-1, -1], [-1, -1]]


@pytest.mark.parametrize("impl", IMPLS)
def test_skewed_tree_no_recursion_error(impl):
    # Tree of depth 3,500 would crash default Python recursion (limit 1,000)
    root = build_skewed_bst(3500)
    queries = [1, 1750, 3500, 5000]
    expected = [[1, 1], [1750, 1750], [3500, 3500], [3500, -1]]
    assert impl(root, queries) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_queries(impl):
    root = build_bst([1, 2, 4, 6])
    queries = [2, 5]
    q_copy = list(queries)
    impl(root, queries)
    assert queries == q_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, morris_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    root = build_bst([4, 9])
    assert sol.closestNodes(root, [3]) == [[-1, 4]]
    assert module.Solution.closestNodes(root, [3]) == [[-1, 4]]


@settings(max_examples=200, deadline=None)
@given(
    tree_vals=st.lists(st.integers(min_value=1, max_value=500), min_size=1, max_size=30, unique=True).map(sorted),
    queries=st.lists(st.integers(min_value=0, max_value=600), min_size=1, max_size=20),
)
def test_hypothesis_matches_oracle_and_all_agree(tree_vals, queries):
    expected = brute_force_oracle(tree_vals, queries)

    # Build fresh BST for each implementation (Morris temporarily rewires pointers)
    r1 = orig_module.closest_nodes(build_bst(tree_vals), list(queries))
    r2 = bisect_module.closest_nodes(build_bst(tree_vals), list(queries))
    r3 = morris_module.closest_nodes(build_bst(tree_vals), list(queries))

    assert r1 == r2 == r3 == expected
