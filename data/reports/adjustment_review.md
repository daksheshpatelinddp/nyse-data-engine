# Adjustment review

One-day RAW price moves no split explains. `looks like a missed split` = the ratio is a usual split ratio, so Yahoo probably missed an event.
To fix one, add to data/manual_adjustments.json: `{"TICKER": [{"ex_date": "YYYY-MM-DD", "factor": 0.5, "description": "missed 2:1 split"}]}`

Jumps: 527, of which look like missed splits: 392

| ticker | company | date | prev | close | ratio | nearest | note |
|---|---|---|---|---|---|---|---|
| UVV | Universal Corporation Common Stock | 1975-11-12 | 39.75 | 20.0 | 0.5031 | 0.5 | looks like a missed split/bonus |
| MRSH | Marsh Common Stock | 1980-11-12 | 62.0 | 30.0 | 0.4839 | 0.4737 | looks like a missed split/bonus |
| NL | NLI Holdings, Inc. Common Stock | 1981-05-22 | 76.0 | 38.625 | 0.5082 | 0.5 | looks like a missed split/bonus |
| THC | Tenet Healthcare Corporation Common Stock | 1981-04-30 | 44.0 | 23.5 | 0.5341 | 0.5333 | looks like a missed split/bonus |
| WTRG | Essential Utilities, Inc. Common Stock | 1981-07-08 | 47.5 | 8.125 | 0.1711 | 0.1667 | looks like a missed split/bonus |
| BBWI | Bath & Body Works, Inc. | 1982-11-23 | 41.75 | 20.875 | 0.5 | 0.5 | looks like a missed split/bonus |
| LXU | LSB Industries, Inc. Common Stock | 1982-12-01 | 2.25 | 0.75 | 0.3333 | 0.3333 | looks like a missed split/bonus |
| LXU | LSB Industries, Inc. Common Stock | 1982-12-08 | 1.5 | 0.75 | 0.5 | 0.5 | looks like a missed split/bonus |
| SU | Suncor Energy  Inc. Common Stock | 1982-04-01 | 0.9375 | 1.875 | 2.0 | 2.0 | looks like a missed split/bonus |
| SU | Suncor Energy  Inc. Common Stock | 1982-05-26 | 1.3125 | 5.0 | 3.8095 | 4.0 | looks like a missed split/bonus |
| BBWI | Bath & Body Works, Inc. | 1983-06-14 | 53.0 | 28.625 | 0.5401 | 0.5385 | looks like a missed split/bonus |
| NBR | Nabors Industries Ltd. | 1983-11-09 | 3.0 | 1.25 | 0.4167 | 0.4167 | looks like a missed split/bonus |
| ODC | Oil-Dri Corporation Of America Common Stock | 1983-08-03 | 20.5 | 10.5 | 0.5122 | 0.5 | looks like a missed split/bonus |
| TSN | Tyson Foods, Inc. Common Stock | 1983-04-18 | 30.25 | 15.0 | 0.4959 | 0.5 | looks like a missed split/bonus |
| BEN | Franklin Templeton, Inc. Common Stock | 1984-12-31 | 24.25 | 9.75 | 0.4021 | 0.4 | looks like a missed split/bonus |
| GL | Globe Life Inc. Common Stock | 1984-05-30 | 39.25 | 19.625 | 0.5 | 0.5 | looks like a missed split/bonus |
| LNC | Lincoln National Corporation Common Stock | 1984-02-01 | 66.5 | 32.25 | 0.485 | 0.4737 | looks like a missed split/bonus |
| WSO-B | Watsco, Inc. Class B Common Stock | 1984-06-20 | 13.75 | 7.125 | 0.5182 | 0.5263 | looks like a missed split/bonus |
| BBWI | Bath & Body Works, Inc. | 1985-06-26 | 49.875 | 24.75 | 0.4962 | 0.5 | looks like a missed split/bonus |
| GL | Globe Life Inc. Common Stock | 1985-09-17 | 45.0 | 21.875 | 0.4861 | 0.4737 | looks like a missed split/bonus |
| TSN | Tyson Foods, Inc. Common Stock | 1985-04-16 | 43.0 | 18.5 | 0.4302 | 0.4286 | looks like a missed split/bonus |
| TRV | The Travelers Companies, Inc. Common Stock | 1986-06-09 | 90.25 | 43.25 | 0.4792 | 0.4737 | looks like a missed split/bonus |
| TSN | Tyson Foods, Inc. Common Stock | 1986-04-16 | 43.5 | 23.75 | 0.546 | 0.5455 | looks like a missed split/bonus |
| NVR | NVR, Inc. Common Stock | 1987-06-23 | 47.125 | 10.25 | 0.2175 | 0.2222 | looks like a missed split/bonus |
| CIA | Citizens, Inc. Class A Common Stock ($1.00 Par) | 1988-12-05 | 48.0 | 3.5 | 0.0729 | 0.0714 | looks like a missed split/bonus |
| CPF | Central Pacific Financial Corp New | 1988-06-02 | 50.5 | 25.875 | 0.5124 | 0.5 | looks like a missed split/bonus |
| KR | Kroger Company (The) Common Stock | 1988-10-31 | 58.0 | 18.25 | 0.3147 | 0.3077 | looks like a missed split/bonus |
| KR | Kroger Company (The) Common Stock | 1988-12-05 | 18.25 | 9.5 | 0.5205 | 0.5263 | looks like a missed split/bonus |
| LCII | LCI Industries | 1988-12-27 | 0.25 | 0.125 | 0.5 | 0.5 | looks like a missed split/bonus |
| LCII | LCI Industries | 1988-12-28 | 0.125 | 0.25 | 2.0 | 2.0 | looks like a missed split/bonus |
| TYL | Tyler Technologies, Inc. Common Stock | 1988-08-22 | 17.375 | 7.125 | 0.4101 | 0.4118 | looks like a missed split/bonus |
| PNW | Pinnacle West Capital Corporation Common Stock | 1989-12-07 | 5.375 | 10.25 | 1.907 | 2.0 | looks like a missed split/bonus |
| BH | Biglari Holdings Inc. Class B Common Stock | 1990-11-28 | 9.25 | 2.0 | 0.2162 | 0.2222 | looks like a missed split/bonus |
| CRD-B | Crawford & Company Common Stock | 1990-08-01 | 31.375 | 15.875 | 0.506 | 0.5 | looks like a missed split/bonus |
| MUX | McEwen Inc. Common Stock | 1990-02-20 | 1.3117 | 0.478 | 0.3644 | 0.3636 | looks like a missed split/bonus |
| RRC | Range Resources Corporation Common Stock | 1990-04-10 | 0.375 | 0.125 | 0.3333 | 0.3333 | looks like a missed split/bonus |
| WPP | WPP plc American Depositary Shares | 1990-11-20 | 11.375 | 5.5 | 0.4835 | 0.4737 | looks like a missed split/bonus |
| MUX | McEwen Inc. Common Stock | 1991-12-05 | 0.0535 | 0.0229 | 0.428 | 0.4286 | looks like a missed split/bonus |
| MUX | McEwen Inc. Common Stock | 1991-12-24 | 0.0229 | 0.1185 | 5.1747 | 5.0 | looks like a missed split/bonus |
| CNMD | CONMED Corporation Common Stock | 1992-10-09 | 17.5 | 9.125 | 0.5214 | 0.5263 | looks like a missed split/bonus |
| CTO | CTO Realty Growth, Inc. Common Stock | 1992-08-19 | 28.0 | 13.5 | 0.4821 | 0.4737 | looks like a missed split/bonus |
| HUM | Humana Inc. Common Stock | 1993-03-08 | 20.0 | 6.875 | 0.3438 | 0.3333 | looks like a missed split/bonus |
| HXL | Hexcel Corporation Common Stock | 1993-12-08 | 6.0 | 2.375 | 0.3958 | 0.4 | looks like a missed split/bonus |
| SAFE | Safehold Inc. New Common Stock | 1993-12-06 | 15.25 | 0.875 | 0.0574 | 0.0588 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1994-11-16 | 1.5 | 0.38 | 0.2533 | 0.25 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1994-11-28 | 0.308 | 0.616 | 2.0 | 2.0 | looks like a missed split/bonus |
| HUBB | Hubbell Inc Common Stock | 1994-10-31 | 5.8702 | 57.876 | 9.8593 | 10.0 | looks like a missed split/bonus |
| LNG | Cheniere Energy, Inc. Common Stock | 1994-05-25 | 0.75 | 1.5 | 2.0 | 2.0 | looks like a missed split/bonus |
| AN | AutoNation, Inc. Common Stock | 1995-05-22 | 3.875 | 7.75 | 2.0 | 2.0 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-09-19 | 0.5 | 0.248 | 0.496 | 0.5 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-11-01 | 0.248 | 0.5 | 2.0161 | 2.0 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-11-06 | 0.5 | 0.216 | 0.432 | 0.4286 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-11-07 | 0.216 | 0.408 | 1.8889 | 2.0 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-12-27 | 0.188 | 0.38 | 2.0213 | 2.0 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1995-12-28 | 0.38 | 0.188 | 0.4947 | 0.5 | looks like a missed split/bonus |
| ING | ING Group, N.V. Common Stock | 1995-09-27 | 58.375 | 114.0 | 1.9529 | 2.0 | looks like a missed split/bonus |
| ING | ING Group, N.V. Common Stock | 1995-09-28 | 114.0 | 58.375 | 0.5121 | 0.5 | looks like a missed split/bonus |
| CBZ | CBIZ, Inc. Common Stock | 1996-05-21 | 10.0 | 20.25 | 2.025 | 2.0 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1996-01-12 | 0.364 | 0.188 | 0.5165 | 0.5263 | looks like a missed split/bonus |
| LNG | Cheniere Energy, Inc. Common Stock | 1996-05-02 | 2.38 | 1.25 | 0.5252 | 0.5263 | looks like a missed split/bonus |
| LEN | Lennar Corporation Class A Common Stock | 1997-11-03 | 40.6875 | 16.625 | 0.4086 | 0.4118 | looks like a missed split/bonus |
| DECK | Deckers Outdoor Corporation Common Stock | 1998-10-13 | 4.375 | 2.0 | 0.4571 | 0.4545 | looks like a missed split/bonus |
| MUX | McEwen Inc. Common Stock | 1998-11-23 | 0.2686 | 0.1434 | 0.5339 | 0.5333 | looks like a missed split/bonus |
| SPB | Spectrum Brands Holdings, Inc. Common Stock | 1998-12-23 | 7.1875 | 14.25 | 1.9826 | 2.0 | looks like a missed split/bonus |
| BHE | Benchmark Electronics, Inc. Common Stock | 1999-10-22 | 29.0 | 15.0 | 0.5172 | 0.5263 | looks like a missed split/bonus |
| CSR | D/B/A Centerspace Common Stock | 1999-07-19 | 17.875 | 8.125 | 0.4545 | 0.4545 | looks like a missed split/bonus |
| DVA | DaVita Inc. Common Stock | 1999-02-18 | 21.0 | 8.75 | 0.4167 | 0.4167 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 1999-02-24 | 0.5 | 0.25 | 0.5 | 0.5 | looks like a missed split/bonus |
| MCK | McKesson Corporation Common Stock | 1999-04-28 | 65.75 | 34.5 | 0.5247 | 0.5263 | looks like a missed split/bonus |
| MD | Pediatrix Medical Group, Inc. Common Stock | 1999-02-12 | 53.625 | 28.0 | 0.5221 | 0.5263 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-09-21 | 0.375 | 0.1562 | 0.4165 | 0.4167 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-10-26 | 0.2812 | 0.5625 | 2.0004 | 2.0 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-10-27 | 0.5625 | 0.25 | 0.4444 | 0.4444 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-11-10 | 0.4375 | 0.1875 | 0.4286 | 0.4286 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-12-02 | 0.1875 | 0.375 | 2.0 | 2.0 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-12-03 | 0.375 | 0.1875 | 0.5 | 0.5 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-12-08 | 0.4688 | 0.1875 | 0.4 | 0.4 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 1999-12-23 | 0.25 | 0.0938 | 0.3752 | 0.375 | looks like a missed split/bonus |
| NSP | Insperity, Inc. Common Stock | 1999-01-28 | 31.25 | 15.875 | 0.508 | 0.5 | looks like a missed split/bonus |
| ARL | American Realty Investors, Inc. Common Stock | 2000-06-15 | 15.4375 | 6.6875 | 0.4332 | 0.4375 | looks like a missed split/bonus |
| BCE | BCE, Inc. Common Stock | 2000-05-09 | 113.6875 | 25.8125 | 0.227 | 0.2308 | looks like a missed split/bonus |
| CBZ | CBIZ, Inc. Common Stock | 2000-01-31 | 6.9375 | 3.7188 | 0.536 | 0.5385 | looks like a missed split/bonus |
| DAR | Darling Ingredients Inc. Common Stock | 2000-09-20 | 0.5625 | 0.25 | 0.4444 | 0.4444 | looks like a missed split/bonus |
| DX | Dynex Capital, Inc. Common Stock | 2000-03-10 | 7.4375 | 3.9375 | 0.5294 | 0.5294 | looks like a missed split/bonus |
| EGY | VAALCO Energy, Inc.  Common Stock | 2000-12-12 | 0.51 | 0.25 | 0.4902 | 0.5 | looks like a missed split/bonus |
| IMAX | Imax Corporation Common Stock | 2000-10-12 | 14.5 | 4.2812 | 0.2953 | 0.3 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 2000-04-27 | 0.1875 | 0.375 | 2.0 | 2.0 | looks like a missed split/bonus |
| MED | MEDIFAST INC Common Stock | 2000-09-12 | 0.25 | 0.5 | 2.0 | 2.0 | looks like a missed split/bonus |
| REX | REX American Resources Corporation | 2000-01-06 | 30.875 | 16.125 | 0.5223 | 0.5263 | looks like a missed split/bonus |
| TCI | Transcontinental Realty Investors, Inc. Common Stock | 2000-06-16 | 9.75 | 3.0 | 0.3077 | 0.3077 | looks like a missed split/bonus |
| AES | The AES Corporation Common Stock | 2001-09-26 | 24.25 | 12.25 | 0.5052 | 0.5 | looks like a missed split/bonus |
| CYD | China Yuchai International Limited Common Stock | 2001-09-28 | 0.56 | 0.3 | 0.5357 | 0.5333 | looks like a missed split/bonus |
| ROK | Rockwell Automation, Inc. Common Stock | 2001-07-02 | 38.12 | 14.7 | 0.3856 | 0.3846 | looks like a missed split/bonus |
| AORT | Artivion, Inc. Common Stock | 2002-08-15 | 5.5 | 2.03 | 0.3691 | 0.3636 | looks like a missed split/bonus |
| AVNT | Avient Corporation Common Stock | 2002-12-18 | 6.4 | 3.2 | 0.5 | 0.5 | looks like a missed split/bonus |
| DAR | Darling Ingredients Inc. Common Stock | 2002-01-14 | 0.7 | 0.32 | 0.4571 | 0.4545 | looks like a missed split/bonus |
| PWR | Quanta Services, Inc. Common Stock | 2002-07-02 | 9.14 | 2.92 | 0.3195 | 0.3077 | looks like a missed split/bonus |
| THC | Tenet Healthcare Corporation Common Stock | 2002-11-08 | 27.95 | 14.9 | 0.5331 | 0.5333 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-10-21 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-10-22 | 0.02 | 0.04 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-10-23 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-11-21 | 0.03 | 0.01 | 0.3333 | 0.3333 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-11-22 | 0.01 | 0.05 | 5.0 | 5.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-02 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-09 | 0.05 | 0.02 | 0.4 | 0.4 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-11 | 0.02 | 0.04 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-16 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-19 | 0.02 | 0.01 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2002-12-20 | 0.01 | 0.02 | 2.0 | 2.0 | looks like a missed split/bonus |
| UHAL | U-Haul Holding Company Common Stock | 2002-10-16 | 7.2 | 3.23 | 0.4486 | 0.4444 | looks like a missed split/bonus |
| WMB | Williams Companies, Inc. (The) Common Stock | 2002-07-22 | 5.16 | 2.01 | 0.3895 | 0.3846 | looks like a missed split/bonus |
| WMB | Williams Companies, Inc. (The) Common Stock | 2002-07-29 | 0.99 | 1.99 | 2.0101 | 2.0 | looks like a missed split/bonus |
| AGX | Argan, Inc. Common Stock | 2003-01-03 | 3.5 | 7.0 | 2.0 | 2.0 | looks like a missed split/bonus |
| EHC | Encompass Health Corporation Common Stock | 2003-07-07 | 0.9 | 1.89 | 2.1 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-01-07 | 0.02 | 0.04 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-01-09 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-01-28 | 0.02 | 0.01 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-01-29 | 0.01 | 0.05 | 5.0 | 5.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-01-31 | 0.04 | 0.01 | 0.25 | 0.25 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-02-13 | 0.01 | 0.04 | 4.0 | 4.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-02-18 | 0.04 | 0.01 | 0.25 | 0.25 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-02-20 | 0.01 | 0.05 | 5.0 | 5.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-02-26 | 0.04 | 0.01 | 0.25 | 0.25 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-02-28 | 0.01 | 0.04 | 4.0 | 4.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-03-03 | 0.04 | 0.01 | 0.25 | 0.25 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-03-05 | 0.01 | 0.03 | 3.0 | 3.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-03-17 | 0.03 | 0.01 | 0.3333 | 0.3333 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-03-31 | 0.1 | 0.02 | 0.2 | 0.2 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-03 | 0.05 | 0.1 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-14 | 0.05 | 0.1 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-15 | 0.1 | 0.02 | 0.2 | 0.2 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-16 | 0.02 | 0.01 | 0.5 | 0.5 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-22 | 0.04 | 0.08 | 2.0 | 2.0 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-04-23 | 0.08 | 0.03 | 0.375 | 0.375 | looks like a missed split/bonus |
| TRAK | ReposiTrak, Inc. Common Stock | 2003-12-30 | 0.02 | 0.04 | 2.0 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2003-06-18 | 0.04 | 0.02 | 0.5 | 0.5 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2003-07-21 | 0.02 | 0.04 | 2.0 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2003-08-19 | 0.06 | 0.12 | 2.0 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2003-08-20 | 0.12 | 0.06 | 0.5 | 0.5 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2003-08-27 | 0.05 | 0.1 | 2.0 | 2.0 | looks like a missed split/bonus |
| FNB | F.N.B. Corporation Common Stock | 2004-01-02 | 35.45 | 19.4 | 0.5472 | 0.5455 | looks like a missed split/bonus |
| IIIN | Insteel Industries, Inc. Common Stock | 2004-02-19 | 1.05 | 0.55 | 0.5238 | 0.5263 | looks like a missed split/bonus |
| SGU | Star Group L.P. Common Stock | 2004-10-18 | 21.6 | 4.32 | 0.2 | 0.2 | looks like a missed split/bonus |
| SKE | Skeena Resources Limited Common Shares | 2004-12-06 | 0.227 | 0.45 | 1.9824 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2004-05-27 | 0.05 | 0.1 | 2.0 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2004-06-24 | 0.1 | 0.05 | 0.5 | 0.5 | looks like a missed split/bonus |
| WT | WisdomTree, Inc. Common Stock | 2004-10-25 | 0.02 | 0.01 | 0.5 | 0.5 | looks like a missed split/bonus |
| WT | WisdomTree, Inc. Common Stock | 2004-10-26 | 0.01 | 0.02 | 2.0 | 2.0 | looks like a missed split/bonus |
| WT | WisdomTree, Inc. Common Stock | 2004-11-19 | 1.5 | 0.75 | 0.5 | 0.5 | looks like a missed split/bonus |
| MUX | McEwen Inc. Common Stock | 2005-08-01 | 0.3728 | 0.7744 | 2.0773 | 2.0 | looks like a missed split/bonus |
| UVE | UNIVERSAL INSURANCE HOLDINGS INC Common Stock | 2005-11-15 | 0.05 | 0.15 | 3.0 | 3.0 | looks like a missed split/bonus |
| VYX | NCR Voyix Corporation Common Stock | 2007-10-01 | 49.8 | 23.93 | 0.4805 | 0.4737 | looks like a missed split/bonus |
| AGM | Federal Agricultural Mortgage Corporation Common Stock | 2008-09-22 | 18.12 | 7.4 | 0.4084 | 0.4118 | looks like a missed split/bonus |
| AGM-A | Federal Agricultural Mortgage Corporation Common Stock | 2008-09-22 | 10.71 | 5.01 | 0.4678 | 0.4667 | looks like a missed split/bonus |
| AGM-A | Federal Agricultural Mortgage Corporation Common Stock | 2008-09-26 | 4.5 | 2.45 | 0.5444 | 0.5455 | looks like a missed split/bonus |
| AIG | American International Group, Inc. New Common Stock | 2008-09-15 | 12.14 | 4.76 | 0.3921 | 0.3846 | looks like a missed split/bonus |
| AIG | American International Group, Inc. New Common Stock | 2008-09-17 | 3.75 | 2.05 | 0.5467 | 0.5455 | looks like a missed split/bonus |
| BLDR | Builders FirstSource, Inc. Common Stock | 2008-11-19 | 1.6653 | 0.8999 | 0.5404 | 0.5385 | looks like a missed split/bonus |
| DIN | Dine Brands Global, Inc. Common Stock | 2008-10-28 | 9.06 | 18.3 | 2.0199 | 2.0 | looks like a missed split/bonus |
| FIS | Fidelity National Information Services, Inc. Common Stock | 2008-07-03 | 37.25 | 20.14 | 0.5407 | 0.5385 | looks like a missed split/bonus |
| FLUT | Flutter Entertainment plc Ordinary Shares | 2008-10-15 | 33.1 | 14.2 | 0.429 | 0.4286 | looks like a missed split/bonus |
| GNW | Genworth Financial Inc Common Stock | 2008-11-11 | 2.72 | 1.24 | 0.4559 | 0.4545 | looks like a missed split/bonus |
| GNW | Genworth Financial Inc Common Stock | 2008-11-24 | 0.9 | 1.7 | 1.8889 | 2.0 | looks like a missed split/bonus |
| GRBK | Green Brick Partners, Inc. Common Stock | 2008-08-12 | 2.52 | 0.93 | 0.369 | 0.3636 | looks like a missed split/bonus |
| HIG | The Hartford Insurance Group, Inc. Common Stock | 2008-10-30 | 19.86 | 9.62 | 0.4844 | 0.4737 | looks like a missed split/bonus |
| HIG | The Hartford Insurance Group, Inc. Common Stock | 2008-12-05 | 7.21 | 14.59 | 2.0236 | 2.0 | looks like a missed split/bonus |
| HOS | Hornbeck Offshore Services, Inc. Common Stock | 2008-11-20 | 7.33 | 4.0 | 0.5457 | 0.5455 | looks like a missed split/bonus |
| HUN | Huntsman Corporation Common Stock | 2008-12-15 | 5.85 | 2.98 | 0.5094 | 0.5 | looks like a missed split/bonus |
| KF | Korea Fund, Inc. (The) New Common Stock | 2008-12-29 | 117.99 | 32.02 | 0.2714 | 0.2727 | looks like a missed split/bonus |
| LAR | Lithium Argentina AG Common Shares | 2008-12-09 | 0.07 | 0.14 | 2.0 | 2.0 | looks like a missed split/bonus |
| LAR | Lithium Argentina AG Common Shares | 2008-12-23 | 0.09 | 0.18 | 2.0 | 2.0 | looks like a missed split/bonus |
| MO | Altria Group, Inc. | 2008-03-31 | 73.83 | 22.2 | 0.3007 | 0.3 | looks like a missed split/bonus |
| MXE | Mexico Equity and Income Fund, Inc. (The) Common Stock | 2008-12-23 | 13.15 | 6.38 | 0.4852 | 0.4737 | looks like a missed split/bonus |
| NX | Quanex Building Products Corporation Common Stock | 2008-04-24 | 54.17 | 16.37 | 0.3022 | 0.3 | looks like a missed split/bonus |
| OGC | OceanaGold Corporation Common Shares | 2008-10-03 | 0.56 | 0.3 | 0.5357 | 0.5333 | looks like a missed split/bonus |
| OGG | Osisko Gold Group Inc. Common Shares | 2008-10-28 | 0.158 | 0.055 | 0.3481 | 0.3571 | looks like a missed split/bonus |
| OGG | Osisko Gold Group Inc. Common Shares | 2008-11-25 | 0.177 | 0.089 | 0.5028 | 0.5 | looks like a missed split/bonus |
| SAFE | Safehold Inc. New Common Stock | 2008-09-29 | 3.8 | 1.75 | 0.4605 | 0.4615 | looks like a missed split/bonus |
| SKE | Skeena Resources Limited Common Shares | 2008-09-12 | 0.166 | 0.07 | 0.4217 | 0.4167 | looks like a missed split/bonus |
| SKE | Skeena Resources Limited Common Shares | 2008-11-18 | 0.063 | 0.016 | 0.254 | 0.25 | looks like a missed split/bonus |
| SUZ | Suzano S.A. American Depositary Shares (each representing One Ordinary Share) | 2008-12-11 | 11.36 | 4.0 | 0.3521 | 0.3571 | looks like a missed split/bonus |
| SUZ | Suzano S.A. American Depositary Shares (each representing One Ordinary Share) | 2008-12-22 | 4.0 | 11.944 | 2.986 | 3.0 | looks like a missed split/bonus |
| BXMT | Blackstone Mortgage Trust, Inc. Common Stock | 2009-03-12 | 1.12 | 2.17 | 1.9375 | 2.0 | looks like a missed split/bonus |
| CNO | CNO Financial Group, Inc. Common Stock | 2009-03-02 | 1.21 | 0.51 | 0.4215 | 0.4167 | looks like a missed split/bonus |
| DAN | Dana Incorporated Common Stock | 2009-03-10 | 0.2 | 0.4 | 2.0 | 2.0 | looks like a missed split/bonus |
| IDT | IDT Corporation Class B Common Stock | 2009-03-04 | 0.7062 | 1.3347 | 1.89 | 2.0 | looks like a missed split/bonus |
| LYG | Lloyds Banking Group Plc American Depositary Shares | 2009-01-20 | 6.0547 | 2.5488 | 0.421 | 0.4167 | looks like a missed split/bonus |
| MOD | Modine Manufacturing Company Common Stock | 2009-02-11 | 1.77 | 0.93 | 0.5254 | 0.5263 | looks like a missed split/bonus |
| NNI | Nelnet, Inc. Common Stock | 2009-02-26 | 10.74 | 4.91 | 0.4572 | 0.4545 | looks like a missed split/bonus |
| NVGS | Navigator Holdings Ltd. Ordinary Shares (Marshall Islands) | 2009-03-05 | 37.25 | 12.0 | 0.3221 | 0.3333 | looks like a missed split/bonus |
| NWG | NatWest Group plc American Depositary Shares, (each representing two (2) Ordinary Shares) | 2009-01-20 | 10.85 | 3.33 | 0.3069 | 0.3077 | looks like a missed split/bonus |
| OGC | OceanaGold Corporation Common Shares | 2009-01-09 | 0.11 | 0.21 | 1.9091 | 2.0 | looks like a missed split/bonus |
| OVV | Ovintiv Inc. (DE) | 2009-12-09 | 51.09 | 28.09 | 0.5498 | 0.5455 | looks like a missed split/bonus |
| SKE | Skeena Resources Limited Common Shares | 2009-11-23 | 0.052 | 0.147 | 2.8269 | 3.0 | looks like a missed split/bonus |
| STT | State Street Corporation Common Stock | 2009-01-20 | 36.35 | 14.89 | 0.4096 | 0.4118 | looks like a missed split/bonus |
| VPG | Vishay Precision Group, Inc. Common Stock | 2010-07-07 | 61.04 | 11.7 | 0.1917 | 0.2 | looks like a missed split/bonus |
| WY | Weyerhaeuser Company Common Stock | 2010-07-20 | 41.83 | 15.94 | 0.3811 | 0.3846 | looks like a missed split/bonus |
| BXMT | Blackstone Mortgage Trust, Inc. Common Stock | 2012-12-21 | 3.7 | 1.82 | 0.4919 | 0.5 | looks like a missed split/bonus |
| GDOT | Green Dot Corporation Class A Common Stock, $0.001 par value | 2012-07-27 | 23.32 | 9.06 | 0.3885 | 0.3846 | looks like a missed split/bonus |
| MTG | MGIC Investment Corporation Common Stock | 2012-08-02 | 2.45 | 0.88 | 0.3592 | 0.3571 | looks like a missed split/bonus |
