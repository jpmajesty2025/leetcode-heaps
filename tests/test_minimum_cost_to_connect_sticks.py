from functools import lru_cache

import pytest
from hypothesis import given, settings, strategies as st

from minimum_cost_to_connect_sticks import connect_sticks as heap_solution
from minimum_cost_to_connect_sticks_two_queues import connect_sticks as queue_solution

IMPLS = [heap_solution, queue_solution]
IDS = ["heap", "two_queues"]


def sorted_list_oracle(sticks: list[int]) -> int:
    """Greedy simulation re-sorting every round: slow but obviously the intended algorithm."""
    sticks = sorted(sticks)
    total = 0
    while len(sticks) > 1:
        merged = sticks[0] + sticks[1]
        total += merged
        sticks = sorted(sticks[2:] + [merged])
    return total


def exhaustive_oracle(sticks: list[int]) -> int:
    """Try every possible pair to merge at every step: independent proof that greedy is optimal."""

    @lru_cache(maxsize=None)
    def best(state: tuple[int, ...]) -> int:
        if len(state) <= 1:
            return 0
        options = []
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                rest = [x for k, x in enumerate(state) if k not in (i, j)]
                merged = state[i] + state[j]
                options.append(merged + best(tuple(sorted(rest + [merged]))))
        return min(options)

    return best(tuple(sorted(sticks)))


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "sticks, expected",
    [
        ([], 0),
        ([5], 0),  # nothing to connect
        ([2, 4, 3], 14),  # LeetCode example 1
        ([1, 8, 3, 5], 30),  # LeetCode example 2
        ([3, 3], 6),
        ([1, 1, 1, 1], 8),  # 2 + 2 + 4
        ([1, 2, 3, 4, 5], 33),
        ([10, 1], 11),
        ([7, 7, 7], 35),  # 14 + 21
    ],
)
def test_examples(solve, sticks, expected):
    assert solve(sticks) == expected


def test_does_not_mutate_input(solve):
    sticks = [2, 4, 3]
    solve(sticks)
    assert sticks == [2, 4, 3]


def test_unsorted_and_sorted_inputs_agree(solve):
    assert solve([9, 1, 5, 3, 7]) == solve([1, 3, 5, 7, 9])


def test_repeated_calls_are_independent(solve):
    sticks = [1, 8, 3, 5]
    assert solve(sticks) == solve(sticks) == 30


def test_constraint_extremes(solve):
    # n = 10^4 equal sticks of 10^4: a balanced merge tree is optimal when the count is a power of two.
    sticks = [10**4] * 2**13
    assert solve(sticks) == 10**4 * 2**13 * 13  # every stick is re-paid once per tree level


sticks_strategy = st.lists(st.integers(min_value=1, max_value=10**4), max_size=40)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(sticks=sticks_strategy)
def test_matches_sorted_list_oracle(fn, sticks):
    assert fn(sticks) == sorted_list_oracle(sticks)


@settings(max_examples=60, deadline=None)
@given(sticks=st.lists(st.integers(min_value=1, max_value=20), max_size=6))
def test_greedy_is_truly_minimal(sticks):
    expected = exhaustive_oracle(sticks)
    assert heap_solution(sticks) == expected
    assert queue_solution(sticks) == expected


@given(sticks=sticks_strategy)
def test_implementations_agree(sticks):
    assert heap_solution(sticks) == queue_solution(sticks)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(sticks=sticks_strategy, scale=st.integers(min_value=1, max_value=50))
def test_cost_scales_linearly(fn, sticks, scale):
    assert fn([s * scale for s in sticks]) == fn(sticks) * scale


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(sticks=sticks_strategy)
def test_bounds_and_order_independence(fn, sticks):
    cost = fn(sticks)
    assert cost == fn(list(reversed(sticks)))
    if len(sticks) >= 2:
        assert cost >= sum(sticks)  # every stick is paid for at least once
        assert cost <= sum(sticks) * (len(sticks) - 1)  # loose upper bound: each merge costs at most the total


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(sticks=sticks_strategy)
def test_input_unchanged(fn, sticks):
    original = list(sticks)
    fn(sticks)
    assert sticks == original
