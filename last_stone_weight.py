"""
Last Stone Weight

You are given an array of integers stones where stones[i] is the weight of the ith
stone. On each turn, we choose the heaviest two stones and smash them together.
Suppose the heaviest two stones have weights x and y with x <= y. If x == y, then
both stones are destroyed. If x != y, then x is destroyed and y loses x weight.
Return the weight of the last remaining stone, or 0 if there are no stones left.
"""

import heapq


def last_stone_weight(stones: list[int]) -> int:
    # heapq is a min-heap, so store negated weights: the smallest value is the heaviest stone.
    heap = [-stone for stone in stones]
    heapq.heapify(heap)  # turns a list into a heap in linear time

    while len(heap) > 1:
        heaviest = heapq.heappop(heap)  # -y
        next_heaviest = heapq.heappop(heap)  # -x, where heaviest <= next_heaviest <= 0
        if heaviest != next_heaviest:
            heapq.heappush(heap, heaviest - next_heaviest)  # -(y - x)

    return -heap[0] if heap else 0
