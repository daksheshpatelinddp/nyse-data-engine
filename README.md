# NYSE data engine

Same design as the NSE and BSE engines: raw prices live in git, adjustments are computed at build time, and only the final yearly parquet files and
the history/pack/manifest files go to Cloudflare R2 (bucket `nse-stock-data`, folder `nyse/`).

* **Source:** Yahoo Finance chart API only (free, unofficial). Stooq is blocked from GitHub, so there is no second source to cross-check against.
* **Tickers:** the NYSE-listed common stocks from nasdaqtrader `otherlisted.txt` (ETFs, test issues, warrants, rights, units, notes and preferred shares are dropped; `BRK.B` is stored as `BRK-B` with `BRK.B` as an alias).
* **Raw prices:** Yahoo gives split-adjusted prices. The fetcher turns them back into the prices actually traded (price x all later splits) and stores them in git (`data/raw/<year>/<yyyy-mm>.parquet`, past months merged, the current month as one small file per day). Splits and dividends go to `data/events/`.
* **Adjustment:** splits at once; cash dividends (total-return style, factor = 1 - dividend / previous close) only in the weekly run, like the NSE engine. A factor below 0.5 is skipped.
* **Missed splits:** if Yahoo has no split event but the raw price jumps (below 0.55 or above 1.8 in one day), it is NOT guessed. It is listed in `data/reports/review_jumps.csv` and `adjustment_review.md`. To fix one, add it to `data/manual_adjustments.json`:
  `{"TICKER": [{"ex_date": "2025-02-17", "factor": 0.5, "replace": true, "description": "2:1 split"}]}`, then run "Daily NYSE Fetcher" with `recompute_factors` ticked, then the upload with `force_all`.

## Order of work
1. Actions -> **Daily NYSE Fetcher** -> Run workflow (leave the boxes as they are). The first run fetches the whole history of about 2,800 tickers and stops itself after 4.5 h; run it again until the log says all tickers are backfilled. (Optional test first: `limit_symbols` = 50.)
2. Open `data/reports/` in the repo and read the dry-run report and `review_jumps.csv`.
3. Actions -> **NYSE Upload to R2** -> tick `force_all` -> Run. This is the only workflow that writes to R2 (first upload: a few hundred writes).
4. Afterwards the daily fetch runs by itself on weekdays. Run the upload by hand when you want R2 updated (normally a daily upload = about 3 writes), and once a week with `weekly_run` ticked to apply dividends.

## Limits to know
* Yahoo is unofficial; it can change or throttle. The fetch stops without saving anything if more than 2% of requests fail.
* Yahoo has no delisted stocks, so the history has survivorship bias. Volume is as Yahoo gives it.
* No R2 secrets are needed in the daily workflow. The upload workflow uses the same three secrets as BSE (`R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`).

Tests (offline, fake Yahoo): `python tests/test_nyse_e2e.py` and `PERIOD_MODE=half python tests/test_nyse_e2e.py`.
