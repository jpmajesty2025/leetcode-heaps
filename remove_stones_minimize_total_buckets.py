"""
Remove Stones to Minimize the Total: counting-bucket alternative.

Instead of a heap, keep counts[size] = number of piles with exactly that many stones and sweep the sizes
from largest to smallest. A halved pile always lands in a strictly smaller bucket (ceil(p / 2) < p for
p >= 2), so the largest size only ever moves down and each bucket can be processed in bulk.

Time O(n + M) where M = max(piles); space O(M). Beats the heap when M is small relative to n * log n,
but depends on the value range, which the heap does not.
"""


def min_stone_sum(piles: list[int], k: int) -> int:
    if not piles:
        return 0

    counts = [0] * (max(piles) + 1)
    for pile in piles:
        counts[pile] += 1

    # Size 1 cannot shrink (floor(1 / 2) == 0), so the sweep stops at 2.
    for size in range(len(counts) - 1, 1, -1):
        if k == 0:
            break
        moved = min(counts[size], k)  # halve as many piles of this size as the budget allows
        counts[size] -= moved
        counts[size - size // 2] += moved  # ceil(size / 2), always a smaller bucket
        k -= moved

    return sum(size * count for size, count in enumerate(counts))
