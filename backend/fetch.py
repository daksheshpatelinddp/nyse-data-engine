"""
NYSE daily fetcher (Yahoo Finance).  Stores RAW (unadjusted) prices in GIT as small files (data/raw/, see rawstore.py); nothing is written to R2 here.

What Yahoo gives and what is stored:
  Yahoo's "close" is already adjusted for SPLITS (older bars divided by the split ratio), "adjclose" also for dividends. Both change when a new split appears.
  To keep an unchanging raw store (like the NSE/BSE engines) the raw price of every bar is rebuilt:  raw = yahoo price x (product of the split ratios AFTER that bar).
  Splits and dividends are stored as events (data/events/splits.csv, dividends.csv; dividend amounts also in raw units) and the build step adjusts from them.

Flow of one run:
  1. ticker list: NYSE-listed common stocks from nasdaqtrader.com (otherlisted.txt), Yahoo tickers (BRK.B -> BRK-B)
  2. tickers already loaded: fetch the last days (since the last stored day, with a few days overlap) -> new bars + new events
  3. tickers not loaded yet: fetch the FULL daily history (explicit period1/period2: Yahoo's range=max returns only monthly bars)
  4. a run where more than MAX_FAIL_PCT % of the tickers fail stores nothing, so the next run simply tries again

Environment (all optional): MAX_RUNTIME_MINUTES, REQUEST_DELAY (0.1 s), NYSE_EXCHANGES (N; add A for NYSE American, P for Arca), INCLUDE_ETF, INCLUDE_PREFERRED,
HISTORY_START (1970-01-02), REFETCH_ALL, OVERLAP_DAYS (5), MAX_FAIL_PCT (2), NO_DATA_RETRY_DAYS (30), FLUSH_ROWS (1500000), LIMIT_SYMBOLS (testing).
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rawstore
from common import STATE_FILE, SCRIPS_FILE, EVENTS_DIR

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
           "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits&includeAdjustedClose=false"
SYMDIR = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
SPLITS_FILE = os.path.join(EVENTS_DIR, "splits.csv")
DIVS_FILE = os.path.join(EVENTS_DIR, "dividends.csv")
SCRIPT_START = time.time()


def _flag(name):
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _num_env(name, default):
    try:
        return float(os.getenv(name, "") or default)
    except ValueError:
        return default


MAX_RUNTIME_MINUTES = _num_env("MAX_RUNTIME_MINUTES", 0)
REQUEST_DELAY = _num_env("REQUEST_DELAY", 0.1)
OVERLAP_DAYS = int(_num_env("OVERLAP_DAYS", 5))
MAX_FAIL_PCT = _num_env("MAX_FAIL_PCT", 2)
NO_DATA_RETRY_DAYS = int(_num_env("NO_DATA_RETRY_DAYS", 30))
FLUSH_ROWS = int(_num_env("FLUSH_ROWS", 1500000))
HISTORY_START = (os.getenv("HISTORY_START") or "").strip()[:10] or "1970-01-02"


# ----------------------------------------------------------------------------------------------------------------------
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except ValueError:
            pass
    return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"), sort_keys=True)


def _ts(date_str):
    return int(datetime.strptime(str(date_str).strip()[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


def _date(ts, offset=-18000):
    return datetime.fromtimestamp(int(ts) + int(offset or 0), tz=timezone.utc).strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------------------------------------------------
# 1. ticker list
# ----------------------------------------------------------------------------------------------------------------------
_SKIP_NAME = re.compile(r"\b(warrants?|rights?|units?|notes?|debentures?|preferred|pfd|pref)\b|%", re.I)


def parse_symbol_list(text):
    """nasdaqtrader otherlisted.txt -> [(yahoo ticker, name)] of the wanted exchanges. Warrants, rights, units, notes, preferred shares, ETFs and test issues are dropped."""
    lines = text.strip().splitlines()
    head = lines[0].split("|")
    ix = {h: i for i, h in enumerate(head)}
    wanted = {e.strip().upper() for e in os.getenv("NYSE_EXCHANGES", "N").split(",") if e.strip()}
    out, seen = [], set()
    for line in lines[1:]:
        if line.startswith("File Creation"):
            continue
        r = line.split("|")
        if len(r) < len(head) or r[ix["Exchange"]] not in wanted or r[ix["Test Issue"]] != "N":
            continue
        if r[ix["ETF"]] == "Y" and not _flag("INCLUDE_ETF"):
            continue
        sym, name = r[ix["ACT Symbol"]].strip(), r[ix["Security Name"]].strip()
        if not _flag("INCLUDE_PREFERRED") and (_SKIP_NAME.search(name) or "$" in sym):
            continue
        y = sym.replace(".", "-").upper()
        if y and y not in seen:
            seen.add(y)
            out.append((y, name))
    return out


def load_symbols(session):
    r = session.get(SYMDIR, timeout=60)
    r.raise_for_status()
    syms = parse_symbol_list(r.text)
    lim = int(_num_env("LIMIT_SYMBOLS", 0))
    return syms[:lim] if lim else syms


# ----------------------------------------------------------------------------------------------------------------------
# 2. Yahoo
# ----------------------------------------------------------------------------------------------------------------------
def get_chart(session, sym, p1, p2):
    """-> (status, json or None). status: 'ok', 'nodata' (Yahoo does not know the ticker), 'error'."""
    url = YAHOO.format(sym=sym, p1=p1, p2=p2)
    for k in range(4):
        try:
            r = session.get(url, timeout=30)
        except Exception:
            time.sleep(2 * (k + 1))
            continue
        if r.status_code == 404:
            return "nodata", None
        if r.status_code == 400 and p1 < 0:                       # a negative start is refused: ask from 1970
            url = YAHOO.format(sym=sym, p1=0, p2=p2)
            p1 = 0
            continue
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(5 * (k + 1))
            continue
        if r.status_code != 200:
            return "error", None
        try:
            return "ok", r.json()
        except ValueError:
            time.sleep(2)
    return "error", None


def parse_chart(js, sym):
    """Yahoo chart JSON -> (bars, splits, dividends) in RAW units, or None when Yahoo has no data.
    bars: DataFrame(scrip_code, date, open, high, low, close, volume); splits: [(date, num, den)]; dividends: [(date, raw amount)]."""
    try:
        res = js["chart"]["result"][0]
    except (KeyError, IndexError, TypeError):
        return None
    off = (res.get("meta") or {}).get("gmtoffset", -18000)
    ts = res.get("timestamp") or []
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    ev = res.get("events") or {}
    splits = []
    for s in (ev.get("splits") or {}).values():
        n, d = s.get("numerator"), s.get("denominator")
        if n and d and n > 0 and d > 0 and n != d:
            splits.append((_date(s["date"], off), float(n), float(d)))
    splits = sorted(set(splits))
    sdates = np.array([s[0] for s in splits], dtype="U10")
    sratio = np.array([s[1] / s[2] for s in splits], dtype="float64")
    suffix = np.append(np.cumprod(sratio[::-1])[::-1], 1.0) if len(splits) else np.array([1.0])

    def after(dates):                                              # product of the split ratios of the splits dated AFTER each date
        d = np.asarray(dates, dtype="U10")
        return suffix[np.searchsorted(sdates, d, side="right")] if len(splits) else np.ones(len(d))

    n = len(ts)
    cols = {k: np.array([np.nan if v is None else v for v in (q.get(k) or [None] * n)], dtype="float64") for k in ("open", "high", "low", "close", "volume")}
    dates = [_date(t, off) for t in ts]
    ok = np.isfinite(cols["close"]) & (cols["close"] > 0)
    bars = pd.DataFrame({"scrip_code": sym, "date": dates})
    mult = after(dates)
    for k in ("open", "high", "low", "close"):
        v = np.where(np.isfinite(cols[k]) & (cols[k] > 0), cols[k], cols["close"])         # a missing open/high/low is replaced by the close
        bars[k] = np.round(v * mult, 4)
    bars["volume"] = np.nan_to_num(cols["volume"], nan=0.0).astype("int64")
    bars = bars[ok].drop_duplicates("date", keep="last").reset_index(drop=True)
    divs = []
    for d in (ev.get("dividends") or {}).values():
        a = d.get("amount")
        if a and a > 0:
            dd = _date(d["date"], off)
            divs.append((dd, round(float(a) * float(after([dd])[0]), 6)))
    return bars, splits, sorted(set(divs))


# ----------------------------------------------------------------------------------------------------------------------
# 3. events and scrips
# ----------------------------------------------------------------------------------------------------------------------
def _load_events():
    sp = pd.read_csv(SPLITS_FILE, dtype={"symbol": str, "date": str}) if os.path.exists(SPLITS_FILE) else pd.DataFrame(columns=["symbol", "date", "num", "den"])
    dv = pd.read_csv(DIVS_FILE, dtype={"symbol": str, "date": str}) if os.path.exists(DIVS_FILE) else pd.DataFrame(columns=["symbol", "date", "amount"])
    return sp, dv


def _save_events(sp, dv):
    os.makedirs(EVENTS_DIR, exist_ok=True)
    sp.drop_duplicates(["symbol", "date"], keep="first").sort_values(["date", "symbol"]).to_csv(SPLITS_FILE, index=False)
    dv.drop_duplicates(["symbol", "date"], keep="first").sort_values(["date", "symbol"]).to_csv(DIVS_FILE, index=False)


def update_scrips(scrips, sym, name, bars):
    s = scrips.setdefault(sym, {"symbol": sym, "name": name, "isin": "", "first": None, "last": None, "prev": []})
    s["name"] = name or s.get("name", "")
    if len(bars):
        lo, hi = bars["date"].min(), bars["date"].max()
        s["first"] = lo if not s.get("first") else min(s["first"], lo)
        s["last"] = hi if not s.get("last") else max(s["last"], hi)


# ----------------------------------------------------------------------------------------------------------------------
def ny_end_date(now):
    """The last day whose Yahoo bar is final: today (New York) after 17:00, else yesterday."""
    try:
        from zoneinfo import ZoneInfo
        ny = now.astimezone(ZoneInfo("America/New_York"))
    except Exception:
        ny = now - timedelta(hours=5)
    d = ny.date() if ny.hour >= 17 else ny.date() - timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def run(session=None, chart=get_chart, symbols=None, now=None):
    now = now or datetime.now(timezone.utc)
    end = ny_end_date(now)
    p2 = _ts(end) + 86400
    cur_month = end[:7]
    if session is None:
        session = requests.Session()
        session.headers.update(HEADERS)
    if symbols is None:
        symbols = load_symbols(session)
    names = dict(symbols)
    state = load_json(STATE_FILE, {})
    days = set(state.get("days") or [])
    backfilled = dict(state.get("backfilled") or {})
    if _flag("REFETCH_ALL") and not state.get("refetch_done"):      # one-off: fetch the full history again for every ticker (rows merge by ticker+date, nothing is duplicated)
        backfilled = {}; state["refetch_done"] = True; print("[FETCH] REFETCH_ALL: full history is fetched again for every ticker")
    no_data = dict(state.get("no_data") or {})
    retry = dict(state.get("retry") or {})                          # ticker -> first date it is missing (a failed fetch earlier)
    through = state.get("fetched_through") or ""
    scrips = load_json(SCRIPS_FILE, {})
    sp_old, dv_old = _load_events()
    new_sp, new_dv = [], []
    stats = {"recent": 0, "backfilled": 0, "no_data": 0, "failed": 0, "rows": 0, "new_days": 0}
    print(f"[FETCH] {len(symbols)} NYSE tickers; last final trading day {end}; fetched through {through or 'never'}")

    def save_small():
        state.update({"days": sorted(days), "backfilled": backfilled, "no_data": no_data, "retry": retry, "fetched_through": through})
        save_json(STATE_FILE, state)
        save_json(SCRIPS_FILE, scrips)
        _save_events(pd.concat([sp_old, pd.DataFrame(new_sp, columns=["symbol", "date", "num", "den"])], ignore_index=True),
                     pd.concat([dv_old, pd.DataFrame(new_dv, columns=["symbol", "date", "amount"])], ignore_index=True))

    def keep_events(sym, splits, divs):
        new_sp.extend((sym, d, n, den) for d, n, den in splits)
        new_dv.extend((sym, d, a) for d, a in divs)

    def over_time():
        return bool(MAX_RUNTIME_MINUTES) and time.time() - SCRIPT_START > MAX_RUNTIME_MINUTES * 60

    # ---- 2. tickers already loaded: the last days --------------------------------------------------------------------------
    todo_recent = [s for s, _ in symbols if s in backfilled]
    if through and todo_recent:
        p1_new = _ts(through) - OVERLAP_DAYS * 86400
        frames, failed = [], []
        for sym in todo_recent:
            p1 = min(p1_new, _ts(retry[sym])) if sym in retry else p1_new
            status, js = chart(session, sym, p1, p2)
            time.sleep(REQUEST_DELAY)
            parsed = parse_chart(js, sym) if status == "ok" else None
            if parsed is None:
                if status == "error":
                    failed.append(sym)
                continue
            bars, splits, divs = parsed
            keep_events(sym, splits, divs)
            fresh = bars[(bars["date"] > through) | (bars["date"] >= retry.get(sym, "9999"))]
            if len(fresh):
                frames.append(fresh)
                update_scrips(scrips, sym, names.get(sym), fresh)
            retry.pop(sym, None)
        pct = 100.0 * len(failed) / max(len(todo_recent), 1)
        if pct > MAX_FAIL_PCT:
            print(f"[FETCH] ERROR {len(failed)} of {len(todo_recent)} tickers failed ({pct:.1f}% > {MAX_FAIL_PCT}%): nothing stored this run, try again later. First: {failed[:10]}")
            raise SystemExit(1)
        for sym in failed:                                          # a few single failures: remember where to continue for them
            retry[sym] = min(retry.get(sym, "9999"), (datetime.strptime(through, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))
        stats["failed"] = len(failed)
        if frames:
            df = pd.concat(frames, ignore_index=True)
            df = df[df["date"] <= end]
            rawstore.merge_rows(df, cur_month)
            new_days = set(df["date"]) - days
            days |= set(df["date"])
            stats["new_days"] = len(new_days)
            stats["rows"] += len(df)
            print(f"[FETCH] recent: {len(df)} rows, new days {sorted(new_days)}" + (f", {len(failed)} tickers failed (will be retried)" if failed else ""))
        through = max(through, end)
        stats["recent"] = len(todo_recent)
        save_small()

    # ---- 3. tickers not loaded yet: the full history ------------------------------------------------------------------------
    today = now.date()
    todo_full = [s for s, _ in symbols if s not in backfilled
                 and not (s in no_data and (today - datetime.strptime(no_data[s], "%Y-%m-%d").date()).days < NO_DATA_RETRY_DAYS)]
    if todo_full:
        print(f"[FETCH] full history for {len(todo_full)} new tickers")
    p1_full = _ts(HISTORY_START)
    buf, buf_rows, pending = [], 0, []

    def flush():
        nonlocal buf, buf_rows, pending
        if buf:
            df = pd.concat(buf, ignore_index=True)
            df = df[df["date"] <= end]
            rawstore.merge_rows(df, cur_month)
            days.update(df["date"])
            stats["rows"] += len(df)
        for sym, first in pending:
            backfilled[sym] = first
        buf, buf_rows, pending = [], 0, []
        save_small()

    stopped = None
    for i, sym in enumerate(todo_full):
        if over_time():
            stopped = i
            break
        status, js = chart(session, sym, p1_full, p2)
        time.sleep(REQUEST_DELAY)
        parsed = parse_chart(js, sym) if status == "ok" else None
        if parsed is None or parsed[0].empty:
            if status == "error":
                stats["failed"] += 1
            else:
                no_data[sym] = today.strftime("%Y-%m-%d")
                stats["no_data"] += 1
            continue
        bars, splits, divs = parsed
        bars = bars[bars["date"] <= end]
        keep_events(sym, splits, divs)
        update_scrips(scrips, sym, names.get(sym), bars)
        no_data.pop(sym, None)
        buf.append(bars)
        buf_rows += len(bars)
        pending.append((sym, str(bars["date"].min())))
        stats["backfilled"] += 1
        if buf_rows >= FLUSH_ROWS:
            flush()
            print(f"[FETCH] backfill progress: {i + 1}/{len(todo_full)} tickers")
    flush()
    if not through and (backfilled or stats["rows"]):
        through = end                                               # first run: every loaded ticker holds data up to the last final day
    merged = rawstore.consolidate(cur_month)
    save_small()
    if stopped is not None:
        print(f"[TIME LIMIT] stopped after {stopped} of {len(todo_full)} new tickers; everything so far is saved. Run again to continue.")
    print(f"[FETCH COMPLETE] recent tickers={stats['recent']} new days={stats['new_days']} backfilled={stats['backfilled']} no data={stats['no_data']} "
          f"failed={stats['failed']} rows={stats['rows']} months merged={merged}")
    return stats


if __name__ == "__main__":
    run()
