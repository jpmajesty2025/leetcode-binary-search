from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import search_in_sorted_array_of_unknown_size as exp_module
import search_in_sorted_array_of_unknown_size_gallop as gallop_module
import search_in_sorted_array_of_unknown_size_bisect as bisect_module

IMPLS = [
    exp_module.search,
    gallop_module.search,
    bisect_module.search,
]


class MockReader:
    """Mock ArrayReader tracking get() calls and returning 2^31 - 1 out-of-bounds."""

    OUT_OF_BOUNDS = 2147483647

    def __init__(self, arr: List[int]):
        self.arr = arr
        self.calls = 0

    def get(self, index: int) -> int:
        self.calls += 1
        if 0 <= index < len(self.arr):
            return self.arr[index]
        return self.OUT_OF_BOUNDS


@pytest.mark.parametrize("impl", IMPLS)
def test_single_element_array(impl):
    arr = [5]
    # Target present
    r1 = MockReader(arr)
    assert impl(r1, 5) == 0

    # Target smaller
    r2 = MockReader(arr)
    assert impl(r2, 2) == -1

    # Target larger
    r3 = MockReader(arr)
    assert impl(r3, 10) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_two_element_array(impl):
    arr = [-3, 4]
    # First element
    r1 = MockReader(arr)
    assert impl(r1, -3) == 0

    # Second element
    r2 = MockReader(arr)
    assert impl(r2, 4) == 1

    # Miss below, middle, above
    assert impl(MockReader(arr), -10) == -1
    assert impl(MockReader(arr), 0) == -1
    assert impl(MockReader(arr), 10) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_standard_array_with_negative_numbers(impl):
    arr = [-1, 0, 3, 5, 9, 12]
    # Present targets
    for idx, val in enumerate(arr):
        r = MockReader(arr)
        assert impl(r, val) == idx

    # Absent targets
    for val in [-5, 2, 7, 15]:
        r = MockReader(arr)
        assert impl(r, val) == -1


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale_and_query_bound(impl):
    N = 10000
    arr = list(range(0, 2 * N, 2))  # 10,000 even numbers

    # Target at the very end (worst-case index)
    target = arr[-1]
    r = MockReader(arr)
    idx = impl(r, target)
    assert idx == N - 1
    # Bound: 2 * ceil(log2 10000) <= 28 calls
    assert r.calls <= 30


@pytest.mark.parametrize("module", [exp_module, gallop_module, bisect_module])
def test_solution_class_compatibility(module):
    sol = module.Solution()
    r = MockReader([1, 2, 3])
    assert sol.search(r, 2) == 1
    assert module.Solution.search(r, 2) == 1


@settings(max_examples=250, deadline=None)
@given(
    data=st.integers(min_value=1, max_value=300).flatmap(
        lambda n: st.tuples(
            st.just(n),
            st.lists(
                st.integers(min_value=-1000, max_value=1000),
                min_size=n,
                max_size=n,
                unique=True,
            ).map(sorted),
            st.integers(min_value=-1200, max_value=1200),
        )
    )
)
def test_hypothesis_agreement_and_accuracy(data):
    n, arr, target = data
    expected = arr.index(target) if target in arr else -1

    for impl in IMPLS:
        r = MockReader(arr)
        ans = impl(r, target)
        assert ans == expected
