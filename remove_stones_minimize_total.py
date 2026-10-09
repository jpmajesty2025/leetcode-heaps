"""
You are given a 0-indexed integer array piles, where piles[i] represents the number of stones in the ith pile, and an
integer k. You should apply the following operation exactly k times:

Choose any piles[i] and remove floor(piles[i] / 2) stones from it.
Notice that you can apply the operation on the same pile more than once.

Return the minimum possible total number of stones remaining after applying the k operations.
"""

import heapq


def min_stone_sum(piles: list[int], k: int) -> int:
    # heapq is a min-heap, so store negated values: the smallest entry is the largest pile.
    heap = [-pile for pile in piles]
    heapq.heapify(heap)  # turns a list into a heap in linear time

    for _ in range(k):
        largest = -heapq.heappop(heap)
        if largest == 1:  # floor(1 / 2) == 0: no pile can shrink any further
            heapq.heappush(heap, -largest)
            break
        # Removing floor(p / 2) leaves ceil(p / 2); stays an exact int.
        heapq.heappush(heap, -(largest - largest // 2))

    return -sum(heap)
