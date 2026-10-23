import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import max_distance_between_pair_of_values as tp_module
import max_distance_binary_search as bs_module
import max_distance_bisect as bisect_module

IMPLS = [
    tp_module.max_distance,
    bs_module.max_distance,
    bisect_module.max_distance,
]


def brute_force_oracle(nums1: List[int], nums2: List[int]) -> int:
    """Independent oracle: exhaustive search over all valid pairs."""
    ans = 0
    for i in range(len(nums1)):
        for j in range(i, len(nums2)):
            if nums1[i] <= nums2[j]:
                ans = max(ans, j - i)
    return ans


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums1, nums2, expected",
    [
        # LeetCode standard examples
        ([55, 30, 5, 4, 2], [100, 20, 10, 10, 5], 2),
        ([2, 2, 2], [10, 10, 1], 1),
        ([30, 29, 19, 5], [25, 25, 25, 25, 25], 2),
        # Empty cases
        ([], [], 0),
        ([1], [], 0),
        ([], [1], 0),
        # No valid pairs (nums1 elements always strictly greater)
        ([100], [5], 0),
        ([50, 40, 30], [20, 10, 5], 0),
        # Diagonal matches only (i == j, max distance 0)
        ([5, 4, 3], [5, 4, 3], 0),
        # Singletons
        ([5], [10], 0),
        ([10], [5], 0),
        # Maximum possible stretch
        ([1], [10] * 50, 49),
        ([1] * 10, [1] * 10, 9),
        # Long identical prefixes
        ([10, 10, 10], [10, 10, 10, 10], 3),
    ],
)
def test_known_and_edge_cases(impl, nums1, nums2, expected):
    assert impl(list(nums1), list(nums2)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_inputs(impl):
    nums1 = [55, 30, 5, 4, 2]
    nums2 = [100, 20, 10, 10, 5]
    n1_copy = copy.deepcopy(nums1)
    n2_copy = copy.deepcopy(nums2)
    impl(nums1, nums2)
    assert nums1 == n1_copy
    assert nums2 == n2_copy


@pytest.mark.parametrize(
    "module",
    [tp_module, bs_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums1 = [55, 30, 5, 4, 2]
    nums2 = [100, 20, 10, 10, 5]
    assert sol.maxDistance(nums1, nums2) == 2
    assert module.Solution.maxDistance(nums1, nums2) == 2


@settings(max_examples=250, deadline=None)
@given(
    data=st.tuples(
        st.lists(st.integers(min_value=1, max_value=300), min_size=1, max_size=25).map(
            lambda l: sorted(l, reverse=True)
        ),
        st.lists(st.integers(min_value=1, max_value=300), min_size=1, max_size=25).map(
            lambda l: sorted(l, reverse=True)
        ),
    )
)
def test_hypothesis_matches_oracle_and_all_agree(data):
    nums1, nums2 = data
    expected = brute_force_oracle(nums1, nums2)

    results = [impl(list(nums1), list(nums2)) for impl in IMPLS]

    # Verify 100% agreement
    assert len(set(results)) == 1
    assert results[0] == expected


@settings(max_examples=250, deadline=None)
@given(
    data=st.tuples(
        st.lists(st.integers(min_value=1, max_value=300), min_size=1, max_size=25).map(
            lambda l: sorted(l, reverse=True)
        ),
        st.lists(st.integers(min_value=1, max_value=300), min_size=1, max_size=25).map(
            lambda l: sorted(l, reverse=True)
        ),
    )
)
def test_optimality_invariants(data):
    nums1, nums2 = data
    d = bs_module.max_distance(list(nums1), list(nums2))

    # Invariant 1: Distance is non-negative
    assert d >= 0

    # Invariant 2: Distance cannot exceed len(nums2) - 1
    assert d < len(nums2)

    # Invariant 3: If d > 0, there exists at least one pair with distance d
    if d > 0:
        found = False
        for i in range(len(nums1)):
            j = i + d
            if j < len(nums2) and nums1[i] <= nums2[j]:
                found = True
                break
        assert found
