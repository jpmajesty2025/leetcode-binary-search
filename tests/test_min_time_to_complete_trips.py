from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import min_time_to_complete_trips as opt_module
import min_time_to_complete_trips_freq as freq_module
import min_time_to_complete_trips_harmonic as harmonic_module

IMPLS = [
    opt_module.minimum_time,
    freq_module.minimum_time,
    harmonic_module.minimum_time,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1
    assert impl([1, 2, 3], 5) == 3
    # Example 2
    assert impl([2], 1) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_single_bus_multiple_trips(impl):
    assert impl([5], 10) == 50
    assert impl([7], 1) == 7


@pytest.mark.parametrize("impl", IMPLS)
def test_duplicate_bus_times(impl):
    # 3 identical buses, 9 trips needed -> each completes 3 trips at time 9
    assert impl([3, 3, 3], 9) == 9
    assert impl([4, 4], 5) == 12


@pytest.mark.parametrize("impl", IMPLS)
def test_skewed_durations(impl):
    # One fast bus and one extremely slow bus
    assert impl([1, 10000], 5) == 5
    assert impl([2, 1000000], 3) == 6


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    # 10,000 buses, 1,000,000 trips
    time_arr = [i % 100 + 1 for i in range(10000)]
    total_trips = 1000000
    res = impl(time_arr, total_trips)
    assert res > 0
    # Verify that at time res, trips >= total_trips
    assert sum(res // t for t in time_arr) >= total_trips
    # Verify that at time res - 1, trips < total_trips
    assert sum((res - 1) // t for t in time_arr) < total_trips


@pytest.mark.parametrize(
    "module",
    [opt_module, freq_module, harmonic_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    assert sol.minimumTime([1, 2, 3], 5) == 3
    assert module.Solution.minimumTime([1, 2, 3], 5) == 3


@settings(max_examples=250, deadline=None)
@given(
    data=st.tuples(
        st.lists(st.integers(min_value=1, max_value=200), min_size=1, max_size=50),
        st.integers(min_value=1, max_value=1000),
    )
)
def test_hypothesis_agreement_and_monotonicity(data):
    time_arr, total_trips = data

    results = [impl(time_arr, total_trips) for impl in IMPLS]
    assert len(set(results)) == 1

    ans = results[0]
    # Invariant: at time ans, total trips completed >= total_trips
    assert sum(ans // t for t in time_arr) >= total_trips
    # Invariant: at time ans - 1, total trips completed < total_trips
    if ans > 1:
        assert sum((ans - 1) // t for t in time_arr) < total_trips
