import copy
import math
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import koko_eating_bananas as orig_module
import koko_eating_bananas_bisect as bisect_module
import koko_eating_bananas_integer_math as int_math_module

IMPLS = [
    orig_module.min_eating_speed,
    bisect_module.min_eating_speed,
    int_math_module.min_eating_speed,
]


def brute_force_oracle(piles: List[int], h: int) -> int:
    """Independent oracle: linear probe starting from theoretical minimum speed."""
    if not piles:
        return 0
    k = max(1, (sum(piles) + h - 1) // h)
    while True:
        hours = sum(math.ceil(p / k) for p in piles)
        if hours <= h:
            return k
        k += 1


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "piles, h, expected",
    [
        # LeetCode standard examples
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        # Empty case
        ([], 5, 0),
        # Exact length: h == len(piles)
        ([10, 20, 30], 3, 30),
        # Large h: Koko can eat at speed 1
        ([3, 6, 7, 11], 1000, 1),
        ([3, 6, 7, 11], 27, 1),
        # Single pile
        ([10], 1, 10),
        ([10], 2, 5),
        ([10], 3, 4),
        ([10], 100, 1),
        # Equal piles
        ([5, 5, 5, 5], 4, 5),
        ([5, 5, 5, 5], 8, 3),
        ([5, 5, 5, 5], 20, 1),
        # Large values up to 10^9
        ([10**9], 2, 500_000_000),
        ([10**9, 10**9], 3, 1_000_000_000),
    ],
)
def test_known_and_edge_cases(impl, piles, h, expected):
    assert impl(list(piles), h) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_piles(impl):
    piles = [3, 6, 7, 11]
    piles_copy = copy.deepcopy(piles)
    impl(piles, 8)
    assert piles == piles_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, int_math_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    piles = [3, 6, 7, 11]
    assert sol.minEatingSpeed(piles, 8) == 4
    assert module.Solution.minEatingSpeed(piles, 8) == 4


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=n, max_value=n * 30),
        )
    )
)
def test_hypothesis_matches_oracle_and_all_agree(data):
    piles, h = data
    expected = brute_force_oracle(piles, h)

    results = [impl(list(piles), h) for impl in IMPLS]

    for res in results:
        assert res == expected

    # 100% agreement
    assert len(set(results)) == 1


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=n, max_value=n * 30),
        )
    )
)
def test_solution_optimality_invariants(data):
    piles, h = data
    k = int_math_module.min_eating_speed(piles, h)

    # Invariant 1: Speed k can finish within h hours
    assert sum(math.ceil(p / k) for p in piles) <= h

    # Invariant 2: Speed k - 1 (if k > 1) CANNOT finish within h hours
    if k > 1:
        assert sum(math.ceil(p / (k - 1)) for p in piles) > h

    # Invariant 3: k respects theoretical bounds
    assert k >= max(1, (sum(piles) + h - 1) // h)
    assert k <= max(piles)
