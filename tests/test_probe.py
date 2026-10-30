"""Offline check of the probe's Yahoo parser with a realistic fake answer."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))
import probe
js = {"chart": {"result": [{"meta": {"currency": "USD", "exchangeName": "NYQ"}, "timestamp": [1600000000, 1600086400, 1600172800],
      "events": {"splits": {"1600086400": {"date": 1600086400, "numerator": 4, "denominator": 1}}, "dividends": {"1600172800": {"amount": 0.2, "date": 1600172800}}},
      "indicators": {"quote": [{"open": [1, 2, 3], "high": [1, 2, 3], "low": [1, 2, 3], "close": [1.0, None, 3.0], "volume": [10, 20, 30]}], "adjclose": [{"adjclose": [0.9, None, 3.0]}]}}], "error": None}}
p = probe.parse_yahoo(js)
assert p["rows"] == 2 and p["splits"] == [(1600086400, 4, 1)] and p["dividends"] == 1 and p["adj_over_close_first"] == 0.9 and p["exchange"] == "NYQ", p
assert isinstance(probe.parse_yahoo({"chart": {"result": None, "error": {"code": "Not Found"}}}), str)
print("probe parser ok")
