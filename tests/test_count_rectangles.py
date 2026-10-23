import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import count_num_rectangles_containing_each_pt as bucket_bs_module
import count_rectangles_fenwick_sweep as fenwick_module
import count_rectangles_binary_search_manual as manual_bs_module

IMPLS = [
    bucket_bs_module.count_rectangles,
    fenwick_module.count_rectangles,
    manual_bs_module.count_rectangles,
]


def brute_force_oracle(rectangles: List[List[int]], points: List[List[int]]) -> List[int]:
    """Independent oracle: exhaustive search over all rectangle-point pairs."""
    ans = []
    for px, py in points:
        count = sum(1 for rx, ry in rectangles if px <= rx and py <= ry)
        ans.append(count)
    return ans


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "rectangles, points, expected",
    [
        # LeetCode standard examples
        ([[1, 2], [2, 3], [2, 5]], [[2, 1], [1, 4]], [2, 1]),
        ([[1, 1], [2, 2], [3, 3]], [[1, 3], [1, 1]], [1, 3]),
        # Empty cases
        ([], [[1, 1]], [0]),
        ([[1, 1]], [], []),
        ([], [], []),
        # Point outside all rectangles
        ([[1, 1]], [[2, 2]], [0]),
        ([[5, 10]], [[6, 5], [4, 11]], [0, 0]),
        # Boundary edges and origin
        ([[5, 5]], [[5, 5], [0, 0], [5, 0], [0, 5]], [1, 1, 1, 1]),
        # Duplicate rectangles
        ([[2, 2], [2, 2], [2, 2]], [[1, 1]], [3]),
        # Maximum height constraint (height = 100)
        ([[10, 100]], [[5, 100], [10, 100], [11, 100]], [1, 1, 0]),
        # Large coordinate lengths (up to 10^9)
        ([[10**9, 50]], [[10**9, 50], [10**9 - 1, 50], [10**9 + 1, 50]], [1, 1, 0]),
    ],
)
def test_known_and_edge_cases(impl, rectangles, points, expected):
    assert impl(copy.deepcopy(rectangles), copy.deepcopy(points)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_inputs(impl):
    rectangles = [[1, 2], [2, 3], [2, 5]]
    points = [[2, 1], [1, 4]]
    r_copy = copy.deepcopy(rectangles)
    p_copy = copy.deepcopy(points)
    impl(rectangles, points)
    assert rectangles == r_copy
    assert points == p_copy


@pytest.mark.parametrize(
    "module",
    [bucket_bs_module, fenwick_module, manual_bs_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    rectangles = [[1, 2], [2, 3], [2, 5]]
    points = [[2, 1], [1, 4]]
    assert sol.countRectangles(rectangles, points) == [2, 1]
    assert module.Solution.countRectangles(rectangles, points) == [2, 1]


@settings(max_examples=250, deadline=None)
@given(
    rectangles=st.lists(
        st.tuples(st.integers(min_value=1, max_value=500), st.integers(min_value=1, max_value=30)).map(list),
        min_size=1,
        max_size=30,
    ),
    points=st.lists(
        st.tuples(st.integers(min_value=1, max_value=500), st.integers(min_value=1, max_value=30)).map(list),
        min_size=1,
        max_size=20,
    ),
)
def test_hypothesis_matches_oracle_and_all_agree(rectangles, points):
    expected = brute_force_oracle(rectangles, points)

    results = [impl(copy.deepcopy(rectangles), copy.deepcopy(points)) for impl in IMPLS]

    # Verify 100% agreement and correctness
    assert len(set(tuple(r) for r in results)) == 1
    assert results[0] == expected


@settings(max_examples=250, deadline=None)
@given(
    rectangles=st.lists(
        st.tuples(st.integers(min_value=1, max_value=500), st.integers(min_value=1, max_value=30)).map(list),
        min_size=1,
        max_size=30,
    ),
    points=st.lists(
        st.tuples(st.integers(min_value=1, max_value=500), st.integers(min_value=1, max_value=30)).map(list),
        min_size=1,
        max_size=20,
    ),
)
def test_containment_invariants(rectangles, points):
    ans = fenwick_module.count_rectangles(copy.deepcopy(rectangles), copy.deepcopy(points))
    n = len(rectangles)

    for count in ans:
        assert 0 <= count <= n
