import inspect
from fractions import Fraction
from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import min_ops_to_halve_array_sum as module


def halve(nums: list[int]) -> int:
    """Call halve_array whether or not it still carries a leftover `self` parameter."""
    fn = module.halve_array
    if next(iter(inspect.signature(fn).parameters)) == "self":
        return fn(None, nums)
    return fn(nums)


def greedy_oracle(nums: list[int]) -> int:
    """Exact-arithmetic simulation: always halve the current maximum."""
    values = [Fraction(n) for n in nums]
    target = sum(values) / 2
    current = sum(values)
    ops = 0
    while current > target:
        i = max(range(len(values)), key=values.__getitem__)
        current -= values[i] / 2
        values[i] /= 2
        ops += 1
    return ops


def exhaustive_oracle(nums: list[int]) -> int:
    """Try every sequence of choices; independent proof that greedy is optimal.

    Halving every element once removes exactly half the sum, so n operations always suffice.
    """
    n = len(nums)
    target = Fraction(sum(nums), 2)
    for depth in range(n + 1):
        for choices in product(range(n), repeat=depth):
            values = [Fraction(x) for x in nums]
            for i in choices:
                values[i] /= 2
            if sum(values) <= target:
                return depth
    raise AssertionError("unreachable: n operations always suffice")


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([5, 19, 8, 1], 3),  # LeetCode example 1
        ([3, 8, 20], 3),  # LeetCode example 2
        ([1], 1),
        ([4], 1),
        ([7], 1),
        ([1, 1], 2),  # 2 -> 1.5 -> 1.0, which is exactly half
        ([2, 2, 2, 2], 4),  # each op removes only 1 of the 8
        ([10, 1, 1, 1], 2),  # 13 -> 8 -> 5.5, target 6.5
        ([1, 1, 1, 1, 1], 5),  # 5 -> ... -> 2.5, exact tie after five ops
        ([8, 8, 8], 3),  # each op removes 4 of the 24
        ([100, 1], 2),  # 101 -> 51 (> 50.5) -> 26
    ],
)
def test_examples(nums, expected):
    assert halve(nums) == expected


def test_empty_needs_no_operations():
    assert halve([]) == 0


def test_does_not_mutate_input():
    nums = [5, 19, 8, 1]
    snapshot = list(nums)
    halve(nums)
    assert nums == snapshot


def test_large_equal_values_hit_exact_tie():
    # Halving each element once removes exactly half the sum, so the answer is n.
    # Exercises the strict '>' comparison at an exact tie with a ~1e12 float sum.
    assert halve([10**7] * 10**5) == 10**5


def test_wide_range_matches_exact_oracle():
    nums = [10**7] + [1] * 2000
    assert halve(nums) == greedy_oracle(nums)


small_lists = st.lists(st.integers(min_value=1, max_value=10**7), min_size=1, max_size=40)
tiny_lists = st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=4)


@given(nums=small_lists)
def test_matches_exact_greedy_oracle(nums):
    assert halve(nums) == greedy_oracle(nums)


@settings(max_examples=60)
@given(nums=tiny_lists)
def test_greedy_is_truly_minimal(nums):
    assert halve(nums) == exhaustive_oracle(nums)


@given(nums=small_lists)
def test_order_independent(nums):
    assert halve(nums) == halve(list(reversed(nums)))


@given(nums=small_lists)
def test_operation_count_bounds(nums):
    ops = halve(nums)
    assert 1 <= ops <= len(nums)


@given(nums=small_lists, k=st.integers(min_value=1, max_value=8))
def test_scaling_by_a_constant_does_not_change_answer(nums, k):
    assert halve([n * k for n in nums]) == halve(nums)


@given(nums=small_lists)
def test_input_unchanged(nums):
    original = list(nums)
    halve(nums)
    assert nums == original
