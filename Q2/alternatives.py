"""Q2 alternative: recursion. Counts calls and stack depth; shows O(a) stack vs O(1) loop; recursion limit."""
import sys, time
from otp import OTP, make_reader, verify_while

depth_seen = 0
calls = 0

def verify_recursive(read, attempts_left=3, depth=1):
    """Each call handles one attempt and calls itself for the next."""
    global depth_seen, calls
    calls += 1
    depth_seen = max(depth_seen, depth)
    if attempts_left == 0:
        return "LOCKED 30 min"
    entry = read("OTP: ").strip()
    if entry == "":
        return verify_recursive(read, attempts_left, depth + 1)       # blank: same attempts left
    if entry == OTP:
        return "OK"
    return verify_recursive(read, attempts_left - 1, depth + 1)

print(f"recursion limit = {sys.getrecursionlimit()}")
print(f"{'attempts a':>10} {'while: iterations':>18} {'recursive: calls':>17} {'max depth (stack frames)':>25} {'time while':>12} {'time recursive':>15}")
for a in (3, 50, 500):
    entries = ["x"] * a                                 # all wrong
    t0 = time.perf_counter()
    # while version with a attempts allowed
    attempts, iters = 0, 0
    rd = make_reader(entries)
    while attempts < a:
        iters += 1; rd(); attempts += 1
    t1 = time.perf_counter()
    depth_seen = 0; calls = 0
    verify_recursive(make_reader(entries), a)
    t2 = time.perf_counter()
    print(f"{a:>10} {iters:>18} {calls:>17} {depth_seen:>25} {(t1 - t0) * 1e6:>10.1f}us {(t2 - t1) * 1e6:>13.1f}us")

try:
    verify_recursive(make_reader(["x"] * 5000), 5000)
except RecursionError as e:
    print("a = 5000 attempts ->", type(e).__name__, "(each attempt keeps one stack frame; a loop would not)")
