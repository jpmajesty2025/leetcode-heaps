"""
Minimum Operations to Make Subarray Elements Equal: sliding-window median with two heaps.

For a window, the cheapest common value is its median (it minimizes the sum of absolute differences),
so the cost of a window is  sum(|x - median|).  Slide a window of size k across the ORIGINAL order
(a subarray is contiguous, so the array must not be sorted) and keep the minimum cost.

Time O(n log n), space O(n).
"""

import heapq
from collections import Counter


class _MedianWindow:
    """Sliding multiset that reports the cost of making every element equal to its median.

    Two heaps hold the window split around the median: `_low` (max-heap, stored negated, holds the
    lower half including the median) and `_high` (min-heap, upper half). Removals are lazy: a value is
    recorded in `_pending` and physically popped only when it reaches a heap top. `_low_size`/`_high_size`
    and the sums count only live elements.
    """

    def __init__(self) -> None:
        self._low: list[int] = []
        self._high: list[int] = []
        self._pending: Counter[int] = Counter()
        self._low_size = self._high_size = 0
        self._low_sum = self._high_sum = 0

    def add(self, value: int) -> None:
        if self._low and value > -self._low[0]:
            self._push_high(value)
        else:
            self._push_low(value)
        self._rebalance()

    def remove(self, value: int) -> None:
        self._pending[value] += 1
        if value <= -self._low[0]:
            self._low_size -= 1
            self._low_sum -= value
        else:
            self._high_size -= 1
            self._high_sum -= value
        self._rebalance()

    def cost(self) -> int:
        median = -self._low[0]
        return (median * self._low_size - self._low_sum) + (self._high_sum - median * self._high_size)

    def _push_low(self, value: int) -> None:
        heapq.heappush(self._low, -value)
        self._low_size += 1
        self._low_sum += value

    def _push_high(self, value: int) -> None:
        heapq.heappush(self._high, value)
        self._high_size += 1
        self._high_sum += value

    def _rebalance(self) -> None:
        # Keep len(low) == len(high) or len(low) == len(high) + 1.
        self._prune()
        if self._low_size > self._high_size + 1:
            moved = -heapq.heappop(self._low)
            self._low_size -= 1
            self._low_sum -= moved
            self._push_high(moved)
        elif self._low_size < self._high_size:
            moved = heapq.heappop(self._high)
            self._high_size -= 1
            self._high_sum -= moved
            self._push_low(moved)
        self._prune()

    def _prune(self) -> None:
        # Discard lazily-deleted values that have surfaced at either heap top.
        while self._low and self._pending[-self._low[0]] > 0:
            self._pending[-self._low[0]] -= 1
            heapq.heappop(self._low)
        while self._high and self._pending[self._high[0]] > 0:
            self._pending[self._high[0]] -= 1
            heapq.heappop(self._high)


def min_operations(nums: list[int], k: int) -> int:
    if not 1 <= k <= len(nums):
        raise ValueError("k must satisfy 1 <= k <= len(nums)")

    window = _MedianWindow()
    best = None
    for i, value in enumerate(nums):
        window.add(value)
        if i >= k:
            window.remove(nums[i - k])
        if i >= k - 1:
            cost = window.cost()
            best = cost if best is None else min(best, cost)
    return best
