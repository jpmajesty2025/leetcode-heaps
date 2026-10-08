"""
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value,
and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far. Answers within 10-5 of the actual answer will be accepted.
"""

import heapq


class MedianFinder:
    """Two heaps: a max-heap for the lower half and a min-heap for the upper half.

    Invariants (hold between calls):
      * every value in `_low` <= every value in `_high`
      * len(_low) == len(_high) or len(_low) == len(_high) + 1

    So the median is always at one or both heap tops. As in the other heap problems, heapq is a
    min-heap, so `_low` stores negated values.
    """

    def __init__(self):
        self._low: list[int] = []  # max-heap of the smaller half (negated values)
        self._high: list[int] = []  # min-heap of the larger half

    def addNum(self, num: int) -> None:
        # Route num through the lower half so the halves stay correctly ordered,
        # then hand that half's maximum to the upper half.
        largest_of_low = -heapq.heappushpop(self._low, -num)
        heapq.heappush(self._high, largest_of_low)

        # Rebalance: the lower half may hold at most one more element than the upper half.
        if len(self._high) > len(self._low):
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def findMedian(self) -> float:
        # Per the problem, this is only called after at least one addNum (empty raises IndexError).
        if len(self._low) > len(self._high):
            return float(-self._low[0])
        return (-self._low[0] + self._high[0]) / 2
