from collections import Counter
import pytest
from hypothesis import given, strategies as st

from rearrange_string_k_distance_apart import (
    rearrange_string as heap_solution,
)
from rearrange_string_k_distance_apart_table import (
    rearrange_string as table_solution,
)

IMPLS = [heap_solution, table_solution]
IDS = ["heap_deque", "table_scan"]


def assert_valid_rearrangement(s: str, k: int, result: str) -> None:
    """Verify that result satisfies all problem constraints."""
    if not result:
        return

    # Invariant 1: Result must be an anagram of s
    assert len(result) == len(s)
    assert Counter(result) == Counter(s)

    # Invariant 2: Every identical character must be at least distance k apart
    last_seen: dict[str, int] = {}
    for i, char in enumerate(result):
        if char in last_seen:
            diff = i - last_seen[char]
            assert (
                diff >= k
            ), f"Character {char} at index {i} is only distance {diff} from index {last_seen[char]} (required {k})"
        last_seen[char] = i


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "s, k",
    [
        ("aabbcc", 3),  # LeetCode Ex 1
        ("aaadbbcc", 2),  # LeetCode Ex 3
        ("abcdef", 3),  # All distinct
        ("a", 2),  # Single character
        ("ab", 2),  # Two characters
        ("aabbcc", 2),  # Looser distance
    ],
)
def test_valid_examples(solve, s, k):
    res = solve(s, k)
    assert res != ""
    assert_valid_rearrangement(s, k, res)


@pytest.mark.parametrize(
    "s, k",
    [
        ("aaabc", 3),  # LeetCode Ex 2: impossible
        ("aa", 2),  # Impossible
        ("aaa", 2),  # Impossible
        ("aaaaa", 3),  # Impossible
    ],
)
def test_impossible_examples(solve, s, k):
    res = solve(s, k)
    assert res == ""


def test_k_zero_or_one(solve):
    assert solve("aaabbb", 1) == "aaabbb"
    assert solve("aaabbb", 0) == "aaabbb"


def test_empty_string(solve):
    assert solve("", 3) == ""


def test_negative_k_raises(solve):
    with pytest.raises(ValueError):
        solve("abc", -1)


def test_large_input(solve):
    # Construct a guaranteed valid workload: 5000 copies of "abcde", k = 5
    s = "abcde" * 2000
    res = solve(s, 5)
    assert res != ""
    assert_valid_rearrangement(s, 5, res)


# Hypothesis Strategies
string_strategy = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=40
)
k_strategy = st.integers(min_value=1, max_value=6)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(s=string_strategy, k=k_strategy)
def test_invariants_hold(fn, s, k):
    res = fn(s, k)
    assert_valid_rearrangement(s, k, res)


@given(s=string_strategy, k=k_strategy)
def test_implementations_agree_on_possibility(s, k):
    r1 = heap_solution(s, k)
    r2 = table_solution(s, k)
    # Both must either succeed or both fail
    assert (r1 == "") == (r2 == "")
    assert_valid_rearrangement(s, k, r1)
    assert_valid_rearrangement(s, k, r2)
