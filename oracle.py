#!/usr/bin/env python3
# Percent Math oracle - mirrors engine.js.
import json, math

def _h(x, msg, lo, hi, allow_zero):
    if not math.isfinite(x) or x < lo or x > hi or (not allow_zero and x == 0):
        raise ValueError(msg)
    return math.floor(x * 100 + 0.5)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _ratio(n, d):
    return (2 * abs(n) * 10000 + d) // (2 * d)

def _move(r, sign):
    if r == 0:
        return "no change" if sign == 0 else ("up less than 0.01%" if sign > 0 else "down less than 0.01%")
    return ("up " if sign > 0 else "down ") + _fmt(r) + "%"

def change_truth(frm, to):
    f = _h(frm, "starting number must be between 0 and 1000000, over 0", 0, 1000000, False)
    t = _h(to, "new number must be between 0 and 1000000", 0, 1000000, True)
    n = t - f
    r = _ratio(n, f)
    sign = 0 if n == 0 else (1 if n > 0 else -1)
    return f"From {_fmt(f)} to {_fmt(t)}: {_move(r, sign)}."

def undo_truth(percent, direction):
    if direction not in ("up", "down"):
        raise ValueError("direction must be up or down")
    p = _h(percent, "percent must be between 0 and 100000, over 0", 0, 100000, False)
    if direction == "up":
        q = (2 * p * 10000 + (10000 + p)) // (2 * (10000 + p))
        return f"A rise of {_fmt(p)}% is undone by a fall of {_fmt(q)}%."
    if p >= 10000:
        raise ValueError("a fall must be under 100%")
    q = (2 * p * 10000 + (10000 - p)) // (2 * (10000 - p))
    return f"A fall of {_fmt(p)}% is undone by a rise of {_fmt(q)}%."

def point_truth(first, second):
    a = _h(first, "first rate must be above 0 and at most 100", 0, 100, False)
    b = _h(second, "second rate must be from 0 to 100", 0, 100, True)
    d = b - a
    if d == 0:
        return f"From {_fmt(a)}% to {_fmt(b)}%: no change."
    ab = abs(d)
    unit = " percentage point" if ab == 100 else " percentage points"
    rel = _ratio(d, a)
    dr = "up " if d > 0 else "down "
    return f"From {_fmt(a)}% to {_fmt(b)}%: {dr}{_fmt(ab)}{unit}, {dr}{_fmt(rel)}% relative."

FNS = {"changeTruth": change_truth, "undoTruth": undo_truth, "pointTruth": point_truth}

CASES = [
    ("changeTruth", [80, 100]), ("changeTruth", [100, 80]), ("changeTruth", [100, 100]), ("changeTruth", [100, 0]),
    ("changeTruth", [3, 4]), ("changeTruth", [0.01, 0.02]), ("changeTruth", [1000000, 999999.99]), ("changeTruth", [7, 7.5]),
    ("changeTruth", [1000000, 1000000.01]), ("changeTruth", [0, 5]), ("changeTruth", [5, -1]), ("changeTruth", [1000001, 5]),
    ("changeTruth", [5, 1000001]),
    ("undoTruth", [25, "up"]), ("undoTruth", [20, "down"]), ("undoTruth", [50, "up"]), ("undoTruth", [50, "down"]),
    ("undoTruth", [100, "up"]), ("undoTruth", [100, "down"]), ("undoTruth", [99, "down"]), ("undoTruth", [0.5, "up"]),
    ("undoTruth", [100000, "up"]), ("undoTruth", [100001, "up"]), ("undoTruth", [0, "up"]), ("undoTruth", [-5, "down"]),
    ("undoTruth", [25, "sideways"]), ("undoTruth", [33.33, "up"]),
    ("pointTruth", [4, 6]), ("pointTruth", [6, 4]), ("pointTruth", [5, 6]), ("pointTruth", [5, 5]), ("pointTruth", [10, 0]),
    ("pointTruth", [0.5, 1]), ("pointTruth", [100, 0]), ("pointTruth", [3, 3.01]), ("pointTruth", [0, 5]), ("pointTruth", [5, 101]),
    ("pointTruth", [101, 5]), ("pointTruth", [5, -1]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
