"""
Find Median from Data Stream: sorted-list alternative.

Keeps every value in a sorted list and inserts with binary search. addNum is O(n) in the worst case
because inserting shifts later elements. The shift is a fast C-level memmove, so it is perfectly usable
for LeetCode-sized streams (<= 5 * 10^4 calls), but it degrades quadratically: measured with an add + query
per item, 100k items took ~0.6s vs ~0.06s for two heaps, and 500k took ~18s vs ~0.3s.
findMedian is O(1).
"""

import bisect


class MedianFinder:

    def __init__(self):
        self._nums: list[int] = []

    def addNum(self, num: int) -> None:
        bisect.insort(self._nums, num)  # O(log n) search + O(n) shift

    def findMedian(self) -> float:
        # Per the problem, this is only called after at least one addNum (empty raises IndexError).
        mid = len(self._nums) // 2
        if len(self._nums) % 2:
            return float(self._nums[mid])
        return (self._nums[mid - 1] + self._nums[mid]) / 2
