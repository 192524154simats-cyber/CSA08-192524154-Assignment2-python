# Q2 – Loops that Count Attempts (K3)

**Run:** `python run_q2.py` · `python alternatives.py` (optional: `python otp.py --live`)
Customer typing is **scripted** in lists so the output is repeatable; the correct OTP is `4821`.

## Designs
| Design | Idea |
|---|---|
| `verify_while` | `while attempts < 3:` read entry; blank → `continue` (counter untouched); then `attempts += 1`; right → return OK |
| `verify_for` | `for attempt in range(3):` one pass = one attempt; blank handled by an **inner** `while entry == ""`; the loop's **`else:`** locks the account |
| `verify_for_break` | textbook form: `for … break … else:` (loop-else runs only if no `break`) |

## break, continue, pass, loop-else (where each is needed)
- `continue` – skip the rest of this pass: used for a **blank** entry in the while design (not counted).
- `break` (or `return`) – leave the loop at once when the OTP is right, so the lock code is skipped.
- `pass` – a placeholder that does nothing: the `HELP` branch is not built yet, so `pass` keeps the code valid.
- `else` on the loop – runs **only if the loop finished without `break`**, i.e. three attempts used up → "LOCKED 30 min". No flag variable is needed.

## Observed (from `run_q2.py`): (status, attempts used, loop iterations)
| Scenario | while | for + inner while |
|---|---|---|
| right on 1st | OK, 1, 1 | OK, 1, 1 |
| wrong, wrong, right | OK, 3, 3 | OK, 3, 3 |
| three wrong | LOCKED, 3, 3 | LOCKED, 3, 3 |
| blank, wrong, blank, right | OK, 2 attempts, 4 iterations | OK, 2, 4 |
| wrong, blank, wrong, wrong | LOCKED, 3 attempts, 4 iterations | LOCKED, 3, 4 |
The blank entries add **iterations but not attempts**.
The simple `for … continue` form (`verify_for_break`) shows the limitation of `range(3)`: `continue` still uses up a pass, so the blank-then-right scenario is wrongly **LOCKED**.

## Answers
**When is while more natural?** When the number of passes is not fixed in advance or can change while the loop runs: blanks that do not count, and the changed condition (extra attempts). `for range(3)` is natural only when the count is exactly fixed and every pass is one attempt.

**Bug when the counter is updated in the wrong place:** `verify_buggy_counter` increments `attempts` *before* the blank check. Scenario "blank, wrong, blank, right" → buggy result `LOCKED (3 attempts)`, correct result `OK (2 attempts)`: a customer who pressed Enter twice is locked out. (Updating after the right/wrong test, or not at all on `continue`, causes the opposite bug: unlimited tries.)

## Changed condition: two extra attempts after a correct security answer
`verify_with_security_question`: `allowed` is a variable that starts at 3; after the 3rd wrong attempt, if the security answer is correct, `allowed += 2` (granted once). The loop condition `attempts < allowed` re-reads `allowed` every pass, so the **while design adapts with a one-line change**. A `for … in range(3)` loop fixed the count when it started; it would need a second loop (`range(2)`) or to be rewritten as a while. Observed: 3 wrong + correct answer + right on 5th → OK; all 5 wrong → LOCKED with 5 attempts; wrong security answer → LOCKED after 3.
Re-evaluation: **keep the while design**, the for-range design is now the weaker choice.

## Alternative concept: recursion (`alternatives.py`)
```python
def verify_recursive(read, attempts_left=3):
    if attempts_left == 0: return "LOCKED"
    entry = read()
    if entry == "": return verify_recursive(read, attempts_left)       # blank
    if entry == OTP: return "OK"
    return verify_recursive(read, attempts_left - 1)                    # next attempt
```
| a attempts | loop iterations | recursive calls | stack depth |
|---|---|---|---|
| 3 | 3 | 4 | 4 |
| 50 | 50 | 51 | 51 |
| 500 | 500 | 501 | 501 |
- **Time:** O(a) in all versions (one pass or one call per attempt); recursion has a larger constant (function-call cost: 201 µs vs 70 µs at a = 500).
- **Space:** loop O(1); recursion **O(a)** stack frames (depth = a + 1). With a = 5000 Python raises `RecursionError` (limit 1000). For a bank with a = 3 the cost is nothing, but a loop is the safer design for the kiosk.
