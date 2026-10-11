"""
Find K Closest Elements: binary search for the window start.

Because arr is sorted, the k closest elements to x are always a contiguous window arr[left:left + k].
Binary search for `left` by comparing the two candidates at the window's edges: if the leftmost element
arr[mid] is farther from x than the element just past the window, arr[mid + k], the window must move right.
On an exact tie, keep the smaller elements, so the window stays left.

Time O(log(n - k) + k), space O(1) beyond the output.
Requires arr to be sorted ascending (as the problem guarantees).
"""


def find_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    if k <= 0:
        return []
    if k >= len(arr):
        return list(arr)

    low, high = 0, len(arr) - k  # candidate window starts
    while low < high:
        mid = (low + high) // 2
        if x - arr[mid] > arr[mid + k] - x:
            low = mid + 1
        else:
            high = mid
    return arr[low : low + k]
