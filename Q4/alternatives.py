"""Q4 alternative: write line by line to a file, or io.StringIO, instead of collecting parts for join().
Measures time and PEAK MEMORY (tracemalloc)."""
import os, time, tracemalloc, tempfile
from statement import make_items, build_join, build_stringio

def to_file(parts, path):
    with open(path, "w") as f:               # line by line: nothing is kept in memory
        for p in parts:
            f.write(p + "\n")

def run(label, fn):
    tracemalloc.start()
    t0 = time.perf_counter()
    fn()
    sec = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f"{label:34} {sec:8.4f} s   peak extra memory {peak / 1024:10.1f} KiB")

path = os.path.join(tempfile.gettempdir(), "statement_demo.txt")
for n in (10_000, 200_000):
    parts = make_items(n)
    print(f"--- {n} lines ---")
    run("join (list of parts in memory)", lambda: build_join(parts))
    run("io.StringIO buffer", lambda: build_stringio(parts))
    run("write line by line to a file", lambda: to_file(parts, path))
    print(f"    file size {os.path.getsize(path):,} bytes")
os.remove(path)
