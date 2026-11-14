# Q3 – Vehicle Registration Number Validator (K4)

**Run:** `python run_q3.py` · `python alternatives.py` (module: `plate.py`)
Complete-the-Code: TODO 1 (`normalise`) and TODO 2 (`is_valid`) are completed in `plate.py` using only string methods and slicing (`strip, replace, upper, len, isalpha, isdigit, isascii, join`); no `re`.

## The three functions
- `normalise(text)`: `strip()` the ends, `replace(" ", "")`, `replace("-", "")`, `upper()` → `'TN09AB1234'`.
- `is_valid(reg)`: length is 9 or 10; `reg[:2].isalpha()`, `reg[2:4].isdigit()`, `reg[4:-4].isalpha()` (the 1–2 series letters; the slice is whatever remains between position 4 and the last 4 characters), `reg[-4:].isdigit()`. `isascii()` is added because `isalpha()`/`isdigit()` also accept other alphabets and digits such as `²` or Arabic-Indic `٣`.
- `format_for_receipt(reg)`: `" ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])` → `'TN 09 AB 1234'`.

## Predictions (made before running) and result – 6/6 correct
| Input | Predicted | Observed normalised | Receipt |
|---|---|---|---|
| `tn 09 ab 1234` | valid | TN09AB1234 | TN 09 AB 1234 |
| `TN-09-AB-1234` | valid | TN09AB1234 | TN 09 AB 1234 |
| `Tn09Ab1234` | valid | TN09AB1234 | TN 09 AB 1234 |
| `  ka 05 m 4321 ` (1-letter series) | valid | KA05M4321 | KA 05 M 4321 |
| `TN 9 AB 1234` (1-digit district) | **rejected** (length 9 but `reg[2:4]`='9A' is not digits) | TN9AB1234 | – |
| `T1 09 AB 1234` (digit in state) | **rejected** | T109AB1234 | – |
Extra edge cases (empty, too short/long, wrong character in last 4, `²`, Arabic digits) are all rejected.

## Inquiry / Explain
**Why are strings immutable?** A string's characters cannot be changed after creation (`text[0] = 'T'` → `TypeError`). Reasons: strings can then be shared safely between names, used as dictionary keys (their hash never changes), cached/interned, and are thread-safe. Any "change" creates a new string.

**Why does `text.upper()` not change `text`?** Because of immutability, `upper()` builds and returns a **new** string; `text` is untouched (the program shows two different `id()`s). To keep the result you must rebind: `text = text.upper()` – this makes the *name* point to the new string.

**`s[-4:]` and `s[4:-4]`** (from the run):
| s | len | `s[-4:]` | `s[4:-4]` |
|---|---|---|---|
| `TN09A1234` | 9 | `1234` | `A` (1 series letter) |
| `TN09AB1234` | 10 | `1234` | `AB` (2 series letters) |
`s[-4:]` = the last four characters; `s[4:-4]` = from index 4 up to (not including) the 4th from the end – the series, whose length is len − 8 (1 or 2).

## Alternative concept: `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)`
- **Same decisions:** 0 differences on 100,000 random plates (43,038 valid). The ASCII behaviour matches because `[0-9]` only means ASCII digits.
- **Time:** both are O(L) for a number of length L (L ≤ 10 here, so effectively O(1)). Measured per check: slicing 324 ns, `re.fullmatch` 432 ns, compiled pattern 197 ns.
- **Readability and change:** the pattern states the whole format in one line and is quick to change (e.g. `{1,3}` letters), but needs regex knowledge and gives no reason for rejection. The slicing version is longer, but each part has a name/comment and the code can report *which* part failed; it needs `len` and slice edits when the format changes. Space: O(1) both (compiled regex keeps a small pattern object).
