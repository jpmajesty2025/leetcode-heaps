from collections import Counter
import pytest
from hypothesis import given, strategies as st

from construct_string_with_repeat_limit import (
    repeat_limited_string as heap_solution,
)
from construct_string_with_repeat_limit_array import (
    repeat_limited_string as array_solution,
)

IMPLS = [heap_solution, array_solution]
IDS = ["heap", "array"]


def assert_valid_repeat_limited(s: str, repeat_limit: int, result: str) -> None:
    """Verify that result satisfies all problem constraints."""
    if not s or repeat_limit <= 0:
        assert result == ""
        return

    # Invariant 1: Character counts in result must not exceed counts in s
    s_counts = Counter(s)
    res_counts = Counter(result)
    for char, count in res_counts.items():
        assert (
            count <= s_counts[char]
        ), f"Character {char} used {count} times, but only {s_counts[char]} in s"

    # Invariant 2: No character appears more than repeat_limit times consecutively
    streak = 0
    prev = None
    for char in result:
        if char == prev:
            streak += 1
            assert (
                streak <= repeat_limit
            ), f"Character {char} exceeded repeat limit {repeat_limit} with streak {streak}"
        else:
            streak = 1
            prev = char


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "s, repeat_limit, expected",
    [
        ("cczazcc", 3, "zzcccac"),  # LeetCode example 1
        ("aababab", 2, "bbabaa"),  # LeetCode example 2
        ("aaaa", 2, "aa"),  # Single character exceeded
        ("a", 1, "a"),  # Single character
        ("zyx", 1, "zyx"),  # Already descending
        ("xyz", 1, "zyx"),  # Ascending
        ("abcde", 10, "edcba"),  # repeat_limit >= len(s)
        ("robokill", 1, "rololkib"),  # Interleaved ties
    ],
)
def test_examples(solve, s, repeat_limit, expected):
    res = solve(s, repeat_limit)
    assert res == expected
    assert_valid_repeat_limited(s, repeat_limit, res)


def test_empty_string(solve):
    assert solve("", 3) == ""


@pytest.mark.parametrize("limit", [0, -1, -5])
def test_non_positive_limit_returns_empty(solve, limit):
    assert solve("abc", limit) == ""


def test_large_input(solve):
    s = "z" * 10_000 + "y" * 5_000 + "a" * 1_000
    res = solve(s, 2)
    assert_valid_repeat_limited(s, 2, res)
    assert res.startswith("zzyzzy")


# Hypothesis Strategies
string_strategy = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=80
)
limit_strategy = st.integers(min_value=1, max_value=5)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(s=string_strategy, repeat_limit=limit_strategy)
def test_invariants_hold(fn, s, repeat_limit):
    res = fn(s, repeat_limit)
    assert_valid_repeat_limited(s, repeat_limit, res)


@given(s=string_strategy, repeat_limit=limit_strategy)
def test_implementations_agree(s, repeat_limit):
    r1 = heap_solution(s, repeat_limit)
    r2 = array_solution(s, repeat_limit)
    assert r1 == r2
