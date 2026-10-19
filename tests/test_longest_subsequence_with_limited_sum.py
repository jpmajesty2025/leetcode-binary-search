import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import longest_subsequence_with_limited_sum as orig_module
import longest_subsequence_with_limited_sum_bisect as bisect_module
import longest_subsequence_with_limited_sum_two_pointer as two_pointer_module

IMPLS = [
    orig_module.answer_queries,
    bisect_module.answer_queries,
    two_pointer_module.answer_queries,
]


def brute_force_oracle(nums: List[int], queries: List[int]) -> List[int]:
    """Independent ground-truth oracle: greedily takes smallest elements until budget exceeded."""
    if not nums:
        return [0] * len(queries)
    sorted_nums = sorted(nums)
    result = []
    for q in queries:
        current_sum = 0
        count = 0
        for x in sorted_nums:
            if current_sum + x <= q:
                current_sum += x
                count += 1
            else:
                break
        result.append(count)
    return result


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "nums, queries, expected",
    [
        # LeetCode standard examples
        ([4, 5, 2, 1], [3, 10, 21], [2, 3, 4]),
        ([2, 3, 4, 5], [1], [0]),
        # Empty cases
        ([], [5, 10], [0, 0]),
        ([1, 2, 3], [], []),
        ([], [], []),
        # Singletons
        ([5], [4], [0]),
        ([5], [5], [1]),
        ([5], [6], [1]),
        # All fit vs none fit
        ([1, 2, 3], [100], [3]),
        ([10, 20, 30], [5], [0]),
        # Duplicate values
        ([2, 2, 2, 2], [1, 2, 4, 6, 8, 10], [0, 1, 2, 3, 4, 4]),
        # Exact prefix sum boundaries: prefix sums are [1, 3, 6]
        ([1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 1, 2, 2, 2, 3, 3]),
        # Large scale numbers
        ([1000] * 5, [999, 1000, 2500, 5000, 10000], [0, 1, 2, 5, 5]),
    ],
)
def test_known_and_edge_cases(impl, nums, queries, expected):
    assert impl(list(nums), list(queries)) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_inputs(impl):
    nums = [4, 5, 2, 1]
    queries = [3, 10, 21]
    nums_copy = copy.deepcopy(nums)
    queries_copy = copy.deepcopy(queries)

    impl(nums, queries)

    assert nums == nums_copy
    assert queries == queries_copy


@pytest.mark.parametrize(
    "module",
    [orig_module, bisect_module, two_pointer_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    nums = [4, 5, 2, 1]
    queries = [3, 10, 21]
    assert sol.answerQueries(nums, queries) == [2, 3, 4]
    assert module.Solution.answerQueries(nums, queries) == [2, 3, 4]


@settings(max_examples=300, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=1, max_value=500), min_size=0, max_size=30),
    queries=st.lists(st.integers(min_value=0, max_value=15000), min_size=0, max_size=30),
)
def test_hypothesis_matches_oracle_and_all_agree(nums, queries):
    expected = brute_force_oracle(nums, queries)

    results = [impl(list(nums), list(queries)) for impl in IMPLS]

    for res in results:
        assert res == expected

    # 100% agreement across all implementations
    assert len(set(tuple(r) for r in results)) == 1


@settings(max_examples=250, deadline=None)
@given(
    nums=st.lists(st.integers(min_value=1, max_value=500), min_size=1, max_size=30),
    queries=st.lists(st.integers(min_value=0, max_value=15000), min_size=2, max_size=30),
)
def test_monotonicity_and_bounds_properties(nums, queries):
    res = bisect_module.answer_queries(nums, queries)
    n = len(nums)

    # Invariant 1: Result size is bounded by [0, n]
    for count in res:
        assert 0 <= count <= n

    # Invariant 2: If query Q1 <= Q2, then ans(Q1) <= ans(Q2)
    paired = sorted(zip(queries, res), key=lambda x: x[0])
    for k in range(len(paired) - 1):
        q1, c1 = paired[k]
        q2, c2 = paired[k + 1]
        if q1 <= q2:
            assert c1 <= c2
