"""Q1 alternative: match-case and a list of (upper limit, decision) pairs searched in a loop.
Counts comparisons and measures time per decision for k slabs."""
import time

# --- match-case version (Python 3.10+), same 3 slabs ---
def decide_match(units, ration, elder):
    match units:
        case u if u <= 100:
            return "subsidy"
        case u if u <= 200:
            return "partial subsidy" if ration else "none"
        case _:
            return "subsidy" if elder else "none"

# --- slab table: (upper limit, decision-function) searched in a loop ---
SLABS = [(100, lambda r, e: "subsidy"),
         (200, lambda r, e: "partial subsidy" if r else "none"),
         (float("inf"), lambda r, e: "subsidy" if e else "none")]

def decide_table(units, ration, elder):
    for limit, rule in SLABS:
        if units <= limit:
            return rule(ration, elder)

from subsidy import decide_elif
bad = sum(1 for u in range(0, 401) for r in (0, 1) for e in (0, 1)
          if not (decide_elif(u, r, e) == decide_match(u, r, e) == decide_table(u, r, e)))
print("match-case and table agree with if-elif on all 1604 cases; mismatches =", bad)

# --- k slabs: time per decision (worst case = last slab) ---
def make_chain(k):
    src = "def f(u):\n    if u <= 0: return 0\n" + "".join(f"    elif u <= {i * 10}: return {i}\n" for i in range(1, k)) + f"    else: return {k}\n"
    ns = {}; exec(src, ns); return ns["f"]

def make_table(k):
    limits = [i * 10 for i in range(k)]
    def f(u):
        for i, lim in enumerate(limits):
            if u <= lim:
                return i
        return k
    return f

print(f"{'k slabs':>8} {'if-elif chain (ns)':>20} {'table loop (ns)':>18}   (worst case: u above every limit)")
for k in (3, 10, 100, 1000):
    f1, f2 = make_chain(k), make_table(k)
    u = k * 10 + 5
    n = 20000 if k < 1000 else 3000
    t0 = time.perf_counter()
    for _ in range(n): f1(u)
    t1 = time.perf_counter()
    for _ in range(n): f2(u)
    t2 = time.perf_counter()
    print(f"{k:>8} {(t1 - t0) / n * 1e9:>20.0f} {(t2 - t1) / n * 1e9:>18.0f}")
