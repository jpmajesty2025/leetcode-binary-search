from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import max_running_time_of_n_computers as standard_module
import max_running_time_of_n_computers_bisect as bisect_module
import max_running_time_of_n_computers_greedy as greedy_module

MODULES = [
    standard_module,
    bisect_module,
    greedy_module,
]

IMPLS = [m.max_run_time for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1: n = 2, batteries = [3, 3, 3] -> 4
    # Computer 1 runs on battery 0 for 3 min, then battery 2 for 1 min.
    # Computer 2 runs on battery 1 for 3 min, then battery 2 for 1 min.
    # Total simultaneous time = 4 min.
    assert impl(2, [3, 3, 3]) == 4

    # Example 2: n = 2, batteries = [1, 1, 1, 1] -> 2
    assert impl(2, [1, 1, 1, 1]) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_n_equals_batteries_length(impl):
    # When n == len(batteries), each computer must receive exactly 1 battery.
    # The bottleneck is the smallest battery in the set.
    assert impl(3, [10, 5, 8]) == 5
    assert impl(1, [42]) == 42
    assert impl(4, [2, 2, 2, 2]) == 2


@pytest.mark.parametrize("impl", IMPLS)
def test_single_computer(impl):
    # When n == 1, all batteries can be used sequentially with 0 waste.
    # The runtime is simply the total sum of all batteries.
    assert impl(1, [4, 7, 2]) == 13
    assert impl(1, [100, 200, 300]) == 600


@pytest.mark.parametrize("impl", IMPLS)
def test_dominant_large_battery(impl):
    # A single battery is massive compared to the others.
    # One computer can be powered exclusively by the massive battery.
    # The other computer must be powered by the remaining small batteries.
    # n = 2, batteries = [100, 1, 1, 1]:
    # Total for computer 2 is 1 + 1 + 1 = 3 min.
    assert impl(2, [100, 1, 1, 1]) == 3

    # n = 3, batteries = [1000, 1000, 5, 5]:
    # Two computers get dedicated 1000-min batteries.
    # Third computer gets 5 + 5 = 10 min.
    assert impl(3, [1000, 1000, 5, 5]) == 10


@pytest.mark.parametrize("impl", IMPLS)
def test_all_identical_batteries(impl):
    # 6 batteries of 5 min each for 3 computers -> (6 * 5) // 3 = 10
    assert impl(3, [5, 5, 5, 5, 5, 5]) == 10
    # 4 batteries of 7 min each for 2 computers -> (4 * 7) // 2 = 14
    assert impl(2, [7, 7, 7, 7]) == 14


@pytest.mark.parametrize("impl", IMPLS)
def test_large_values(impl):
    # Checking 64-bit integer values up to 10^9
    assert impl(2, [10**9, 10**9, 10**9]) == 1500000000


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    # 10,000 batteries for 5,000 computers
    batteries = [100] * 10000
    assert impl(5000, batteries) == 200


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_interface(module):
    sol = module.Solution()
    assert sol.maxRunTime(2, [3, 3, 3]) == 4
    assert module.Solution.maxRunTime(2, [3, 3, 3]) == 4


def can_run_for_time(n: int, batteries: List[int], target_time: int) -> bool:
    """Independent oracle based on McNaughton's theorem condition."""
    if target_time == 0:
        return True
    return sum(min(b, target_time) for b in batteries) >= n * target_time


@settings(max_examples=150, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda m: st.tuples(
            st.integers(min_value=1, max_value=m),
            st.lists(
                st.integers(min_value=1, max_value=500),
                min_size=m,
                max_size=m,
            ),
        )
    )
)
def test_hypothesis_agreement_and_monotonicity(data):
    n, batteries = data
    batteries_copy = batteries.copy()

    results = [impl(n, batteries.copy()) for impl in IMPLS]

    # Verify input was not modified in-place
    assert batteries == batteries_copy

    # All 3 implementations must agree
    assert len(set(results)) == 1

    ans = results[0]

    # Invariant 1: Time ans must be feasible
    assert can_run_for_time(n, batteries, ans) is True

    # Invariant 2: Time ans + 1 must be infeasible (maximality)
    assert can_run_for_time(n, batteries, ans + 1) is False
