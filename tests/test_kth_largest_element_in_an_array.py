import random
import pytest
from hypothesis import given, strategies as st

from kth_largest_element_in_an_array import find_kth_largest as heap_solution
from kth_largest_element_in_an_array_quickselect import find_kth_largest as quickselect_solution

IMPLS = [heap_solution, quickselect_solution]
IDS = ["heap", "quickselect"]


def oracle(nums: list[int], k: int) -> int:
    """Independent ground-truth oracle using full Python sort."""
    return sorted(nums, reverse=True)[k - 1]


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([3, 2, 1, 5, 6, 4], 2, 5),  # LeetCode example 1
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),  # LeetCode example 2
        ([1], 1, 1),  # Singleton
        ([1, 2], 1, 2),  # k = 1 (maximum)
        ([1, 2], 2, 1),  # k = n (minimum)
        ([7, 10, 4, 3, 20, 15], 3, 10),
        ([7, 10, 4, 3, 20, 15], 1, 20),
        ([7, 10, 4, 3, 20, 15], 6, 3),
        ([-1, -1], 2, -1),  # Duplicates of negatives
        ([-1, 2, 0], 2, 0),  # Mixed negatives, zero, positives
        ([-5, -2, -1, -10, -7], 1, -1),
        ([-5, -2, -1, -10, -7], 5, -10),
        ([4, 4, 4, 4, 4], 3, 4),  # All identical elements
        ([1, 2, 3, 4, 5, 6], 3, 4),  # Already sorted ascending
        ([6, 5, 4, 3, 2, 1], 3, 4),  # Already sorted descending
        ([10**4, -(10**4), 0], 1, 10**4),  # Constraint extreme max
        ([10**4, -(10**4), 0], 3, -(10**4)),  # Constraint extreme min
    ],
)
def test_examples(solve, nums, k, expected):
    assert solve(nums, k) == expected


def test_returns_int(solve):
    result = solve([3, 2, 1, 5, 6, 4], 2)
    assert isinstance(result, int)


@pytest.mark.parametrize("k", [0, -1, -5])
def test_non_positive_k_raises(solve, k):
    with pytest.raises(ValueError):
        solve([1, 2, 3], k)


def test_k_greater_than_length_raises(solve):
    with pytest.raises(ValueError):
        solve([1, 2, 3], 4)


def test_empty_array_raises(solve):
    with pytest.raises(ValueError):
        solve([], 1)


def test_does_not_mutate_input(solve):
    original = [3, 2, 1, 5, 6, 4]
    nums = original.copy()
    solve(nums, 2)
    assert nums == original


def test_large_input(solve):
    nums = list(range(100_000))
    # 1st largest is 99_999, 100_000th largest is 0
    assert solve(nums, 1) == 99_999
    assert solve(nums, 100_000) == 0
    assert solve(nums, 50_000) == 50_000


def test_heavy_duplicates_large(solve):
    nums = [42] * 50_000 + [99] * 10
    assert solve(nums, 5) == 99
    assert solve(nums, 15) == 42


# Hypothesis Strategies
nums_strategy = st.lists(
    st.integers(min_value=-(10**4), max_value=10**4),
    min_size=1,
    max_size=60,
)
dup_strategy = st.lists(
    st.integers(min_value=-2, max_value=3),
    min_size=1,
    max_size=60,
)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize("strategy", [nums_strategy, dup_strategy], ids=["wide", "duplicates"])
def test_matches_oracle(fn, strategy):
    @given(nums=strategy, data=st.data())
    def check(nums, data):
        k = data.draw(st.integers(min_value=1, max_value=len(nums)))
        assert fn(nums, k) == oracle(nums, k)

    check()


@given(nums=nums_strategy, data=st.data())
def test_implementations_agree(nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    assert heap_solution(nums, k) == quickselect_solution(nums, k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data())
def test_result_is_element_of_array(fn, nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    assert fn(nums, k) in nums


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data(), c=st.integers(min_value=-500, max_value=500))
def test_shift_invariance(fn, nums, data, c):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    shifted = [x + c for x in nums]
    assert fn(shifted, k) == fn(nums, k) + c


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data(), seed=st.integers(min_value=0, max_value=1000))
def test_order_invariance(fn, nums, data, seed):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    shuffled = nums.copy()
    random.Random(seed).shuffle(shuffled)
    assert fn(shuffled, k) == fn(nums, k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data())
def test_duality_with_negation(fn, nums, data):
    """The kth largest in nums is -((n - k + 1)th largest in -nums)."""
    n = len(nums)
    k = data.draw(st.integers(min_value=1, max_value=n))
    negated = [-x for x in nums]
    dual_k = n - k + 1
    assert fn(nums, k) == -fn(negated, dual_k)
