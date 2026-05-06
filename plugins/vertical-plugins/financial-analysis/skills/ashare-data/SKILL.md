---
name: ashare-data
description: |
  Fetch and analyze Chinese A-share market data via baostock. Covers historical OHLCV, fundamentals (profitability, growth, balance sheet, cash flow), industry classification, and trading calendar.

  **Perfect for:**
  - A-share valuation and comps analysis (Shanghai/Shenzhen)
  - Chinese company fundamental research
  - Sector/industry screening on SSE and SZSE
  - Trading calendar checks for A-share markets
---

# A-Share Market Data (baostock)

## Data Source

This skill uses **baostock** (http://baostock.com), a free open-source Python library providing comprehensive Chinese A-share market data from the Shanghai and Shenzhen stock exchanges.

## Available Tools

| Tool | Description |
|---|---|
| `ashare_history` | Historical K-line data (OHLCV) with adjustable frequency and price adjustment |
| `ashare_fundamentals` | Quarterly fundamentals: profit, growth, balance sheet, cash flow, operations |
| `ashare_trade_dates` | Trading calendar for A-share markets |
| `ashare_industry` | Industry classification (Shenwan/CSRC) |
| `ashare_stock_list` | List all A-share stocks with basic info |

## Stock Code Format

A-share codes use the format `{market}{code}`:
- Shanghai: `sh` prefix (e.g., `sh600000` = Pudong Development Bank)
- Shenzhen: `sz` prefix (e.g., `sz000001` = Ping An Bank)
- ChiNext: `sz300xxx`
- STAR Market: `sh688xxx`

## Usage Patterns

### Historical Price Data

```
ashare_history(code="sh600000", start_date="2024-01-01", end_date="2024-12-31", frequency="d", adjustflag="2")
```

- `frequency`: `d` (daily), `w` (weekly), `m` (monthly), `5` (5-min), `15` (15-min), `30` (30-min), `60` (60-min)
- `adjustflag`: `1` (forward-adjusted), `2` (backward-adjusted), `3` (unadjusted)

### Fundamentals

```
ashare_fundamentals(code="sh600000", year=2024, quarter=3)
```

Returns a dict with keys: `profit`, `growth`, `balance`, `cash_flow`, `operation`.

### Industry Classification

```
ashare_industry(code="sh600000")
```

### Trading Calendar

```
ashare_trade_dates(start_date="2024-01-01", end_date="2024-12-31")
```

## Integration Notes

- Data coverage: Full A-share history from 1990 onward
- Fundamentals: Quarterly reports from 2007 onward
- No API key required — baostock is free and open-source
- Data updates may lag by 1 business day
- For real-time data, supplement with other sources
