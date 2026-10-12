from collections import Counter
import random
import pytest
from hypothesis import given, strategies as st

from k_closest_points_to_origin import k_closest as heap_solution
from k_closest_points_to_origin_quickselect import k_closest as quickselect_solution

IMPLS = [heap_solution, quickselect_solution]
IDS = ["heap", "quickselect"]


def dist_sq(point: list[int]) -> int:
    return point[0] * point[0] + point[1] * point[1]


def oracle_distances(points: list[list[int]], k: int) -> list[int]:
    """Returns the sorted squared distances of the true k closest points."""
    return sorted(dist_sq(p) for p in points)[:k]


def assert_valid_k_closest(
    points: list[list[int]], k: int, result: list[list[int]]
) -> None:
    """Verify result is a valid set of k closest points (order independent)."""
    assert len(result) == k, f"Expected {k} points, got {len(result)}"

    result_dists = sorted(dist_sq(p) for p in result)
    expected_dists = oracle_distances(points, k)
    assert (
        result_dists == expected_dists
    ), f"Distances do not match: {result_dists} vs {expected_dists}"

    # Verify every element in result was drawn from points
    input_counts = Counter(tuple(p) for p in points)
    result_counts = Counter(tuple(p) for p in result)
    for pt, count in result_counts.items():
        assert (
            count <= input_counts[pt]
        ), f"Point {pt} appeared {count} times in result, but only {input_counts[pt]} in input"


@pytest.fixture(params=IMPLS, ids=IDS)
def solve(request):
    return request.param


@pytest.mark.parametrize(
    "points, k, expected_dists",
    [
        ([[1, 3], [-2, 2]], 1, [8]),  # LeetCode example 1
        ([[3, 3], [5, -1], [-2, 4]], 2, [18, 20]),  # LeetCode example 2
        ([[0, 0]], 1, [0]),  # Origin singleton
        ([[0, 0], [1, 1], [-1, -1]], 1, [0]),
        ([[-5, -4], [-2, -1], [-1, 0]], 2, [1, 5]),  # Negatives
        ([[1, 0], [0, 1], [-1, 0], [0, -1]], 2, [1, 1]),  # Circle of ties
        ([[2, 3], [1, 1]], 2, [2, 13]),  # k == len(points)
        ([[10**4, 10**4], [0, 1]], 1, [1]),  # Constraint extremes
        ([[7, 7], [7, 7], [1, 1]], 1, [2]),  # Duplicates
        ([[7, 7], [7, 7], [1, 1]], 2, [2, 98]),
    ],
)
def test_examples(solve, points, k, expected_dists):
    result = solve(points, k)
    assert sorted(dist_sq(p) for p in result) == expected_dists


def test_returns_list_of_lists(solve):
    result = solve([[1, 3], [-2, 2]], 1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], list)
    assert len(result[0]) == 2


@pytest.mark.parametrize("k", [0, -1, -5])
def test_non_positive_k_raises(solve, k):
    with pytest.raises(ValueError):
        solve([[1, 1], [2, 2]], k)


def test_k_greater_than_length_raises(solve):
    with pytest.raises(ValueError):
        solve([[1, 1], [2, 2]], 3)


def test_empty_points_raises(solve):
    with pytest.raises(ValueError):
        solve([], 1)


def test_does_not_mutate_input(solve):
    original = [[1, 3], [-2, 2], [3, 1], [-1, -1]]
    points = [p.copy() for p in original]
    solve(points, 2)
    assert points == original


def test_large_input(solve):
    # 50_000 points far away, 5 points close to origin
    far_points = [[1000 + i, 1000 + i] for i in range(50_000)]
    close_points = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1]]
    points = far_points + close_points
    result = solve(points, 5)
    assert sorted(dist_sq(p) for p in result) == [1, 1, 1, 1, 2]


point_strategy = st.lists(
    st.integers(min_value=-(10**4), max_value=10**4),
    min_size=2,
    max_size=2,
)

points_strategy = st.lists(point_strategy, min_size=1, max_size=50)

# Duplicate-heavy strategy for ties
small_point_strategy = st.lists(
    st.integers(min_value=-3, max_value=3),
    min_size=2,
    max_size=2,
)
dup_points_strategy = st.lists(small_point_strategy, min_size=1, max_size=50)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@pytest.mark.parametrize(
    "strategy", [points_strategy, dup_points_strategy], ids=["wide", "duplicates"]
)
def test_matches_oracle(fn, strategy):
    @given(points=strategy, data=st.data())
    def check(points, data):
        k = data.draw(st.integers(min_value=1, max_value=len(points)))
        result = fn(points, k)
        assert_valid_k_closest(points, k, result)

    check()


@given(points=points_strategy, data=st.data())
def test_implementations_agree_on_distances(points, data):
    k = data.draw(st.integers(min_value=1, max_value=len(points)))
    heap_dists = sorted(dist_sq(p) for p in heap_solution(points, k))
    qs_dists = sorted(dist_sq(p) for p in quickselect_solution(points, k))
    assert heap_dists == qs_dists


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(points=points_strategy, data=st.data())
def test_no_excluded_point_is_closer_than_included_point(fn, points, data):
    k = data.draw(st.integers(min_value=1, max_value=len(points)))
    result = fn(points, k)
    if k == len(points):
        return

    result_dists = [dist_sq(p) for p in result]
    max_included_dist = max(result_dists)

    # Count frequencies of points to identify excluded points
    input_counts = Counter(tuple(p) for p in points)
    result_counts = Counter(tuple(p) for p in result)
    excluded_counts = input_counts - result_counts

    for pt_tuple in excluded_counts:
        pt_dist = pt_tuple[0] * pt_tuple[0] + pt_tuple[1] * pt_tuple[1]
        assert (
            pt_dist >= max_included_dist
        ), f"Excluded point {pt_tuple} with dist {pt_dist} is strictly closer than max included {max_included_dist}"


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(points=points_strategy, data=st.data(), seed=st.integers(min_value=0, max_value=1000))
def test_order_invariance(fn, points, data, seed):
    k = data.draw(st.integers(min_value=1, max_value=len(points)))
    shuffled = [p.copy() for p in points]
    random.Random(seed).shuffle(shuffled)
    r1 = fn(points, k)
    r2 = fn(shuffled, k)
    assert sorted(dist_sq(p) for p in r1) == sorted(dist_sq(p) for p in r2)


@pytest.mark.parametrize("fn", IMPLS, ids=IDS)
@given(points=points_strategy, data=st.data())
def test_reflection_invariance(fn, points, data):
    """Reflecting points across origin preserves distances."""
    k = data.draw(st.integers(min_value=1, max_value=len(points)))
    reflected = [[-p[0], -p[1]] for p in points]
    r1 = fn(points, k)
    r2 = fn(reflected, k)
    assert sorted(dist_sq(p) for p in r1) == sorted(dist_sq(p) for p in r2)
