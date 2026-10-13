"""
Construct String With Repeat Limit: 26-Element Array Alternative.

Because the alphabet is restricted to lowercase English letters (|Σ| = 26),
we can replace the heap with a 26-element frequency array and two pointers:
  * Pointer i: tracks the largest available character
  * Pointer j: scans downward for the next largest delimiter character

Time Complexity: O(n + |Σ|)
Space Complexity: O(|Σ|) fixed 26 integers
"""


def repeat_limited_string(s: str, repeat_limit: int) -> str:
    """Construct the lexicographically largest repeat-limited string using a 26-element array."""
    if not s or repeat_limit <= 0:
        return ""

    counts = [0] * 26
    for char in s:
        counts[ord(char) - 97] += 1

    result: list[str] = []
    i = 25  # Primary character pointer (scanning down from 'z')
    j = 24  # Delimiter character pointer (scanning down for smaller characters)

    while i >= 0:
        if counts[i] == 0:
            i -= 1
            continue

        use = min(counts[i], repeat_limit)
        result.append(chr(97 + i) * use)
        counts[i] -= use

        if counts[i] > 0:
            # Need a delimiter character strictly smaller than i
            j = min(j, i - 1)
            while j >= 0 and counts[j] == 0:
                j -= 1

            if j < 0:
                # No smaller character available to break streak
                break

            result.append(chr(97 + j))
            counts[j] -= 1

    return "".join(result)
