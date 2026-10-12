"""
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?
"""

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    """Find the kth largest element in nums using a min-heap of size k.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    if not nums:
        raise ValueError("nums cannot be empty")
    if k <= 0 or k > len(nums):
        raise ValueError(
            f"k={k} is out of valid bounds for array of length {len(nums)}"
        )

    # Initialize a min-heap with the first k elements
    heap = nums[:k].copy()
    heapq.heapify(heap)

    # For each remaining element, maintain the k largest seen so far.
    # If the element is larger than the smallest in the heap, replace it.
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]
