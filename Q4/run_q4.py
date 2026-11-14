"""Q4: predictions, then measurements for 1,000 / 10,000 / 200,000 lines."""
import sys
from statement import *

print("PREDICTION (before running): join is fastest and grows linearly; += looks linear in CPython because of the in-place")
print("optimisation, but is O(n^2) when it cannot apply; f-string lines cost slightly more than join of ready parts.\n")

# ---- The Complete-the-Code program exactly as given ----
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]
import time
start = time.perf_counter(); a = build_plus(items); t_plus = time.perf_counter() - start
start = time.perf_counter(); b = build_join(items); t_join = time.perf_counter() - start
print(f"same text: {a == b}, length: {len(b)}")
print(f"+ = time: {t_plus:.4f} s join time: {t_join:.4f} s\n")

# ---- Three sizes ----
print(f"{'lines':>9} | {'(a) +=':>10} {'(b) join':>10} {'(c) f-string+join':>18} {'(c) f-string+=':>15} | {'+= aliased':>12} | final length")
for n in (1_000, 10_000, 200_000):
    parts = make_items(n)
    ta = timed(build_plus, parts)[1]
    text_b, tb = timed(build_join, parts)
    length = len(text_b)
    tc, tcp = timed(build_fstring, parts), timed(build_fstring_plus, parts)
    if n <= 10_000:
        tal = f"{timed(build_plus_aliased, parts)[1]:.4f} s"
    else:
        tal = "(skipped)"
    print(f"{n:>9} | {ta:>9.4f}s {tb:>9.4f}s {tc[1]:>17.4f}s {tcp[1]:>14.4f}s | {tal:>12} | {length}")

# ---- Counting characters copied ----
print("\nCharacters copied if every += copies the whole text (no optimisation):")
for n in (1_000, 10_000, 200_000):
    parts = make_items(n)
    total = 0; length = 0
    for p in parts:
        length += len(p) + 1
        total += length                      # each += would copy `length` characters
    print(f"  n = {n:>7}: {total:>18,} characters copied   vs join: {length:>10,} (one pass)   ratio {total / length:,.0f}x")

# ---- Evidence of O(n^2): doubling n for the aliased += ----
print("\nAliased += (cannot be optimised): doubling the lines should make it ~4x slower")
prev = None
for n in (10_000, 20_000, 40_000):
    t = timed(build_plus_aliased, make_items(n))[1]
    print(f"  n = {n:>6}: {t:.4f} s" + (f"   ratio to previous = {t / prev:.1f}x" if prev else ""))
    prev = t
