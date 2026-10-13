import pytest
from hypothesis import given, strategies as st

from seat_reservation_manager import SeatManager as OptimalSeatManager
from seat_reservation_manager_full_heap import SeatManager as FullHeapSeatManager

IMPLS = [OptimalSeatManager, FullHeapSeatManager]
IDS = ["optimal_pointer", "full_heap"]


class SetOracle:
    """Independent oracle maintaining available seats as an explicit set."""

    def __init__(self, n: int):
        self.available = set(range(1, n + 1))

    def reserve(self) -> int:
        seat = min(self.available)
        self.available.remove(seat)
        return seat

    def unreserve(self, seat: int) -> None:
        self.available.add(seat)


@pytest.fixture(params=IMPLS, ids=IDS)
def make_manager(request):
    return request.param


def test_leetcode_example(make_manager):
    sm = make_manager(5)
    assert sm.reserve() == 1
    assert sm.reserve() == 2
    sm.unreserve(2)
    assert sm.reserve() == 2
    assert sm.reserve() == 3
    assert sm.reserve() == 4
    assert sm.reserve() == 5
    sm.unreserve(5)
    assert sm.reserve() == 5


def test_sequential_reservations(make_manager):
    sm = make_manager(10)
    for expected in range(1, 11):
        assert sm.reserve() == expected


def test_all_seats_exhausted_raises(make_manager):
    sm = make_manager(2)
    assert sm.reserve() == 1
    assert sm.reserve() == 2
    with pytest.raises(RuntimeError):
        sm.reserve()


@pytest.mark.parametrize("n", [0, -1, -10])
def test_invalid_n_raises(make_manager, n):
    with pytest.raises(ValueError):
        make_manager(n)


@pytest.mark.parametrize("bad_seat", [0, -1, 6, 10])
def test_unreserve_out_of_bounds_raises(make_manager, bad_seat):
    sm = make_manager(5)
    sm.reserve()
    with pytest.raises(ValueError):
        sm.unreserve(bad_seat)


def test_unreserve_priority_order(make_manager):
    sm = make_manager(10)
    for _ in range(5):
        sm.reserve()  # seats 1, 2, 3, 4, 5 reserved

    # Unreserve non-consecutively
    sm.unreserve(4)
    sm.unreserve(2)

    # Must pop smallest available first
    assert sm.reserve() == 2
    assert sm.reserve() == 4
    assert sm.reserve() == 6


def test_large_volume(make_manager):
    n = 10_000
    sm = make_manager(n)
    reserved = []

    # Reserve 2000 seats
    for _ in range(2000):
        reserved.append(sm.reserve())
    assert reserved == list(range(1, 2001))

    # Unreserve odd-numbered seats from the first 100
    for s in range(1, 100, 2):
        sm.unreserve(s)

    # Next reserves must be the released odd seats in ascending order
    re_reserved = [sm.reserve() for _ in range(50)]
    assert re_reserved == list(range(1, 100, 2))


@pytest.mark.parametrize("cls", IMPLS, ids=IDS)
@given(
    n=st.integers(min_value=5, max_value=50),
    data=st.data(),
)
def test_matches_set_oracle(cls, n, data):
    sm = cls(n)
    oracle = SetOracle(n)

    currently_reserved = set()
    num_ops = data.draw(st.integers(min_value=5, max_value=60))

    for _ in range(num_ops):
        # Decide whether to reserve or unreserve
        can_reserve = len(currently_reserved) < n
        can_unreserve = len(currently_reserved) > 0

        if can_reserve and can_unreserve:
            action = data.draw(st.sampled_from(["reserve", "unreserve"]))
        elif can_reserve:
            action = "reserve"
        elif can_unreserve:
            action = "unreserve"
        else:
            break

        if action == "reserve":
            actual = sm.reserve()
            expected = oracle.reserve()
            assert actual == expected
            currently_reserved.add(actual)
        else:
            seat_to_release = data.draw(
                st.sampled_from(sorted(list(currently_reserved)))
            )
            sm.unreserve(seat_to_release)
            oracle.unreserve(seat_to_release)
            currently_reserved.remove(seat_to_release)


@given(
    n=st.integers(min_value=5, max_value=50),
    data=st.data(),
)
def test_implementations_agree(n, data):
    sm_opt = OptimalSeatManager(n)
    sm_full = FullHeapSeatManager(n)

    currently_reserved = set()
    num_ops = data.draw(st.integers(min_value=5, max_value=60))

    for _ in range(num_ops):
        can_reserve = len(currently_reserved) < n
        can_unreserve = len(currently_reserved) > 0

        if can_reserve and can_unreserve:
            action = data.draw(st.sampled_from(["reserve", "unreserve"]))
        elif can_reserve:
            action = "reserve"
        else:
            action = "unreserve"

        if action == "reserve":
            s1 = sm_opt.reserve()
            s2 = sm_full.reserve()
            assert s1 == s2
            currently_reserved.add(s1)
        else:
            seat_to_release = data.draw(
                st.sampled_from(sorted(list(currently_reserved)))
            )
            sm_opt.unreserve(seat_to_release)
            sm_full.unreserve(seat_to_release)
            currently_reserved.remove(seat_to_release)
