"""Q6 alternative + deployment: run naive / memo / loop for n = 1000 and compare time and space."""
import sys, time
import steps
from steps import ways_naive, ways_memo, ways_loop

N = 1000
print(f"recursion limit now = {sys.getrecursionlimit()}")

# ---- plain recursion at n = 1000: cannot be run; estimate from measured speed ----
steps.calls = 0
t0 = time.perf_counter(); ways_naive(30); t30 = time.perf_counter() - t0
per_call = t30 / steps.calls
calls_1000 = 2 * ways_loop(N) - 1
seconds = per_call * calls_1000
print(f"\nPlain recursion: n=30 took {t30:.3f} s for {steps.calls:,} calls ({per_call * 1e9:.0f} ns per call)")
print(f"  n=1000 needs 2*ways(1000)-1 calls = a {len(str(calls_1000))}-digit number (~{float(calls_1000):.2e})")
print(f"  at that speed: ~{seconds:.1e} seconds = ~{seconds / 3.15e7:.1e} years  -> NOT run (growth is O(phi^n), phi = 1.618)")
for n in (30, 32, 34):
    steps.calls = 0; t0 = time.perf_counter(); ways_naive(n); t = time.perf_counter() - t0
    print(f"  measured: n={n}: {steps.calls:>10,} calls, {t:.3f} s")

# ---- memoised: needs the recursion limit raised, or a warm-up ----
ways_memo.cache_clear()
try:
    ways_memo(N)
except RecursionError:
    print("\nMemoised, default limit: RecursionError (depth ~1000 frames > limit 1000)")

ways_memo.cache_clear()
sys.setrecursionlimit(5000)
steps.calls = 0
t0 = time.perf_counter(); a = ways_memo(N); t_memo = time.perf_counter() - t0
print(f"Memoised with sys.setrecursionlimit(5000): {len(str(a))} digits, calls = {steps.calls}, time = {t_memo * 1000:.3f} ms, cache entries = {ways_memo.cache_info().currsize}")
sys.setrecursionlimit(1000)

ways_memo.cache_clear()
t0 = time.perf_counter()
for k in range(0, N + 1, 100):                # warm-up: fill the cache from the bottom in steps of 100 -> depth never above ~100
    ways_memo(k)
b = ways_memo(N)
t_warm = time.perf_counter() - t0
print(f"Memoised with warm-up (default limit 1000): same answer {a == b}, time = {t_warm * 1000:.3f} ms (works without changing the limit)")

t0 = time.perf_counter(); c = ways_loop(N); t_loop = time.perf_counter() - t0
print(f"Loop (last two values): same answer {a == c}, time = {t_loop * 1000:.3f} ms, extra space O(1) (two numbers), no recursion at all")

# ---- larger n shows the limits of raising the limit ----
n_big = 5000
t0 = time.perf_counter(); big = ways_loop(n_big); t_big = time.perf_counter() - t0
print(f"\nLoop for n = {n_big}: {len(str(big))} digits in {t_big * 1000:.2f} ms; memoised recursion would need ~{n_big} frames (limit must be raised again, risk of crashing the interpreter)")
