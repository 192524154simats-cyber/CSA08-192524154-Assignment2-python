from plate import normalise, is_valid, format_for_receipt, process

# six inputs + what I PREDICTED before running: (input, predicted valid?, predicted receipt)
tests = [
    ("tn 09 ab 1234",   True,  "TN 09 AB 1234"),
    ("TN-09-AB-1234",   True,  "TN 09 AB 1234"),
    ("Tn09Ab1234",      True,  "TN 09 AB 1234"),
    ("  ka 05 m 4321 ", True,  "KA 05 M 4321"),      # one-letter series, extra spaces
    ("TN 9 AB 1234",    False, None),                # district has 1 digit -> length 8
    ("T1 09 AB 1234",   False, None),                # digit inside state code
]
print(f"{'input':<18}{'normalised':<14}{'pred':<7}{'valid':<7}{'receipt':<16}{'ok'}")
ok_all = 0
for text, pred_valid, pred_receipt in tests:
    reg, valid, receipt = process(text)
    ok = valid == pred_valid and receipt == pred_receipt
    ok_all += ok
    print(f"{text!r:<18}{reg:<14}{str(pred_valid):<7}{str(valid):<7}{str(receipt):<16}{'Y' if ok else 'N'}")
print(f"\nPredictions correct: {ok_all}/{len(tests)}")

print("\n--- More edge cases ---")
for text in ("", "TN09AB123", "TN09ABC1234", "TN09AB12345", "TN09AB12A4", "TN09AB1234\u00b2", "TN\u0663\u0664AB1234"):
    print(f"{text!r:<20} -> normalised {normalise(text)!r:<16} valid = {is_valid(normalise(text))}")

print("\n--- Immutability ---")
text = "tn09ab1234"
up = text.upper()
print("text         =", text, "(unchanged)")
print("text.upper() =", up, "(a NEW string)")
try:
    text[0] = "T"
except TypeError as e:
    print("text[0] = 'T' ->", type(e).__name__ + ":", e)
print("id(text) =", id(text), " id(up) =", id(up), "-> different objects")
text = text.upper()                                    # rebinding the NAME, not changing the string
print("after text = text.upper():", text)

print("\n--- Slicing: s[-4:] and s[4:-4] ---")
for s in ("TN09A1234", "TN09AB1234"):
    print(f"{s!r} (len {len(s)}): s[-4:] = {s[-4:]!r}, s[4:-4] = {s[4:-4]!r}")
