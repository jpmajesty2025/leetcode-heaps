"""
Kth Largest Element in a Stream: Sorted-List Alternative.

Maintains the top-k elements in a sorted list using binary search insertion (bisect.insort).
For each incoming element, bisect finds the insertion point in O(log k) and inserts it
in O(k) memmove time, popping the smallest if length exceeds k.
"""

import bisect


class KthLargest:
    """Maintains the top-k elements of a stream in a sorted list."""

    def __init__(self, k: int, nums: list[int]):
        """Initialize the object with at most the k largest elements."""
        if k <= 0:
            raise ValueError("k must be a positive integer")

        self.k = k
        sorted_nums = sorted(nums)
        self._nums: list[int] = (
            sorted_nums[-k:] if len(sorted_nums) >= k else sorted_nums
        )

    def add(self, val: int) -> int:
        """Add val to the stream and return the kth largest element."""
        if len(self._nums) < self.k:
            bisect.insort(self._nums, val)
        elif val > self._nums[0]:
            bisect.insort(self._nums, val)
            self._nums.pop(0)

        return self._nums[0]
