"""
Splits and dividends -> price adjustment factors for NYSE, computed from the RAW prices at build time (never applied twice, can be recomputed at any time).

Events come from Yahoo through the fetcher (data/events/splits.csv, dividends.csv, converted to raw units):
  SPLIT     num:den (4:1 = 4 new shares for 1 old)  -> factor den/num for every row BEFORE the ex-date   (reverse split 1:10 gives 10)
  DIVIDEND  amount in raw dollars                   -> factor 1 - amount / last raw close before the ex-date   (total-return style, like the NSE engine)
data/manual_adjustments.json  {"JPM": [{"ex_date": "2020-01-02", "factor": 0.9, "description": "..."}]}
  an entry with "replace": true first cancels every computed event of that ticker + ex-date (factor 1.0 = ignore it).
data/reports/ lists raw price jumps that no split explains (Yahoo missed an event, or a real crash) for you to check.

Dividends bigger than half the price are skipped (DIVIDEND_MIN_FACTOR). ADJUST_DIVIDENDS=false switches dividends off.
"""
import hashlib
import json
import os
import sys
from collections import OrderedDict
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rawstore
from common import period_of, period_sort_key, DATA_DIR, FACTORS_FILE, EVENTS_DIR

MANUAL_FILE = os.getenv("MANUAL_FILE", os.path.join(DATA_DIR, "manual_adjustments.json"))
REPORT_DIR = os.getenv("REPORT_DIR", os.path.join(DATA_DIR, "reports"))
SPLITS_FILE = os.path.join(EVENTS_DIR, "splits.csv")
DIVS_FILE = os.path.join(EVENTS_DIR, "dividends.csv")
ROUND_TO = int(os.getenv("PRICE_ROUND", "4") or 4)
MIN_FACTOR = float(os.getenv("DIVIDEND_MIN_FACTOR", "0.5") or 0.5)
JUMP_LOW, JUMP_HIGH = float(os.getenv("JUMP_LOW", "0.55") or 0.55), float(os.getenv("JUMP_HIGH", "1.8") or 1.8)


def _on(name, default="true"):
    return os.getenv(name, default).strip().lower() not in ("0", "false", "no", "off")


def load_events():
    """-> DataFrame(scrip_code, ex_date, type, parsed, amount); the column is called scrip_code because the build code is shared with the BSE engine."""
    rows = []
    if os.path.exists(SPLITS_FILE):
        for r in pd.read_csv(SPLITS_FILE, dtype={"symbol": str, "date": str}).itertuples(index=False):
            if r.num and r.den and r.num > 0 and r.den > 0 and r.num != r.den:
                rows.append((r.symbol, r.date, "SPLIT", float(r.den) / float(r.num), np.nan))
    if os.path.exists(DIVS_FILE) and _on("ADJUST_DIVIDENDS"):
        for r in pd.read_csv(DIVS_FILE, dtype={"symbol": str, "date": str}).itertuples(index=False):
            if r.amount and r.amount > 0:
                rows.append((r.symbol, r.date, "DIVIDEND", np.nan, float(r.amount)))
    df = pd.DataFrame(rows, columns=["scrip_code", "ex_date", "type", "parsed", "amount"])
    return df.sort_values(["ex_date", "scrip_code"]).reset_index(drop=True) if len(df) else df


class RawLookup:
    def __init__(self, periods, keep=4):
        self.keep = keep
        self.periods = sorted(periods, key=period_sort_key)
        self.cache = OrderedDict()

    def _groups(self, p):
        if p in self.cache:
            self.cache.move_to_end(p)
            return self.cache[p]
        df = rawstore.read_period(p, columns=["scrip_code", "date", "close"]).sort_values(["scrip_code", "date"])
        g = {c: (x["date"].values.astype("U10"), x["close"].values.astype("float64")) for c, x in df.groupby("scrip_code")}
        self.cache[p] = g
        while len(self.cache) > self.keep:
            self.cache.popitem(last=False)
        return g

    def before(self, code, ex):
        """Last positive raw close before ex, or None."""
        pk = period_sort_key(period_of(ex))
        for p in [p for p in self.periods if period_sort_key(p) <= pk][::-1][:4]:
            hit = self._groups(p).get(code)
            if hit is None:
                continue
            dates, close = hit
            i = int(np.searchsorted(dates, ex, side="left")) - 1
            while i >= 0 and not close[i] > 0:
                i -= 1
            if i >= 0:
                return float(close[i])
        return None


def compute_event(look, code, ex, typ, parsed, amount):
    """-> (factor or None, note)"""
    if typ == "SPLIT":
        return float(parsed), ""
    cum = look.before(code, ex)
    if not cum:
        return None, "no price before the ex-date (nothing to adjust)"
    f = 1.0 - amount / cum
    if f < MIN_FACTOR:
        return None, f"dividend {amount:g} is {100 * amount / cum:.0f}% of price {cum:.2f}"
    return f, ""


def load_manual():
    cols = ["scrip_code", "ex_date", "type", "factor", "amount", "override"]
    if not os.path.exists(MANUAL_FILE):
        return pd.DataFrame(columns=cols)
    rows = []
    for code, evs in json.load(open(MANUAL_FILE, encoding="utf-8")).items():
        for e in evs:
            f = float(e.get("factor", 1))
            if 0 < f < 500 and e.get("ex_date"):
                rows.append((str(code).upper(), e["ex_date"], "MANUAL", f, 0.0, bool(e.get("replace", False))))
    return pd.DataFrame(rows, columns=cols)


def load_factor_cache():
    if not os.path.exists(FACTORS_FILE):
        return pd.DataFrame(columns=["scrip_code", "ex_date", "type", "key", "factor", "amount", "status", "note"])
    return pd.read_csv(FACTORS_FILE, dtype={"scrip_code": str, "key": str, "note": str, "status": str})


def compute_all(periods, asof=None, force=False, known_codes=None, dividend_cutoff=None):
    """Incremental: only new events are looked up. Returns (factors, report_lines).
    factors = DataFrame(scrip_code, ex_date, factor), one row per (ticker, ex-date), several events multiplied.
    Dividends with an ex-date AFTER dividend_cutoff are left out (the weekly run moves the cutoff forward)."""
    events = load_events()
    if known_codes is not None and len(events):
        events = events[events["scrip_code"].isin(known_codes)]
    cache = load_factor_cache()
    if force:
        cache = cache.iloc[0:0]
    asof = asof or datetime.now().strftime("%Y-%m-%d")
    report = []
    if len(events):
        events["key"] = events["amount"].fillna(0).round(6).astype(str) + "|" + events["parsed"].fillna(0).round(8).astype(str)
        done = {(r.scrip_code, r.ex_date, r.type, r.key): r for r in cache.itertuples(index=False) if r.status == "ok"}
        look = RawLookup(periods)
        rows, new_ok, new_skip, future = [], 0, 0, 0
        for r in events.itertuples(index=False):
            k = (r.scrip_code, r.ex_date, r.type, r.key)
            if k in done:
                d = done[k]
                rows.append((r.scrip_code, r.ex_date, r.type, r.key, d.factor, d.amount, d.status, d.note))
                continue
            if r.ex_date > asof:
                future += 1
                continue
            f, note = compute_event(look, r.scrip_code, r.ex_date, r.type, r.parsed, r.amount)
            amt = 0.0 if pd.isna(r.amount) else float(r.amount)
            if f is None:
                new_skip += 1
                rows.append((r.scrip_code, r.ex_date, r.type, r.key, np.nan, amt, "skip", note))
            else:
                new_ok += 1
                rows.append((r.scrip_code, r.ex_date, r.type, r.key, float(f), amt, "ok", note))
        cache = pd.DataFrame(rows, columns=["scrip_code", "ex_date", "type", "key", "factor", "amount", "status", "note"])
        report.append(f"events: {len(events)}; newly computed ok={new_ok} skipped={new_skip}; future ex-date={future}")
    os.makedirs(os.path.dirname(FACTORS_FILE) or ".", exist_ok=True)
    cache.to_csv(FACTORS_FILE, index=False)
    ok = cache[cache["status"] == "ok"]
    if dividend_cutoff:
        late = (ok["type"] == "DIVIDEND") & (ok["ex_date"] > dividend_cutoff)
        if late.any():
            report.append(f"{int(late.sum())} dividend(s) with ex-date after {dividend_cutoff} wait for the weekly run")
        ok = ok[~late]
    man = load_manual()
    if len(man) and man["override"].any():
        rep = set(zip(man.loc[man["override"], "scrip_code"], man.loc[man["override"], "ex_date"]))
        ok = ok[[(c, e) not in rep for c, e in zip(ok["scrip_code"], ok["ex_date"])]]
    fac = pd.concat([ok[["scrip_code", "ex_date", "type", "factor", "amount"]], man[["scrip_code", "ex_date", "type", "factor", "amount"]]], ignore_index=True)
    skipped = cache[cache["status"] == "skip"]
    if len(skipped):
        report.append(f"skipped events by type: {skipped['type'].value_counts().to_dict()}")
    if fac.empty:
        return pd.DataFrame(columns=["scrip_code", "ex_date", "factor"]), report or ["no events"]
    fac = fac.groupby(["scrip_code", "ex_date"], as_index=False).agg(factor=("factor", "prod"))
    return fac, report


class Adjuster:
    """adjust(df) multiplies open/high/low/close of each row by the product of the factors of that ticker's events with ex-date AFTER the row's date."""

    def __init__(self, factors):
        self.by_code, self.sig = {}, {}
        if factors is not None and len(factors):
            for code, g in factors.sort_values("ex_date").groupby("scrip_code"):
                ex = np.array(g["ex_date"].values, dtype="datetime64[D]")
                f = g["factor"].values.astype("float64")
                self.by_code[code] = (ex, np.append(np.cumprod(f[::-1])[::-1], 1.0))
                self.sig[code] = hashlib.sha1("".join(f"{e}|{x:.8f};" for e, x in zip(g["ex_date"], f)).encode()).hexdigest()[:12]

    def __bool__(self):
        return bool(self.by_code)

    def signature_for(self, codes):
        return hashlib.sha1("".join(f"{c}:{self.sig[c]};" for c in sorted(codes) if c in self.sig).encode()).hexdigest()[:16]

    def adjust(self, df):
        """df needs scrip_code, date, open, high, low, close. Returns an adjusted copy."""
        if not self.by_code or df.empty:
            return df
        df = df.copy()
        mult = np.ones(len(df))
        codes = df["scrip_code"].values
        dates = df["date"].values
        for code in set(self.by_code) & set(np.unique(codes)):
            idx = np.nonzero(codes == code)[0]
            ex, suffix = self.by_code[code]
            mult[idx] = suffix[np.searchsorted(ex, np.asarray(dates[idx], dtype="datetime64[D]"), side="right")]
        hit = mult != 1.0
        if hit.any():
            for c in ("open", "high", "low", "close"):
                df.loc[hit, c] = np.round(df.loc[hit, c].values * mult[hit], ROUND_TO)
        return df


# ----------------------------------------------------------------------------------------------------------------------
# review: raw price jumps that no split explains
# ----------------------------------------------------------------------------------------------------------------------
_NICE = sorted({b / (a + b) for a in range(1, 11) for b in range(1, 11)} | {1.0 / k for k in range(2, 21)} | {1.5, 2.0, 3.0, 4.0, 5.0, 10.0})


def nearest_ratio(r):
    return min(_NICE, key=lambda c: abs(r / c - 1))


def write_review(periods, names=None):
    """data/reports/review_jumps.csv + adjustment_review.md: one-day RAW close moves below JUMP_LOW or above JUMP_HIGH with no split event on that day
    (Yahoo may have missed a split / spin-off, or it is a real crash). Look at them; fix real misses in data/manual_adjustments.json."""
    names = names or {}
    sp = pd.read_csv(SPLITS_FILE, dtype=str) if os.path.exists(SPLITS_FILE) else pd.DataFrame(columns=["symbol", "date"])
    split_days = set(zip(sp["symbol"], sp["date"]))
    man = load_manual()
    handled = set(zip(man["scrip_code"], man["ex_date"]))
    rows, tail = [], None
    for p in sorted(periods, key=period_sort_key):
        df = rawstore.read_period(p, columns=["scrip_code", "date", "close"])
        df = df[df["close"] > 0]
        if tail is not None:
            df = pd.concat([tail, df], ignore_index=True)
        df = df.sort_values(["scrip_code", "date"])
        prev = df.groupby("scrip_code")["close"].shift()
        ratio = df["close"] / prev
        tail = df.groupby("scrip_code").tail(1)
        bad = df[(ratio < JUMP_LOW) | (ratio > JUMP_HIGH)].assign(ratio=ratio, prev_close=prev)
        bad = bad[bad["date"].str[:4] >= p[:4]]                       # the carried-over row itself is not a candidate
        for r in bad.itertuples(index=False):
            if (r.scrip_code, r.date) in split_days or (r.scrip_code, r.date) in handled:
                continue
            near = nearest_ratio(r.ratio)
            rows.append((r.scrip_code, names.get(r.scrip_code, ""), r.date, round(r.prev_close, 4), round(r.close, 4), round(r.ratio, 4),
                         round(near, 4), "looks like a missed split/bonus" if abs(r.ratio / near - 1) < 0.06 else "no clean ratio (crash, spin-off or bad data?)"))
    out = pd.DataFrame(rows, columns=["ticker", "company", "date", "prev_close", "close", "ratio", "nearest_ratio", "note"])
    os.makedirs(REPORT_DIR, exist_ok=True)
    out.to_csv(os.path.join(REPORT_DIR, "review_jumps.csv"), index=False)
    clean = out[out["note"].str.startswith("looks like")]
    with open(os.path.join(REPORT_DIR, "adjustment_review.md"), "w", encoding="utf-8") as f:
        f.write("# Adjustment review\n\nOne-day RAW price moves no split explains. `looks like a missed split` = the ratio is a usual split ratio, so Yahoo probably missed an event.\n"
                "To fix one, add to data/manual_adjustments.json: `{\"TICKER\": [{\"ex_date\": \"YYYY-MM-DD\", \"factor\": 0.5, \"description\": \"missed 2:1 split\"}]}`\n\n")
        f.write(f"Jumps: {len(out)}, of which look like missed splits: {len(clean)}\n\n")
        show = pd.concat([clean, out[~out.index.isin(clean.index)]]).head(200)
        f.write("| ticker | company | date | prev | close | ratio | nearest | note |\n|---|---|---|---|---|---|---|---|\n")
        for r in show.itertuples(index=False):
            f.write("| " + " | ".join(str(x) for x in r) + " |\n")
    return f"review files written to {REPORT_DIR}/ (price jumps without a split: {len(out)}, look like missed splits: {len(clean)})"


def print_report():
    c = load_factor_cache()
    if c.empty:
        print("[REPORT] no splits or dividends loaded yet")
        return
    print("[REPORT] events by type and result:")
    for (typ, st), n in c.groupby(["type", "status"]).size().items():
        print(f"[REPORT]   {typ:9s} {st:5s} {n}")
    sk = c[c["status"] == "skip"]
    if len(sk):
        why = sk["note"].fillna("").str.replace(r"[\d.]+", "#", regex=True).value_counts().head(8)
        print("[REPORT] skipped because:")
        for note, n in why.items():
            print(f"[REPORT]   {n:5d}  {note}")
