"""
Given a string s and an integer k, rearrange s such that the same characters are at least distance k from each 
other. If it is not possible to rearrange the string, return an empty string "".
"""

from collections import Counter, deque
import heapq


def rearrange_string(s: str, k: int) -> str:
    """Rearrange s so that identical characters are at least distance k apart.

    Algorithm: Max-Heap + Sliding Cooldown Deque
    1. Count character frequencies.
    2. Maintain a max-heap of currently available characters (ordered by frequency).
    3. Maintain a FIFO cooldown queue of size up to k:
       - When a character is placed, decrement its count and enqueue it into `cooldown`.
       - When `len(cooldown) == k`, the front character has satisfied the distance-k requirement.
         If it still has remaining counts, return it to the max-heap.
    4. If the max-heap is exhausted before all characters are placed, it is impossible; return "".

    Time Complexity: O(n log |Σ|) where |Σ| is the number of distinct characters
    Space Complexity: O(|Σ| + k)
    """
    if k < 0:
        raise ValueError("k must be a non-negative integer")
    if k <= 1 or not s:
        return s

    counts = Counter(s)
    # Max-heap based on remaining count: (-count, char)
    max_heap = [(-count, char) for char, count in counts.items()]
    heapq.heapify(max_heap)

    cooldown: deque[tuple[str, int]] = deque()
    result: list[str] = []

    while max_heap:
        neg_count, char = heapq.heappop(max_heap)
        result.append(char)
        remaining = -neg_count - 1

        cooldown.append((char, remaining))

        # Once the cooldown queue reaches size k, the oldest character is ready to be reused
        if len(cooldown) == k:
            ready_char, ready_count = cooldown.popleft()
            if ready_count > 0:
                heapq.heappush(max_heap, (-ready_count, ready_char))

    return "".join(result) if len(result) == len(s) else ""
