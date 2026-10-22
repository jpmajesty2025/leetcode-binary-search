import math
from typing import Callable
import pytest
from hypothesis import given, settings, strategies as st

import guess_number_higher_or_lower as orig_module
import guess_number_higher_or_lower_ternary as ternary_module
import guess_number_higher_or_lower_bisect as bisect_module

IMPLS = [
    orig_module.guess_number,
    ternary_module.guess_number,
    bisect_module.guess_number,
]


def make_api(pick: int) -> Callable[[int], int]:
    def api(num: int) -> int:
        if num > pick:
            return -1
        elif num < pick:
            return 1
        return 0

    return api


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "n, pick",
    [
        # LeetCode standard examples
        (10, 6),
        (1, 1),
        (2, 1),
        (2, 2),
        # Boundaries
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
def test_known_and_edge_cases(impl, n, pick):
    api = make_api(pick)
    assert impl(n, api) == pick


def test_default_guess_api():
    # Tests the default fallback pick (42)
    assert orig_module.guess_number(100) == 42
    assert ternary_module.guess_number(100) == 42
    assert bisect_module.guess_number(100) == 42


@pytest.mark.parametrize(
    "module",
    [orig_module, ternary_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    # Solution.guessNumber uses the default module-level guess (pick 42)
    assert sol.guessNumber(100) == 42


def test_query_call_count_bound():
    n = 2**31 - 1
    pick = 2**31 - 5

    calls_binary = 0

    def binary_api(x):
        nonlocal calls_binary
        calls_binary += 1
        return 0 if x == pick else (-1 if x > pick else 1)

    calls_ternary = 0

    def ternary_api(x):
        nonlocal calls_ternary
        calls_ternary += 1
        return 0 if x == pick else (-1 if x > pick else 1)

    ans_b = orig_module.guess_number(n, binary_api)
    ans_t = ternary_module.guess_number(n, ternary_api)

    assert ans_b == pick
    assert ans_t == pick

    # Binary search makes at most ceil(log2(n)) + 1 calls (<= 31)
    assert calls_binary <= 32
    # Ternary search makes at most 2 * ceil(log3(n)) calls (<= 40)
    assert calls_ternary <= 40
    # Binary search is more query-efficient in the worst-case
    assert calls_binary <= calls_ternary


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20000).flatmap(
        lambda n: st.tuples(
            st.just(n),
            st.integers(min_value=1, max_value=n),
        )
    )
)
def test_hypothesis_matches_pick_and_all_agree(data):
    n, pick = data
    api = make_api(pick)

    results = [impl(n, api) for impl in IMPLS]

    # Verify 100% agreement and correctness
    assert len(set(results)) == 1
    assert results[0] == pick
