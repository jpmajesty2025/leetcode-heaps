"""
Rearrange String k Distance Apart: Frequency Table Cooldown Alternative.

Maintains remaining frequencies and last seen positions for each character.
At each position from 0 to n - 1, scans the alphabet to find the character with the
maximum remaining frequency whose last used position is at least k steps away.

Time Complexity: O(n * |Σ|) where |Σ| is the alphabet size
Space Complexity: O(|Σ|)
"""

from collections import Counter


def rearrange_string(s: str, k: int) -> str:
    """Rearrange s using an O(n * |Σ|) frequency table scan."""
    if k < 0:
        raise ValueError("k must be a non-negative integer")
    if k <= 1 or not s:
        return s

    counts = Counter(s)
    distinct = list(counts.keys())
    last_pos: dict[str, int] = {char: -k for char in distinct}
    result: list[str] = []
    n = len(s)

    for pos in range(n):
        best_char = None
        best_count = -1

        for char in distinct:
            if counts[char] > best_count and pos - last_pos[char] >= k:
                best_count = counts[char]
                best_char = char

        if best_char is None or best_count <= 0:
            return ""

        result.append(best_char)
        counts[best_char] -= 1
        last_pos[best_char] = pos

    return "".join(result)
