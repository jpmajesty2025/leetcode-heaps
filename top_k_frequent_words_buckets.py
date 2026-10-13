"""
Top K Frequent Words: bucket-sort alternative (no heap).

Frequencies live in the range 1..n. Put each distinct word in the bucket for its frequency,
sort each bucket lexicographically (to handle ties), and collect words from the highest frequency
bucket down until k words are accumulated.

Time Complexity: O(n + sum(b_len log b_len))
Space Complexity: O(n)
"""

from collections import Counter


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """Return the k most frequent words using frequency buckets and lexicographical sorting."""
    if k <= 0 or not words:
        return []

    counts = Counter(words)
    k = min(k, len(counts))

    # Size buckets by the highest frequency actually present
    max_freq = max(counts.values())
    buckets: list[list[str]] = [[] for _ in range(max_freq + 1)]

    for word, freq in counts.items():
        buckets[freq].append(word)

    result: list[str] = []
    for freq in range(max_freq, 0, -1):
        if not buckets[freq]:
            continue

        # Sort words in the same frequency bucket alphabetically
        buckets[freq].sort()

        for word in buckets[freq]:
            result.append(word)
            if len(result) == k:
                return result

    return result
