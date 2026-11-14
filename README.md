# CSA08-<RegisterNumber>-Assignment2 – Control flow, Strings, Functions

| | |
|---|---|
| Name | `<your name>` |
| Register number | `<your register number>` |
| Python version | 3.12 (match-case needs 3.10+) |
| Libraries | none to install – standard library only (see `requirements.txt`) |
| GitHub link | `<paste your repository link here>` |

> Replace the `<...>` parts and rename the folder to `CSA08-<RegisterNumber>-Assignment2` before pushing.

## How to use
1. Open this folder in VS Code (File → Open Folder). 2. Open the terminal, `cd` into a question folder and run the commands below. 3. Take a screenshot of every output and upload it into the matching folder on GitHub. 4. Commit one question at a time (`git add Q1`, `git commit -m "Q1: subsidy rules"`), because the commit history is checked.
Each folder has a `README.md` with the written answers (predictions, explanations, the *Alternative Concept and Complexity Analysis*, the tables of counts and times) and the code. Optional: `python run_all.py` runs everything. Timings change from computer to computer; **counts** (calls, comparisons, characters copied) do not – put your own numbers in the screenshots.

| Q | Topic | Run (inside the folder) | Main evidence |
|---|---|---|---|
| Q1 | Subsidy decisions | `python run_q1.py` · `python alternatives.py` | 8 predictions (8/8), double subsidy shown, 1,604-case check, k-slab timings |
| Q2 | OTP attempts | `python run_q2.py` · `python alternatives.py` | while vs for, break/continue/pass/loop-else, changed condition, recursion depth |
| Q3 | Plate validator | `python run_q3.py` · `python alternatives.py` | 6 predictions (6/6), immutability, slicing, regex comparison |
| Q4 | `+=` vs join | `python run_q4.py` · `python alternatives.py` | times at 1,000 / 10,000 / 200,000 lines, chars copied, memory |
| Q5 | Functions and scope | `python run_q5.py` · `python alternatives.py` | `__defaults__`, 3 customers, local/global/nonlocal |
| Q6 | Recursion | `python run_q6.py` · `python alternatives.py` | call counts 242,785 vs 26, call tree, RecursionError, n = 1000 |
| Q7 | Diagnose and redesign | `python run_q7.py` | linear → binary search: 502 → 10 comparisons at k = 1000 |

## Complete-the-Code locations
Q3: `Q3/plate.py` (TODO 1, 2) · Q4: `Q4/statement.py` (`build_join`, run in `run_q4.py`) · Q5: `Q5/canteen.py` (`add_item`) · Q6: `Q6/steps.py` (`ways_memo`).

## Short result note per question
1. Separate ifs gave household A two subsidies and F a wrong one; if-elif gives exactly one; flat elif with combined conditions chosen.
2. while is the natural loop (blanks and the extra-attempts rule); for-else works only for the fixed 3-attempt case; recursion costs O(a) stack.
3. All six predictions correct; strings are immutable so every operation returns a new string.
4. join is O(n); `+=` is only fast because CPython sometimes resizes in place; with a second reference it becomes quadratic (4×, 5× per doubling).
5. The default list is created once at `def` time – use `None`; each customer's order is independent.
6. Plain recursion 242,785 calls vs memo 26 calls for n = 25; memo hits RecursionError at n = 1000; loop is the deployment choice.
7. Binary search over sorted slab limits: 50× fewer comparisons and 19.7× faster at k = 1000, no gain at k = 3.
