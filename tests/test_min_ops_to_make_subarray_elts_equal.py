import random

import pytest
from hypothesis import given, settings, strategies as st

import min_ops_to_make_subarray_elts_equal as original
from min_ops_to_make_subarray_elts_equal_fenwick import min_operations as fenwick_solution
from min_ops_to_make_subarray_elts_equal_heaps import min_operations as heap_solution

IMPLS = [heap_solution, fenwick_solution]
IDS = ["heaps", "fenwick"]


def brute_force(nums: list[int], k: int) -> int:
    """Every contiguous window, sorted from scratch; cost against its median."""
    best = None
    for i in range(len(nums) - k + 1):
        window = sorted(nums[i : i + k])
        median = window[len(window) // 2]
        cost = sum(abs(x - median) for x in window)
        best = cost if best is None else min(best, cost)
    return best


def exhaustive_oracle(nums: list[int], k: int) -> int:
    """Independent proof that the median is the best target: try every target value in range."""
    best = None
    for i in range(len(nums) - k + 1):
        window = nums[i : i + k]
        for target in range(min(nums), max(nums) + 1):
            cost = sum(abs(x - target) for x in window)
            best = cost if best is None else min(best, cost)
    return best


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([4, 1, 5, 2, 6], 3, 4),  # median 4 of [4,1,5] -> 0+3+1
        ([5, 1, 5, 1], 2, 4),  # sorting would wrongly give 0
        ([1, 100, 2], 3, 99),  # target is the median 2, not the max 100
        ([7], 1, 0),
        ([1, 2, 3], 1, 0),  # k = 1: any single element is already equal
        ([3, 3, 3, 3], 3, 0),  # already equal
        ([1, 2], 2, 1),
        ([1, 10], 2, 9),
        ([1, 2, 3, 4], 4, 4),  # whole array: median 2 or 3 -> 1+0+1+2
        ([9, 1, 1, 9], 2, 0),  # window [1,1] already equal
        ([10, 20, 10, 20, 10], 3, 10),
        ([5, 5, 6, 5, 5], 5, 1),
    ],
)
def test_examples(solve, nums, k, expected):
    assert solve(nums, k) == expected


def test_subarray_must_be_contiguous_in_original_order(solve):
    # Sorted, [1, 1, 5, 5] has a free window of two 1s. In the real order every pair is [1, 5] or [5, 1].
    assert solve([5, 1, 5, 1], 2) == 4


def test_does_not_mutate_input(solve):
    nums = [4, 1, 5, 2, 6]
    solve(nums, 3)
    assert nums == [4, 1, 5, 2, 6]


@pytest.mark.parametrize("nums, k", [([], 1), ([1, 2], 0), ([1, 2], 3), ([1], -1)])
def test_invalid_k_raises(solve, nums, k):
    with pytest.raises(ValueError):
        solve(nums, k)


def test_large_values_no_overflow_issues(solve):
    nums = [10**6, 1] * 500
    assert solve(nums, 2) == 10**6 - 1


def test_larger_random_inputs_match_brute_force(solve):
    rng = random.Random(7)
    for _ in range(25):
        n = rng.randint(1, 150)
        nums = [rng.randint(1, 10**6) for _ in range(n)]
        k = rng.randint(1, n)
        assert solve(nums, k) == brute_force(nums, k)


def test_many_duplicates_match_brute_force(solve):
    rng = random.Random(11)
    for _ in range(25):
        n = rng.randint(1, 120)
        nums = [rng.randint(1, 4) for _ in range(n)]  # heavy ties stress the lazy-deletion bookkeeping
        k = rng.randint(1, n)
        assert solve(nums, k) == brute_force(nums, k)


def test_original_file_is_still_incorrect():
    """Documents defects in the submitted min_ops_to_make_subarray_elts_equal.py.

    It sorts the array (so windows stop being contiguous subarrays) and targets the window maximum
    instead of the median. If you fix that file in place, this test will start failing: delete it and
    add the original module to IMPLS above.
    """
    def run(nums, k):
        fn = original.min_operations
        # tolerate the earlier `self` signature as well as the current one
        try:
            return fn(list(nums), k)
        except TypeError:
            return fn(None, list(nums), k)

    wrong = [([5, 1, 5, 1], 2), ([1, 100, 2], 3), ([4, 1, 5, 2, 6], 3)]
    assert all(run(nums, k) != brute_force(nums, k) for nums, k in wrong)


nums_strategy = st.lists(st.integers(min_value=1, max_value=10**6), min_size=1, max_size=40)
dup_strategy = st.lists(st.integers(min_value=1, max_value=5), min_size=1, max_size=40)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize("strategy", [nums_strategy, dup_strategy], ids=["wide", "duplicates"])
def test_matches_brute_force(fn, strategy):
    @given(nums=strategy, data=st.data())
    def check(nums, data):
        k = data.draw(st.integers(min_value=1, max_value=len(nums)))
        assert fn(nums, k) == brute_force(nums, k)

    check()


@settings(max_examples=60, deadline=None)
@given(nums=st.lists(st.integers(min_value=1, max_value=8), min_size=1, max_size=7), data=st.data())
def test_median_is_truly_the_best_target(nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    expected = exhaustive_oracle(nums, k)
    assert heap_solution(nums, k) == expected
    assert fenwick_solution(nums, k) == expected


@given(nums=nums_strategy, data=st.data())
def test_implementations_agree(nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    assert heap_solution(nums, k) == fenwick_solution(nums, k)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data(), shift=st.integers(min_value=-1000, max_value=1000))
def test_shift_invariance_and_scaling(fn, nums, data, shift):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    base = fn(nums, k)
    assert fn([x + shift for x in nums], k) == base  # adding a constant changes no differences
    assert fn([x * 3 for x in nums], k) == base * 3


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data())
def test_bounds_and_reversal(fn, nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    cost = fn(nums, k)
    assert cost >= 0
    assert cost == fn(list(reversed(nums)), k)  # reversing preserves the set of windows
    assert fn(nums, 1) == 0  # a single element is always already "all equal"


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(nums=nums_strategy, data=st.data())
def test_input_unchanged(fn, nums, data):
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    original_copy = list(nums)
    fn(nums, k)
    assert nums == original_copy
