"""Q2 - OTP kiosk. Entries are SCRIPTED lists (so the demo is repeatable); `python otp.py --live` lets you type.
Correct OTP = 4821. Blank entries never count as an attempt."""
import sys

OTP = "4821"
MAX_ATTEMPTS = 3

def make_reader(entries):
    """Returns a function that gives the next scripted entry (stands in for input())."""
    it = iter(entries)
    return lambda prompt="": next(it, "")

def verify_while(read):
    """while-loop design. Returns (status, attempts_used, loop_iterations)."""
    attempts, iterations = 0, 0
    while attempts < MAX_ATTEMPTS:
        iterations += 1
        entry = read("OTP: ").strip()
        if entry == "":
            continue                          # blank: skip, attempts NOT increased
        attempts += 1                         # counter updated only after a real entry
        if entry == OTP:
            return "OK", attempts, iterations
        elif entry.upper() == "HELP":
            pass                              # placeholder: help screen not built yet (pass = do nothing)
    return "LOCKED 30 min", attempts, iterations

def verify_for(read):
    """for range(3) design: each pass is one attempt, so blanks are skipped by an INNER loop."""
    iterations = 0
    for attempt in range(MAX_ATTEMPTS):
        entry = ""
        while entry == "":                    # blank entries do not use up a pass of the for loop
            iterations += 1
            entry = read("OTP: ").strip()
            if iterations > 50:               # safety: stop kiosk if the customer keeps entering blanks
                return "TIMEOUT", attempt, iterations
        if entry == OTP:
            return "OK", attempt + 1, iterations
        # wrong entry: loop goes on to the next attempt
    else:                                     # loop-else: runs only when the loop ended WITHOUT break/return
        return "LOCKED 30 min", MAX_ATTEMPTS, iterations

def verify_for_break(read):
    """Same design written with break + loop-else (the textbook form)."""
    for attempt in range(MAX_ATTEMPTS):
        entry = read("OTP: ").strip()
        if entry == "":
            continue                          # NOTE: this burns a pass of range(3) -> blank counts as attempt (limitation)
        if entry == OTP:
            status = "OK"
            break
    else:
        status = "LOCKED 30 min"              # else clause: reached only if no break happened
    return status, attempt + 1

def verify_buggy_counter(read):
    """BUG: counter updated before the blank check -> blank entries count as attempts."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        attempts += 1                         # wrong place
        entry = read("OTP: ").strip()
        if entry == "":
            continue
        if entry == OTP:
            return "OK", attempts
    return "LOCKED 30 min", attempts

def verify_with_security_question(read, answered_correctly):
    """Changed condition: two extra attempts after a correct security answer (granted once)."""
    allowed, attempts, bonus_given = MAX_ATTEMPTS, 0, False
    while attempts < allowed:
        entry = read("OTP: ").strip()
        if entry == "":
            continue
        attempts += 1
        if entry == OTP:
            return "OK", attempts, allowed
        if attempts == MAX_ATTEMPTS and not bonus_given:      # 3 wrong attempts used
            bonus_given = True
            if answered_correctly():
                allowed += 2                                   # while re-reads `allowed` every time
    return "LOCKED 30 min", attempts, allowed

if __name__ == "__main__" and "--live" in sys.argv:
    print(verify_while(input))
