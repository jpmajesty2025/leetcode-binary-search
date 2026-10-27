"""
LeetCode 1482: Minimum Number of Days to Make m Bouquets
https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/

Event Sweep with Boundary Table Segment Merging:
Processes flower blooms in chronological order, maintaining connected components
in O(1) time per event via endpoint length tracking.
Completely bypasses binary search.

Complexity:
- Time: O(N log N) dominated by sorting bloom events, followed by an O(N) sweep.
- Space: O(N) for boundary table and sorted index array.
"""

from typing import List


def min_days(bloomDay: List[int], m: int, k: int) -> int:
    """
    Find minimum days using chronological event sweep with O(1) segment merging.

    Mechanism:
    - Sort flower indices in ascending order of bloomDay in O(N log N).
    - Maintain a boundary length table where length[pos] stores the size of the
      contiguous bloomed segment spanning pos.
    - When flower pos blooms:
      - It merges adjacent left segment of size L = length[pos - 1] and right segment
        of size R = length[pos + 1].
      - The delta in bouquets is:
          delta = (L + 1 + R) // k - (L // k) - (R // k)
      - The merged segment has size new_len = L + 1 + R.
      - We update both endpoints in O(1):
          length[pos - L] = new_len
          length[pos + R] = new_len
      - The moment total_bouquets >= m, return the current flower's bloom day!
    """
    n = len(bloomDay)
    if n < m * k:
        return -1
    if n == m * k:
        return max(bloomDay)
    if k == 1:
        # For k = 1, we simply need the m-th smallest bloom day
        return sorted(bloomDay)[m - 1]

    length = [0] * (n + 2)  # 1-indexed with padding
    total_bouquets = 0
    order = sorted(range(n), key=lambda i: bloomDay[i])

    for idx in order:
        pos = idx + 1
        left_len = length[pos - 1]
        right_len = length[pos + 1]

        total_bouquets += (left_len + 1 + right_len) // k - (left_len // k) - (right_len // k)
        new_len = left_len + 1 + right_len
        length[pos - left_len] = new_len
        length[pos + right_len] = new_len

        if total_bouquets >= m:
            return bloomDay[idx]

    return -1


class Solution:
    """LeetCode submission interface."""
    minDays = staticmethod(min_days)
