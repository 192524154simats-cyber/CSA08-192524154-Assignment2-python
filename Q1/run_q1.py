"""Q1 runner: PREDICTIONS (written before running) vs observed, for 8 households."""
from subsidy import decide_separate_ifs, decide_elif, decide_nested, decide_combined

# (label, units, ration card, member > 80) and my PREDICTION (made before execution)
# predicted_elif = what the correct if-elif-else must give; predicted_separate = number of subsidies the buggy version gives
households = [
    ("A", 100, True,  False, "subsidy",         2),   # 100 with ration card: slab 1 AND 'units<=200 and ration' both true
    ("B", 100, False, False, "subsidy",         1),
    ("C", 101, True,  False, "partial subsidy", 1),
    ("D", 101, False, False, "none",            0),
    ("E", 200, True,  False, "partial subsidy", 1),
    ("F", 200, False, True,  "none",            1),   # elder rule leaks into the 101-200 slab
    ("G", 201, False, False, "none",            0),
    ("H", 201, False, True,  "subsidy",         1),
]
print(f"{'HH':<3}{'units':>6}{'ration':>8}{'80+':>6} | {'predicted':<16}{'if-elif':<16}{'ok':<4}| {'pred #':>6}{'separate-ifs result':<40}{'ok':<4}")
good = 0
for name, u, r, e, pred, pred_n in households:
    out_elif = decide_elif(u, r, e)
    out_sep = decide_separate_ifs(u, r, e)
    ok1, ok2 = out_elif == pred, len(out_sep) == pred_n
    good += ok1 and ok2
    print(f"{name:<3}{u:>6}{str(r):>8}{str(e):>6} | {pred:<16}{out_elif:<16}{'Y' if ok1 else 'N':<4}| {pred_n:>6} {str(out_sep):<38}{'Y' if ok2 else 'N'}")
print(f"\nPredictions correct for {good}/8 households.")
print("Households that got MORE THAN ONE subsidy with separate ifs:", [h[0] for h in households if len(decide_separate_ifs(h[1], h[2], h[3])) > 1])
print("Households where separate ifs disagree with the correct rule:",
      [h[0] for h in households if (decide_separate_ifs(h[1], h[2], h[3]) or ["none"])[0] != decide_elif(h[1], h[2], h[3]) or len(decide_separate_ifs(h[1], h[2], h[3])) > 1])

# Exhaustive check: nested == combined == if-elif for every units 0..400 and all Boolean combinations
cases = 0; mismatch = 0
for units in range(0, 401):
    for r in (False, True):
        for e in (False, True):
            cases += 1
            if not (decide_elif(units, r, e) == decide_nested(units, r, e) == decide_combined(units, r, e)):
                mismatch += 1
print(f"\nExhaustive comparison nested / combined / if-elif: {cases} cases, {mismatch} mismatches")
