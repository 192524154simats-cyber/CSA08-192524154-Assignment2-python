"""Q6 - ways to climb n temple steps taking 1 or 2 steps at a time."""
import sys
from functools import lru_cache

calls = 0

def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:                       # base case: 0 or 1 step left -> exactly 1 way
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)     # recursive case: last move was 1 step or 2 steps

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1                       # counts only the calls that are actually computed (cache misses)
    # TODO 1 (done): same base case and recursive case, calling ways_memo
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_dict(n, memo=None):
    """Memoisation with an explicit dictionary (no functools) - counts calls including cache hits."""
    global calls
    calls += 1
    if memo is None:
        memo = {}
    if n <= 1:
        return 1
    if n not in memo:
        memo[n] = ways_dict(n - 1, memo) + ways_dict(n - 2, memo)
    return memo[n]

def ways_loop(n):
    """Loop that keeps only the last two values: O(n) time, O(1) extra space."""
    prev, cur = 1, 1                 # ways(0), ways(1)
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur if n >= 1 else 1

def call_tree(n, depth=0, out=None):
    """Prints the call tree of ways_naive(n) with indentation; returns number of calls."""
    print("    " * depth + f"ways({n})")
    if n <= 1:
        return 1
    return 1 + call_tree(n - 1, depth + 1) + call_tree(n - 2, depth + 1)
