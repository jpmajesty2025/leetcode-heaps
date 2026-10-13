import pytest
from hypothesis import given, strategies as st

from smallest_number_in_an_infinte_set import (
    SmallestInfiniteSet as HeapInfiniteSet,
)
from smallest_number_in_an_infinte_set_hash_set import (
    SmallestInfiniteSet as HashInfiniteSet,
)

IMPLS = [HeapInfiniteSet, HashInfiniteSet]
IDS = ["heap_set", "hash_set"]


class InfiniteSetOracle:
    """Independent ground-truth oracle tracking popped numbers."""

    def __init__(self):
        self.popped: set[int] = set()

    def popSmallest(self) -> int:
        num = 1
        while num in self.popped:
            num += 1
        self.popped.add(num)
        return num

    def addBack(self, num: int) -> None:
        if num > 0:
            self.popped.discard(num)


@pytest.fixture(params=IMPLS, ids=IDS)
def make_set(request):
    return request.param


def test_leetcode_example(make_set):
    sis = make_set()
    sis.addBack(2)  # 2 is already in set, no change
    assert sis.popSmallest() == 1
    assert sis.popSmallest() == 2
    assert sis.popSmallest() == 3
    sis.addBack(1)  # 1 is added back
    assert sis.popSmallest() == 1  # 1 is smallest again
    assert sis.popSmallest() == 4
    assert sis.popSmallest() == 5


def test_sequential_pops(make_set):
    sis = make_set()
    for expected in range(1, 11):
        assert sis.popSmallest() == expected


def test_duplicate_add_back(make_set):
    sis = make_set()
    for _ in range(5):
        sis.popSmallest()  # popped 1, 2, 3, 4, 5

    # Add back 2 multiple times
    sis.addBack(2)
    sis.addBack(2)
    sis.addBack(2)

    # 2 should only be popped once
    assert sis.popSmallest() == 2
    assert sis.popSmallest() == 6  # next fresh smallest


def test_add_back_future_number_ignored(make_set):
    sis = make_set()
    assert sis.popSmallest() == 1
    # 10 is already in the infinite set (never popped)
    sis.addBack(10)
    assert sis.popSmallest() == 2
    assert sis.popSmallest() == 3


def test_non_positive_numbers_ignored(make_set):
    sis = make_set()
    sis.addBack(0)
    sis.addBack(-1)
    sis.addBack(-10)
    assert sis.popSmallest() == 1
    assert sis.popSmallest() == 2


def test_reverse_order_add_back(make_set):
    sis = make_set()
    for _ in range(10):
        sis.popSmallest()  # popped 1..10

    # Add back even numbers in descending order: 10, 8, 6, 4, 2
    for x in [10, 8, 6, 4, 2]:
        sis.addBack(x)

    # Must pop in ascending order: 2, 4, 6, 8, 10, followed by fresh 11
    assert [sis.popSmallest() for _ in range(6)] == [2, 4, 6, 8, 10, 11]


def test_large_volume(make_set):
    sis = make_set()
    # Pop 1,000
    for _ in range(1000):
        sis.popSmallest()

    # Add back first 500
    for i in range(1, 501):
        sis.addBack(i)

    # Pops should return 1..500 then 1001..1100
    expected = list(range(1, 501)) + list(range(1001, 1101))
    actual = [sis.popSmallest() for _ in range(600)]
    assert actual == expected


@pytest.mark.parametrize("cls", IMPLS, ids=IDS)
@given(data=st.data())
def test_matches_oracle(cls, data):
    sis = cls()
    oracle = InfiniteSetOracle()

    num_ops = data.draw(st.integers(min_value=10, max_value=80))
    for _ in range(num_ops):
        action = data.draw(st.sampled_from(["pop", "add_back"]))
        if action == "pop":
            actual = sis.popSmallest()
            expected = oracle.popSmallest()
            assert actual == expected
        else:
            val = data.draw(st.integers(min_value=1, max_value=30))
            sis.addBack(val)
            oracle.addBack(val)


@given(data=st.data())
def test_implementations_agree(data):
    s1 = HeapInfiniteSet()
    s2 = HashInfiniteSet()

    num_ops = data.draw(st.integers(min_value=10, max_value=80))
    for _ in range(num_ops):
        action = data.draw(st.sampled_from(["pop", "add_back"]))
        if action == "pop":
            assert s1.popSmallest() == s2.popSmallest()
        else:
            val = data.draw(st.integers(min_value=1, max_value=30))
            s1.addBack(val)
            s2.addBack(val)
