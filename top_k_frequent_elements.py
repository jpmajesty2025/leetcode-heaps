'''
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer 
in any order.
'''

from collections import Counter
import heapq


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    heap = []
    
    for key, val in counts.items():
        heapq.heappush(heap, (val, key))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [pair[1] for pair in heap]