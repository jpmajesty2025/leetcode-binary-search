from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import find_index_of_large_int as orig_module
import find_index_of_large_int_ternary as ternary_module
import find_index_of_large_int_recursive as recursive_module

IMPLS = [
    orig_module.get_index,
    ternary_module.get_index,
    recursive_module.get_index,
]


class MockReader:
    """Mock ArrayReader tracking compareSub call count."""

    def __init__(self, arr: List[int]):
        self.arr = arr
        self.calls = 0

    def length(self) -> int:
        return len(self.arr)

    def compareSub(self, l: int, r: int, x: int, y: int) -> int:
        self.calls += 1
        s1 = sum(self.arr[l : r + 1])
        s2 = sum(self.arr[x : y + 1])
        if s1 > s2:
            return 1
        elif s1 == s2:
            return 0
        return -1


@pytest.mark.parametrize("impl", IMPLS)
def test_length_2_arrays(impl):
    # Length 2
    r1 = MockReader([10, 20])
    assert impl(r1) == 1
    r2 = MockReader([20, 10])
    assert impl(r2) == 0


@pytest.mark.parametrize("impl", IMPLS)
def test_length_3_critical_odd_parity_cases(impl):
    # This specifically broke on the original code due to unequal slice comparisons
    for target in range(3):
        arr = [10, 10, 10]
        arr[target] = 11
        reader = MockReader(arr)
        assert impl(reader) == target


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize("n", [4, 5, 6, 7])
def test_all_positions_in_small_arrays(impl, n):
    for target in range(n):
        arr = [5] * n
        arr[target] = 10
        reader = MockReader(arr)
        assert impl(reader) == target


@pytest.mark.parametrize("impl", IMPLS)
def test_large_constraints_and_query_limits(impl):
    N = 500000
    for target in [0, 1, 42, 250000, N - 2, N - 1]:
        arr = [1] * N
        arr[target] = 2
        reader = MockReader(arr)
        res = impl(reader)
        assert res == target
        # Strict LeetCode problem constraint: <= 20 calls
        assert reader.calls <= 20


def test_ternary_balance_scale_query_count_superiority():
    N = 500000
    target = 123456
    arr = [1] * N
    arr[target] = 2

    # Binary Search
    r_binary = MockReader(list(arr))
    orig_module.get_index(r_binary)

    # Ternary Balance Search
    r_ternary = MockReader(list(arr))
    ternary_module.get_index(r_ternary)

    assert r_binary.calls <= 19
    # Ternary search takes at most 13 calls (32% reduction!)
    assert r_ternary.calls <= 13
    assert r_ternary.calls < r_binary.calls


@pytest.mark.parametrize(
    "module",
    [orig_module, ternary_module, recursive_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    reader = MockReader([10, 10, 20])
    assert sol.getIndex(reader) == 2
    assert module.Solution.getIndex(reader) == 2


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=2, max_value=1000).flatmap(
        lambda n: st.tuples(
            st.just(n),
            st.integers(min_value=0, max_value=n - 1),
            st.integers(min_value=1, max_value=50),
        )
    )
)
def test_hypothesis_matches_target_and_all_agree(data):
    n, target, base_val = data
    arr = [base_val] * n
    arr[target] = base_val + 5

    results = []
    for impl in IMPLS:
        reader = MockReader(arr)
        res = impl(reader)
        results.append(res)
        assert reader.calls <= 20

    # Verify 100% agreement and correctness
    assert len(set(results)) == 1
    assert results[0] == target
