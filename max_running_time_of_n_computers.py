"""
LeetCode 2141: Maximum Running Time of N Computers
https://leetcode.com/problems/maximum-running-time-of-n-computers/

You have n computers. You are given the integer n and a 0-indexed integer array batteries where the 
ith battery can run a computer for batteries[i] minutes. You are interested in running all n computers 
simultaneously using the given batteries.

Initially, you can insert at most one battery into each computer. After that and at any integer time 
moment, you can remove a battery from a computer and insert another battery any number of times. The 
inserted battery can be a totally new battery or a battery from another computer. You may assume that 
the removing and inserting processes take no time.

Note that the batteries cannot be recharged.

Return the maximum number of minutes you can run all the n computers simultaneously.

Constraints:
- 1 <= n <= batteries.length <= 10^5
- 1 <= batteries[i] <= 10^9

Complexity:
- Time: O(M log(sum(batteries) // n)) where M = len(batteries)
- Space: O(1) auxiliary space
"""

from typing import List


def max_run_time(n: int, batteries: List[int]) -> int:
    """
    Find maximum runtime for n computers using binary search on answer.

    Mathematical Feasibility (McNaughton's Wrap-Around Rule):
    To run n computers for T minutes, total required energy is n * T.
    No single battery can be inserted into multiple computers simultaneously,
    so battery i can contribute at most min(batteries[i], T) minutes.
    Hence, a necessary condition is:
        sum(min(b, T) for b in batteries) >= n * T
    By McNaughton's parallel-machine scheduling theorem (or open shop scheduling),
    because each usable battery segment is <= T, we can always pack these segments
    into n machine schedules of length T without any battery overlapping with itself.
    Thus, the condition is both necessary and sufficient!

    Monotonicity & Bounds:
    - Usable energy sum(min(b, T)) is monotonically non-decreasing in T.
    - Lower bound: left = 1 (since len(batteries) >= n and batteries[i] >= 1).
    - Upper bound: right = sum(batteries) // n (total energy divided by n computers).
    """
    total = sum(batteries)
    left, right = 1, total // n

    while left < right:
        mid = (left + right + 1) // 2
        needed = mid * n
        usable = 0
        for b in batteries:
            usable += b if b < mid else mid
            if usable >= needed:
                break

        if usable >= needed:
            left = mid
        else:
            right = mid - 1

    return left


class Solution:
    """LeetCode submission interface."""
    maxRunTime = staticmethod(max_run_time)
