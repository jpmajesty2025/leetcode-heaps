"""
Minimum Operations to Make Subarray Elements Equal: sliding window over Fenwick trees.

Same idea as the heap version (cost of a window = sum(|x - median|), windows taken in the ORIGINAL order),
but the window lives in two Fenwick (binary indexed) trees over coordinate-compressed values: one counting
elements, one summing them. That gives the median by binary descent and the sum of everything <= median by a
prefix query, with no lazy deletion and no rebalancing.

Time O(n log n), space O(n).
"""


class _Fenwick:
    def __init__(self, size: int) -> None:
        self._size = size
        self._counts = [0] * (size + 1)
        self._sums = [0] * (size + 1)

    def update(self, rank: int, value: int, delta: int) -> None:
        while rank <= self._size:
            self._counts[rank] += delta
            self._sums[rank] += delta * value
            rank += rank & -rank

    def prefix(self, rank: int) -> tuple[int, int]:
        """(count, sum) of all live elements with rank <= `rank`."""
        count = total = 0
        while rank > 0:
            count += self._counts[rank]
            total += self._sums[rank]
            rank -= rank & -rank
        return count, total

    def kth_rank(self, kth: int) -> int:
        """Smallest rank whose prefix count reaches `kth` (1-based), by binary descent."""
        position = 0
        step = 1 << self._size.bit_length()
        while step:
            nxt = position + step
            if nxt <= self._size and self._counts[nxt] < kth:
                position = nxt
                kth -= self._counts[nxt]
            step >>= 1
        return position + 1


def min_operations(nums: list[int], k: int) -> int:
    if not 1 <= k <= len(nums):
        raise ValueError("k must satisfy 1 <= k <= len(nums)")

    values = sorted(set(nums))
    rank_of = {value: rank for rank, value in enumerate(values, start=1)}
    tree = _Fenwick(len(values))

    window_sum = 0
    best = None
    for i, value in enumerate(nums):
        tree.update(rank_of[value], value, +1)
        window_sum += value
        if i >= k:
            old = nums[i - k]
            tree.update(rank_of[old], old, -1)
            window_sum -= old
        if i >= k - 1:
            median_rank = tree.kth_rank((k + 1) // 2)
            median = values[median_rank - 1]
            count_low, sum_low = tree.prefix(median_rank)  # elements <= median
            cost = (median * count_low - sum_low) + ((window_sum - sum_low) - median * (k - count_low))
            best = cost if best is None else min(best, cost)
    return best
