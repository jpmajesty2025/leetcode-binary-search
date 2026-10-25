from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import search_in_rotated_sorted_array as orig_module
import search_in_rotated_sorted_array_two_pass as two_pass_module
import search_in_rotated_sorted_array_modulo as modulo_module
import search_in_rotated_sorted_array_inflection as inflection_module

IMPLS = [
    orig_module.search,
    two_pass_module.search,
    modulo_module.search,
    inflection_module.search,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_empty_and_single_element(impl):
    assert impl([], 5) == -1
    assert impl([5], 5) == 0
    assert impl([5], 3) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_two_element_arrays(impl):
    # Unrotated
    assert impl([1, 3], 1) == 0
    assert impl([1, 3], 3) == 1
    assert impl([1, 3], 0) == -1
    assert impl([1, 3], 2) == -1
    assert impl([1, 3], 4) == -1

    # Rotated
    assert impl([3, 1], 3) == 0
    assert impl([3, 1], 1) == 1
    assert impl([3, 1], 0) == -1
    assert impl([3, 1], 2) == -1
    assert impl([3, 1], 4) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert impl(nums, 0) == 4
    assert impl(nums, 3) == -1
    assert impl([1], 0) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_all_rotation_offsets(impl):
    base = [0, 1, 2, 4, 5, 6, 7]
    n = len(base)
    for k in range(n):
        rotated = base[k:] + base[:k]
        # Target present
        for expected_idx, val in enumerate(rotated):
            assert impl(rotated, val) == expected_idx
        # Target absent
        for val in [-5, 3, 10]:
            assert impl(rotated, val) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_numbers(impl):
    nums = [-3, -1, -10, -7, -5]
    for expected_idx, val in enumerate(nums):
        assert impl(nums, val) == expected_idx
    assert impl(nums, -4) == -1
    assert impl(nums, 0) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    N = 5000
    base = list(range(0, 2 * N, 2))
    k = 1842
    rotated = base[k:] + base[:k]

    # Search boundaries and pivot
    assert impl(rotated, rotated[0]) == 0
    assert impl(rotated, rotated[-1]) == N - 1
    assert impl(rotated, base[0]) == (N - k) % N
    assert impl(rotated, 99999) == -1


@pytest.mark.parametrize(
    "module",
    [orig_module, two_pass_module, modulo_module, inflection_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert sol.search(nums, 0) == 4
    assert module.Solution.search(nums, 0) == 4


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=200).flatmap(
        lambda n: st.tuples(
            st.just(n),
            st.lists(
                st.integers(min_value=-5000, max_value=5000),
                min_size=n,
                max_size=n,
                unique=True,
            ).map(sorted),
            st.integers(min_value=0, max_value=n - 1),
            st.integers(min_value=-6000, max_value=6000),
        )
    )
)
def test_hypothesis_agreement_and_accuracy(data):
    n, sorted_nums, k, target = data
    rotated = sorted_nums[k:] + sorted_nums[:k]
    expected = rotated.index(target) if target in rotated else -1

    results = [impl(rotated, target) for impl in IMPLS]
    assert len(set(results)) == 1
    assert results[0] == expected
