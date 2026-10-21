import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import min_speed_to_arrive_on_time as orig_module
import min_speed_to_arrive_on_time_bisect as bisect_module
import min_speed_to_arrive_on_time_scaled as scaled_module

IMPLS = [
    orig_module.min_speed_on_time,
    bisect_module.min_speed_on_time,
    scaled_module.min_speed_on_time,
]


def calculate_time(dist: List[int], speed: int) -> float:
    return sum((d + speed - 1) // speed for d in dist[:-1]) + dist[-1] / speed


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "dist, hour, expected",
    [
        # LeetCode standard examples
        ([1, 3, 2], 6, 1),
        ([1, 3, 2], 2.7, 3),
        ([1, 3, 2], 1.9, -1),
        # Hour strictly between n - 1 and n
        ([1, 1, 1], 2.01, 100),
        ([1, 1], 1.01, 100),
        # Hour <= n - 1 (mathematically impossible)
        ([1, 3, 2], 2.0, -1),
        ([1, 1], 1.0, -1),
        ([1, 2, 3, 4], 3.0, -1),
        ([1, 2, 3, 4], 2.5, -1),
        # Exact integer match hour == n
        ([1, 3, 2], 3, 3),
        ([1, 1, 1], 3, 1),
        # Single train (no waiting at all)
        ([5], 1.0, 5),
        ([5], 2.5, 2),
        ([5], 5.0, 1),
        ([5], 0.5, 10),
        # Empty dist
        ([], 5.0, -1),
        # Maximum speed limit boundary (10^7)
        ([1, 1, 100000], 2.01, 10000000),
        ([1, 1, 100001], 2.01, -1),
    ],
)
def test_known_and_edge_cases(impl, dist, hour, expected):
    assert impl(list(dist), hour) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_dist(impl):
    dist = [1, 3, 2]
    dist_copy = copy.deepcopy(dist)
    impl(dist, 2.7)
    assert dist == dist_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, scaled_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    dist = [1, 3, 2]
    assert sol.minSpeedOnTime(dist, 6) == 1
    assert sol.minSpeedOnTime(dist, 2.7) == 3
    assert module.Solution.minSpeedOnTime(dist, 1.9) == -1


@settings(max_examples=250, deadline=None)
@given(
    dist=st.lists(st.integers(min_value=1, max_value=300), min_size=1, max_size=20),
    hour_int=st.integers(min_value=1, max_value=2500),
)
def test_hypothesis_matches_scaled_and_all_agree(dist, hour_int):
    hour = hour_int / 100.0  # Float with 2 decimal places

    results = [impl(list(dist), hour) for impl in IMPLS]

    # Verify 100% agreement
    assert len(set(results)) == 1

    ans = results[0]
    n = len(dist)

    if ans != -1:
        # Feasibility check: speed ans gets there on time
        assert calculate_time(dist, ans) <= hour + 1e-9
        # Minimality check: speed ans - 1 (if > 0) does not get there on time
        if ans > 1:
            assert calculate_time(dist, ans - 1) > hour - 1e-9
    else:
        # If -1, either hour <= n - 1 or max speed 10^7 cannot make it
        assert hour <= n - 1 or calculate_time(dist, 10**7) > hour
