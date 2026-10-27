from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import max_tastiness_of_candy_basket as standard_module
import max_tastiness_of_candy_basket_hop as hop_module
import max_tastiness_of_candy_basket_adaptive as adaptive_module
import max_tastiness_of_candy_basket_bisect as bisect_module

IMPLS = [
    standard_module.maximum_tastiness,
    hop_module.maximum_tastiness,
    adaptive_module.maximum_tastiness,
    bisect_module.maximum_tastiness,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1
    assert impl([13, 5, 1, 8, 21, 2], 3) == 8
    # Example 2
    assert impl([1, 3, 1], 2) == 2
    # Example 3 (all identical prices -> tastiness 0)
    assert impl([7, 7, 7, 7], 2) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_two(impl):
    # For k=2, the optimal choice is always (min, max)
    assert impl([1, 100], 2) == 99
    assert impl([5, 15, 30], 2) == 25


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_length(impl):
    # Every candy must be picked; tastiness is min adjacent difference
    prices = [1, 4, 8, 13]
    # differences: 3, 4, 5 -> min is 3
    assert impl(prices, 4) == 3


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    N = 10000
    prices = list(range(0, 2 * N, 2))
    k = 50
    ans = impl(prices, k)
    assert ans > 0
    # Bound verification: ans <= (prices[-1] - prices[0]) // (k - 1)
    assert ans <= (prices[-1] - prices[0]) // (k - 1)


@pytest.mark.parametrize(
    "module",
    [standard_module, hop_module, adaptive_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    assert sol.maximumTastiness([13, 5, 1, 8, 21, 2], 3) == 8
    assert module.Solution.maximumTastiness([13, 5, 1, 8, 21, 2], 3) == 8


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=2, max_value=50).flatmap(
        lambda n: st.tuples(
            st.lists(
                st.integers(min_value=1, max_value=1000),
                min_size=n,
                max_size=n,
            ),
            st.integers(min_value=2, max_value=n),
        )
    )
)
def test_hypothesis_agreement_and_monotonicity(data):
    prices, k = data

    results = [impl(prices.copy(), k) for impl in IMPLS]
    assert len(set(results)) == 1

    ans = results[0]
    sorted_p = sorted(prices)

    def can_pick(t):
        if t == 0:
            return True
        count = 1
        last = sorted_p[0]
        for p in sorted_p[1:]:
            if p - last >= t:
                count += 1
                last = p
                if count >= k:
                    return True
        return False

    # Invariant: at tastiness ans, k candies can be chosen
    assert can_pick(ans) is True
    # Invariant: at tastiness ans + 1, k candies cannot be chosen
    assert can_pick(ans + 1) is False
