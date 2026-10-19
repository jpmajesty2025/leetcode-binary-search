"""
Given an array of integers nums which is sorted in ascending order, and an integer 
target, write a function to search target in nums. If target exists, then return its 
index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

1 <= nums.length <= 104
-104 < nums[i], target < 104
All the integers in nums are unique.
nums is sorted in ascending order.
"""

def search(self, nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1