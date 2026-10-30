"""End-to-end test of the NYSE engine without network: fake Yahoo -> fetch -> raw files in "git" -> build -> adjusted files in a fake R2.
Run:  python tests/test_nyse_e2e.py            (PERIOD_MODE=half python tests/test_nyse_e2e.py   for half-year files)

Hand-calculated expectations (adjusted to today's share structure, dividends total-return style):
  AAA  : raw 100 until a 2:1 split on 2025-02-03 (50 after); dividend $1.00 ex 2025-03-03 (raw close before = 50 -> factor 0.98)
         close 2024-12-02 = 100 * 0.5 * 0.98 = 49.0 ; 2025-02-10 = 50 * 0.98 = 49.0 ; 2025-03-31 = 50.0
  BBB  : new listing in run 2 (full history fetched then)
  CCC  : Yahoo has no data (404)
  DDD  : raw 90; a 3:1 split ex 2025-04-02 appears in run 2 -> old closes 30.0 ; the stored raw bars are NOT rewritten
  EEE  : raw 10; dividend $1 ex 2025-04-02 (run 2) waits for the weekly run, then 10 * 0.9 = 9.0
  FFF  : raw 80 -> 40 on 2025-02-17 with NO split event (Yahoo missed it): must show in the review file
  GGG  : fetch fails once in run 2, is healed in run 3 (no missing day)
  BRK-B: ticker with a dash -> alias BRK.B
"""
import json, os, shutil, sys, tempfile
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend"))
import numpy, pandas as pd
try:
    import pyarrow, boto3
    STUB = False
except ImportError:
    sys.path.insert(0, os.path.join(ROOT, "tests", "stubs")); STUB = True

tmp = tempfile.mkdtemp(prefix="nyse_e2e_")
DATA = os.path.join(tmp, "data")
os.environ.update(DATA_DIR=DATA, HIST_BUCKET_SIZE="2", REQUEST_DELAY="0", MAX_FAIL_PCT="40", FLUSH_ROWS="300", HISTORY_START="2024-11-01")
import actions, build, common, fetch, rawstore, pio
from packs import decode_pack_block
from storage import LocalStore
MODE = common.PERIOD_MODE
print("period mode:", MODE, "| stand-in parquet:", STUB)

# ---- the fake world -------------------------------------------------------------------------------------------------------------
def raw_price(sym, d):
    if sym == "AAA": return 100.0 if d < "2025-02-03" else 50.0
    if sym == "BBB": return 20.0
    if sym == "DDD": return 90.0 if d < "2025-04-02" else 30.0
    if sym == "FFF": return 80.0 if d < "2025-02-17" else 40.0
    if sym == "GGG": return 25.0
    if sym == "BRK-B": return 500.0
    return 10.0
WORLD = {"AAA": dict(start="2024-11-01", splits=[("2025-02-03", 2, 1)], divs=[("2025-03-03", 1.0)]),
         "BBB": dict(start="2025-04-01", splits=[], divs=[]),
         "DDD": dict(start="2024-11-01", splits=[("2025-04-02", 3, 1)], divs=[]),
         "EEE": dict(start="2024-11-01", splits=[], divs=[("2025-04-02", 1.0)]),
         "FFF": dict(start="2024-11-01", splits=[], divs=[]),
         "GGG": dict(start="2024-11-01", splits=[], divs=[]),
         "BRK-B": dict(start="2024-11-01", splits=[], divs=[])}
STATE = {"last": "2025-03-31", "fail": set()}

def dstr(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
def ts_of(d): return int(datetime.strptime(d, "%Y-%m-%d").replace(hour=14, minute=30, tzinfo=timezone.utc).timestamp())

def fake_chart(session, sym, p1, p2):
    w = WORLD.get(sym)
    if w is None: return "nodata", None                                      # CCC
    if sym in STATE["fail"]: return "error", None
    last = STATE["last"]
    splits = [s for s in w["splits"] if s[0] <= last]
    def after(d):                                                            # Yahoo divides older prices by the splits that come AFTER them
        f = 1.0
        for sd, n, den in splits:
            if sd > d: f *= n / den
        return f
    lo, hi = max(w["start"], dstr(p1)), min(last, dstr(p2 - 86400))
    ts, o, h, l, c, v = [], [], [], [], [], []
    d = datetime.strptime(lo, "%Y-%m-%d").date()
    while d.strftime("%Y-%m-%d") <= hi:
        if d.weekday() < 5:
            s = d.strftime("%Y-%m-%d"); a = after(s); r = raw_price(sym, s)
            ts.append(ts_of(s)); o.append(r / a); h.append(r / a + 1); l.append(r / a - 1); c.append(r / a); v.append(1000)
        d += timedelta(days=1)
    ev = {}
    if splits: ev["splits"] = {str(ts_of(sd)): {"date": ts_of(sd), "numerator": n, "denominator": den} for sd, n, den in splits}
    dv = [x for x in w["divs"] if x[0] <= last]
    if dv: ev["dividends"] = {str(ts_of(dd)): {"date": ts_of(dd), "amount": amt / after(dd)} for dd, amt in dv}
    js = {"chart": {"result": [{"meta": {"gmtoffset": -18000, "currency": "USD"}, "timestamp": ts, "events": ev,
                                "indicators": {"quote": [{"open": o, "high": h, "low": l, "close": c, "volume": v}]}}], "error": None}}
    return "ok", js

def NOW(d): return datetime.strptime(d + " 22:30", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)      # 18:30 New York = after the 17:00 cut-off
NAMES = [("AAA", "AAA Corp"), ("CCC", "CCC Inc"), ("DDD", "DDD Co"), ("EEE", "EEE Co"), ("FFF", "FFF Co"), ("GGG", "GGG Co"), ("BRK-B", "Berkshire B")]

# ---- the ticker list parser --------------------------------------------------------------------------------------------------
txt = ("ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol\n"
       "JPM|JPMorgan Chase & Co. Common Stock|N|JPM|N|100|N|JPM\nBRK.B|Berkshire Hathaway Inc. Class B|N|BRK.B|N|100|N|BRK.B\n"
       "AAC.U|Ares Acquisition Units|N|AAC.U|N|100|N|AAC.U\nAAC.W|Ares Acquisition Warrants|N|AAC.W|N|100|N|AAC.W\n"
       "SPY|SPDR S&P 500 ETF|P|SPY|Y|100|N|SPY\nXYZ|Some Bank 6.5% Series A Preferred Stock|N|XYZ|N|100|N|XYZ\n"
       "TST|Test Co|N|TST|N|100|Y|TST\nAMX|American Co|A|AMX|N|100|N|AMX\nFile Creation Time: 1030202600:00|||||||\n")
assert fetch.parse_symbol_list(txt) == [("JPM", "JPMorgan Chase & Co. Common Stock"), ("BRK-B", "Berkshire Hathaway Inc. Class B")], fetch.parse_symbol_list(txt)
print("ticker list parser ok")

store = LocalStore(os.path.join(tmp, "r2"))

# ---- 1. first run: full history of every ticker -----------------------------------------------------------------------------
assert fetch.ny_end_date(datetime(2025, 3, 31, 14, 0, tzinfo=timezone.utc)) == "2025-03-30", "before 17:00 New York the day is not final yet"
st = fetch.run(session=object(), chart=fake_chart, symbols=NAMES, now=NOW("2025-03-31"))
assert st["backfilled"] == 6 and st["no_data"] == 1 and st["failed"] == 0, st
files = sorted(os.path.relpath(os.path.join(d, f), DATA) for d, _, fs in os.walk(os.path.join(DATA, "raw")) for f in fs)
assert "raw/2024/2024-11.parquet" in files and "raw/2025/2025-02.parquet" in files, files
assert "raw/2025/2025-03-31.parquet" in files and "raw/2025/2025-03.parquet" not in files, "current month: one small file per day"
state = json.load(open(os.path.join(DATA, "state.json")))
assert "CCC" in state["no_data"] and "AAA" in state["backfilled"] and state["fetched_through"] == "2025-03-31", state
raw = pd.concat([rawstore.read_period(p) for p in rawstore.periods()])
a = raw[raw.scrip_code == "AAA"].set_index("date")["close"]
assert a["2024-12-02"] == 100.0 and a["2025-02-03"] == 50.0, "raw price rebuilt from Yahoo's split-adjusted price"
sp = pd.read_csv(os.path.join(DATA, "events", "splits.csv")); dv = pd.read_csv(os.path.join(DATA, "events", "dividends.csv"))
assert list(sp.symbol) == ["AAA"] and list(dv.symbol) == ["AAA"] and dv.amount[0] == 1.0, (sp, dv)
n1 = len(raw)
st = fetch.run(session=object(), chart=fake_chart, symbols=NAMES, now=NOW("2025-03-31"))      # same day again: nothing new
assert st["rows"] == 0 and st["new_days"] == 0, st
assert len(pd.concat([rawstore.read_period(p) for p in rawstore.periods()])) == n1
print("fetch run 1 ok:", n1, "rows")

# ---- 2. build -> fake R2 ----------------------------------------------------------------------------------------------------
build.run(store); assert not build.FAILED, build.FAILED
cur = "2025_H1" if MODE == "half" else "2025"; first = "2024_H2" if MODE == "half" else "2024"
allp = pd.concat([pio.read_bytes(store.get(f"nyse/{first}.parquet")), pio.read_bytes(store.get(f"nyse/{cur}.parquet"))])
cl = lambda sym: allp[allp.symbol == sym].set_index("date")["close"]
assert cl("AAA")["2024-12-02"] == 49.0 and cl("AAA")["2025-02-10"] == 49.0 and cl("AAA")["2025-03-31"] == 50.0 and cl("AAA")["2025-03-03"] == 50.0, cl("AAA").to_dict()
assert cl("FFF")["2024-12-02"] == 80.0, "a split Yahoo missed is NOT guessed: it stays unadjusted and is reported"
assert set(allp.symbol) == {"AAA", "DDD", "EEE", "FFF", "GGG", "BRK-B"}, set(allp.symbol)
assert list(pio.read_bytes(store.get(f"nyse/{cur}.parquet")).columns) == ["symbol", "date", "open", "high", "low", "close", "volume", "delivery"]
assert not [k for k, _, _ in store.list("nyse/") if "raw" in k], "raw prices must never reach R2"
rev = pd.read_csv(os.path.join(DATA, "reports", "review_jumps.csv"), dtype=str)
assert list(rev.ticker) == ["FFF"] and rev.note[0].startswith("looks like a missed split"), rev.to_dict("records")
man = json.loads(store.get("nyse/manifest.json"))
assert man["format"] == 2 and man["currentPeriod"] == cur and man["aliases"]["BRK.B"] == "BRK-B" and len(man["buckets"]) == 3, man["aliases"]
bname = [n for n, v in man["buckets"].items() if "AAA" in v["symbols"]][0]
off, ln, n = man["packs"]["buckets"][bname]["idx"]["AAA"]
blk = decode_pack_block(store.get(f"nyse/{man['packs']['path']}/{bname}.pack")[off:off + ln])
assert len(blk["dates"]) == n and abs(blk["close"][0] - 49.0) < 1e-9, blk["close"][:3]
sy = json.loads(store.get("nyse/symbols.json")); assert sorted(sy["symbols"]) == ["AAA", "BRK-B", "DDD", "EEE", "FFF", "GGG"], sy
print("build 1 ok (split + dividend + alias + missed-split report); R2 writes:", build.PUTS["n"])
fp1 = man["fingerprint"]
build.run(store); assert build.PUTS["n"] == 0, f"unchanged data must not write to R2, wrote {build.PUTS['n']}"
print("unchanged run: 0 R2 writes ok")

# ---- 3. run 2: new days, a new listing, a split and a dividend appear, GGG fails ------------------------------------------------------
STATE["last"] = "2025-04-04"; STATE["fail"] = {"GGG"}
st = fetch.run(session=object(), chart=fake_chart, symbols=NAMES + [("BBB", "BBB Co")], now=NOW("2025-04-04"))
assert st["new_days"] == 4 and st["backfilled"] == 1 and st["failed"] == 1, st
files = sorted(os.listdir(os.path.join(DATA, "raw", "2025")))
assert "2025-03.parquet" in files and not [f for f in files if f.startswith("2025-03-")], files           # March merged when April started
assert "2025-04-04.parquet" in files, files
raw = pd.concat([rawstore.read_period(p) for p in rawstore.periods()])
d = raw[raw.scrip_code == "DDD"].set_index("date")["close"]
assert d["2025-03-31"] == 90.0 and d["2025-04-02"] == 30.0, "old raw bars are not rewritten; new bars are on the new share basis"
assert sorted(raw[raw.scrip_code == "BBB"].date) == ["2025-04-01", "2025-04-02", "2025-04-03", "2025-04-04"]
assert "GGG" not in set(raw[raw.date > "2025-03-31"].scrip_code), "the failed ticker has no new bars yet"
assert json.load(open(os.path.join(DATA, "state.json")))["retry"] == {"GGG": "2025-04-01"}
build.run(store)
m2 = json.loads(store.get("nyse/manifest.json"))
assert m2["fingerprint"] != fp1, "the split changes DDD's history"
e = pd.concat([pio.read_bytes(store.get(f"nyse/h/{m2['fingerprint'][:10]}/{n}.parquet")) for n in m2["buckets"]])
assert e[e.symbol == "DDD"].set_index("date")["close"]["2024-12-02"] == 30.0, "3:1 split applied at once"
assert e[e.symbol == "EEE"].set_index("date")["close"]["2024-12-02"] == 10.0, "the dividend waits for the weekly run"
print("fetch + build run 2 ok (split applied, dividend waiting), writes:", build.PUTS["n"])

# ---- 4. run 3: GGG is healed ------------------------------------------------------------------------------------------------------
STATE["last"] = "2025-04-07"; STATE["fail"] = set()
st = fetch.run(session=object(), chart=fake_chart, symbols=NAMES + [("BBB", "BBB Co")], now=NOW("2025-04-07"))
raw = pd.concat([rawstore.read_period(p) for p in rawstore.periods()])
g = sorted(raw[(raw.scrip_code == "GGG") & (raw.date > "2025-03-31")].date)
assert g == ["2025-04-01", "2025-04-02", "2025-04-03", "2025-04-04", "2025-04-07"], g
assert json.load(open(os.path.join(DATA, "state.json")))["retry"] == {}
assert not raw.duplicated(["scrip_code", "date"]).any()
print("retry ok: the missing days of GGG were filled in")

# ---- 5. too many failures: nothing is stored ------------------------------------------------------------------------------------------
STATE["last"] = "2025-04-08"; STATE["fail"] = set(WORLD)
before = sorted(os.listdir(os.path.join(DATA, "raw", "2025")))
try:
    fetch.run(session=object(), chart=fake_chart, symbols=NAMES + [("BBB", "BBB Co")], now=NOW("2025-04-08")); raise AssertionError("should have stopped")
except SystemExit:
    pass
assert sorted(os.listdir(os.path.join(DATA, "raw", "2025"))) == before
print("mass failure: nothing stored, ok")

# ---- 6. weekly run applies the dividend ------------------------------------------------------------------------------------------------
STATE["fail"] = set(); STATE["last"] = "2025-04-07"
build.WEEKLY = True
build.run(store); assert not build.FAILED
m3 = json.loads(store.get("nyse/manifest.json"))
e = pd.concat([pio.read_bytes(store.get(f"nyse/h/{m3['fingerprint'][:10]}/{n}.parquet")) for n in m3["buckets"]])
assert e[e.symbol == "EEE"].set_index("date")["close"]["2024-12-02"] == 9.0
print("weekly run ok: dividend applied (EEE 10 -> 9.0)")

# ---- 7. dry run ---------------------------------------------------------------------------------------------------------------------------
build.WEEKLY = False
before_state = open(common.BUILD_STATE_FILE).read(); before_r2 = store.list("nyse/")
os.environ["DRY_RUN"] = "true"; build.run(); del os.environ["DRY_RUN"]
assert open(common.BUILD_STATE_FILE).read() == before_state and store.list("nyse/") == before_r2
print("dry run ok")
print("\nALL OK")
shutil.rmtree(tmp, ignore_errors=True)
