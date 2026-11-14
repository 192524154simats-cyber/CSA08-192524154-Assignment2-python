"""Optional helper: runs every non-interactive program. Usage: python run_all.py"""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).parent
PLAN = {"Q1": ["run_q1.py", "alternatives.py"], "Q2": ["run_q2.py", "alternatives.py"], "Q3": ["run_q3.py", "alternatives.py"],
        "Q4": ["run_q4.py", "alternatives.py"], "Q5": ["run_q5.py", "alternatives.py"], "Q6": ["run_q6.py", "alternatives.py"], "Q7": ["run_q7.py"]}
for folder, files in PLAN.items():
    for f in files:
        print(f"\n{'=' * 70}\n{folder}/{f}\n{'=' * 70}", flush=True)
        subprocess.run([sys.executable, f], cwd=ROOT / folder)
