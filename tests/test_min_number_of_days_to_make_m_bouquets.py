from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import min_number_of_days_to_make_m_bouquets as standard_module
import min_number_of_days_to_make_m_bouquets_unique as unique_module
import min_number_of_days_to_make_m_bouquets_sweep as sweep_module

MODULES = [
    standard_module,
    unique_module,
    sweep_module,
]

IMPLS = [m.min_days for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1: bloomDay = [1, 10, 3, 10, 2], m = 3, k = 1 -> 3
    # After day 3, flowers bloomed: [x, _, x, _, x] -> 3 bouquets of 1
    assert impl([1, 10, 3, 10, 2], 3, 1) == 3

    # Example 2: bloomDay = [1, 10, 3, 10, 2], m = 3, k = 2 -> -1
    # Need 3 * 2 = 6 flowers, but only 5 exist
    assert impl([1, 10, 3, 10, 2], 3, 2) == -1

    # Example 3: bloomDay = [7, 7, 7, 7, 12, 7, 7], m = 2, k = 3 -> 12
    # At day 7: [x, x, x, x, _, x, x] -> only 1 bouquet of 3 can be made
    # At day 12: all bloomed -> 2 bouquets of 3 can be made
    assert impl([7, 7, 7, 7, 12, 7, 7], 2, 3) == 12


@pytest.mark.parametrize("impl", IMPLS)
def test_impossible_not_enough_flowers(impl):
    # len(bloomDay) < m * k
    assert impl([1, 2], 2, 2) == -1
    assert impl([10], 1, 2) == -1
    assert impl([5, 5, 5], 2, 2) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_exact_capacity(impl):
    # len(bloomDay) == m * k: every flower must bloom
    assert impl([1, 10, 2, 9], 2, 2) == 10
    assert impl([100], 1, 1) == 100
    assert impl([5, 4, 3, 2, 1], 5, 1) == 5


@pytest.mark.parametrize("impl", IMPLS)
def test_k_equals_one(impl):
    # k = 1: adjacency is trivial, need m-th smallest bloom day
    assert impl([5, 2, 8, 1, 9], 3, 1) == 5
    assert impl([10, 20, 30], 1, 1) == 10
    assert impl([10, 20, 30], 3, 1) == 30


@pytest.mark.parametrize("impl", IMPLS)
def test_m_equals_one(impl):
    # m = 1: need at least 1 adjacent window of length k
    # Windows of length 2: [10, 1] max 10; [1, 2] max 2; [2, 10] max 10; [10, 3] max 10; [3, 4] max 4
    # Minimum of window maximums is 2
    assert impl([10, 1, 2, 10, 3, 4], 1, 2) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_bloom_days(impl):
    assert impl([7, 7, 7, 7, 7], 2, 2) == 7
    assert impl([42, 42], 1, 2) == 42


@pytest.mark.parametrize("impl", IMPLS)
def test_large_bloom_day_values(impl):
    # Checking values up to 10^9
    assert impl([10**9, 10**9, 1], 1, 2) == 10**9


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    N = 10000
    bloomDay = list(range(1, N + 1))
    m = 2000
    k = 3
    # Needs m * k = 6000 contiguous flowers
    ans = impl(bloomDay, m, k)
    assert ans == 6000


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_interface(module):
    sol = module.Solution()
    assert sol.minDays([1, 10, 3, 10, 2], 3, 1) == 3
    assert module.Solution.minDays([1, 10, 3, 10, 2], 3, 1) == 3


def oracle_can_make(bloomDay: List[int], m: int, k: int, day: int) -> bool:
    bouquets = 0
    flowers = 0
    for b in bloomDay:
        if b <= day:
            flowers += 1
            if flowers == k:
                bouquets += 1
                flowers = 0
        else:
            flowers = 0
    return bouquets >= m


@settings(max_examples=150, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=25).flatmap(
        lambda n: st.tuples(
            st.lists(
                st.integers(min_value=1, max_value=200),
                min_size=n,
                max_size=n,
            ),
            st.integers(min_value=1, max_value=n),
            st.integers(min_value=1, max_value=n),
        )
    )
)
def test_hypothesis_agreement_and_oracle(data):
    bloomDay, m, k = data
    bloomDay_copy = bloomDay.copy()

    results = [impl(bloomDay.copy(), m, k) for impl in IMPLS]

    # Verify input was not modified in-place
    assert bloomDay == bloomDay_copy

    # All implementations agree
    assert len(set(results)) == 1
    ans = results[0]

    if len(bloomDay) < m * k:
        assert ans == -1
    else:
        assert ans != -1
        # Feasible on day ans
        assert oracle_can_make(bloomDay, m, k, ans) is True
        # Infeasible on day ans - 1
        assert oracle_can_make(bloomDay, m, k, ans - 1) is False
