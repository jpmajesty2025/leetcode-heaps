"""
Given an array of strings words and an integer k, return the k most frequent strings.

Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by 
their lexicographical order.

Follow-up: Could you solve it in O(n log k) time and O(n) extra space?
"""

from collections import Counter
import heapq


class _WordEntry:
    """Wrapper for heap elements to enforce compound tie-breaking.

    In a min-heap capped at size k, the root represents the weakest candidate to evict:
    1. Lower frequency has higher eviction priority (smaller in min-heap).
    2. For equal frequencies, lexicographically LARGER words have higher eviction priority
       (since lexicographically smaller words are preferred).
    """

    __slots__ = ("freq", "word")

    def __init__(self, freq: int, word: str):
        self.freq = freq
        self.word = word

    def __lt__(self, other: "_WordEntry") -> bool:
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.word > other.word


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """Return the k most frequent words sorted by frequency (desc) and lexicographical order (asc).

    Time Complexity: O(n + m log k) where n = len(words), m = unique words
    Space Complexity: O(m + k)
    """
    if k <= 0 or not words:
        return []

    counts = Counter(words)
    k = min(k, len(counts))

    heap: list[_WordEntry] = []
    for word, freq in counts.items():
        entry = _WordEntry(freq, word)
        if len(heap) < k:
            heapq.heappush(heap, entry)
        elif heap[0] < entry:
            heapq.heapreplace(heap, entry)

    # Pop elements from min-heap (weakest to strongest) and reverse to get highest-to-lowest order
    result: list[str] = []
    while heap:
        result.append(heapq.heappop(heap).word)

    return result[::-1]
