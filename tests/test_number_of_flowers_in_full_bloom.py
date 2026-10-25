from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import number_of_flowers_in_full_bloom as bisect_module
import number_of_flowers_in_full_bloom_heap as heap_module
import number_of_flowers_in_full_bloom_sweep as sweep_module

IMPLS = [
    bisect_module.full_bloom_flowers,
    heap_module.full_bloom_flowers,
    sweep_module.full_bloom_flowers,
]


@pytest.mark.parametrize("impl", IMPLS)
def test_leetcode_examples(impl):
    # Example 1
    f1 = [[1, 6], [3, 7], [9, 12], [4, 13]]
    p1 = [2, 3, 7, 11]
    assert impl(f1, p1) == [1, 2, 2, 2]

    # Example 2
    f2 = [[1, 10], [3, 3]]
    p2 = [3, 3, 2]
    assert impl(f2, p2) == [2, 2, 1]


@pytest.mark.parametrize("impl", IMPLS)
def test_single_day_bloom(impl):
    # Flower blooms only on day 5
    flowers = [[5, 5]]
    people = [4, 5, 6]
    assert impl(flowers, people) == [0, 1, 0]


@pytest.mark.parametrize("impl", IMPLS)
def test_boundaries_and_misses(impl):
    flowers = [[10, 20], [15, 25]]
    # Before all, exactly at start, within overlap, exactly at end, after all
    people = [5, 10, 18, 25, 30]
    assert impl(flowers, people) == [0, 1, 2, 1, 0]


@pytest.mark.parametrize("impl", IMPLS)
def test_duplicate_intervals_and_arrivals(impl):
    flowers = [[1, 5], [1, 5], [1, 5]]
    people = [1, 1, 5, 5, 6]
    assert impl(flowers, people) == [3, 3, 3, 3, 0]


@pytest.mark.parametrize("impl", IMPLS)
def test_large_scale(impl):
    N = 5000
    M = 5000
    flowers = [[i, i + 100] for i in range(1, N + 1)]
    people = [50, 100, 500, 2000, 99999]

    res = impl(flowers, people)
    # At time 50: flowers 1..50 started (50), none finished -> 50
    assert res[0] == 50
    # At time 100: flowers 1..100 started (100), none finished -> 100
    assert res[1] == 100
    # At time 500: flowers 1..500 started (500), flowers 1..399 finished (399) -> 101
    assert res[2] == 101
    # At time 99999: all finished -> 0
    assert res[4] == 0


@pytest.mark.parametrize(
    "module",
    [bisect_module, heap_module, sweep_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    flowers = [[1, 6], [3, 7], [9, 12], [4, 13]]
    people = [2, 3, 7, 11]
    assert sol.fullBloomFlowers(flowers, people) == [1, 2, 2, 2]
    assert module.Solution.fullBloomFlowers(flowers, people) == [1, 2, 2, 2]


@settings(max_examples=250, deadline=None)
@given(
    data=st.tuples(
        st.lists(
            st.tuples(
                st.integers(min_value=1, max_value=500),
                st.integers(min_value=1, max_value=500),
            ).map(lambda pair: [min(pair), max(pair)]),
            min_size=1,
            max_size=50,
        ),
        st.lists(
            st.integers(min_value=1, max_value=600),
            min_size=1,
            max_size=30,
        ),
    )
)
def test_hypothesis_agreement_with_brute_force(data):
    flowers, people = data

    # Ground truth via brute force
    expected = [
        sum(1 for s, e in flowers if s <= arrival <= e)
        for arrival in people
    ]

    for impl in IMPLS:
        ans = impl(flowers, people)
        assert ans == expected
