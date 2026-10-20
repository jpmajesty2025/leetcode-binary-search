import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import path_with_minimum_effect as bs_module
import path_with_minimum_effort_dijkstra as dijkstra_module
import path_with_minimum_effort_union_find as uf_module

IMPLS = [
    bs_module.minimum_effort_path,
    dijkstra_module.minimum_effort_path,
    uf_module.minimum_effort_path,
]


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "heights, expected",
    [
        # LeetCode standard examples
        ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
        ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
        (
            [
                [1, 2, 1, 1, 1],
                [1, 2, 1, 2, 1],
                [1, 2, 1, 2, 1],
                [1, 2, 1, 2, 1],
                [1, 1, 1, 2, 1],
            ],
            0,
        ),
        # Empty cases
        ([], 0),
        ([[]], 0),
        # Singleton grid
        ([[5]], 0),
        # Single row grid (1 x n)
        ([[1, 3, 5, 8]], 3),
        # Single column grid (m x 1)
        ([[1], [10], [12]], 9),
        # Flat plateau grid
        ([[4, 4, 4], [4, 4, 4]], 0),
        # 2x2 grid choosing easier path
        ([[1, 10], [2, 3]], 1),
        # Large jump vs winding path
        ([[1, 100], [1, 1]], 0),
        # Large values up to 10^6
        ([[1, 1000000], [1, 1]], 0),
        ([[1, 1000000], [1000000, 1000000]], 999999),
    ],
)
def test_known_and_edge_cases(impl, heights, expected):
    assert impl(copy.deepcopy(heights)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_heights(impl):
    heights = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    heights_copy = copy.deepcopy(heights)
    impl(heights)
    assert heights == heights_copy


@pytest.mark.parametrize(
    "module",
    [bs_module, dijkstra_module, uf_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    heights = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    assert sol.minimumEffortPath(heights) == 2
    assert module.Solution.minimumEffortPath(heights) == 2


@settings(max_examples=150, deadline=None)
@given(
    heights=st.tuples(st.integers(min_value=1, max_value=8), st.integers(min_value=1, max_value=8)).flatmap(
        lambda dims: st.lists(
            st.lists(st.integers(min_value=1, max_value=500), min_size=dims[1], max_size=dims[1]),
            min_size=dims[0],
            max_size=dims[0],
        )
    )
)
def test_hypothesis_all_agree_and_respect_bounds(heights):
    results = [impl(copy.deepcopy(heights)) for impl in IMPLS]

    # Verify 100% agreement among all three algorithms
    assert len(set(results)) == 1

    ans = results[0]
    min_h = min(min(r) for r in heights)
    max_h = max(max(r) for r in heights)

    # Invariant: 0 <= effort <= max(heights) - min(heights)
    assert 0 <= ans <= max_h - min_h
