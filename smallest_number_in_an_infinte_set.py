"""
You have a set which contains all positive integers [1, 2, 3, 4, 5, ...].

Implement the SmallestInfiniteSet class:

SmallestInfiniteSet() Initializes the SmallestInfiniteSet object to contain all positive integers.
int popSmallest() Removes and returns the smallest integer contained in the infinite set.
void addBack(int num) Adds a positive integer num back into the infinite set, if it is not already in the 
infinite set.
"""

import heapq


class SmallestInfiniteSet:
    """Maintains an infinite set of positive integers using a frontier pointer, min-heap, and hash set.

    Invariants:
      * Every integer >= self._current is implicitly in the set and has never been popped.
      * Numbers < self._current that have been added back are stored in `self._heap` and `self._in_heap`.
      * `self._in_heap` ensures no duplicates enter `self._heap`.
      * The globally smallest available integer is `self._heap[0]` if `self._heap` else `self._current`.
    """

    def __init__(self):
        """Initialize the SmallestInfiniteSet to contain all positive integers [1, 2, 3, ...].

        Time Complexity: O(1)
        Space Complexity: O(1) initial space (O(k) where k is the count of added-back numbers)
        """
        self._current: int = 1
        self._heap: list[int] = []
        self._in_heap: set[int] = set()

    def popSmallest(self) -> int:
        """Remove and return the smallest integer currently contained in the infinite set.

        Time Complexity: O(log k) if popping a previously added-back number; O(1) if taking from the frontier
        """
        if self._heap:
            num = heapq.heappop(self._heap)
            self._in_heap.remove(num)
            return num

        num = self._current
        self._current += 1
        return num

    def addBack(self, num: int) -> None:
        """Add a positive integer num back into the infinite set if it is not already present.

        Time Complexity: O(log k)
        """
        if num <= 0:
            return

        # Only numbers strictly less than _current can be missing from the set
        if num < self._current and num not in self._in_heap:
            heapq.heappush(self._heap, num)
            self._in_heap.add(num)
