// Percent Math engine - percent change, undoing a change, and percentage points.
// Mirrored by oracle.py; keep the op order identical.
// Numbers are rounded to hundredths on the way in; percents come out to hundredths of a percent.

function _h(x, msg, min, max, allowZero) {
  if (!isFinite(x) || x < min || x > max || (!allowZero && x === 0)) throw new Error(msg);
  return Math.floor(x * 100 + 0.5);
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

// n/d as hundredths of a percent, rounded half up on the size, with its sign kept apart.
function _ratio(n, d) {
  var a = Math.abs(n);
  return Math.floor((2 * a * 10000 + d) / (2 * d));
}

function _move(r, sign) {
  if (r === 0) return sign === 0 ? "no change" : (sign > 0 ? "up less than 0.01%" : "down less than 0.01%");
  return (sign > 0 ? "up " : "down ") + _fmt(r) + "%";
}

// The change truth: percent change from one number to another.
function changeTruth(from, to) {
  var f = _h(from, "starting number must be between 0 and 1000000, over 0", 0, 1000000, false);
  var t = _h(to, "new number must be between 0 and 1000000", 0, 1000000, true);
  var n = t - f;
  var r = _ratio(n, f);
  var sign = n === 0 ? 0 : (n > 0 ? 1 : -1);
  return "From " + _fmt(f) + " to " + _fmt(t) + ": " + _move(r, sign) + ".";
}

// The undo truth: the opposite change that gets back to the start.
function undoTruth(percent, direction) {
  if (direction !== "up" && direction !== "down") throw new Error("direction must be up or down");
  var p = _h(percent, "percent must be between 0 and 100000, over 0", 0, 100000, false);
  var q;
  if (direction === "up") {
    q = Math.floor((2 * p * 10000 + (10000 + p)) / (2 * (10000 + p)));
    return "A rise of " + _fmt(p) + "% is undone by a fall of " + _fmt(q) + "%.";
  }
  if (p >= 10000) throw new Error("a fall must be under 100%");
  q = Math.floor((2 * p * 10000 + (10000 - p)) / (2 * (10000 - p)));
  return "A fall of " + _fmt(p) + "% is undone by a rise of " + _fmt(q) + "%.";
}

// The point truth: percentage points between two rates, and the relative change.
function pointTruth(first, second) {
  var a = _h(first, "first rate must be above 0 and at most 100", 0, 100, false);
  var b = _h(second, "second rate must be from 0 to 100", 0, 100, true);
  var d = b - a;
  if (d === 0) return "From " + _fmt(a) + "% to " + _fmt(b) + "%: no change.";
  var abs = Math.abs(d);
  var unit = abs === 100 ? " percentage point" : " percentage points";
  var rel = _ratio(d, a);
  var dir = d > 0 ? "up " : "down ";
  return "From " + _fmt(a) + "% to " + _fmt(b) + "%: " + dir + _fmt(abs) + unit + ", " + dir + _fmt(rel) + "% relative.";
}
