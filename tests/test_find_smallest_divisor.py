import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import find_smallest_divisor_to_achieve_sum_lte_threshold as orig_module
import find_smallest_divisor_bisect as bisect_module
import find_smallest_divisor_counting as counting_module

IMPLS = [
    orig_module.smallest_divisor,
    bisect_module.smallest_divisor,
    counting_module.smallest_divisor,
]


def brute_force_oracle(nums: List[int], threshold: int) -> int:
    """Independent oracle: linear probe starting from theoretical lower bound."""
    if not nums:
        return 1
    d = max(1, (sum(nums) + threshold - 1) // threshold)
    while True:
        if sum((x + d - 1) // d for x in nums) <= threshold:
            return d
        d += 1


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, threshold, expected",
    [
        # LeetCode standard examples
        ([1, 2, 5, 9], 6, 5),
        ([44, 22, 33, 11, 1], 5, 44),
        ([21212, 10101, 12121], 1000000, 1),
        # Empty case
        ([], 5, 1),
        # threshold == len(nums)
        ([10, 20, 30], 3, 30),
        ([5, 5, 5, 5], 4, 5),
        # Single element
        ([5], 1, 5),
        ([5], 5, 1),
        ([5], 10, 1),
        # Exact integer division sum matches threshold
        ([10, 20, 30], 6, 10),
        # Duplicate values
        ([2, 2, 2, 2], 4, 2),
        ([2, 2, 2, 2], 8, 1),
        ([3, 3, 3, 3], 6, 3),
        # Large values up to 10^6
        ([1000000], 1, 1000000),
        ([1000000], 2, 500000),
    ],
)
def test_known_and_edge_cases(impl, nums, threshold, expected):
    assert impl(list(nums), threshold) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_nums(impl):
    nums = [1, 2, 5, 9]
    nums_copy = copy.deepcopy(nums)
    impl(nums, 6)
    assert nums == nums_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, counting_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums = [1, 2, 5, 9]
    assert sol.smallestDivisor(nums, 6) == 5
    assert module.Solution.smallestDivisor(nums, 6) == 5


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=n, max_value=n * 50),
        )
    )
)
def test_hypothesis_matches_oracle_and_all_agree(data):
    nums, threshold = data
    expected = brute_force_oracle(nums, threshold)

    results = [impl(list(nums), threshold) for impl in IMPLS]

    # Verify 100% agreement
    assert len(set(results)) == 1
    assert results[0] == expected


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=n, max_value=n * 50),
        )
    )
)
def test_optimality_invariants(data):
    nums, threshold = data
    d = counting_module.smallest_divisor(nums, threshold)

    # Invariant 1: Divisor d achieves sum <= threshold
    assert sum((x + d - 1) // d for x in nums) <= threshold

    # Invariant 2: Divisor d - 1 (if d > 1) fails to achieve threshold
    if d > 1:
        assert sum((x + d - 2) // (d - 1) for x in nums) > threshold

    # Invariant 3: Divisor respects theoretical bounds
    assert d >= max(1, (sum(nums) + threshold - 1) // threshold)
    assert d <= max(nums)
