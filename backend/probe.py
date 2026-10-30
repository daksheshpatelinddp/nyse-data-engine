"""PROBE: what can this machine (a GitHub runner) reach, and what do Yahoo / Stooq / the NYSE symbol list really return?
Changes nothing. Run it from the "NYSE Probe" workflow and read the [PROBE SUMMARY] block at the end of the log."""
import io
import json
import os
import sys
import time
from collections import Counter

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
      "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"}
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d&events=div%2Csplits&includeAdjustedClose=true"
STOOQ = "https://stooq.com/q/d/l/?s={sym}&i=d"
SYMDIR = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
SUMMARY = []


def say(msg):
    print(msg, flush=True)


def note(line):
    SUMMARY.append(line)
    say(line)


def get(session, url, timeout=30):
    t = time.time()
    try:
        r = session.get(url, headers=UA, timeout=timeout)
        return r, time.time() - t, None
    except Exception as e:
        return None, time.time() - t, f"{type(e).__name__}: {e}"


def parse_yahoo(js):
    """Yahoo chart JSON -> dict(rows, first, last, splits, dividends, adj_ratio_first, currency, exchange) or an error string."""
    try:
        res = js["chart"]["result"][0]
    except (KeyError, IndexError, TypeError):
        return f"no result: {str(js.get('chart', {}).get('error'))[:150]}"
    ts = res.get("timestamp") or []
    q = (res.get("indicators", {}).get("quote") or [{}])[0]
    adj = ((res.get("indicators", {}).get("adjclose") or [{}])[0]).get("adjclose")
    close = q.get("close") or []
    ev = res.get("events") or {}
    rows = [i for i, c in enumerate(close) if c is not None]
    out = {"rows": len(rows), "splits": [(s.get("date"), s.get("numerator"), s.get("denominator")) for s in (ev.get("splits") or {}).values()],
           "dividends": len(ev.get("dividends") or {}), "currency": res.get("meta", {}).get("currency"),
           "exchange": res.get("meta", {}).get("exchangeName"), "has_adjclose": bool(adj)}
    if rows:
        i0, i1 = rows[0], rows[-1]
        out["first"] = (time.strftime("%Y-%m-%d", time.gmtime(ts[i0])), close[i0], q.get("open", [None])[i0], q.get("volume", [None])[i0])
        out["last"] = (time.strftime("%Y-%m-%d", time.gmtime(ts[i1])), close[i1])
        if adj and adj[i0] and close[i0]:
            out["adj_over_close_first"] = round(adj[i0] / close[i0], 4)
    return out


def probe_symbol_list(session):
    say("\n=== 1. NYSE symbol list (nasdaqtrader otherlisted.txt)")
    r, dt, err = get(session, SYMDIR)
    if err or r.status_code != 200:
        note(f"symbol list: FAILED {err or r.status_code}")
        return []
    lines = r.text.strip().splitlines()
    head = lines[0].split("|")
    say(f"columns: {head}")
    rows = [l.split("|") for l in lines[1:] if not l.startswith("File Creation")]
    ix = {h: i for i, h in enumerate(head)}
    ex = Counter(r_[ix["Exchange"]] for r_ in rows)
    nyse = [r_ for r_ in rows if r_[ix["Exchange"]] == "N" and r_[ix["ETF"]] == "N" and r_[ix["Test Issue"]] == "N"]
    note(f"symbol list: OK {len(rows)} rows, by exchange {dict(ex)}; NYSE non-ETF non-test = {len(nyse)}")
    say("sample: " + ", ".join(r_[ix["ACT Symbol"]] for r_ in nyse[:12]))
    return [r_[ix["ACT Symbol"]] for r_ in nyse]


def probe_yahoo_depth(session):
    say("\n=== 2. Yahoo: full history of known NYSE stocks (splits, dividends, adjusted close)")
    ok = 0
    for sym in ("JPM", "KO", "NKE", "BRK-B", "^DJI", "^NYA"):
        r, dt, err = get(session, YAHOO.format(sym=sym, rng="max"))
        if err or r.status_code != 200:
            say(f"{sym}: FAILED {err or r.status_code} {'' if err else r.text[:120]!r}")
            continue
        try:
            p = parse_yahoo(r.json())
        except ValueError:
            say(f"{sym}: not JSON: {r.text[:120]!r}")
            continue
        if isinstance(p, str):
            say(f"{sym}: {p}")
            continue
        ok += 1
        say(f"{sym}: {p['rows']} days, first {p.get('first')}, last {p.get('last')}, splits {p['splits'][:4]}, dividends {p['dividends']}, "
            f"adjclose={p['has_adjclose']} adj/close at first day {p.get('adj_over_close_first')}, {p['exchange']} {p['currency']}, {dt:.1f}s")
        time.sleep(0.5)
    note(f"yahoo history: {ok}/6 symbols OK (JPM, KO, NKE, BRK-B, ^DJI, ^NYA)")


def probe_yahoo_rate(session, symbols, n=80, delay=0.25):
    say(f"\n=== 3. Yahoo: {n} NYSE symbols in a row, {delay}s apart (is this machine throttled or blocked?)")
    codes, times, first_bad = Counter(), [], None
    for s in symbols[:n]:
        r, dt, err = get(session, YAHOO.format(sym=s.replace(".", "-"), rng="1mo"))
        code = "EXC" if err else r.status_code
        codes[code] += 1
        times.append(dt)
        if code != 200 and first_bad is None:
            first_bad = (s, err or r.text[:150])
        time.sleep(delay)
    avg = sum(times) / max(len(times), 1)
    note(f"yahoo rate test: {dict(codes)} avg {avg:.2f}s/request" + (f", first problem {first_bad}" if first_bad else ""))


def probe_stooq(session):
    say("\n=== 4. Stooq: daily CSV (jpm.us) and the page of bulk files")
    r, dt, err = get(session, STOOQ.format(sym="jpm.us"))
    if err or r.status_code != 200:
        note(f"stooq csv: FAILED {err or r.status_code}")
    else:
        body = r.text
        say(f"first 300 chars: {body[:300]!r}")
        looks_csv = body.lstrip().lower().startswith("date,open,high,low,close")
        note(f"stooq csv: HTTP 200, {len(body)} bytes, {'real CSV with ' + str(body.count(chr(10))) + ' lines' if looks_csv else 'NOT a data CSV (see text above)'}")
    r, dt, err = get(session, "https://stooq.com/db/h/")
    note(f"stooq bulk page: {'FAILED ' + str(err) if err else 'HTTP ' + str(r.status_code) + ', ' + str(len(r.text)) + ' bytes'}")


def main():
    session = requests.Session()
    syms = probe_symbol_list(session)
    probe_yahoo_depth(session)
    if syms:
        probe_yahoo_rate(session, syms, n=int(os.getenv("RATE_N", "80")))
    probe_stooq(session)
    say("\n===== [PROBE SUMMARY] =====")
    for l in SUMMARY:
        say(l)


if __name__ == "__main__":
    main()
