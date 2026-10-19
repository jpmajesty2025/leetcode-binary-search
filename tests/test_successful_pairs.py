import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import successful_pairs_of_spells_and_potions as bs_module
import successful_pairs_of_spells_and_potions_bisect as bisect_module
import successful_pairs_of_spells_and_potions_counting as counting_module
import successful_pairs_of_spells_and_potions_two_pointer as two_pointer_module

IMPLS = [
    bs_module.successful_pairs,
    bisect_module.successful_pairs,
    counting_module.successful_pairs,
    two_pointer_module.successful_pairs,
]


def brute_force_oracle(spells: List[int], potions: List[int], success: int) -> List[int]:
    """Independent ground truth counting successful pairs by exhaustive check."""
    return [sum(1 for p in potions if s * p >= success) for s in spells]


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "spells, potions, success, expected",
    [
        # LeetCode standard examples
        ([5, 1, 3], [1, 2, 3, 4, 5], 7, [4, 0, 3]),
        ([3, 1, 2], [8, 5, 8], 16, [2, 0, 2]),
        # Empty cases
        ([], [1, 2, 3], 5, []),
        ([1, 2, 3], [], 5, [0, 0, 0]),
        ([], [], 10, []),
        # Singletons
        ([10], [10], 100, [1]),
        ([10], [9], 100, [0]),
        ([5], [20], 100, [1]),
        # All successful vs none successful
        ([10, 20, 30], [5, 6, 7], 50, [3, 3, 3]),
        ([1, 2, 3], [1, 2, 3], 100, [0, 0, 0]),
        # Duplicates in potions
        ([2], [3, 3, 3, 3], 6, [4]),
        ([2], [1, 2, 2, 3, 3], 6, [2]),
        # Duplicates in spells
        ([3, 3, 3], [1, 2, 3], 6, [2, 2, 2]),
        # Unsorted inputs with exact boundary matches
        ([9, 1, 4], [5, 1, 8, 2, 4], 16, [4, 0, 3]),
        # Large products up to 10^10
        ([100000], [100000], 10000000000, [1]),
        ([100000], [99999], 10000000000, [0]),
    ],
)
def test_known_and_edge_cases(impl, spells, potions, success, expected):
    assert impl(list(spells), list(potions), success) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_inputs(impl):
    spells = [5, 1, 3]
    potions = [5, 2, 4, 1, 3]
    spells_copy = copy.deepcopy(spells)
    potions_copy = copy.deepcopy(potions)

    impl(spells, potions, 7)

    assert spells == spells_copy
    assert potions == potions_copy


@pytest.mark.parametrize(
    "module",
    [bs_module, bisect_module, counting_module, two_pointer_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    spells = [5, 1, 3]
    potions = [1, 2, 3, 4, 5]
    assert sol.successfulPairs(spells, potions, 7) == [4, 0, 3]
    assert module.Solution.successfulPairs(spells, potions, 7) == [4, 0, 3]


@settings(max_examples=250, deadline=None)
@given(
    spells=st.lists(st.integers(min_value=1, max_value=2000), min_size=0, max_size=25),
    potions=st.lists(st.integers(min_value=1, max_value=2000), min_size=0, max_size=25),
    success=st.integers(min_value=1, max_value=1000000),
)
def test_hypothesis_matches_oracle_and_all_agree(spells, potions, success):
    expected = brute_force_oracle(spells, potions, success)

    results = [impl(list(spells), list(potions), success) for impl in IMPLS]

    for res in results:
        assert res == expected

    # Verify 100% agreement across all implementations
    assert len(set(tuple(r) for r in results)) == 1


@settings(max_examples=200, deadline=None)
@given(
    spells=st.lists(st.integers(min_value=1, max_value=2000), min_size=2, max_size=20),
    potions=st.lists(st.integers(min_value=1, max_value=2000), min_size=1, max_size=20),
    success=st.integers(min_value=1, max_value=1000000),
)
def test_monotonicity_and_bounds_properties(spells, potions, success):
    res = bisect_module.successful_pairs(spells, potions, success)
    m = len(potions)

    # Property 1: Each answer is bounded by [0, m]
    for count in res:
        assert 0 <= count <= m

    # Property 2: A stronger spell always produces at least as many pairs
    paired = sorted(zip(spells, res), key=lambda x: x[0])
    for k in range(len(paired) - 1):
        s1, c1 = paired[k]
        s2, c2 = paired[k + 1]
        if s1 <= s2:
            assert c1 <= c2
