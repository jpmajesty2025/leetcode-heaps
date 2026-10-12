"""
You are part of a university admissions office and need to keep track of the kth highest test score from 
applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically 
as new applicants submit their scores.

You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and 
continuously returns the kth highest test score after a new score has been submitted. More specifically, 
we are looking for the kth highest score in the sorted list of all scores.

Implement the KthLargest class:

KthLargest(int k, int[] nums) Initializes the object with the integer k and the stream of test scores nums.
int add(int val) Adds a new test score val to the stream and returns the element representing the kth largest 
element in the pool of test scores so far.
"""

import heapq


class KthLargest:
    """Maintains the kth largest element of a growing stream using a min-heap capped at size k.

    Invariants:
      * len(self._min_heap) <= k
      * When len(self._min_heap) == k, self._min_heap[0] is the kth largest element seen so far.
      * Every element in self._min_heap is >= self._min_heap[0].
    """

    def __init__(self, k: int, nums: list[int]):
        """Initialize the KthLargest object with a min-heap of size at most k.

        Time Complexity: O(n log k) (O(k) heapify + fast filtering for remaining elements)
        Space Complexity: O(k) auxiliary space
        """
        if k <= 0:
            raise ValueError("k must be a positive integer")

        self.k = k

        # Initialize heap with at most k elements
        if len(nums) <= k:
            self._min_heap = nums.copy()
            heapq.heapify(self._min_heap)
        else:
            self._min_heap = nums[:k].copy()
            heapq.heapify(self._min_heap)
            for num in nums[k:]:
                if num > self._min_heap[0]:
                    heapq.heapreplace(self._min_heap, num)

    def add(self, val: int) -> int:
        """Add a new score to the stream and return the kth largest score so far.

        Time Complexity: O(log k) when inserted or replaced; O(1) when val <= cutoff
        Space Complexity: O(k)
        """
        if len(self._min_heap) < self.k:
            heapq.heappush(self._min_heap, val)
        elif val > self._min_heap[0]:
            heapq.heapreplace(self._min_heap, val)

        return self._min_heap[0]
