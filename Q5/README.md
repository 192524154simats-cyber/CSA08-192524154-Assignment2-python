# Q5 – Functions, Parameters and Scope (K4)

**Run:** `python run_q5.py` · `python alternatives.py`  (functions in `canteen.py`)
Complete-the-Code: TODO 1 done in `add_item`; output exactly as expected:
```
['Tea', 'Vada'] ['Tea', 'Vada']
['Tea'] ['Vada']
```

## Explaining the bug (principle: a default value is created once, when the function is *defined*)
`def add_item_buggy(item, order=[])` creates the empty list **once**, when Python executes the `def`. It is stored in the function object. Every call that does not pass `order` receives **that same list**, so the next customer sees the previous customer's items. Proof from the program:
- `add_item_buggy.__defaults__` after the calls prints `(['Tea', 'Vada'],)` – the default list itself has been changed and carries the old orders.
- `a is b` → `True`: two later calls returned the same list object.
- `add_item.__defaults__` is `(None,)` – `None` is immutable and never changes. The fix: use `None` as the "no order yet" signal and create `[]` **inside** the function body, which runs on every call.

## Parameter kinds (when to use)
- **Positional** – the main, obvious values in a natural order: `add_to_order("Tea", 2)`.
- **Keyword** – clearer for optional or easily mixed-up values: `add_to_order("Vada", order=None, quantity=4)`, `bill(order, gst_rate=18)`.
- **Default** – a sensible usual value (`quantity=1`, `gst_rate=GST_RATE`); mutable defaults (`[]`, `{}`) must never be used – use `None`.

## Returning more than one value
`bill(order)` returns `subtotal, gst, total` – Python packs them as a **tuple**, and the caller unpacks: `sub, gst, total = bill(order)`. Customer 1: subtotal 35, GST 1.75, total 36.75.

## Local, global, nonlocal (all demonstrated in `run_q5.py`)
| Kind | Demo | Result |
|---|---|---|
| local | `x` inside `local_demo()` | outside the function → `NameError` |
| global (read) | `read_global()` | works without a keyword |
| global (change) | `change_global_wrong()` assigns `counter_global = 99` | creates a **new local**; the global stays 0 |
| `global` keyword | `change_global_right()` | global becomes 1 |
| `nonlocal` | `make_counter()` inner function does `nonlocal count; count += 1` | 1, 2, 3 – rebinding an enclosing function's variable |
**Why `global` is needed to change a global:** an assignment inside a function always creates a local name, unless `global` says otherwise. **Why avoid it:** any function can silently change shared state, so results depend on call order, the function cannot be tested on its own, and bugs (like the shared default list) are hard to trace. Prefer parameters and return values.

## Test: three customers in sequence (output)
| Customer | Order | Subtotal | GST 5 % | Total |
|---|---|---|---|---|
| 1 | Tea 2, Vada 1 | 35 | 1.75 | 36.75 |
| 2 | Dosa 1 | 40 | 2.00 | 42.00 |
| 3 | Coffee 3, Tea 1, Dosa 2 | 126 | 6.30 | 132.30 |
Customer 1's order has no Dosa and the three dictionaries are different objects (`is not` checks print True) – each order is independent.

## Alternative concept: explicit list from the caller, or a closure
```python
def add_explicit(item, order):  order.append(item); return order      # caller always passes the list
def make_taker():                                                      # closure keeps the order
    order = []
    def add(item): order.append(item); return order
    return add
```
- **Time:** O(1) per item in all three (list append): measured about 35-45 ns for all three (default None slowest by a few ns, closure fastest; differences are within timing noise).
- **Space per customer:** list of m items = O(m) in all designs. Measured for 10,000 customers × 10 items: default and explicit ≈ 192 bytes per customer; closure ≈ 440 bytes per customer (extra function object and cell).
- **Design:** explicit passing is simplest and makes data flow visible but puts the burden on every caller (forget it → TypeError, not a silent bug); closure hides the order and gives each customer private state, at a bit more memory; `None` default is the most convenient for callers.
