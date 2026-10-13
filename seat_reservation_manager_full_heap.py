"""
Seat Reservation Manager: Full Min-Heap Alternative.

Initializes all n seats into a min-heap upfront. Each reserve pops the minimum
available seat in O(log n), and each unreserve pushes the released seat in O(log n).

Time Complexity: O(n) initialization, O(log n) reserve, O(log n) unreserve
Space Complexity: O(n)
"""

import heapq


class SeatManager:
    """Manages seat reservations by storing all available seats in a single min-heap."""

    def __init__(self, n: int):
        """Initialize all n seats into a min-heap.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if n <= 0:
            raise ValueError("n must be a positive integer")

        self._n = n
        self._available_heap = list(range(1, n + 1))
        # Already sorted list is already a valid min-heap, but heapify guarantees heap structure
        heapq.heapify(self._available_heap)

    def reserve(self) -> int:
        """Fetch the smallest-numbered unreserved seat, reserve it, and return its number.

        Time Complexity: O(log n)
        """
        if not self._available_heap:
            raise RuntimeError("All seats are currently reserved")
        return heapq.heappop(self._available_heap)

    def unreserve(self, seatNumber: int) -> None:
        """Unreserve the seat with the given seatNumber.

        Time Complexity: O(log n)
        """
        if seatNumber < 1 or seatNumber > self._n:
            raise ValueError(
                f"seatNumber={seatNumber} is out of bounds for [1, {self._n}]"
            )
        heapq.heappush(self._available_heap, seatNumber)
