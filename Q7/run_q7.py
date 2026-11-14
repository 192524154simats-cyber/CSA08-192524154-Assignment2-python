"""Q7 E: compare Original -> Redesigned on the SAME inputs (counts first, then times)."""
import random, time, math
from redesign import make_slabs, decide_linear, decide_binary

random.seed(11)
print("PREDICTION (before implementing): comparisons per decision for k slabs: linear ~ k/2 on average (k-1 worst), binary ~ log2(k).")
print("  k = 3 -> no gain (about 1-2 comparisons either way); k = 1000 -> ~500 vs ~10 (about 50x fewer); time should improve less than the count\n  because the loop version of binary search has more work per comparison.\n")

print(f"{'k':>6} {'inputs':>8} | {'linear avg cmp':>15} {'linear max':>11} | {'binary avg cmp':>15} {'binary max':>11} | {'log2(k)':>8} | {'same answers':>12}")
for k in (3, 10, 100, 1000, 10000):
    limits, labels = make_slabs(k)
    inputs = [random.randint(0, k * 10 + 50) for _ in range(20000)]
    lin = [decide_linear(u, limits, labels) for u in inputs]
    bin_ = [decide_binary(u, limits, labels) for u in inputs]
    same = all(a[0] == b[0] for a, b in zip(lin, bin_))
    print(f"{k:>6} {len(inputs):>8} | {sum(c for _, c in lin) / len(lin):>15.1f} {max(c for _, c in lin):>11} | "
          f"{sum(c for _, c in bin_) / len(bin_):>15.1f} {max(c for _, c in bin_):>11} | {math.log2(k):>8.1f} | {str(same):>12}")

# boundary-focused validation: every limit, limit+1, limit-1 and 0, negative, huge
limits, labels = make_slabs(1000)
edge = [0, -5, 10 ** 9] + [x for l in limits for x in (l - 1, l, l + 1)]
bad = sum(1 for u in edge if decide_linear(u, limits, labels)[0] != decide_binary(u, limits, labels)[0])
print(f"\nBoundary validation (k=1000): {len(edge)} boundary inputs, mismatches = {bad}")

# the original 3-slab subsidy slabs: 100 / 200 / above -> labels 0,1,2
lim3, lab3 = [100, 200], [0, 1, 2]
print("Original subsidy slabs (limits 100, 200): ", [(u, decide_binary(u, lim3, lab3)[0]) for u in (100, 101, 200, 201)], "-> slab 0,1,1,2 expected")

print("\n== Time per decision (ns), 20,000 random inputs ==")
print(f"{'k':>6} {'original linear':>16} {'redesign binary':>16} {'speed-up':>9}")
for k in (3, 10, 100, 1000, 10000):
    limits, labels = make_slabs(k)
    inputs = [random.randint(0, k * 10 + 50) for _ in range(20000)]
    t0 = time.perf_counter()
    for u in inputs: decide_linear(u, limits, labels)
    t1 = time.perf_counter()
    for u in inputs: decide_binary(u, limits, labels)
    t2 = time.perf_counter()
    a, b = (t1 - t0) / len(inputs) * 1e9, (t2 - t1) / len(inputs) * 1e9
    print(f"{k:>6} {a:>16.0f} {b:>16.0f} {a / b:>8.1f}x")
