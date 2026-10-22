import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import split_largest_array_sum as orig_module
import split_largest_array_sum_prefix_jump as prefix_jump_module
import split_largest_array_sum_bisect as bisect_module

IMPLS = [
    orig_module.split_array,
    prefix_jump_module.split_array,
    bisect_module.split_array,
]


def can_split(nums: List[int], max_sum: int, k: int) -> bool:
    curr = 0
    subarrays = 1
    for x in nums:
        curr += x
        if curr > max_sum:
            subarrays += 1
            curr = x
            if subarrays > k:
                return False
    return True


def brute_force_oracle(nums: List[int], k: int) -> int:
    """Independent oracle: linear probe upwards from theoretical minimum."""
    if not nums:
        return 0
    target = max(max(nums), (sum(nums) + k - 1) // k)
    while True:
        if can_split(nums, target, k):
            return target
        target += 1


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, k, expected",
    [
        # LeetCode standard examples
        ([7, 2, 5, 10, 8], 2, 18),
        ([1, 2, 3, 4, 5], 2, 9),
        # Empty case
        ([], 1, 0),
        # k == 1 (single subarray)
        ([1, 2, 3, 4, 5], 1, 15),
        ([10], 1, 10),
        # k == len(nums) (each element is its own subarray)
        ([1, 2, 3, 4, 5], 5, 5),
        ([10, 20, 30], 3, 30),
        # Identical elements
        ([3, 3, 3, 3], 2, 6),
        ([3, 3, 3, 3], 4, 3),
        ([5, 5, 5, 5], 3, 10),
        # Large values up to 10^5
        ([100000] * 5, 2, 300000),
        ([100000] * 5, 5, 100000),
    ],
)
def test_known_and_edge_cases(impl, nums, k, expected):
    assert impl(list(nums), k) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_nums(impl):
    nums = [7, 2, 5, 10, 8]
    nums_copy = copy.deepcopy(nums)
    impl(nums, 2)
    assert nums == nums_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, prefix_jump_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums = [7, 2, 5, 10, 8]
    assert sol.splitArray(nums, 2) == 18
    assert module.Solution.splitArray(nums, 2) == 18


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=1, max_value=n),
        )
    )
)
def test_hypothesis_matches_oracle_and_all_agree(data):
    nums, k = data
    expected = brute_force_oracle(nums, k)

    results = [impl(list(nums), k) for impl in IMPLS]

    # Verify 100% agreement
    assert len(set(results)) == 1
    assert results[0] == expected


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=1, max_value=n),
        )
    )
)
def test_optimality_invariants(data):
    nums, k = data
    ans = prefix_jump_module.split_array(nums, k)

    # Invariant 1: Can partition into <= k subarrays of max sum ans
    assert can_split(nums, ans, k)

    # Invariant 2: Cannot partition into <= k subarrays of max sum ans - 1
    if ans > max(nums):
        assert not can_split(nums, ans - 1, k)

    # Invariant 3: Respects theoretical bounds
    assert ans >= max(max(nums), (sum(nums) + k - 1) // k)
    assert ans <= sum(nums)
