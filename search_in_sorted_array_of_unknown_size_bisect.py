"""
LeetCode 702: Search in a Sorted Array of Unknown Size (Virtual Sequence Bisect Adapter)
https://leetcode.com/problems/search-in-a-sorted-array-of-unknown-size/

Strategy:
Bridges Python's C-accelerated `bisect.bisect_left` with the interactive `ArrayReader` API:
1. Performs exponential search to identify the bounds [left, right].
2. Wraps the reader into a zero-memory `VirtualReaderView` lazy sequence implementing
   `__len__` and `__getitem__`.
3. Calls `bisect.bisect_left` directly over the virtual view.

Complexity:
- Time: O(log k) calls to reader.get().
- Space: O(1) auxiliary space (zero array allocations).
"""

import bisect
from typing import Protocol


class ArrayReader:
    """ArrayReader API specification."""

    def get(self, index: int) -> int:
        return -1


class VirtualReaderView:
    """
    A zero-allocation lazy sequence view wrapping ArrayReader
    to satisfy Python's sequence protocol for bisect.
    """

    def __init__(self, reader: "ArrayReader", length: int):
        self.reader = reader
        self.length = length

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> int:
        return self.reader.get(index)


def search(reader: "ArrayReader", target: int) -> int:
    """
    Search using Exponential Search + bisect.bisect_left.
    """
    left, right = 0, 1

    # Exponential bounding
    while reader.get(right) < target:
        left = right + 1
        right <<= 1

    # Virtual lazy view over [0, right + 1]
    view = VirtualReaderView(reader, right + 1)
    idx = bisect.bisect_left(view, target, lo=left, hi=right + 1)

    if idx <= right and reader.get(idx) == target:
        return idx

    return -1


class Solution:
    """LeetCode submission interface."""
    search = staticmethod(search)
