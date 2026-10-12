"""
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, 
return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
"""

import random


def _squared_distance(point: list[int]) -> int:
    """Calculate the squared Euclidean distance from the origin."""
    x, y = point
    return x * x + y * y


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """Find the k closest points to the origin using randomized 3-way Quickselect.

    Time Complexity: O(n) average, O(n^2) worst-case (astronomically rare with random pivot)
    Space Complexity: O(1) auxiliary space (operates on a copy)
    """
    if not points:
        raise ValueError("points cannot be empty")
    if k <= 0 or k > len(points):
        raise ValueError(
            f"k={k} is out of valid bounds for array of length {len(points)}"
        )

    # Work on a copy so we do not mutate the input array
    arr = [p.copy() for p in points]

    left = 0
    right = len(arr) - 1

    while left <= right:
        pivot_idx = random.randint(left, right)
        pivot_dist = _squared_distance(arr[pivot_idx])

        # 3-way partition (Dutch National Flag) based on squared distance
        lt = left
        gt = right
        i = left

        while i <= gt:
            d = _squared_distance(arr[i])
            if d < pivot_dist:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif d > pivot_dist:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1

        # arr[left..lt-1] has distance < pivot_dist
        # arr[lt..gt] has distance == pivot_dist
        # arr[gt+1..right] has distance > pivot_dist
        if k < lt:
            right = lt - 1
        elif k > gt + 1:
            left = gt + 1
        else:
            return arr[:k]

    return arr[:k]
