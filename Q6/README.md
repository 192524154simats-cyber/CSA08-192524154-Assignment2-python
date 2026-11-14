# Q6 – Recursion and Its Limits (K5)

**Run:** `python run_q6.py` · `python alternatives.py`  (functions in `steps.py`)
Complete-the-Code: TODO 1 done in `ways_memo`; output matches the expected values:
```
naive: 121393 calls = 242785
memo: 121393 calls = 26
```

## Recursive design
- **Base case:** `n <= 1` → 1 way (0 steps left: already at the top; 1 step: one way).
- **Recursive case:** the last move was 1 step or 2 steps → `ways(n) = ways(n-1) + ways(n-2)`.
- This is the Fibonacci pattern: `ways(n) = 1, 2, 3, 5, 8, 13, …`

## Correctness check (n = 1…6)
By hand: ways(1)=1, ways(2)=2 (1+1, 2), ways(3)=3 (111, 12, 21), ways(4)=5, ways(5)=8, ways(6)=13. The program (naive, memo, loop) gave the same six values – all OK.

## Why plain recursion repeats work – call tree for n = 5 (15 calls; printed by the program)
```
ways(5)
  ways(4)
    ways(3)
      ways(2)
        ways(1)
        ways(0)
      ways(1)
    ways(2)
      ways(1)
      ways(0)
  ways(3)
    ways(2)
      ways(1)
      ways(0)
    ways(1)
```
`ways(3)` is computed 2 times, `ways(2)` 3 times, `ways(1)` 5 times. Each repeated call repeats its whole sub-tree, so the repetition grows with n.
**Memoisation** (a dictionary or `@lru_cache`) stores each result the first time: `ways(k)` is computed once, later calls just look it up. The tree collapses to a single chain of n + 1 computations.

## Growth investigation – prediction vs count
Prediction: naive calls = 2·ways(n) − 1 (every non-leaf call makes two calls); memo computations = n + 1.
| n | ways(n) | predicted naive calls | counted naive | predicted memo | counted memo |
|---|---|---|---|---|---|
| 10 | 89 | 177 | 177 | 11 | 11 |
| 20 | 10,946 | 21,891 | 21,891 | 21 | 21 |
| 25 | 121,393 | 242,785 | 242,785 | 26 | 26 |
| 30 | 1,346,269 | 2,692,537 | 2,692,537 | 31 | 31 |
Both predictions were exact. (A dictionary version that counts cache *hits* too makes 2n − 1 calls: 19, 39, 49, 59.) Measured time for plain recursion: n = 30 → 0.26 s, n = 32 → 0.58 s, n = 34 → 1.44 s: each +2 steps multiplies the time by ≈ φ² ≈ 2.6.

## Deployment decision: n = 1,000
`ways_memo(1000)` → **`RecursionError: maximum recursion depth exceeded`**. `sys.getrecursionlimit()` is **1000**: Python allows only about 1000 nested calls. The first call goes down the chain 1000 → 999 → … → 1, each waiting for the next, so ~1000 frames (plus the frames already used by the script) exceed the limit. Memoisation removed the repeated *work* but not the *depth*.
| Option | Result for n = 1000 | Comment |
|---|---|---|
| raise limit `sys.setrecursionlimit(5000)` | works: 209 digits, 1,001 calls, 0.62 ms | quick fix, but each frame uses memory; a very large limit can crash the interpreter (stack overflow) |
| warm-up (call ways_memo(100), (200)… first) | works at the default limit, 0.30 ms | cache fills from below so depth stays ~100; a trick that must be remembered |
| **loop with two variables** | works: 0.05 ms, O(1) extra space | no depth limit; n = 5000 → 1,045 digits in 0.6 ms |
**Decision:** for the trust's program (n up to 1,000) use the **loop** in production – it needs no stack, is fastest and cannot hit the limit; keep the memoised recursive version as the readable specification and as a test oracle (the two agree). Raising the limit alone is not recommended because it only moves the failure point (n ≈ 5000) and risks a crash.

## Alternative concept: loop keeping only the last two values
```python
prev, cur = 1, 1
for _ in range(n - 1): prev, cur = cur, prev + cur
```
| Version | Time | Space | n = 1000 |
|---|---|---|---|
| plain recursion | O(φⁿ), φ ≈ 1.618 | O(n) stack | **not run**: ≈ 1.4×10²⁰⁹ calls, ≈ 10²⁰² seconds estimated from 79 ns/call |
| memoised recursion | O(n) | O(n) cache + O(n) stack | 1,001 calls, 0.6 ms (limit raised) |
| loop | O(n) | O(1) (two numbers) | 0.05 ms |
(Arithmetic on the 209-digit numbers costs a little more than on small ints, but all three formulas count additions the same way.)
