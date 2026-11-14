"""Q4 - three ways to build the statement, plus a version that defeats CPython's += optimisation."""
import time, io

def make_items(n):
    return [f"Item{i}:Rs{i % 50}" for i in range(n)]

def build_plus(parts):                      # (a) repeated +=
    text = ""
    for p in parts:
        text += p + "\n"
    return text

def build_join(parts):                      # (b) list of parts + single join   (TODO 1 of the assignment)
    return "\n".join(parts) + "\n"          # same text as build_plus (one "\n" after every line)

def build_fstring(parts):                   # (c) f-string for each line, then join
    lines = []
    for i, p in enumerate(parts):
        lines.append(f"{i + 1:>6}  {p}")
    return "\n".join(lines) + "\n"

def build_fstring_plus(parts):              # (c) variant: f-string for each line, joined with +=
    text = ""
    for i, p in enumerate(parts):
        text += f"{i + 1:>6}  {p}\n"
    return text

def build_plus_aliased(parts):
    """+= with a second reference to the old string: CPython can no longer resize in place,
    so every += copies the whole text -> O(n^2) characters copied."""
    text, keep = "", None
    for p in parts:
        keep = text                         # second reference -> refcount 2 -> in-place trick not allowed
        text += p + "\n"
    return text

def build_stringio(parts):                  # alternative: io.StringIO buffer
    buf = io.StringIO()
    for p in parts:
        buf.write(p); buf.write("\n")
    return buf.getvalue()

def timed(fn, *args):
    t0 = time.perf_counter(); r = fn(*args); return r, time.perf_counter() - t0
