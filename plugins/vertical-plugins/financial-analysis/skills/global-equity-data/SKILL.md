---
name: global-equity-data
description: |
  Fetch market data for Hong Kong and US-listed stocks via yfinance. Covers historical prices, company info, financials (income/balance/cashflow), dividends, splits, and analyst recommendations.

  **Perfect for:**
  - US stock analysis (NYSE, NASDAQ, AMEX)
  - Hong Kong stock analysis (HKEX)
  - Cross-market comps (US + HK peers)
  - Analyst consensus and dividend history

  **Not ideal for:**
  - Real-time tick data or Level 2 quotes
  - Chinese A-shares (use ashare-data instead)
---

# Global Equity Data (yfinance)

## Data Source

This skill uses **yfinance**, a popular open-source library that downloads market data from Yahoo Finance. It covers US equities, Hong Kong stocks, global indices, ETFs, and more.

## Available Tools

| Tool | Description |
|---|---|
| `equity_history` | Historical OHLCV data with flexible periods and intervals |
| `equity_info` | Company profile: sector, industry, market cap, PE, business summary |
| `equity_financials` | Financial statements: income, balance sheet, cash flow |
| `equity_actions` | Dividend and stock split history |
| `equity_recommendations` | Analyst upgrade/downgrade history |

## Ticker Formats

| Market | Format | Examples |
|---|---|---|
| US stocks | `SYMBOL` | `AAPL`, `MSFT`, `GOOGL`, `TSLA` |
| Hong Kong stocks | `XXXX.HK` | `0700.HK` (Tencent), `9988.HK` (Alibaba), `0005.HK` (HSBC) |
| US indices | `^XXXX` | `^GSPC` (S&P 500), `^DJI` (Dow Jones), `^IXIC` (NASDAQ) |
| HK index | `^XXXX` | `^HSI` (Hang Seng) |
| ETFs | `SYMBOL` | `SPY`, `QQQ`, `2800.HK` (Tracker Fund) |

## Usage Patterns

### Price History

```
equity_history(ticker="AAPL", period="1y", interval="1d")
equity_history(ticker="0700.HK", period="6mo", interval="1d")
```

- `period`: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
- `interval`: `1m`, `5m`, `15m`, `30m`, `60m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

### Company Info

```
equity_info(ticker="0700.HK")
```

Returns: name, sector, industry, market cap, PE ratios, 52-week range, business summary, etc.

### Financial Statements

```
equity_financials(ticker="MSFT", statement="income", freq="yearly")
equity_financials(ticker="0700.HK", statement="balance", freq="quarterly")
```

- `statement`: `income`, `balance`, `cashflow`
- `freq`: `yearly`, `quarterly`

### Dividends & Splits

```
equity_actions(ticker="AAPL", period="10y")
```

### Analyst Recommendations

```
equity_recommendations(ticker="TSLA", period="3mo")
```

## Integration Notes

- No API key required — yfinance scrapes Yahoo Finance
- Data may have a 15-minute delay for intraday
- Hong Kong financials may be less comprehensive than US
- For institutional-grade data, supplement with MCP providers (FactSet, S&P)
