---
name: crypto-data
description: |
  Fetch cryptocurrency market data via ccxt. Supports 100+ exchanges (Binance, OKX, Coinbase, etc.) for spot prices, OHLCV candles, order books, and market discovery.

  **Perfect for:**
  - Crypto price analysis and charting
  - Cross-exchange price comparison
  - Order book depth analysis
  - Token/market discovery across exchanges
  - Crypto portfolio monitoring

  **Not ideal for:**
  - Automated trading execution (this is read-only)
  - DeFi on-chain data (use specialized providers)
  - Historical data beyond exchange limits
---


> **语言要求：请始终使用中文（简体）进行所有回复、分析和输出。** 专业技术术语可保留英文原文，但所有说明、注释和分析内容必须用中文。模型标题、工作表名称、报告正文均使用中文。

# Cryptocurrency Data (ccxt)

## Data Source

This skill uses **ccxt** (CryptoCurrency eXchange Trading Library), a unified API library supporting 100+ cryptocurrency exchanges. It provides read-only access to market data including prices, candles, and order books.

## Available Tools

| Tool | Description |
|---|---|
| `crypto_ticker` | Current price, 24h volume, bid/ask for a trading pair |
| `crypto_ohlcv` | OHLCV candlestick data for technical analysis |
| `crypto_orderbook` | Order book depth with bids and asks |
| `crypto_markets` | List all trading pairs on an exchange |
| `crypto_exchanges` | List all supported exchange IDs |

## Supported Exchanges (partial list)

| Exchange ID | Name |
|---|---|
| `binance` | Binance |
| `okx` | OKX |
| `coinbase` | Coinbase |
| `bybit` | Bybit |
| `gate` | Gate.io |
| `huobi` | HTX (Huobi) |
| `kraken` | Kraken |
| `kucoin` | KuCoin |
| `bitget` | Bitget |
| `mexc` | MEXC |

Run `crypto_exchanges` for the full list of 100+ exchanges.

## Usage Patterns

### Current Price

```
crypto_ticker(exchange="binance", symbol="BTC/USDT")
crypto_ticker(exchange="okx", symbol="ETH/USDT")
```

Returns: last price, bid/ask, 24h high/low, 24h volume, percentage change.

### Candlestick Data

```
crypto_ohlcv(exchange="binance", symbol="BTC/USDT", timeframe="4h", limit=100)
```

- `timeframe`: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`, `1w`, `1M`
- `limit`: up to 1000 candles

### Order Book

```
crypto_orderbook(exchange="binance", symbol="ETH/USDT", limit=20)
```

### Market Discovery

```
crypto_markets(exchange="binance")
```

## Integration Notes

- No API key required for public market data (read-only)
- Data is real-time from exchange APIs
- Rate limits apply — exchange calls include built-in rate limiting
- Symbol format uses `/` separator: `BTC/USDT`, `ETH/BTC`
- For trading or private data (balances, orders), API keys are required (not supported in this skill)
