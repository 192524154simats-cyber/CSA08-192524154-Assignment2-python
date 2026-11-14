"""Q2 demonstration: each scenario is a scripted list of what the customer types."""
from otp import *

scenarios = {
    "S1 right on 1st try":              ["4821"],
    "S2 wrong, wrong, right":           ["1111", "2222", "4821"],
    "S3 three wrong":                   ["1", "2", "3"],
    "S4 blank, wrong, blank, right":    ["", "1", "", "4821"],
    "S5 wrong, blank, wrong, wrong":    ["1", "", "2", "3"],
    "S6 HELP then right (pass)":        ["HELP", "4821"],
}
print("== while design vs for-range(3) design (status, attempts used, loop iterations) ==")
for name, entries in scenarios.items():
    print(f"{name:34} while: {verify_while(make_reader(entries))}   for: {verify_for(make_reader(entries))}")

print("\n== for + break/continue + loop-else (textbook form): blank burns a pass ==")
for name in ("S3 three wrong", "S4 blank, wrong, blank, right"):
    print(f"{name:34} {verify_for_break(make_reader(scenarios[name]))}")

print("\n== Bug: counter updated in the wrong place (blank counted) ==")
for name in ("S4 blank, wrong, blank, right",):
    print(f"{name:34} buggy: {verify_buggy_counter(make_reader(scenarios[name]))}   correct: {verify_while(make_reader(scenarios[name]))[:2]}")

print("\n== Changed condition: 2 extra attempts after correct security answer ==")
cases = {
    "3 wrong, answer correct, 4th wrong, 5th right": (["1", "2", "3", "4", "4821"], True),
    "3 wrong, answer correct, all wrong":            (["1", "2", "3", "4", "5"], True),
    "3 wrong, answer WRONG":                         (["1", "2", "3", "4821"], False),
    "right on 2nd":                                  (["1", "4821"], True),
}
for name, (entries, ans) in cases.items():
    print(f"{name:48} (status, attempts, allowed) = {verify_with_security_question(make_reader(entries), lambda a=ans: a)}")
