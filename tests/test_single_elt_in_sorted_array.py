import functools
import operator
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import single_elt_in_sorted_array as orig_module
import single_elt_in_sorted_array_xor as xor_module
import single_elt_in_sorted_array_even as even_module
import single_elt_in_sorted_array_bisect as bisect_module

IMPLS = [
    orig_module.single_non_duplicate,
    xor_module.single_non_duplicate,
    even_module.single_non_duplicate,
    bisect_module.single_non_duplicate,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_single_element_array(impl):
    assert impl([42]) == 42
    assert impl([-99]) == -99
    assert impl([0]) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_three_element_arrays(impl):
    # Single at index 0
    assert impl([1, 2, 2]) == 1
    # Single at index 2
    assert impl([1, 1, 2]) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_boundary_positions_in_medium_array(impl):
    # Single at index 0 (very start)
    assert impl([0, 1, 1, 2, 2, 3, 3]) == 0
    # Single at end
    assert impl([1, 1, 2, 2, 3, 3, 4]) == 4
    # Single in middle
    assert impl([1, 1, 2, 3, 3, 4, 4, 8, 8]) == 2
    assert impl([3, 3, 7, 7, 10, 11, 11]) == 10


@pytest.mark.parametrize("impl", IMPLS)
def test_negative_and_zero_values(impl):
    arr = [-10, -10, -5, -1, -1, 0, 0]
    assert impl(arr) == -5


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale_array(impl):
    # 50,000 pairs + 1 single element at index 70,000
    N_PAIRS = 50000
    single_val = 9999999
    single_pair_idx = 35000

    arr = []
    val = 1
    for i in range(N_PAIRS):
        if i == single_pair_idx:
            arr.append(single_val)
        arr.append(val)
        arr.append(val)
        val += 1

    assert impl(arr) == single_val


@pytest.mark.parametrize(
    "module",
    [orig_module, xor_module, even_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    arr = [1, 1, 2, 3, 3]
    assert sol.singleNonDuplicate(arr) == 2
    assert module.Solution.singleNonDuplicate(arr) == 2


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=0, max_value=200).flatmap(
        lambda num_pairs: st.tuples(
            st.just(num_pairs),
            st.lists(
                st.integers(min_value=-10000, max_value=10000),
                min_size=num_pairs + 1,
                max_size=num_pairs + 1,
                unique=True,
            ),
            st.integers(min_value=0, max_value=num_pairs),
        )
    )
)
def test_hypothesis_matches_xor_ground_truth(data):
    num_pairs, unique_elts, target_insert_pos = data
    single_val = unique_elts[-1]
    pair_vals = unique_elts[:-1]

    # Build sorted array
    arr = []
    for i in range(num_pairs):
        if i == target_insert_pos:
            arr.append(single_val)
        arr.append(pair_vals[i])
        arr.append(pair_vals[i])
    if target_insert_pos == num_pairs:
        arr.append(single_val)

    arr.sort()

    # Ground truth: bitwise XOR reduction
    expected = functools.reduce(operator.xor, arr)

    results = [impl(arr) for impl in IMPLS]
    assert len(set(results)) == 1
    assert results[0] == expected
