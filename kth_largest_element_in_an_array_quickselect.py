"""
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?
"""

import random


def find_kth_largest(nums: list[int], k: int) -> int:
    """Find the kth largest element in nums using randomized 3-way Quickselect.

    Time Complexity: O(n) average, O(n^2) worst-case (extremely rare with random pivot)
    Space Complexity: O(1) auxiliary space (iterative, operates on a copy)
    """
    if not nums:
        raise ValueError("nums cannot be empty")
    if k <= 0 or k > len(nums):
        raise ValueError(
            f"k={k} is out of valid bounds for array of length {len(nums)}"
        )

    # Work on a copy so we do not mutate the input array
    arr = nums.copy()
    target_idx = len(arr) - k  # kth largest is (n - k)-th in 0-indexed ascending order

    left = 0
    right = len(arr) - 1

    while left <= right:
        # Pick random pivot to avoid O(n^2) on sorted/reverse-sorted inputs
        pivot_idx = random.randint(left, right)
        pivot = arr[pivot_idx]

        # 3-way partition (Dutch National Flag):
        # arr[left..lt-1] < pivot
        # arr[lt..gt] == pivot
        # arr[gt+1..right] > pivot
        lt = left
        gt = right
        i = left

        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1

        # Check which partition contains target_idx
        if target_idx < lt:
            right = lt - 1
        elif target_idx > gt:
            left = gt + 1
        else:
            return arr[target_idx]

    raise RuntimeError("Target index not found")
