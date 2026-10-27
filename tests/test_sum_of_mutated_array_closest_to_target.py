from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import sum_of_mutated_array_closest_to_target as standard_module
import sum_of_mutated_array_closest_to_target_bisect as bisect_module
import sum_of_mutated_array_closest_to_target_greedy as greedy_module

MODULES = [
    standard_module,
    bisect_module,
    greedy_module,
]

IMPLS = [m.find_best_value for m in MODULES]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1: [4, 9, 3], target = 10 -> 3
    # value=3 gives sum [3, 3, 3] = 9 (diff 1); value=4 gives sum [4, 4, 3] = 11 (diff 1); tie -> 3
    assert impl([4, 9, 3], 10) == 3

    # Example 2: [2, 3, 5], target = 10 -> 5
    # sum(arr) == 10 == target -> returns max(arr) = 5
    assert impl([2, 3, 5], 10) == 5

    # Example 3: [60864, 25176, 27249, 21296, 20204], target = 56803 -> 11361
    assert impl([60864, 25176, 27249, 21296, 20204], 56803) == 11361


@pytest.mark.parametrize("impl", IMPLS)
def test_zero_value_needed(impl):
    # When target is small, value = 0 must be reachable
    # arr = [2, 20, 11], target = 1:
    # value=0 gives sum 0 (diff 1)
    # value=1 gives sum 3 (diff 2) -> best value is 0
    assert impl([2, 20, 11], 1) == 0

    # Large elements with small target
    assert impl([100, 200, 300], 1) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_tie_breaking_behavior(impl):
    # Tie breaking rule: return the MINIMUM integer in case of a tie
    # arr = [1, 1], target = 1:
    # value=0 -> sum 0, diff 1
    # value=1 -> sum 2, diff 1
    # Tie between 0 and 1 -> returns 0
    assert impl([1, 1], 1) == 0

    # arr = [5, 5, 5, 5], target = 14:
    # value=3 -> sum 12 (diff 2)
    # value=4 -> sum 16 (diff 2)
    # Tie between 3 and 4 -> returns 3
    assert impl([5, 5, 5, 5], 14) == 3


@pytest.mark.parametrize("impl", IMPLS)
def test_sum_less_or_equal_to_target(impl):
    # When sum(arr) <= target, max(arr) is optimal
    assert impl([1, 2, 3], 6) == 3
    assert impl([1, 2, 3], 100) == 3
    assert impl([5, 5], 10) == 5
    assert impl([5, 5], 25) == 5


@pytest.mark.parametrize("impl", IMPLS)
def test_single_element_array(impl):
    # Singleton array
    assert impl([10], 5) == 5
    assert impl([10], 10) == 10
    assert impl([10], 25) == 10
    assert impl([1], 1) == 1


@pytest.mark.parametrize("impl", IMPLS)
def test_all_elements_identical(impl):
    # arr = [7, 7, 7], target = 15 -> value = 5 gives sum 15 (diff 0)
    assert impl([7, 7, 7], 15) == 5

    # arr = [7, 7, 7], target = 20 -> value = 7 gives sum 21 (diff 1) vs 6 gives sum 18 (diff 2)
    assert impl([7, 7, 7], 20) == 7


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    # 10,000 elements within LeetCode constraints
    arr = list(range(1, 10001))
    target = 25000000
    res = impl(arr, target)
    assert res > 0
    assert res <= max(arr)


@pytest.mark.parametrize("module", MODULES)
def test_solution_class_interface(module):
    sol = module.Solution()
    assert sol.findBestValue([4, 9, 3], 10) == 3
    assert module.Solution.findBestValue([4, 9, 3], 10) == 3


def brute_force_oracle(arr: List[int], target: int) -> int:
    """Independent oracle: exhaustive search over [0, max(arr)]."""
    if sum(arr) <= target:
        return max(arr)

    best_v = 0
    min_diff = float("inf")
    for v in range(0, max(arr) + 1):
        s = sum(min(a, v) for a in arr)
        d = abs(s - target)
        if d < min_diff:
            min_diff = d
            best_v = v
    return best_v


@settings(max_examples=250, deadline=None)
@given(
    arr=st.lists(st.integers(min_value=1, max_value=200), min_size=1, max_size=30),
    target=st.integers(min_value=1, max_value=5000),
)
def test_hypothesis_agreement_and_oracle(arr, target):
    # Ensure inputs are not mutated by implementations
    arr_copy = arr.copy()
    expected = brute_force_oracle(arr_copy, target)

    results = [impl(arr.copy(), target) for impl in IMPLS]

    # Verify input was not modified in-place
    assert arr == arr_copy

    # All implementations agree
    assert len(set(results)) == 1

    # Result matches independent oracle
    assert results[0] == expected
