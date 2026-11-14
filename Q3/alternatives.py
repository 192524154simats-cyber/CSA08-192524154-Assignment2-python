"""Q3 alternative: re.fullmatch vs slicing + string methods. Same decisions, time per check, readability."""
import re, time
from plate import is_valid, normalise

PATTERN = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}")

def is_valid_re(reg):
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None

def is_valid_re_compiled(reg):
    return PATTERN.fullmatch(reg) is not None

import random, string
random.seed(3)
def rand_plate():
    return "".join(random.choice(string.ascii_uppercase + string.digits) if random.random() < 0.15 else c
                   for c in random.choice(["TN09AB1234", "KA05M4321", "MH12XY9999"]))
data = [rand_plate() for _ in range(100000)]
diff = sum(1 for d in data if is_valid(d) != is_valid_re(d))
print(f"Same decision on {len(data)} random plates: differences = {diff}   (valid count = {sum(map(is_valid, data))})")
print("ASCII check: is_valid('TN09AB123\\u0664') =", is_valid("TN09AB123\u0664"), "| regex [0-9] =", is_valid_re("TN09AB123\u0664"))

for name, fn in (("slicing + isalpha/isdigit", is_valid), ("re.fullmatch (string pattern)", is_valid_re), ("re.fullmatch (compiled)", is_valid_re_compiled)):
    t0 = time.perf_counter()
    for d in data: fn(d)
    print(f"{name:32} {(time.perf_counter() - t0) / len(data) * 1e9:8.0f} ns per check")
