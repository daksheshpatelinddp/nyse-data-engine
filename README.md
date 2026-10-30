# NYSE data engine (work in progress)

Step 1 - **NYSE Probe** (Actions -> NYSE Probe -> Run workflow). It changes nothing and tells us whether a GitHub runner can reach Yahoo Finance,
Stooq and the NYSE symbol list, how fast Yahoo answers 80 symbols in a row, and what the data looks like (splits, dividends, adjusted close, history depth).
Read the `[PROBE SUMMARY]` block at the end of the log. The engine itself (fetch -> git -> adjust -> yearly parquet in R2 under `nyse/`) is built after that,
against what the probe really returns.
