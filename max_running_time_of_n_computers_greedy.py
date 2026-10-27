"""
LeetCode 2141: Maximum Running Time of N Computers
https://leetcode.com/problems/maximum-running-time-of-n-computers/

Greedy Reverse Elimination Implementation:
Completely eliminates the outer binary search over the runtime range [1, sum(batteries) // n].
Solves in a single sorted pass in O(M log M) time and O(1) auxiliary space.

Complexity:
- Time: O(M log M) dominated by sorting, followed by at most (M - n) O(1) eliminations.
- Space: O(1) auxiliary space (or O(M) if preserving original array input).
"""

from typing import List


def max_run_time(n: int, batteries: List[int]) -> int:
    """
    Find maximum runtime using greedy reverse elimination.

    Mathematical Invariant:
    Let total = sum(batteries).
    The theoretical maximum average runtime for n computers is total // n.
    If the largest battery has capacity B > total // n:
      No computer can run longer than total // n on average across all n machines.
      Therefore, battery B has more capacity than the entire system can average.
      Because B cannot power two computers simultaneously, its excess energy above
      the final runtime would be wasted unless it is assigned exclusively to run
      one single computer for the full duration.
      We therefore greedily dedicate this battery to one computer:
          total -= B
          n -= 1
    We repeat this deduction from largest to smallest.
    Once the largest remaining battery has capacity <= total // n:
      Every remaining battery can be fully utilized without being capped!
      By McNaughton's theorem, these remaining batteries can be perfectly scheduled
      to achieve an exact runtime of total // n across the remaining n computers.
      Thus, total // n is the exact optimal answer!
    """
    sorted_batteries = sorted(batteries)
    total = sum(sorted_batteries)
    idx = len(sorted_batteries) - 1

    while sorted_batteries[idx] > total // n:
        total -= sorted_batteries[idx]
        n -= 1
        idx -= 1

    return total // n


class Solution:
    """LeetCode submission interface."""
    maxRunTime = staticmethod(max_run_time)
