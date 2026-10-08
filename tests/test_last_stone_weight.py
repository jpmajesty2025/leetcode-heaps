import pytest
from hypothesis import given, strategies as st

from last_stone_weight import last_stone_weight


def oracle(stones: list[int]) -> int:
    """Obviously-correct O(n^2 log n) simulation: re-sort every turn."""
    stones = list(stones)
    while len(stones) > 1:
        stones.sort()
        y = stones.pop()
        x = stones.pop()
        if x != y:
            stones.append(y - x)
    return stones[0] if stones else 0


@pytest.mark.parametrize(
    "stones, expected",
    [
        ([], 0),
        ([7], 7),
        ([5, 5], 0),
        ([2, 7], 5),
        ([3, 3, 3], 3),
        ([1, 1, 1, 1], 0),
        ([2, 7, 4, 1, 8, 1], 1),  # LeetCode example 1
        ([1], 1),  # LeetCode example 2
        ([10, 4, 3], 3),
        ([1000, 1, 1, 1], 997),
        ([9, 3, 2, 10], 0),
        ([1, 3], 2),
    ],
)
def test_examples(stones, expected):
    assert last_stone_weight(stones) == expected


def test_does_not_mutate_input():
    stones = [2, 7, 4, 1, 8, 1]
    snapshot = list(stones)
    last_stone_weight(stones)
    assert stones == snapshot


def test_large_input():
    stones = list(range(1, 3001))
    assert last_stone_weight(stones) == oracle(stones)


stone_lists = st.lists(st.integers(min_value=1, max_value=1000), max_size=30)


@given(stones=stone_lists)
def test_matches_oracle(stones):
    assert last_stone_weight(stones) == oracle(stones)


@given(stones=stone_lists)
def test_order_independent(stones):
    assert last_stone_weight(stones) == last_stone_weight(list(reversed(stones)))


@given(stones=stone_lists)
def test_invariants(stones):
    result = last_stone_weight(stones)
    assert 0 <= result <= (max(stones) if stones else 0)
    # Each smash removes 2*min(x, y) from the total, so parity is preserved.
    assert result % 2 == sum(stones) % 2


@given(stones=stone_lists)
def test_input_unchanged(stones):
    original = list(stones)
    last_stone_weight(stones)
    assert stones == original
