import random
import statistics

import pytest
from hypothesis import given, strategies as st

from find_median_from_data_stream import MedianFinder as TwoHeaps
from find_median_from_data_stream_sorted_list import MedianFinder as SortedList

IMPLS = [TwoHeaps, SortedList]


def oracle(values: list[int]) -> float:
    """Independent reference: statistics.median on the full prefix."""
    return float(statistics.median(values))


@pytest.fixture(params=IMPLS, ids=lambda cls: cls.__module__)
def make(request):
    return request.param


def run_stream(cls, values: list[int]) -> list[float]:
    finder = cls()
    medians = []
    for value in values:
        finder.addNum(value)
        medians.append(finder.findMedian())
    return medians


def test_leetcode_example(make):
    finder = make()
    finder.addNum(1)
    finder.addNum(2)
    assert finder.findMedian() == 1.5
    finder.addNum(3)
    assert finder.findMedian() == 2.0


def test_single_element(make):
    finder = make()
    finder.addNum(7)
    assert finder.findMedian() == 7.0


@pytest.mark.parametrize(
    "values, expected",
    [
        ([5, 5, 5, 5], [5.0, 5.0, 5.0, 5.0]),  # all duplicates
        ([-1, -2, -3, -4, -5], [-1.0, -1.5, -2.0, -2.5, -3.0]),  # negatives, descending
        ([-5, 5], [-5.0, 0.0]),  # median is exactly zero
        ([1, 2, 3, 4, 5], [1.0, 1.5, 2.0, 2.5, 3.0]),  # ascending
        ([5, 4, 3, 2, 1], [5.0, 4.5, 4.0, 3.5, 3.0]),  # descending
        ([0, 0, 1], [0.0, 0.0, 0.0]),
        ([10**5, -(10**5)], [100000.0, 0.0]),  # constraint extremes
    ],
)
def test_streams(make, values, expected):
    assert run_stream(make, values) == expected


def test_empty_raises(make):
    with pytest.raises(IndexError):
        make().findMedian()


def test_find_median_is_idempotent(make):
    finder = make()
    for value in [3, 1, 4, 1, 5]:
        finder.addNum(value)
    first = finder.findMedian()
    assert finder.findMedian() == first == 3.0
    finder.addNum(9)
    assert finder.findMedian() == 3.5


@pytest.mark.parametrize("order", ["ascending", "descending", "equal", "shuffled"])
def test_large_streams_match_oracle(make, order):
    rng = random.Random(0)
    values = list(range(2000))
    if order == "descending":
        values.reverse()
    elif order == "equal":
        values = [42] * 2000
    elif order == "shuffled":
        rng.shuffle(values)
    finder = make()
    seen: list[int] = []
    for i, value in enumerate(values):
        finder.addNum(value)
        seen.append(value)
        if i % 97 == 0 or i == len(values) - 1:  # spot-check along the way
            assert finder.findMedian() == oracle(seen)


streams = st.lists(st.integers(min_value=-(10**5), max_value=10**5), min_size=1, max_size=60)


@pytest.mark.parametrize("cls", IMPLS, ids=lambda cls: cls.__module__)
@given(values=streams)
def test_every_prefix_matches_oracle(cls, values):
    medians = run_stream(cls, values)
    for i, median in enumerate(medians):
        assert median == oracle(values[: i + 1])


@given(values=streams)
def test_implementations_agree(values):
    assert run_stream(TwoHeaps, values) == run_stream(SortedList, values)


@given(
    ops=st.lists(
        st.one_of(
            st.integers(min_value=-1000, max_value=1000).map(lambda n: ("add", n)),
            st.just(("query", 0)),
        ),
        min_size=1,
        max_size=80,
    )
)
def test_interleaved_adds_and_queries(ops):
    heaps, sorted_list = TwoHeaps(), SortedList()
    seen: list[int] = []
    for kind, value in ops:
        if kind == "add":
            heaps.addNum(value)
            sorted_list.addNum(value)
            seen.append(value)
        elif seen:
            expected = oracle(seen)
            assert heaps.findMedian() == expected
            assert sorted_list.findMedian() == expected


@given(values=streams)
def test_two_heap_invariants(values):
    finder = TwoHeaps()
    for value in values:
        finder.addNum(value)
        low, high = finder._low, finder._high
        assert len(low) in (len(high), len(high) + 1)  # balanced, lower half never smaller
        if high:
            assert -low[0] <= high[0]  # halves are correctly ordered
