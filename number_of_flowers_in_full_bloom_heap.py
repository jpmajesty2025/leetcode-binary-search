"""
LeetCode 2251: Number of Flowers in Full Bloom (Min-Heap Active Interval Simulation)
https://leetcode.com/problems/number-of-flowers-in-full-bloom/

Strategy:
Simulates chronological progression using a min-heap (Meeting Rooms II pattern):
1. Sort flowers by start time.
2. Sort people by arrival time, tracking their original indices: (time, original_index).
3. Use a min-heap to store the end times of all currently blooming flowers.
4. For each person at arrival time `t`:
   - Push all flowers with start <= t onto the min-heap.
   - Pop all expired flowers with end < t from the min-heap.
   - The size of the min-heap len(heap) is the exact number of flowers blooming at time t!

Complexity:
- Time: O(N log N + M log M)
  - Sorting flowers: O(N log N)
  - Sorting people: O(M log M)
  - Each flower is pushed once and popped at most once: O(N log N)
- Space: O(N + M) auxiliary space
"""

import heapq
from typing import List


def full_bloom_flowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    Count blooming flowers using a chronological min-heap simulation.
    """
    sorted_flowers = sorted(flowers, key=lambda f: f[0])
    sorted_people = sorted((p, i) for i, p in enumerate(people))

    heap: List[int] = []  # Min-heap of end times
    ans = [0] * len(people)
    flower_idx = 0
    num_flowers = len(sorted_flowers)

    for arrival, person_idx in sorted_people:
        # Push all flowers that have started blooming by arrival time
        while flower_idx < num_flowers and sorted_flowers[flower_idx][0] <= arrival:
            heapq.heappush(heap, sorted_flowers[flower_idx][1])
            flower_idx += 1

        # Pop all flowers whose bloom ended strictly before arrival time
        while heap and heap[0] < arrival:
            heapq.heappop(heap)

        ans[person_idx] = len(heap)

    return ans


class Solution:
    """LeetCode submission interface."""
    fullBloomFlowers = staticmethod(full_bloom_flowers)
