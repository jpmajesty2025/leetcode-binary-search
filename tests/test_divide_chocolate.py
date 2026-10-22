import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import divide_chocolate as orig_module
import divide_chocolate_prefix_jump as prefix_jump_module
import divide_chocolate_bisect as bisect_module

IMPLS = [
    orig_module.maximize_sweetness,
    prefix_jump_module.maximize_sweetness,
    bisect_module.maximize_sweetness,
]


def can_partition(sweetness: List[int], target: int, needed_pieces: int) -> bool:
    curr = 0
    pieces = 0
    for s in sweetness:
        curr += s
        if curr >= target:
            pieces += 1
            if pieces == needed_pieces:
                return True
            curr = 0
    return False


def brute_force_oracle(sweetness: List[int], k: int) -> int:
    """Independent oracle: linear probe downwards from theoretical maximum."""
    if not sweetness:
        return 0
    target = sum(sweetness) // (k + 1)
    needed = k + 1
    while target >= min(sweetness):
        if can_partition(sweetness, target, needed):
            return target
        target -= 1
    return min(sweetness)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "sweetness, k, expected",
    [
        # LeetCode standard examples
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 5, 6),
        ([5, 6, 7, 8, 9, 1, 2, 3, 4], 8, 1),
        ([1, 2, 2, 1, 2, 2, 1, 2, 2], 2, 5),
        # Empty case
        ([], 0, 0),
        # k == 0 (keep entire chocolate bar)
        ([1, 2, 3], 0, 6),
        ([10], 0, 10),
        # k + 1 == len(sweetness) (each chunk is a piece)
        ([10, 5, 20], 2, 5),
        ([4, 4, 4], 2, 4),
        # Identical chunks
        ([5, 5, 5, 5], 1, 10),
        ([5, 5, 5, 5], 3, 5),
        # Large values up to 10^5
        ([100000] * 10, 4, 200000),
        ([100000] * 10, 9, 100000),
    ],
)
def test_known_and_edge_cases(impl, sweetness, k, expected):
    assert impl(list(sweetness), k) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_sweetness(impl):
    sweetness = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sweetness_copy = copy.deepcopy(sweetness)
    impl(sweetness, 5)
    assert sweetness == sweetness_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, prefix_jump_module, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    sweetness = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sol.maximizeSweetness(sweetness, 5) == 6
    assert module.Solution.maximizeSweetness(sweetness, 5) == 6


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=0, max_value=n - 1),
        )
    )
)
def test_hypothesis_matches_oracle_and_all_agree(data):
    sweetness, k = data
    expected = brute_force_oracle(sweetness, k)

    results = [impl(list(sweetness), k) for impl in IMPLS]

    # Verify 100% agreement
    assert len(set(results)) == 1
    assert results[0] == expected


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=20).flatmap(
        lambda n: st.tuples(
            st.lists(st.integers(min_value=1, max_value=500), min_size=n, max_size=n),
            st.integers(min_value=0, max_value=n - 1),
        )
    )
)
def test_optimality_invariants(data):
    sweetness, k = data
    w = prefix_jump_module.maximize_sweetness(sweetness, k)

    # Invariant 1: Can achieve at least k + 1 pieces with sweetness >= w
    assert can_partition(sweetness, w, k + 1)

    # Invariant 2: Cannot achieve k + 1 pieces with sweetness >= w + 1
    assert not can_partition(sweetness, w + 1, k + 1)

    # Invariant 3: Respects theoretical bounds
    assert w >= min(sweetness)
    assert w <= sum(sweetness) // (k + 1)
