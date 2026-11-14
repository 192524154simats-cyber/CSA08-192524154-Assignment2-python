"""Q5 alternative designs: caller always passes the list explicitly, or a closure holds the order.
Time per item and memory per customer."""
import time, tracemalloc
from canteen import add_item

def add_explicit(item, order):          # caller MUST pass a list
    order.append(item)
    return order

def make_taker():                       # closure
    order = []
    def add(item):
        order.append(item)
        return order
    return add

N = 200_000
def bench(label, fn):
    t0 = time.perf_counter(); fn(); sec = time.perf_counter() - t0
    print(f"{label:28} {sec / N * 1e9:8.0f} ns per item")

def run_default():
    o = None
    for _ in range(N): o = add_item("Tea", o)
def run_explicit():
    o = []
    for _ in range(N): add_explicit("Tea", o)
def run_closure():
    add = make_taker()
    for _ in range(N): add("Tea")
bench("default None", run_default); bench("explicit list from caller", run_explicit); bench("closure", run_closure)

# memory per customer (10 items) for 10,000 customers
def customers(kind):
    out = []
    for _ in range(10_000):
        if kind == "closure":
            add = make_taker()
            for _ in range(10): add("Tea")
            out.append(add)
        else:
            o = None if kind == "default" else []
            for _ in range(10): o = add_item("Tea", o) if kind == "default" else add_explicit("Tea", o)
            out.append(o)
    return out
for kind in ("default", "explicit", "closure"):
    tracemalloc.start(); keep = customers(kind); cur = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    print(f"{kind:10} memory for 10,000 customers x 10 items: {cur / 1024:8.0f} KiB  ({cur / 10_000:.0f} bytes per customer)")
