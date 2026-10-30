# Adjustment review

One-day RAW price moves no split explains. `looks like a missed split` = the ratio is a usual split ratio, so Yahoo probably missed an event.
To fix one, add to data/manual_adjustments.json: `{"TICKER": [{"ex_date": "YYYY-MM-DD", "factor": 0.5, "description": "missed 2:1 split"}]}`

Jumps: 6, of which look like missed splits: 5

| ticker | company | date | prev | close | ratio | nearest | note |
|---|---|---|---|---|---|---|---|
| AES | The AES Corporation Common Stock | 2001-09-26 | 24.25 | 12.25 | 0.5052 | 0.5 | looks like a missed split/bonus |
| ACR | ACRES Commercial Realty Corp. Common Stock | 2020-03-18 | 4.71 | 2.5 | 0.5308 | 0.5294 | looks like a missed split/bonus |
| AD | Array Digital Infrastructure, Inc. Common Shares | 2023-08-04 | 17.5 | 33.76 | 1.9291 | 2.0 | looks like a missed split/bonus |
| ACH | Accendra Health, Inc. Common Stock | 2026-08-10 | 2.8 | 1.4 | 0.5 | 0.5 | looks like a missed split/bonus |
| ADCT | ADC Therapeutics SA Common Shares | 2026-06-04 | 3.08 | 1.32 | 0.4286 | 0.4286 | looks like a missed split/bonus |
| ACH | Accendra Health, Inc. Common Stock | 2020-07-21 | 7.94 | 14.4 | 1.8136 | 2.0 | no clean ratio (crash, spin-off or bad data?) |
