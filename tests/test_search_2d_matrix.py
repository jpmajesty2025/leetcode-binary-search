import copy
from typing import List
import pytest
from hypothesis import given, settings, strategies as st

import search_2d_matrix as virtual_1d
import search_2d_matrix_two_pass as two_pass
import search_2d_matrix_bisect as bisect_module

IMPLS = [
    virtual_1d.search_matrix,
    two_pass.search_matrix,
    bisect_module.search_matrix,
    bisect_module.search_matrix_bisect_twopass,
]


def brute_force_oracle(matrix: List[List[int]], target: int) -> bool:
    """Independent ground-truth oracle for verification."""
    if not matrix or not matrix[0]:
        return False
    return any(target in row for row in matrix)


@pytest.mark.parametrize("impl", IMPLS)
@pytest.mark.parametrize(
    "matrix, target, expected",
    [
        # LeetCode standard examples
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3, True),
        ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13, False),
        # Empty cases
        ([], 1, False),
        ([[]], 1, False),
        # 1x1 singleton matrix
        ([[5]], 5, True),
        ([[5]], 4, False),
        ([[5]], 6, False),
        # 1-row matrix (1 x n)
        ([[1, 3, 5, 7, 9]], 1, True),
        ([[1, 3, 5, 7, 9]], 5, True),
        ([[1, 3, 5, 7, 9]], 9, True),
        ([[1, 3, 5, 7, 9]], 0, False),
        ([[1, 3, 5, 7, 9]], 6, False),
        ([[1, 3, 5, 7, 9]], 10, False),
        # 1-column matrix (m x 1)
        ([[1], [3], [5], [7]], 1, True),
        ([[1], [3], [5], [7]], 5, True),
        ([[1], [3], [5], [7]], 7, True),
        ([[1], [3], [5], [7]], 0, False),
        ([[1], [3], [5], [7]], 4, False),
        ([[1], [3], [5], [7]], 8, False),
        # Gap between rows
        ([[1, 2], [5, 6]], 3, False),
        ([[1, 2], [5, 6]], 4, False),
        ([[1, 2], [5, 6]], 2, True),
        ([[1, 2], [5, 6]], 5, True),
        # Negative values and zero
        ([[-10, -5], [-2, 0], [3, 7]], -10, True),
        ([[-10, -5], [-2, 0], [3, 7]], 0, True),
        ([[-10, -5], [-2, 0], [3, 7]], 7, True),
        ([[-10, -5], [-2, 0], [3, 7]], -6, False),
        ([[-10, -5], [-2, 0], [3, 7]], -1, False),
        ([[-10, -5], [-2, 0], [3, 7]], 8, False),
        # 32-bit signed integer limits
        ([[-(2**31), -1], [0, 2**31 - 1]], -(2**31), True),
        ([[-(2**31), -1], [0, 2**31 - 1]], 2**31 - 1, True),
        ([[-(2**31), -1], [0, 2**31 - 1]], 42, False),
    ],
)
def test_known_and_edge_cases(impl, matrix, target, expected):
    assert impl(matrix, target) == expected


@pytest.mark.parametrize("impl", IMPLS)
def test_does_not_mutate_matrix(impl):
    matrix = [[1, 3, 5], [10, 11, 16], [23, 30, 34]]
    original_copy = copy.deepcopy(matrix)
    impl(matrix, 11)
    impl(matrix, 99)
    assert matrix == original_copy


@pytest.mark.parametrize(
    "module",
    [virtual_1d, two_pass, bisect_module],
)
def test_solution_class_compatibility(module):
    sol = module.Solution()
    matrix = [[1, 3, 5], [10, 11, 16]]
    assert sol.searchMatrix(matrix, 3) is True
    assert sol.searchMatrix(matrix, 4) is False
    assert module.Solution.searchMatrix(matrix, 10) is True


# Strategy to generate valid LeetCode 74 matrices
# Property: Row sorted non-decreasing, row[i+1][0] > row[i][-1]
# Equivalent to: a strictly increasing or non-decreasing sequence partitioned into m x n rows
@st.composite
def valid_matrix_and_target(draw):
    m = draw(st.integers(min_value=1, max_value=20))
    n = draw(st.integers(min_value=1, max_value=20))
    total_elements = m * n

    # Generate total_elements sorted integers
    # To strictly satisfy row[i+1][0] > row[i][-1], we can generate strictly increasing values
    values = draw(
        st.lists(
            st.integers(min_value=-10000, max_value=10000),
            min_size=total_elements,
            max_size=total_elements,
            unique=True,
        )
    )
    values.sort()

    matrix = [values[i * n : (i + 1) * n] for i in range(m)]

    # Draw target: either an element from the matrix or an arbitrary integer
    choose_existing = draw(st.booleans())
    if choose_existing:
        target = draw(st.sampled_from(values))
    else:
        target = draw(st.integers(min_value=-15000, max_value=15000))

    return matrix, target


@settings(max_examples=250, deadline=None)
@given(data=valid_matrix_and_target())
def test_hypothesis_matches_oracle_and_all_agree(data):
    matrix, target = data
    expected = brute_force_oracle(matrix, target)

    results = [impl(matrix, target) for impl in IMPLS]

    # Verify every implementation matches the independent oracle
    for res in results:
        assert res == expected

    # Verify 100% agreement among all implementations
    assert len(set(results)) == 1
