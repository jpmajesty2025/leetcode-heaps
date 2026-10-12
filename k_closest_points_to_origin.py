"""
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, 
return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
"""

import heapq


def _squared_distance(point: list[int]) -> int:
    """Calculate the squared Euclidean distance from the origin.

    Uses integer multiplication to avoid floating-point inaccuracy and the overhead of pow (** 2).
    """
    x, y = point
    return x * x + y * y


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """Find the k closest points to the origin using a max-heap of size k.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    if not points:
        raise ValueError("points cannot be empty")
    if k <= 0 or k > len(points):
        raise ValueError(
            f"k={k} is out of valid bounds for array of length {len(points)}"
        )

    # Initialize a max-heap with the first k points.
    # Negate the squared distance so Python's min-heap acts as a max-heap:
    # the root will always hold the farthest candidate among the k points.
    heap = [(-_squared_distance(point), point) for point in points[:k]]
    heapq.heapify(heap)

    # For each remaining point, compare with the farthest candidate in the heap.
    # If the new point is closer, evict the farthest and insert the newcomer.
    for point in points[k:]:
        dist = _squared_distance(point)
        if dist < -heap[0][0]:
            heapq.heapreplace(heap, (-dist, point))

    return [point for _, point in heap]
