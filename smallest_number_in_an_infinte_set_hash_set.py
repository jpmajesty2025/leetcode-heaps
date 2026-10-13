"""
Smallest Infinite Set: Hash-Set Alternative.

Uses a frontier pointer for untouched numbers and a Python hash set for added-back numbers.
Because Python's set does not maintain heap order, popSmallest must scan the entire set
using min(self._added_back), incurring O(k) linear time per pop.

Time Complexity: O(k) popSmallest, O(1) addBack
Space Complexity: O(k)
"""


class SmallestInfiniteSet:
    """Hash-set alternative using min() to extract the smallest added-back number."""

    def __init__(self):
        self._current: int = 1
        self._added_back: set[int] = set()

    def popSmallest(self) -> int:
        """Remove and return smallest number. O(k) scan over _added_back."""
        if self._added_back:
            num = min(self._added_back)
            self._added_back.remove(num)
            return num

        num = self._current
        self._current += 1
        return num

    def addBack(self, num: int) -> None:
        """Add back number if it is strictly below the current frontier."""
        if num <= 0:
            return

        if num < self._current:
            self._added_back.add(num)
