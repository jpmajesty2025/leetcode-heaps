"""
You are given a string s and an integer repeatLimit. Construct a new string repeatLimitedString using the 
characters of s such that no letter appears more than repeatLimit times in a row. You do not have to use all 
characters from s.

Return the lexicographically largest repeatLimitedString possible.

A string a is lexicographically larger than a string b if in the first position where a and b differ, string 
a has a letter that appears later in the alphabet than the corresponding letter in b. If the first min(a.length, 
b.length) characters do not differ, then the longer string is the lexicographically larger one.
"""

from collections import Counter
import heapq


def repeat_limited_string(s: str, repeat_limit: int) -> str:
    """Construct the lexicographically largest repeat-limited string using a max-heap.

    Greedy Strategy:
    1. Always use the largest available character up to `repeat_limit` times.
    2. If that character has remaining counts, insert exactly ONE instance of the
       next largest available character as a delimiter to break the consecutive streak.
    3. If no delimiter character exists, we cannot continue; stop and return the result.

    Time Complexity: O(n + |Σ| log |Σ|) where |Σ| <= 26 is the alphabet size
    Space Complexity: O(|Σ|) for the heap and frequency map
    """
    if not s or repeat_limit <= 0:
        return ""

    counts = Counter(s)

    # Max-heap based on character ASCII value: store (-ord(char), char, count)
    max_heap = [(-ord(char), char, count) for char, count in counts.items()]
    heapq.heapify(max_heap)

    result: list[str] = []

    while max_heap:
        neg_code, char, count = heapq.heappop(max_heap)
        use = min(count, repeat_limit)
        result.append(char * use)
        remaining = count - use

        if remaining > 0:
            if not max_heap:
                # No smaller character available to break the consecutive streak
                break

            # Pop the next largest available character to serve as a 1-character delimiter
            neg_next_code, next_char, next_count = heapq.heappop(max_heap)
            result.append(next_char)

            # Return remaining copies of next_char back to the heap if any remain
            if next_count > 1:
                heapq.heappush(max_heap, (neg_next_code, next_char, next_count - 1))

            # Return the primary character with its remaining count back to the heap
            heapq.heappush(max_heap, (neg_code, char, remaining))

    return "".join(result)
