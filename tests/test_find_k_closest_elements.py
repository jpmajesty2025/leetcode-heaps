import pytest
from hypothesis import given, strategies as st

from find_k_closest_elements import find_closest_elements as heap_solution
from find_k_closest_elements_binary_search import find_closest_elements as binary_solution

IMPLS = [heap_solution, binary_solution]
IDS = ["heap", "binary_search"]


def oracle(arr: list[int], k: int, x: int) -> list[int]:
    """Rank everything by (distance, value), take k, then sort: encodes the 'prefer smaller' tie-break."""
    if k <= 0:
        return []
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "arr, k, x, expected",
    [
        ([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]),  # LeetCode example 1
        ([1, 1, 2, 3, 4, 5], 4, -1, [1, 1, 2, 3]),  # LeetCode example 2
        ([1, 2, 3, 4, 5], 4, 4, [2, 3, 4, 5]),
        ([1, 3], 1, 2, [1]),  # tie: prefer the smaller element
        ([1, 2, 3, 4, 5], 2, 3, [2, 3]),  # x present
        ([1, 2, 3, 4, 5], 2, 100, [4, 5]),  # x beyond the right end
        ([1, 2, 3, 4, 5], 2, -100, [1, 2]),  # x beyond the left end
        ([5], 1, 5, [5]),
        ([1, 2, 3], 3, 2, [1, 2, 3]),  # k == len(arr)
        ([1, 2, 3], 10, 2, [1, 2, 3]),  # k > len(arr)
        ([1, 2, 3], 0, 2, []),
        ([], 3, 5, []),
        ([-5, -3, 0, 4], 2, -1, [-3, 0]),  # negatives: distances to -1 are 4, 2, 1, 5
        ([0, 0, 1, 2, 3, 3, 4, 7, 7, 8], 3, 5, [3, 3, 4]),  # duplicates; 3, 3 and 7 tie at distance 2, smaller wins
        ([1, 1, 1, 10, 10, 10], 2, 5, [1, 1]),  # equidistant groups, smaller side wins
        ([1, 10, 15, 25, 35, 45, 50, 59], 1, 30, [25]),  # LeetCode tie-break regression
    ],
)
def test_examples(solve, arr, k, x, expected):
    assert solve(arr, k, x) == expected


def test_tie_prefers_smaller_elements(solve):
    # 2 and 4 are equally far from 3; the smaller one must win.
    assert solve([2, 4], 1, 3) == [2]
    assert solve([1, 2, 4, 5], 2, 3) == [2, 4]


def test_result_is_sorted(solve):
    result = solve([1, 4, 6, 8, 10, 12], 4, 7)
    assert result == sorted(result)


def test_does_not_mutate_input(solve):
    arr = [1, 2, 3, 4, 5]
    solve(arr, 3, 3)
    assert arr == [1, 2, 3, 4, 5]


def test_result_is_a_new_list(solve):
    arr = [1, 2, 3]
    result = solve(arr, 3, 2)
    result.append(99)
    assert arr == [1, 2, 3]


def test_large_input(solve):
    arr = list(range(0, 2_000_000, 2))
    # Distances from 1_000_001: 1, 1, 3, 3, then a 5-vs-5 tie that goes to the smaller element, 999_996.
    expected = [999_996, 999_998, 1_000_000, 1_000_002, 1_000_004]
    assert solve(arr, 5, 1_000_001) == expected


sorted_lists = st.lists(st.integers(min_value=-50, max_value=50), max_size=30).map(sorted)
dup_lists = st.lists(st.integers(min_value=0, max_value=6), max_size=30).map(sorted)
k_strategy = st.integers(min_value=-1, max_value=35)
x_strategy = st.integers(min_value=-60, max_value=60)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize("strategy", [sorted_lists, dup_lists], ids=["wide", "duplicates"])
def test_matches_oracle(fn, strategy):
    @given(arr=strategy, k=k_strategy, x=x_strategy)
    def check(arr, k, x):
        assert fn(arr, k, x) == oracle(arr, k, x)

    check()


@given(arr=sorted_lists, k=k_strategy, x=x_strategy)
def test_implementations_agree(arr, k, x):
    assert heap_solution(arr, k, x) == binary_solution(arr, k, x)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(arr=sorted_lists, k=st.integers(min_value=1, max_value=35), x=x_strategy)
def test_result_is_contiguous_window_of_arr(fn, arr, k, x):
    result = fn(arr, k, x)
    assert len(result) == min(k, len(arr))
    starts = [i for i in range(len(arr) - len(result) + 1) if arr[i : i + len(result)] == result]
    assert starts, "result must appear as a contiguous slice of arr"


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(arr=sorted_lists, k=st.integers(min_value=1, max_value=35), x=x_strategy, shift=st.integers(-100, 100))
def test_shift_invariance(fn, arr, k, x, shift):
    shifted = fn([v + shift for v in arr], k, x + shift)
    assert shifted == [v + shift for v in fn(arr, k, x)]


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(arr=sorted_lists, k=st.integers(min_value=1, max_value=35), x=x_strategy)
def test_no_excluded_element_is_closer_than_an_included_one(fn, arr, k, x):
    result = fn(arr, k, x)
    if not result:
        return
    worst_included = max(abs(v - x) for v in result)
    remaining = list(arr)
    for v in result:
        remaining.remove(v)
    assert all(abs(v - x) >= worst_included for v in remaining)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(arr=sorted_lists, k=k_strategy, x=x_strategy)
def test_input_unchanged(fn, arr, k, x):
    original = list(arr)
    fn(arr, k, x)
    assert arr == original
