from collections import Counter

import pytest
from hypothesis import given, strategies as st

from top_k_frequent_elements import top_k_frequent as heap_solution
from top_k_frequent_elements_buckets import top_k_frequent as bucket_solution

IMPLS = [heap_solution, bucket_solution]
IDS = ["heap", "buckets"]


def assert_valid_top_k(nums: list[int], k: int, result: list[int]) -> None:
    """Checks the answer without assuming a tie-break order (the problem allows any valid answer)."""
    counts = Counter(nums)
    expected_size = min(max(k, 0), len(counts))
    assert len(result) == expected_size
    assert len(set(result)) == len(result), "values must be distinct"
    assert set(result) <= set(counts), "values must come from nums"
    expected_counts = sorted(counts.values(), reverse=True)[:expected_size]
    assert sorted((counts[v] for v in result), reverse=True) == expected_counts


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([1, 1, 1, 2, 2, 3], 2, {1, 2}),  # LeetCode example 1
        ([1], 1, {1}),  # LeetCode example 2
        ([4, 4, 4, 4], 1, {4}),
        ([-1, -1, 2, 2, 2, 3], 1, {2}),
        ([-1, -1, -1, 2, 2, 3], 2, {-1, 2}),
        ([5, 3, 5, 3, 5, 1], 2, {5, 3}),
        ([0, 0, 0, 7, 7, 9], 3, {0, 7, 9}),  # k equals the number of distinct values
        ([1, 2, 3, 4], 4, {1, 2, 3, 4}),
        ([10**4, -(10**4), 10**4], 1, {10**4}),  # constraint extremes
    ],
)
def test_examples(solve, nums, k, expected):
    assert set(solve(nums, k)) == expected


def test_returns_list_of_ints(solve):
    result = solve([1, 1, 2], 1)
    assert isinstance(result, list)
    assert all(isinstance(v, int) for v in result)


def test_empty_input(solve):
    assert solve([], 3) == []


@pytest.mark.parametrize("k", [0, -1])
def test_non_positive_k_returns_empty(solve, k):
    assert solve([1, 1, 2], k) == []


def test_k_larger_than_distinct_count_returns_all(solve):
    assert sorted(solve([1, 1, 2, 3], 10)) == [1, 2, 3]


def test_ties_return_a_valid_answer(solve):
    nums = [1, 2, 3, 4]  # every value ties at count 1
    result = solve(nums, 2)
    assert_valid_top_k(nums, 2, result)


def test_tie_at_the_boundary(solve):
    nums = [1, 1, 1, 2, 2, 3, 3]  # 1 is clearly first; 2 and 3 tie for the second slot
    result = solve(nums, 2)
    assert 1 in result
    assert_valid_top_k(nums, 2, result)


def test_does_not_mutate_input(solve):
    nums = [1, 1, 1, 2, 2, 3]
    solve(nums, 2)
    assert nums == [1, 1, 1, 2, 2, 3]


def test_large_input(solve):
    nums = [i % 1000 for i in range(200_000)] + [7] * 500
    assert solve(nums, 1) == [7]
    assert_valid_top_k(nums, 25, solve(nums, 25))


nums_strategy = st.lists(st.integers(min_value=-(10**4), max_value=10**4), max_size=60)
dup_strategy = st.lists(st.integers(min_value=0, max_value=6), max_size=60)
k_strategy = st.integers(min_value=-2, max_value=12)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize("strategy", [nums_strategy, dup_strategy], ids=["wide", "duplicates"])
def test_valid_top_k_for_any_input(fn, strategy):
    @given(nums=strategy, k=k_strategy)
    def check(nums, k):
        assert_valid_top_k(nums, k, fn(nums, k))

    check()


@given(nums=nums_strategy, k=k_strategy)
def test_implementations_return_same_frequency_profile(nums, k):
    counts = Counter(nums)
    heap_profile = sorted((counts[v] for v in heap_solution(nums, k)), reverse=True)
    bucket_profile = sorted((counts[v] for v in bucket_solution(nums, k)), reverse=True)
    assert heap_profile == bucket_profile


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=dup_strategy, k=st.integers(min_value=1, max_value=7))
def test_result_matches_most_common_when_answer_is_unique(fn, nums, k):
    ranked = Counter(nums).most_common()
    if len(ranked) > k and ranked[k - 1][1] == ranked[k][1]:
        return  # tie at the boundary: the answer is not unique, covered by the validity tests
    assert set(fn(nums, k)) == {v for v, _ in ranked[:k]}


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, k=k_strategy)
def test_order_independent_frequency_profile(fn, nums, k):
    counts = Counter(nums)
    a = sorted((counts[v] for v in fn(nums, k)), reverse=True)
    b = sorted((counts[v] for v in fn(list(reversed(nums)), k)), reverse=True)
    assert a == b


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, k=k_strategy)
def test_input_unchanged(fn, nums, k):
    original = list(nums)
    fn(nums, k)
    assert nums == original
