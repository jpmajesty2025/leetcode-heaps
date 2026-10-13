"""
Design a system that manages the reservation state of n seats that are numbered from 1 to n.

Implement the SeatManager class:

SeatManager(int n) Initializes a SeatManager object that will manage n seats numbered from 1 to n. 
All seats are initially available.
int reserve() Fetches the smallest-numbered unreserved seat, reserves it, and returns its number.
void unreserve(int seatNumber) Unreserves the seat with the given seatNumber.
"""

import heapq


class SeatManager:
    """Manages seat reservations using a high-water mark pointer and a min-heap for released seats.

    Instead of pre-allocating all n seats into a heap at O(n) initialization cost,
    we use a single pointer `_marker` for fresh seats (1 to n) and only maintain a min-heap
    for seats that have been reserved and subsequently unreserved.

    Invariants:
      * Every seat in `_available_heap` is < `_marker` and is currently unreserved.
      * Every seat from `_marker` to `_n` has never been reserved yet.
      * The overall smallest available seat is `min(_available_heap[0], _marker)`.
    """

    def __init__(self, n: int):
        """Initialize the SeatManager object to manage n seats numbered from 1 to n.

        Time Complexity: O(1)
        Space Complexity: O(1) initial space (O(k) where k is the number of unreserved seats)
        """
        if n <= 0:
            raise ValueError("n must be a positive integer")

        self._n = n
        self._marker = 1
        self._available_heap: list[int] = []

    def reserve(self) -> int:
        """Fetch the smallest-numbered unreserved seat, reserve it, and return its number.

        Time Complexity: O(log k) if reusing an unreserved seat, O(1) if allocating a fresh seat
        """
        if self._available_heap:
            return heapq.heappop(self._available_heap)

        if self._marker > self._n:
            raise RuntimeError("All seats are currently reserved")

        seat = self._marker
        self._marker += 1
        return seat

    def unreserve(self, seatNumber: int) -> None:
        """Unreserve the seat with the given seatNumber.

        Time Complexity: O(log k) where k is the number of unreserved seats
        """
        if seatNumber < 1 or seatNumber > self._n:
            raise ValueError(
                f"seatNumber={seatNumber} is out of bounds for [1, {self._n}]"
            )
        if seatNumber >= self._marker:
            raise ValueError(
                f"seatNumber={seatNumber} was never reserved"
            )

        heapq.heappush(self._available_heap, seatNumber)
