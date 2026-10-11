"""
Top K Frequent Elements: bucket-sort alternative (no heap).

A value can appear at most len(nums) times, so frequencies live in the small range 1..n. Put each
distinct value in the bucket for its frequency, then read the buckets from the highest frequency down
until k values have been collected.

Time O(n), space O(n). The heap version is O(n + m log k) for m distinct values.
"""

from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    if k <= 0:
        return []

    counts = Counter(nums)
    if not counts:
        return []

    # Size the array by the highest frequency actually present, not by len(nums):
    # allocating n + 1 empty lists would dominate the runtime when counts are small.
    buckets: list[list[int]] = [[] for _ in range(max(counts.values()) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)

    result: list[int] = []
    for count in range(len(buckets) - 1, 0, -1):
        for value in buckets[count]:
            result.append(value)
            if len(result) == k:
                return result
    return result  # fewer than k distinct values: return them all
