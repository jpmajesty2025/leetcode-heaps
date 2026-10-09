"""
You have some number of sticks with positive integer lengths. These lengths are given as an array sticks, where
sticks[i] is the length of the ith stick.

You can connect any two sticks of lengths x and y into one stick by paying a cost of x + y. You must connect all
the sticks until there is only one stick remaining.

Return the minimum cost of connecting all the given sticks into one stick in this way.
"""

import heapq


def connect_sticks(sticks: list[int]) -> int:
    heap = list(sticks)  # copy: heapify and the pops below would otherwise destroy the caller's list
    heapq.heapify(heap)  # turns a list into a heap in linear time

    total_cost = 0
    while len(heap) > 1:
        # Greedy (Huffman-style): always merge the two shortest sticks, so short sticks get re-paid the fewest times.
        merged = heapq.heappop(heap) + heapq.heappop(heap)
        total_cost += merged
        heapq.heappush(heap, merged)

    return total_cost
