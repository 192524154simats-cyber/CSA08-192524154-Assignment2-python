# Q4 – Building Long Text: + or join()? (K4)

**Run:** `python run_q4.py` · `python alternatives.py`  (functions in `statement.py`)
Complete-the-Code: TODO 1 is done in `build_join` (`"\n".join(parts) + "\n"`); the program prints `same text: True` and the two times.

## Three implementations
(a) `build_plus` – `text += p + "\n"` in a loop · (b) `build_join` – list of parts, one `"\n".join(...)` · (c) `build_fstring` – one f-string per line (`f"{i+1:>6}  {p}"`) collected and joined (`build_fstring_plus` joins the f-strings with `+=`).

## Prediction (written before running)
`join()` is fastest and grows linearly. `+=` should be quadratic because every `+=` copies the old text into a new string. f-string lines cost a little extra formatting time per line.

## Measured (seconds, your numbers will differ slightly)
| lines | (a) `+=` | (b) join | (c) f-string + join | (c) f-string + `+=` | `+=` with second reference |
|---|---|---|---|---|---|
| 1,000 | 0.0001 | 0.0000 | 0.0004 | 0.0004 | 0.0002 |
| 10,000 | 0.0008 | 0.0002 | 0.0042 | 0.0044 | 0.0187 |
| 200,000 | 0.0174 | 0.0150 | 0.1216 | 0.0933 | (skipped – too slow) |
Complete-the-Code program (200,000 items): `+ = time: 0.0158 s   join time: 0.0068 s`, same text: True, length 3,048,890.
Doubling test of the un-optimisable `+=`: 10,000 → 0.017 s, 20,000 → 0.068 s (4.0×), 40,000 → 0.345 s (5.1×) = quadratic growth.

## What happened versus the prediction
- **Plain `+=` was *not* quadratic** (0.017 s for 200,000 lines): CPython has an optimisation – when the left string has only one reference, `+=` resizes it **in place** (amortised, like list append) instead of copying. My prediction of "+= is slow" was wrong for this simple loop; join was still faster (0.0068 s vs 0.0158 s in the assignment program).
- When another reference to the old string exists (`keep = text` in `build_plus_aliased`) the optimisation cannot be used and growth is quadratic as predicted.
- f-string lines are slower mainly because of the extra formatting work per line (width `:>6`, number conversion), not because of how they are joined.

## Characters copied (counts, from `run_q4.py`)
| n lines | chars copied by naive `+=` (every += copies all) | chars handled by join | ratio |
|---|---|---|---|
| 1,000 | 6,297,395 | 12,690 | 496× |
| 10,000 | 679,433,495 | 136,890 | 4,963× |
| 200,000 | 298,829,229,495 | 3,048,890 | 98,012× |

## Explanation: immutability and why join() is still recommended
Strings are immutable, so `text += x` cannot append to `text`; it must create a **new** string of length len(text)+len(x) and copy everything. Over n lines that is 1 + 2 + … + n copies = **O(n²)** characters. CPython hides this only in a special case (single reference, and only in the CPython implementation – PyPy and other Pythons do not do it, and the trick fails when a second reference exists, e.g. in a class attribute, a list item, or a debugging alias). `join()` first computes the total length, allocates once and copies each part once: **O(n)** in every Python, every situation. So join() is the dependable practice; `+=` is fast only by luck.

## Alternative concept: write line by line to a file, or io.StringIO
| 200,000 lines | time | peak extra memory |
|---|---|---|
| join (list of parts) | 0.0075 s | ~5.8 MiB |
| io.StringIO | 0.0201 s | ~6.5 MiB |
| write line by line to a file | 0.1475 s | ~52 KiB |
- **Time:** all O(n) in the number of characters (join: one pass; `+=` unoptimised: up to O(n²) characters copied). File writing is slower (≈20×) because of per-call I/O, but still linear.
- **Memory:** join and StringIO need O(total size) memory (list/buffer plus the final string); writing to a file keeps O(1) (about 52 KiB, just the file buffer). For 100,000+ line statements to be printed or emailed, streaming to a file is the memory-safe design; join is the fastest when the text must exist as one string.
