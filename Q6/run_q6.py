import sys, time
import steps
from steps import ways_naive, ways_memo, ways_dict, ways_loop, call_tree

print("== Complete the Code ==")
steps.calls = 0; print("naive:", ways_naive(25), "calls =", steps.calls)
ways_memo.cache_clear()
steps.calls = 0; print("memo:", ways_memo(25), "calls =", steps.calls)
print("(expected: naive: 121393 calls = 242785 / memo: 121393 calls = 26)")

print("\n== Correctness check n = 1..6: by hand vs program ==")
by_hand = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}     # ways(n) = ways(n-1) + ways(n-2): 1,2,3,5,8,13
for n in range(1, 7):
    print(f"n={n}: hand {by_hand[n]:>2}  naive {ways_naive(n):>2}  memo {ways_memo(n):>2}  loop {ways_loop(n):>2}  ->", "OK" if by_hand[n] == ways_naive(n) == ways_memo(n) == ways_loop(n) else "MISMATCH")

print("\n== Call tree for n = 5 (plain recursion) ==")
total = call_tree(5)
print("total calls for n = 5:", total)

print("\n== Growth investigation: predicted vs counted calls ==")
print("Prediction: naive calls = 2*ways(n) - 1 (each call except leaves makes 2 calls), memo calls = n + 1")
print(f"{'n':>3} {'ways(n)':>10} {'predicted naive':>16} {'naive calls':>12} {'predicted memo':>15} {'memo calls':>11} {'dict-memo calls (incl. hits)':>29}")
for n in (10, 20, 25, 30):
    steps.calls = 0; ways_naive(n); cn = steps.calls
    ways_memo.cache_clear(); steps.calls = 0; ways_memo(n); cm = steps.calls
    steps.calls = 0; ways_dict(n); cd = steps.calls
    print(f"{n:>3} {ways_loop(n):>10} {2 * ways_loop(n) - 1:>16} {cn:>12} {n + 1:>15} {cm:>11} {cd:>29}")

print("\n== Deployment: n = 1000 ==")
print("sys.getrecursionlimit() =", sys.getrecursionlimit())
ways_memo.cache_clear()
try:
    r = ways_memo(1000)
    print("ways_memo(1000) worked, digits:", len(str(r)))
except RecursionError as e:
    print("ways_memo(1000) -> RecursionError:", e)
    print("  The first call goes ways_memo(1000) -> (999) -> (998) ... -> (1) = about 1000 nested calls, and the limit is 1000 frames (the starting script already uses some).")
