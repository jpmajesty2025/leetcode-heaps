"""
You are given an array nums of positive integers. In one operation, you can choose any number from nums and reduce it to
exactly half the number. (Note that you may choose this reduced number in future operations.)

Return the minimum number of operations to reduce the sum of nums by at least half.
"""

import heapq


def halve_array(nums: list[int]) -> int:
    current_sum: float = sum(nums)
    target_sum = current_sum / 2

    # heapq is a min-heap, so store negated values: the smallest entry is the largest number.
    # Typed as float because halved values are no longer ints (halving is exact in binary floating point).
    heap: list[float] = [-num for num in nums]
    heapq.heapify(heap)  # turns a list into a heap in linear time

    operations = 0
    while current_sum > target_sum:
        halved = -heapq.heappop(heap) / 2
        current_sum -= halved  # halving x removes exactly x / 2 from the sum
        heapq.heappush(heap, -halved)
        operations += 1

    return operations
