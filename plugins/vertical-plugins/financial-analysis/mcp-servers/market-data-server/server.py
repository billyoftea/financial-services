#!/usr/bin/env python3
"""
Market Data MCP Server
Integrates baostock (A-shares), yfinance (HK/US stocks), and ccxt (crypto).
"""

import json
import os
import sys
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# ── Proxy config ───────────────────────────────────────────────────────────────
# Set MARKET_DATA_PROXY env var or default to http://127.0.0.1:7890
PROXY_URL = os.environ.get("MARKET_DATA_PROXY", "http://127.0.0.1:7890")

server = Server("market-data")


# ── A-Share helpers (baostock) ────────────────────────────────────────────────

def _bs_login():
    import baostock as bs
    lg = bs.login()
    if lg.error_code != "0":
        raise RuntimeError(f"baostock login failed: {lg.error_msg}")
    return bs


def _bs_logout(bs):
    bs.logout()


def _date_str(d):
    return d.strftime("%Y-%m-%d") if isinstance(d, datetime) else str(d)


def _normalize_code(code):
    """Accept both sh600000 and sh.600000 formats, return sh.600000."""
    code = code.strip().lower()
    if "." not in code and len(code) >= 8:
        code = code[:2] + "." + code[2:]
    return code


def _rs_to_records(rs):
    rows = []
    while rs.next():
        values = rs.get_row_data()
        rows.append({rs.fields[i]: values[i] for i in range(len(rs.fields))})
    return rows


# ── A-Share tools ─────────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools():
    return [
        # ── A-Share (baostock) ──
        Tool(
            name="ashare_history",
            description="Get A-share historical K-line data (OHLCV). code format: sh600000, sz000001, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Stock code, e.g. sh600000"},
                    "start_date": {"type": "string", "description": "Start date YYYY-MM-DD, default 30 days ago"},
                    "end_date": {"type": "string", "description": "End date YYYY-MM-DD, default today"},
                    "frequency": {"type": "string", "description": "d=daily, w=weekly, m=monthly", "default": "d"},
                    "adjustflag": {"type": "string", "description": "1=forward, 2=backward, 3=none", "default": "2"},
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="ashare_fundamentals",
            description="Get A-share fundamental data: profitability, growth, balance sheet, cash flow.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Stock code, e.g. sh600000"},
                    "year": {"type": "integer", "description": "Report year, e.g. 2024"},
                    "quarter": {"type": "integer", "description": "Report quarter 1-4"},
                },
                "required": ["code", "year", "quarter"],
            },
        ),
        Tool(
            name="ashare_trade_dates",
            description="Get A-share trading dates for a given period.",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "End date YYYY-MM-DD"},
                },
                "required": ["start_date", "end_date"],
            },
        ),
        Tool(
            name="ashare_industry",
            description="Get stock industry classification.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Stock code, e.g. sh600000"},
                    "date": {"type": "string", "description": "Date YYYY-MM-DD, default today"},
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="ashare_stock_list",
            description="List A-share stocks by industry sector. Returns stocks filtered by tradeStatus.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date YYYY-MM-DD, default today"},
                    "limit": {"type": "integer", "description": "Max results (default 200)", "default": 200},
                },
                "required": [],
            },
        ),
        # ── HK/US (yfinance) ──
        Tool(
            name="equity_history",
            description="Get historical market data for HK/US stocks. Tickers: AAPL, 0700.HK, ^GSPC, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker symbol, e.g. AAPL, 0700.HK"},
                    "period": {"type": "string", "description": "1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max", "default": "1mo"},
                    "interval": {"type": "string", "description": "1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo", "default": "1d"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="equity_info",
            description="Get company info, sector, industry, market cap, PE, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker symbol"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="equity_financials",
            description="Get income statement, balance sheet, or cash flow statement.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker symbol"},
                    "statement": {"type": "string", "description": "income, balance, cashflow", "default": "income"},
                    "freq": {"type": "string", "description": "yearly or quarterly", "default": "yearly"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="equity_actions",
            description="Get dividends and stock splits history.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker symbol"},
                    "period": {"type": "string", "description": "max, 5y, 10y, etc.", "default": "max"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="equity_recommendations",
            description="Get analyst recommendations/upgrade-downgrade for a stock.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Ticker symbol"},
                    "period": {"type": "string", "description": "1mo, 3mo, 6mo, 1y", "default": "3mo"},
                },
                "required": ["ticker"],
            },
        ),
        # ── Crypto (ccxt) ──
        Tool(
            name="crypto_ticker",
            description="Get current price/ticker for a crypto pair on an exchange.",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {"type": "string", "description": "Exchange id, e.g. binance, okx, coinbase", "default": "binance"},
                    "symbol": {"type": "string", "description": "Trading pair, e.g. BTC/USDT"},
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="crypto_ohlcv",
            description="Get OHLCV (candlestick) data for a crypto pair.",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {"type": "string", "description": "Exchange id", "default": "binance"},
                    "symbol": {"type": "string", "description": "Trading pair, e.g. BTC/USDT"},
                    "timeframe": {"type": "string", "description": "1m,5m,15m,1h,4h,1d,1w", "default": "1d"},
                    "limit": {"type": "integer", "description": "Number of candles (max 1000)", "default": 100},
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="crypto_orderbook",
            description="Get order book for a crypto pair.",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {"type": "string", "description": "Exchange id", "default": "binance"},
                    "symbol": {"type": "string", "description": "Trading pair, e.g. BTC/USDT"},
                    "limit": {"type": "integer", "description": "Depth levels", "default": 20},
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="crypto_markets",
            description="List available markets on an exchange.",
            inputSchema={
                "type": "object",
                "properties": {
                    "exchange": {"type": "string", "description": "Exchange id", "default": "binance"},
                },
                "required": [],
            },
        ),
        Tool(
            name="crypto_exchanges",
            description="List supported crypto exchanges.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name, arguments):
    try:
        if name.startswith("ashare_"):
            return await _handle_ashare(name, arguments)
        elif name.startswith("equity_"):
            return await _handle_equity(name, arguments)
        elif name.startswith("crypto_"):
            return await _handle_crypto(name, arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {type(e).__name__}: {e}")]


# ── A-Share handlers ──────────────────────────────────────────────────────────

async def _handle_ashare(name, args):
    bs = _bs_login()
    try:
        if name == "ashare_history":
            code = _normalize_code(args["code"])
            end = args.get("end_date", _date_str(datetime.today()))
            start = args.get("start_date", _date_str(datetime.today() - timedelta(days=30)))
            freq = args.get("frequency", "d")
            adj = args.get("adjustflag", "2")
            rs = bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                start_date=start, end_date=end,
                frequency=freq, adjustflag=adj,
            )
            data = _rs_to_records(rs)

        elif name == "ashare_fundamentals":
            code = _normalize_code(args["code"])
            year, quarter = args["year"], args["quarter"]
            fields_map = {
                "profit": bs.query_profit_data,
                "growth": bs.query_growth_data,
                "balance": bs.query_balance_data,
                "cash_flow": bs.query_cash_flow_data,
                "operation": bs.query_operation_data,
            }
            data = {}
            for key, fn in fields_map.items():
                rs = fn(code=code, year=year, quarter=quarter)
                rows = _rs_to_records(rs)
                if rows:
                    data[key] = rows[0]

        elif name == "ashare_trade_dates":
            start = args["start_date"]
            end = args["end_date"]
            rs = bs.query_trade_dates(start_date=start, end_date=end)
            data = _rs_to_records(rs)

        elif name == "ashare_industry":
            code = _normalize_code(args["code"])
            date = args.get("date", _date_str(datetime.today()))
            rs = bs.query_stock_industry(code=code, date=date)
            data = _rs_to_records(rs)

        elif name == "ashare_stock_list":
            date = args.get("date", _date_str(datetime.today()))
            limit = min(args.get("limit", 200), 500)
            data = []
            rs = bs.query_all_stock(day=date)
            while rs.next() and len(data) < limit:
                row = rs.get_row_data()
                row_dict = {rs.fields[i]: row[i] for i in range(len(rs.fields))}
                if row_dict.get("tradeStatus") == "1":
                    data.append(row_dict)
        else:
            data = {"error": f"Unknown ashare tool: {name}"}

        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2, default=str))]

    finally:
        _bs_logout(bs)


# ── Equity handlers (yfinance) ────────────────────────────────────────────────

async def _handle_equity(name, args):
    import yfinance as yf
    os.environ["HTTP_PROXY"] = PROXY_URL
    os.environ["HTTPS_PROXY"] = PROXY_URL

    if name == "equity_history":
        ticker = yf.Ticker(args["ticker"])
        hist = ticker.history(
            period=args.get("period", "1mo"),
            interval=args.get("interval", "1d"),
        )
        data = hist.reset_index().to_dict(orient="records")
        for r in data:
            for k, v in r.items():
                if hasattr(v, "isoformat"):
                    r[k] = v.isoformat()
                elif hasattr(v, "item"):
                    r[k] = v.item()

    elif name == "equity_info":
        ticker = yf.Ticker(args["ticker"])
        info = ticker.info
        keep_keys = [
            "shortName", "longName", "symbol", "sector", "industry", "country", "city",
            "marketCap", "totalRevenue", "grossProfits", "ebitda",
            "trailingPE", "forwardPE", "priceToBook", "enterpriseToRevenue",
            "enterpriseToEbitda", "dividendYield", "beta",
            "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
            "fiftyDayAverage", "twoHundredDayAverage",
            "currentPrice", "previousClose", "open", "dayLow", "dayHigh",
            "volume", "averageVolume", "sharesOutstanding", "floatShares",
            "longBusinessSummary",
        ]
        data = {k: info.get(k) for k in keep_keys if k in info}

    elif name == "equity_financials":
        ticker = yf.Ticker(args["ticker"])
        stmt_type = args.get("statement", "income")
        freq = args.get("freq", "yearly")
        if stmt_type == "income":
            df = ticker.income_stmt if freq == "yearly" else ticker.quarterly_income_stmt
        elif stmt_type == "balance":
            df = ticker.balance_sheet if freq == "yearly" else ticker.quarterly_balance_sheet
        else:
            df = ticker.cashflow if freq == "yearly" else ticker.quarterly_cashflow
        if df is not None and not df.empty:
            data = df.to_dict()
            cleaned = {}
            for col, vals in data.items():
                col_key = col.isoformat() if hasattr(col, "isoformat") else str(col)
                cleaned[col_key] = {str(k): (v.item() if hasattr(v, "item") else v) for k, v in vals.items() if v == v}
            data = cleaned
        else:
            data = {}

    elif name == "equity_actions":
        ticker = yf.Ticker(args["ticker"])
        period = args.get("period", "max")
        divs = ticker.dividends
        splits = ticker.splits
        data = {
            "dividends": [{"date": idx.isoformat(), "amount": val.item() if hasattr(val, "item") else val}
                          for idx, val in divs.items()] if divs is not None and not divs.empty else [],
            "splits": [{"date": idx.isoformat(), "ratio": val.item() if hasattr(val, "item") else val}
                       for idx, val in splits.items()] if splits is not None and not splits.empty else [],
        }

    elif name == "equity_recommendations":
        ticker = yf.Ticker(args["ticker"])
        rec = ticker.recommendations
        if rec is not None and not rec.empty:
            data = rec.tail(20).to_dict(orient="records")
            for r in data:
                for k, v in r.items():
                    if hasattr(v, "isoformat"):
                        r[k] = v.isoformat()
                    elif hasattr(v, "item"):
                        r[k] = v.item()
        else:
            data = []

    else:
        data = {"error": f"Unknown equity tool: {name}"}

    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2, default=str))]


# ── Crypto handlers (ccxt) ────────────────────────────────────────────────────

async def _handle_crypto(name, args):
    if name == "crypto_exchanges":
        import ccxt
        data = ccxt.exchanges
        return [TextContent(type="text", text=json.dumps(data))]

    exchange_id = args.get("exchange", "binance")
    import ccxt
    exchange_cls = getattr(ccxt, exchange_id, None)
    if exchange_cls is None:
        return [TextContent(type="text", text=f"Error: unknown exchange '{exchange_id}'")]
    ex = exchange_cls({
        "enableRateLimit": True,
        "proxies": {"http": PROXY_URL, "https": PROXY_URL},
    })

    try:
        if name == "crypto_ticker":
            symbol = args["symbol"]
            ticker = ex.fetch_ticker(symbol)
            data = {k: v for k, v in ticker.items()
                    if not isinstance(v, (dict, list)) or k in ("info",)}

        elif name == "crypto_ohlcv":
            symbol = args["symbol"]
            tf = args.get("timeframe", "1d")
            limit = min(args.get("limit", 100), 1000)
            ohlcv = ex.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
            data = [{"timestamp": c[0], "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[5]}
                    for c in ohlcv]

        elif name == "crypto_orderbook":
            symbol = args["symbol"]
            limit = args.get("limit", 20)
            ob = ex.fetch_order_book(symbol, limit=limit)
            data = {
                "bids": ob["bids"][:limit],
                "asks": ob["asks"][:limit],
                "timestamp": ob.get("timestamp"),
            }

        elif name == "crypto_markets":
            ex.load_markets()
            data = [{"symbol": m["symbol"], "base": m["base"], "quote": m["quote"], "active": m.get("active", True)}
                    for m in ex.markets.values()]
            data = data[:500]

        else:
            data = {"error": f"Unknown crypto tool: {name}"}

    finally:
        if hasattr(ex, "close"):
            ex.close()

    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2, default=str))]


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
