# Percent Math

Percent change arithmetic. Up 25% and down 25% do not cancel.

## What it computes

- **The change truth** - percent change from one number to another: from 80 to 100 is up 25%.
- **The undo truth** - the opposite change that gets back to the start: a 25% rise is undone by a 20% fall.
- **The point truth** - the gap between two rates in percentage points, and the change relative to the first rate: 4% to 6% is up 2 points, up 50% relative.

Results are rounded to hundredths of a percent.

## Boundary

Arithmetic only. Percent Math works out percent change, the opposite change, and percentage points from the numbers you type. It does not say whether a change is large, good or meaningful. You decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (39 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/percentmath/
Repo: https://github.com/iLanis-agent/percentmath
