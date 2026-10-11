"""
You are given an integer array nums and an integer k. You can perform the following operation any number of times:

Increase or decrease any element of nums by 1.
Return the minimum number of operations required to ensure that at least one subarray of size k in nums has all 
elements equal.
"""

def min_operations(nums: list[int], k: int) -> int:
    n = len(nums)
    if k == 1:
        return 0

    nums.sort()
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]

    def window_cost(i: int) -> int:
        total = prefix_sum[i + k] - prefix_sum[i]
        target = nums[i + k - 1]
        return target * k - total

    return min(window_cost(i) for i in range(n - k + 1))