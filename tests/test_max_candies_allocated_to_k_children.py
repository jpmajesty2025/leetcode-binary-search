from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import max_candies_allocated_to_k_children as opt_module
import max_candies_allocated_to_k_children_freq as freq_module
import max_candies_allocated_to_k_children_bisect as bisect_module

IMPLS = [
    opt_module.maximum_candies,
    freq_module.maximum_candies,
    bisect_module.maximum_candies,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_sum_less_than_k(impl):
    # Impossible to allocate even 1 candy to each child
    assert impl([2, 5], 11) == 0
    assert impl([1, 2, 3], 10) == 0
    assert impl([1], 2) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_exact_sum_matches_k(impl):
    assert impl([1, 2, 3], 6) == 1
    assert impl([5, 5], 10) == 1


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1: candies = [5, 8, 6], k = 3 -> 5
    assert impl([5, 8, 6], 3) == 5
    # Example 2: candies = [2, 5], k = 11 -> 0
    assert impl([2, 5], 11) == 0
    # Additional test
    assert impl([4, 7, 5], 4) == 3


@pytest.mark.parametrize("impl", IMPLS)
def test_single_pile(impl):
    assert impl([100], 4) == 25
    assert impl([7], 2) == 3
    assert impl([1], 1) == 1


@pytest.mark.parametrize("impl", IMPLS)
def test_large_k_impossible(impl):
    assert impl([10**7] * 10, 10**12) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    N = 10000
    candies = [i % 50 + 1 for i in range(N)]
    k = 5000
    ans = impl(candies, k)
    assert ans > 0
    assert sum(c // ans for c in candies) >= k
    assert sum(c // (ans + 1) for c in candies) < k


@pytest.mark.parametrize(
    "module",
    [opt_module, freq_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    assert sol.maximumCandies([5, 8, 6], 3) == 5
    assert module.Solution.maximumCandies([5, 8, 6], 3) == 5


@settings(max_examples=250, deadline=None)
@given(
    data=st.tuples(
        st.lists(st.integers(min_value=1, max_value=500), min_size=1, max_size=50),
        st.integers(min_value=1, max_value=2000),
    )
)
def test_hypothesis_agreement_and_monotonicity(data):
    candies, k = data

    results = [impl(candies, k) for impl in IMPLS]
    assert len(set(results)) == 1

    ans = results[0]
    if ans > 0:
        # At ans candies per child, at least k children can be served
        assert sum(c // ans for c in candies) >= k
    else:
        # At 1 candy per child, strictly fewer than k children can be served
        assert sum(c for c in candies) < k

    # At ans + 1 candies per child, strictly fewer than k children can be served
    assert sum(c // (ans + 1) for c in candies) < k
