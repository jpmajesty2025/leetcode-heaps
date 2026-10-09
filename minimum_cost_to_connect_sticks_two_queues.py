"""
Minimum Cost to Connect Sticks: two-queue alternative (no heap).

Sort the sticks once. Merged sticks are produced in non-decreasing order (each merge combines the two
smallest values, and the two smallest only ever grow), so they can be kept in a plain FIFO queue.
The next two smallest sticks are then always at the fronts of the sorted queue and the merged queue.

Time O(n log n) for the sort, then O(n) for the merging; space O(n).
Same asymptotics as the heap, but the merge phase does no heap pushes or pops.
"""

from collections import deque


def connect_sticks(sticks: list[int]) -> int:
    originals = deque(sorted(sticks))  # sorted() copies, so the caller's list is untouched
    merged: deque[int] = deque()

    def pop_smallest() -> int:
        if not merged or (originals and originals[0] <= merged[0]):
            return originals.popleft()
        return merged.popleft()

    total_cost = 0
    for _ in range(len(originals) - 1):  # n sticks need exactly n - 1 merges
        combined = pop_smallest() + pop_smallest()
        total_cost += combined
        merged.append(combined)

    return total_cost
