import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import search_insert_position as orig_module
import search_insert_position_half_open as half_open_module
import search_insert_position_bisect as bisect_module

IMPLS = [
    orig_module.search_insert,
    half_open_module.search_insert,
    bisect_module.search_insert,
]


def brute_force_oracle(nums: List[int], target: int) -> int:
    """Independent ground truth: first index where nums[i] >= target, or len(nums)."""
    for i, x in enumerate(nums):
        if x >= target:
            return i
    return len(nums)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, target, expected",
    [
        # LeetCode standard examples
        ([1, 3, 5, 6], 5, 2),
        ([1, 3, 5, 6], 2, 1),
        ([1, 3, 5, 6], 7, 4),
        # Boundary cases
        ([1, 3, 5, 6], 0, 0),
        ([1, 3, 5, 6], 1, 0),
        ([1, 3, 5, 6], 6, 3),
        # Empty array
        ([], 5, 0),
        # Singletons
        ([5], 2, 0),
        ([5], 5, 0),
        ([5], 8, 1),
        # Two elements
        ([1, 3], 0, 0),
        ([1, 3], 1, 0),
        ([1, 3], 2, 1),
        ([1, 3], 3, 1),
        ([1, 3], 4, 2),
        # Negative numbers and zeros
        ([-10, -5, -2, 0, 3], -12, 0),
        ([-10, -5, -2, 0, 3], -5, 1),
        ([-10, -5, -2, 0, 3], -1, 3),
        ([-10, -5, -2, 0, 3], 0, 3),
        ([-10, -5, -2, 0, 3], 4, 5),
        # 32-bit signed integer boundaries
        ([-(2**31), 0, 2**31 - 1], -(2**31), 0),
        ([-(2**31), 0, 2**31 - 1], 2**31 - 1, 2),
        ([-(2**31), 0, 2**31 - 1], 2**31, 3),
    ],
)
def test_known_and_edge_cases(impl, nums, target, expected):
    assert impl(list(nums), target) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_nums(impl):
    nums = [1, 3, 5, 6]
    nums_copy = copy.deepcopy(nums)
    impl(nums, 2)
    impl(nums, 5)
    assert nums == nums_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, half_open_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums = [1, 3, 5, 6]
    assert sol.searchInsert(nums, 5) == 2
    assert sol.searchInsert(nums, 2) == 1
    assert module.Solution.searchInsert(nums, 7) == 4


@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-5000, max_value=5000), unique=True, min_size=0, max_size=40),
    target=st.integers(min_value=-6000, max_value=6000),
)
def test_hypothesis_matches_oracle_and_all_agree(nums, target):
    sorted_nums = sorted(nums)
    expected = brute_force_oracle(sorted_nums, target)

    results = [impl(list(sorted_nums), target) for impl in IMPLS]

    for res in results:
        assert res == expected

    # 100% agreement across all implementations
    assert len(set(results)) == 1


@settings(max_examples=250, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=-5000, max_value=5000), unique=True, min_size=1, max_size=40),
    target=st.integers(min_value=-6000, max_value=6000),
)
def test_lower_bound_invariants(nums, target):
    sorted_nums = sorted(nums)
    idx = half_open_module.search_insert(sorted_nums, target)
    n = len(sorted_nums)

    # Invariant 1: 0 <= idx <= n
    assert 0 <= idx <= n

    # Invariant 2: all elements strictly before idx are < target
    if idx > 0:
        assert sorted_nums[idx - 1] < target

    # Invariant 3: element at idx (if within bounds) is >= target
    if idx < n:
        assert sorted_nums[idx] >= target

    # Invariant 4: if target is in array, nums[idx] == target
    if target in sorted_nums:
        assert sorted_nums[idx] == target
