from collections import Counter
import pytest
from hypothesis import given, strategies as st

from top_k_frequent_words import top_k_frequent as heap_solution
from top_k_frequent_words_buckets import top_k_frequent as bucket_solution

IMPLS = [heap_solution, bucket_solution]
IDS = ["heap", "buckets"]


def oracle(words: list[str], k: int) -> list[str]:
    """Independent ground-truth oracle using full Python sort."""
    if k <= 0 or not words:
        return []
    counts = Counter(words)
    k = min(k, len(counts))
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in sorted_items[:k]]


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "words, k, expected",
    [
        (
            ["i", "love", "leetcode", "i", "love", "coding"],
            2,
            ["i", "love"],
        ),  # LeetCode example 1
        (
            [
                "the",
                "day",
                "is",
                "sunny",
                "the",
                "the",
                "the",
                "sunny",
                "is",
                "is",
            ],
            4,
            ["the", "is", "sunny", "day"],
        ),  # LeetCode example 2
        (["apple"], 1, ["apple"]),  # Singleton
        (["zebra", "apple", "mango"], 2, ["apple", "mango"]),  # Frequency tie
        (["zebra", "apple", "mango"], 3, ["apple", "mango", "zebra"]),
        (["a", "b"], 10, ["a", "b"]),  # k > distinct words
        (["repeat"] * 50, 1, ["repeat"]),
        (["b", "a", "b", "a", "c"], 2, ["a", "b"]),  # Tie between a and b
    ],
)
def test_examples(solve, words, k, expected):
    assert solve(words, k) == expected


def test_empty_input(solve):
    assert solve([], 3) == []


@pytest.mark.parametrize("k", [0, -1, -5])
def test_non_positive_k_returns_empty(solve, k):
    assert solve(["a", "b", "c"], k) == []


def test_does_not_mutate_input(solve):
    original = ["i", "love", "leetcode", "i", "love", "coding"]
    words = original.copy()
    solve(words, 2)
    assert words == original


def test_large_input(solve):
    words = ["common"] * 10_000 + ["runner_up"] * 5_000 + ["rare"] * 10
    result = solve(words, 2)
    assert result == ["common", "runner_up"]


# Hypothesis Strategies
words_vocab = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf"]
words_strategy_small = st.lists(st.sampled_from(words_vocab), min_size=1, max_size=60)
words_strategy_random = st.lists(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8),
    min_size=1,
    max_size=60,
)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize(
    "strategy", [words_strategy_small, words_strategy_random], ids=["small_vocab", "random_words"]
)
def test_matches_oracle(fn, strategy):
    @given(words=strategy, data=st.data())
    def check(words, data):
        k = data.draw(st.integers(min_value=-2, max_value=len(set(words)) + 5))
        assert fn(words, k) == oracle(words, k)

    check()


@given(words=words_strategy_small, data=st.data())
def test_implementations_agree(words, data):
    k = data.draw(st.integers(min_value=1, max_value=len(set(words))))
    assert heap_solution(words, k) == bucket_solution(words, k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(words=words_strategy_small, data=st.data())
def test_invariants_hold(fn, words, data):
    k = data.draw(st.integers(min_value=1, max_value=len(set(words))))
    res = fn(words, k)

    counts = Counter(words)
    expected_k = min(k, len(counts))

    assert len(res) == expected_k
    assert len(set(res)) == len(res), "Results must be distinct"
    assert set(res) <= set(counts.keys()), "Results must come from input"

    # Check ordering invariants:
    # 1. Frequencies must be non-increasing
    # 2. For identical frequencies, words must be in strict alphabetical order
    for i in range(len(res) - 1):
        w1, w2 = res[i], res[i + 1]
        f1, f2 = counts[w1], counts[w2]
        assert f1 >= f2, f"Frequency decreased unexpectedly: {w1}({f1}) vs {w2}({f2})"
        if f1 == f2:
            assert w1 < w2, f"Alphabetical tie-break broken: {w1} should precede {w2}"
