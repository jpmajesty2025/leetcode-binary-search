import math
from typing import Callable
import pytest
from hypothesis import given, settings, strategies as st

import first_bad_version as orig_module
import first_bad_version_bisect as bisect_module
import first_bad_version_exponential as exp_module

IMPLS = [
    orig_module.first_bad_version,
    bisect_module.first_bad_version,
    exp_module.first_bad_version,
]


def make_api(bad: int) -> Callable[[int], bool]:
    return lambda version: version >= bad


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, bad",
    [
        # LeetCode standard examples
        (5, 4),
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 2),
        # Boundaries
        (10, 1),
        (10, 10),
        (100, 1),
        (100, 100),
        (100, 50),
        # Large values up to 2^31 - 1
        (2**31 - 1, 1),
        (2**31 - 1, 2**31 - 1),
        (2**31 - 1, 17011993),
        (2**31 - 1, (2**31 - 1) // 2),
    ],
)
def test_known_and_edge_cases(impl, n, bad):
    api = make_api(bad)
    assert impl(n, api) == bad


def test_default_mock_api():
    # Tests the default fallback bad version (4)
    assert orig_module.first_bad_version(10) == 4
    assert bisect_module.first_bad_version(10) == 4
    assert exp_module.first_bad_version(10) == 4


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, exp_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    # Solution.firstBadVersion uses the default module-level mock (bad = 4)
    assert sol.firstBadVersion(10) == 4


def test_query_call_count_bound():
    n = 2**31 - 1

    # 1. Worst-case binary search calls
    calls_binary = 0

    def binary_api(x):
        nonlocal calls_binary
        calls_binary += 1
        return x >= n - 1

    ans_b = orig_module.first_bad_version(n, binary_api)
    assert ans_b == n - 1
    assert calls_binary <= 31

    # 2. Exponential search makes 3.4x fewer calls when regression is recent
    calls_exp = 0

    def exp_api(x):
        nonlocal calls_exp
        calls_exp += 1
        return x >= 10

    ans_exp = exp_module.first_bad_version(n, exp_api)
    assert ans_exp == 10
    assert calls_exp <= 10  # Exponential search finishes in 9 calls vs 31


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20000).flatmap(
        lambda n: st.tuples(
            st.just(n),
            st.integers(min_value=1, max_value=n),
        )
    )
)
def test_hypothesis_matches_bad_version_and_all_agree(data):
    n, bad = data
    api = make_api(bad)

    results = [impl(n, api) for impl in IMPLS]

    # Verify 100% agreement and correctness
    assert len(set(results)) == 1
    assert results[0] == bad
