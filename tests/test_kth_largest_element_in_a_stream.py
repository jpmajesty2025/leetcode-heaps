import random
import pytest
from hypothesis import given, strategies as st

from kth_largest_element_in_a_stream import KthLargest as HeapKthLargest
from kth_largest_element_in_a_stream_sorted_list import (
    KthLargest as SortedListKthLargest,
)

IMPLS = [HeapKthLargest, SortedListKthLargest]
IDS = ["heap", "sorted_list"]


def oracle(all_nums: list[int], k: int) -> int:
    """Independent ground-truth oracle: sort all numbers seen so far and take the kth largest."""
    return sorted(all_nums)[-k]


@pytest.fixture(params=IMPLS, ids=IDS)
def make_kth(request):
    return request.param


def test_leetcode_example(make_kth):
    kth = make_kth(3, [4, 5, 8, 2])
    assert kth.add(3) == 4
    assert kth.add(5) == 5
    assert kth.add(10) == 5
    assert kth.add(9) == 8
    assert kth.add(4) == 8


def test_singleton_k_is_running_maximum(make_kth):
    kth = make_kth(1, [])
    assert kth.add(-3) == -3
    assert kth.add(-2) == -2
    assert kth.add(-4) == -2
    assert kth.add(0) == 0
    assert kth.add(4) == 4
    assert kth.add(2) == 4


def test_empty_initial_nums(make_kth):
    kth = make_kth(2, [])
    kth.add(10)
    assert kth.add(20) == 10
    assert kth.add(15) == 15
    assert kth.add(5) == 15
    assert kth.add(30) == 20


def test_fewer_than_k_elements_initially(make_kth):
    kth = make_kth(3, [1, 2])
    assert kth.add(3) == 1
    assert kth.add(4) == 2
    assert kth.add(5) == 3


def test_duplicates_in_stream(make_kth):
    kth = make_kth(2, [5, 5, 5])
    assert kth.add(5) == 5
    assert kth.add(10) == 5
    assert kth.add(10) == 10
    assert kth.add(2) == 10


def test_negative_numbers_stream(make_kth):
    kth = make_kth(3, [-10, -20, -30])
    assert kth.add(-5) == -20
    assert kth.add(-1) == -10
    assert kth.add(-100) == -10


@pytest.mark.parametrize("k", [0, -1, -10])
def test_invalid_k_raises(make_kth, k):
    with pytest.raises(ValueError):
        make_kth(k, [1, 2, 3])


def test_does_not_mutate_input_nums(make_kth):
    original = [4, 5, 8, 2]
    nums = original.copy()
    make_kth(3, nums)
    assert nums == original


def test_large_stream(make_kth):
    kth = make_kth(5, list(range(100)))
    for val in range(100, 10_000):
        res = kth.add(val)
        assert res == val - 4  # 5th largest in 0..val is val - 4


# Hypothesis Strategies
stream_strategy = st.lists(
    st.integers(min_value=-(10**4), max_value=10**4),
    min_size=1,
    max_size=50,
)


@pytest.mark.parametrize("cls", IMPLS, ids=IDS)
@given(
    initial=stream_strategy,
    stream=stream_strategy,
    data=st.data(),
)
def test_matches_oracle(cls, initial, stream, data):
    k = data.draw(st.integers(min_value=1, max_value=len(initial)))
    kth = cls(k, initial)
    history = initial.copy()

    for val in stream:
        history.append(val)
        res = kth.add(val)
        assert res == oracle(history, k)


@given(
    initial=stream_strategy,
    stream=stream_strategy,
    data=st.data(),
)
def test_implementations_agree(initial, stream, data):
    k = data.draw(st.integers(min_value=1, max_value=len(initial)))
    h = HeapKthLargest(k, initial)
    s = SortedListKthLargest(k, initial)

    for val in stream:
        assert h.add(val) == s.add(val)


@pytest.mark.parametrize("cls", IMPLS, ids=IDS)
@given(
    initial=stream_strategy,
    stream=stream_strategy,
    data=st.data(),
)
def test_kth_largest_is_monotonically_non_decreasing(cls, initial, stream, data):
    """Adding new elements to a pool can never decrease the kth largest score."""
    k = data.draw(st.integers(min_value=1, max_value=len(initial)))
    kth = cls(k, initial)

    prev = kth.add(initial[0])  # ensure at least k elements present
    for val in stream:
        curr = kth.add(val)
        assert curr >= prev, f"kth largest decreased from {prev} to {curr}"
        prev = curr


@pytest.mark.parametrize("cls", IMPLS, ids=IDS)
@given(
    initial=stream_strategy,
    stream=stream_strategy,
    c=st.integers(min_value=-500, max_value=500),
    data=st.data(),
)
def test_shift_invariance(cls, initial, stream, c, data):
    """Adding c to all inputs shifts every output by c."""
    k = data.draw(st.integers(min_value=1, max_value=len(initial)))
    kth1 = cls(k, initial)
    kth2 = cls(k, [x + c for x in initial])

    for val in stream:
        r1 = kth1.add(val)
        r2 = kth2.add(val + c)
        assert r2 == r1 + c
