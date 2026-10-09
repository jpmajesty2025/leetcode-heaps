from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

from remove_stones_minimize_total import min_stone_sum as heap_solution
from remove_stones_minimize_total_buckets import min_stone_sum as bucket_solution

IMPLS = [heap_solution, bucket_solution]
IDS = ["heap", "buckets"]


def greedy_oracle(piles: list[int], k: int) -> int:
    """Plain simulation: k times, shrink the current maximum (re-scanned each time)."""
    piles = list(piles)
    for _ in range(k):
        i = max(range(len(piles)), key=piles.__getitem__)
        piles[i] -= piles[i] // 2
    return sum(piles)


def exhaustive_oracle(piles: list[int], k: int) -> int:
    """Try every sequence of k choices: independent proof that greedy is optimal."""
    best = sum(piles)
    for choices in product(range(len(piles)), repeat=k):
        current = list(piles)
        for i in choices:
            current[i] -= current[i] // 2
        best = min(best, sum(current))
    return best


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "piles, k, expected",
    [
        ([5, 4, 9], 2, 12),  # LeetCode example 1
        ([4, 3, 6, 7], 3, 12),  # LeetCode example 2
        ([5], 1, 3),  # odd pile leaves ceil, not a fraction
        ([1], 5, 1),  # size 1 can never shrink
        ([1, 1, 1], 10, 3),
        ([10], 0, 10),  # k = 0 changes nothing
        ([2], 1, 1),
        ([7], 3, 1),  # 7 -> 4 -> 2 -> 1
        ([8, 8], 2, 8),
        ([3, 3, 3], 3, 6),
        ([100, 1], 1, 51),
        ([5, 5, 5], 100, 3),  # k far beyond what is needed
    ],
)
def test_examples(solve, piles, k, expected):
    assert solve(piles, k) == expected


def test_returns_int(solve):
    result = solve([5, 4, 9], 2)
    assert isinstance(result, int)


def test_does_not_mutate_input(solve):
    piles = [5, 4, 9]
    solve(piles, 2)
    assert piles == [5, 4, 9]


def test_constraint_extremes(solve):
    piles = [10**4] * 1000
    assert solve(piles, 10**5) == greedy_oracle_fast(piles, 10**5)


def greedy_oracle_fast(piles: list[int], k: int) -> int:
    """Oracle for big inputs: after enough rounds every pile is 1, so mimic with per-pile halving counts."""
    # All piles are equal, so k operations spread round-robin: each full round halves every pile once.
    n = len(piles)
    rounds, extra = divmod(k, n)
    total = 0
    for index, pile in enumerate(piles):
        for _ in range(rounds + (1 if index < extra else 0)):
            pile -= pile // 2
        total += pile
    return total


piles_strategy = st.lists(st.integers(min_value=1, max_value=10**4), min_size=1, max_size=30)
k_strategy = st.integers(min_value=0, max_value=60)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(piles=piles_strategy, k=k_strategy)
def test_matches_greedy_oracle(fn, piles, k):
    assert fn(piles, k) == greedy_oracle(piles, k)


@settings(max_examples=80)
@given(
    piles=st.lists(st.integers(min_value=1, max_value=30), min_size=1, max_size=3),
    k=st.integers(min_value=0, max_value=4),
)
def test_greedy_is_truly_minimal(piles, k):
    expected = exhaustive_oracle(piles, k)
    assert heap_solution(piles, k) == expected
    assert bucket_solution(piles, k) == expected


@given(piles=piles_strategy, k=k_strategy)
def test_implementations_agree(piles, k):
    assert heap_solution(piles, k) == bucket_solution(piles, k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(piles=piles_strategy, k=k_strategy)
def test_bounds_and_order_independence(fn, piles, k):
    result = fn(piles, k)
    assert len(piles) <= result <= sum(piles)  # every pile keeps at least one stone
    assert result == fn(list(reversed(piles)), k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(piles=piles_strategy, k=st.integers(min_value=0, max_value=59))
def test_more_operations_never_hurt(fn, piles, k):
    assert fn(piles, k + 1) <= fn(piles, k)
