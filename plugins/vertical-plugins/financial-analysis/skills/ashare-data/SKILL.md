---
name: ashare-data
description: |
  Fetch and analyze Chinese A-share market data. Primary source: **akshare** (Sina/THS/Baidu).
  Fallback: **baostock** for trade dates, industry classification, and stock lists.

  **Perfect for:**
  - A-share valuation and comps analysis (Shanghai/Shenzhen)
  - Chinese company fundamental research (EPS, ROE, ROA, margins)
  - PE/PB/market cap valuation metrics
  - Sector/industry screening on SSE and SZSE
  - Market-wide PB/PE quantile analysis
  - Trading calendar checks for A-share markets
---

# A-Share Market Data

## Data Sources

| Source | Backend | Tools | Notes |
|---|---|---|---|
| **akshare** (primary) | Sina | K-line history | Free, no API key, no proxy needed |
| **akshare** (primary) | THS (同花顺) | Fundamentals (EPS, ROE, margins) | Rich per-share and profitability metrics |
| **akshare** (primary) | Baidu | PE, PB, market cap | Daily valuation time series |
| **akshare** (primary) | Sina | Financial statements | Income, balance sheet, cash flow |
| **akshare** (primary) | Sina | Index daily data | SSE/SZSE indices |
| **baostock** (fallback) | BaoStock | K-line, fundamentals | Used if akshare fails |
| **baostock** | BaoStock | Trade dates, industry, stock list | Only available via baostock |

## Available Tools

| Tool | Source | Description |
|---|---|---|
| `ashare_history` | akshare/baostock | Historical K-line data (OHLCV) |
| `ashare_fundamentals` | akshare/baostock | Per-share metrics, ROE, ROA, margins, growth rates |
| `ashare_financials` | akshare | Financial statements: 利润表, 资产负债表, 现金流量表 |
| `ashare_valuation` | akshare | PE (TTM), PB, total market cap (Baidu) |
| `ashare_index_daily` | akshare | SSE/SZSE index daily data |
| `ashare_market_pb` | akshare | Market-wide PB with historical quantiles |
| `ashare_market_pe` | akshare | Market-wide PE with historical quantiles |
| `ashare_trade_dates` | baostock | Trading calendar |
| `ashare_industry` | baostock | Industry classification (CSRC) |
| `ashare_stock_list` | baostock | List all A-share stocks with basic info |

## Stock Code Format

All tools accept flexible formats:
- `sh600000`, `sz000001` (with exchange prefix)
- `600036` (6-digit code, auto-detected)
- `sh.600000` (baostock format also accepted)

## Usage Patterns

### Historical Price Data

```
ashare_history(code="600036", start_date="2024-01-01", end_date="2024-12-31")
```

### Fundamentals (EPS, ROE, etc.)

```
ashare_fundamentals(code="600036", year=2024, quarter=3)
```

Returns per-share metrics (摊薄每股收益, 每股净资产, 每股经营性现金流), profitability ratios (总资产利润率, 净资产收益率, 销售净利率), and more.

### Financial Statements

```
ashare_financials(code="600036", statement="利润表")
ashare_financials(code="600036", statement="资产负债表")
ashare_financials(code="600036", statement="现金流量表")
```

### Valuation Metrics

```
ashare_valuation(code="600036", indicator="市盈率(TTM)")
ashare_valuation(code="600036", indicator="市净率")
ashare_valuation(code="600036", indicator="总市值")
```

### Market-Wide Valuation

```
ashare_market_pb()  # Overall A-share PB + historical quantiles
ashare_market_pe()  # Overall A-share PE
```

### Index Data

```
ashare_index_daily(symbol="sh000001", start_date="2025-01-01", end_date="2025-04-01")
```

Common indices: `sh000001` (上证综指), `sz399001` (深证成指), `sz399006` (创业板指).

## Integration Notes

- Data coverage: Full A-share history from 1990 onward
- Fundamentals: Quarterly reports via THS, dating back to IPO
- Valuation: Daily PE/PB/market cap via Baidu Finance
- No API key required — all sources are free
- akshare tools use domestic APIs (no proxy needed)
- baostock requires login/logout session management (handled automatically)
- Data updates may lag by 1 business day
