# Q1 – Decisions with Many Boundaries (K4)

**Run (screenshot each):** `python run_q1.py` · `python alternatives.py`
Files: `subsidy.py` (all four implementations), `run_q1.py` (predictions vs observed), `alternatives.py` (match-case, slab table, timings).

## The rule (assumption: above 200 units with a member above 80 gets "subsidy")
| Units | Decision |
|---|---|
| ≤ 100 | subsidy |
| 101 – 200 | partial subsidy only with a ration card, else none |
| > 200 | none, unless a member is above 80 → subsidy |

## Predictions made BEFORE running (8 households)
| HH | units | ration | 80+ | Predicted (correct rule) | Predicted subsidies with separate ifs |
|---|---|---|---|---|---|
| A | 100 | yes | no | subsidy | **2** (slab-1 test and "≤200 and ration" are both true) |
| B | 100 | no | no | subsidy | 1 |
| C | 101 | yes | no | partial subsidy | 1 |
| D | 101 | no | no | none | 0 |
| E | 200 | yes | no | partial subsidy | 1 |
| F | 200 | no | yes | none | 1 (wrong: the "elder" test is not tied to units > 200) |
| G | 201 | no | no | none | 0 |
| H | 201 | no | yes | subsidy | 1 |
Observed: all 8 predictions were correct (output of `run_q1.py`). The separate-ifs version gave household A two subsidies and household F a wrong subsidy.

## Why separate `if` statements can give more than one result, `if–elif–else` exactly one
Every separate `if` is tested independently, so several conditions can be true at the same time (100 units + ration card satisfies "≤ 100" and "≤ 200 and ration"). In `if–elif–else` the chain stops at the **first** true condition; later branches are skipped, so exactly one branch runs. Writing the slabs in order (≤100, then 101–200, then the rest) also means the later conditions can assume the earlier ones were false.

## Chained comparison
`101 <= units <= 200` means `101 <= units and units <= 200` with `units` evaluated once – it reads like the rule in the problem.

## Design decision: nested if or combined Boolean conditions?
I implemented both (`decide_nested`, `decide_combined`) and checked them against the if-elif version on all 1,604 combinations (units 0–400 × ration × elder): 0 mismatches.
- **Nested**: 3 levels, 7 lines of `if/else` – every path is explicit but the rule is hidden in indentation, and one extra condition (a new slab) means re-indenting.
- **Combined (flat elif chain with `and`)**: one line per slab; each line is the sentence of the rule (`101 <= units <= 200 and ration`). Adding a slab or a condition changes one line.
**Choice:** a flat `if–elif–else` on the unit slabs, with a *combined* `and` condition (or a small conditional expression) inside the slab – the slab structure follows the problem statement and is the easiest to change. Nesting is reserved for decisions that only make sense inside another decision.

## Alternative concept: match–case or a table of (upper limit, decision) pairs
```python
match units:
    case u if u <= 100: ...        # match-case with guards
SLABS = [(100, rule1), (200, rule2), (inf, rule3)]
for limit, rule in SLABS:          # table searched in a loop
    if units <= limit: return rule(...)
```
Both agree with if–elif on all 1,604 cases.
- **Time per decision for k slabs:** all three are **O(k)** in the worst case (checked slab after slab). Measured worst case: if-elif chain 69 / 120 / 905 / 11,196 ns for k = 3 / 10 / 100 / 1000; table loop 177 / 284 / 2,610 / 35,195 ns. The loop is ~3× slower per slab (loop and tuple unpacking overhead) but both grow linearly. `match-case` with guards is also a sequential test, so it is O(k) too; match-case only helps when the patterns are literal values or structures, not numeric ranges.
- **Space:** if-elif and match-case: O(1) data (the rule is in the code, k conditions of code). Table: O(k) list of k pairs, but changing the rule means changing data, not code – and it allows a faster search (binary search, see Q7).
