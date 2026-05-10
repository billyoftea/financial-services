#!/usr/bin/env python3
"""
ESG 数据获取工具 - 从多个数据源获取 ESG 评分数据

支持的数据源:
1. Yahoo Finance (免费, 通过 yfinance 库)
2. 本地 CSV/Excel 文件导入
3. 手动输入数据

用法:
    python esg_data_fetcher.py --ticker AAPL --source yahoo
    python esg_data_fetcher.py --file esg_data.csv --source csv
    python esg_data_fetcher.py --ticker MSFT --source yahoo --output json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def fetch_yahoo_esg(ticker: str) -> dict:
    """
    从 Yahoo Finance 获取 ESG 评分数据。
    Yahoo Finance 提供 MSCI 相似评分体系（可持续性得分）。

    返回:
        dict: 包含 ESG 总分、E/S/G 维度分、争议得分等
    """
    try:
        import yfinance as yf
    except ImportError:
        print("错误: 需要 yfinance 库。请运行: pip install yfinance")
        sys.exit(1)

    stock = yf.Ticker(ticker)
    sustainability = stock.sustainability

    if sustainability is None or sustainability.empty:
        print(f"警告: 未找到 {ticker} 的 ESG 数据")
        return {
            "ticker": ticker,
            "source": "Yahoo Finance",
            "fetch_time": datetime.now().isoformat(),
            "data_available": False,
            "message": f"未找到 {ticker} 的 ESG 可持续性数据"
        }

    # 提取关键 ESG 指标
    esg_data = {
        "ticker": ticker,
        "source": "Yahoo Finance",
        "fetch_time": datetime.now().isoformat(),
        "data_available": True,
        "esg_scores": {},
        "environmental": {},
        "social": {},
        "governance": {},
        "controversy": {}
    }

    # 解析 Yahoo Finance 可持续性数据
    # Yahoo 使用百分位排名（0-100，越高越好）
    score_map = {
        "totalEsg": "ESG总分",
        "environmentScore": "环境得分",
        "socialScore": "社会得分",
        "governanceScore": "治理得分",
        "esgPerformance": "ESG表现等级",
        "percentile": "ESG百分位排名",
        "peerGroup": "行业分组",
        "highestControversy": "最高争议等级",
    }

    for key, label in score_map.items():
        if key in sustainability.index:
            val = sustainability.loc[key]
            # yfinance 返回 DataFrame，取第一列的值
            if hasattr(val, 'iloc'):
                val = val.iloc[0]
            esg_data["esg_scores"][label] = val

    # 提取环境维度
    env_keys = ["environmentScore"]
    for key in env_keys:
        if key in sustainability.index:
            val = sustainability.loc[key]
            if hasattr(val, 'iloc'):
                val = val.iloc[0]
            esg_data["environmental"][key] = val

    # 提取社会维度
    social_keys = ["socialScore"]
    for key in social_keys:
        if key in sustainability.index:
            val = sustainability.loc[key]
            if hasattr(val, 'iloc'):
                val = val.iloc[0]
            esg_data["social"][key] = val

    # 提取治理维度
    gov_keys = ["governanceScore"]
    for key in gov_keys:
        if key in sustainability.index:
            val = sustainability.loc[key]
            if hasattr(val, 'iloc'):
                val = val.iloc[0]
            esg_data["governance"][key] = val

    # 争议信息
    controversy_keys = ["highestControversy", "controversyScore"]
    for key in controversy_keys:
        if key in sustainability.index:
            val = sustainability.loc[key]
            if hasattr(val, 'iloc'):
                val = val.iloc[0]
            esg_data["controversy"][key] = val

    return esg_data


def fetch_from_csv(file_path: str) -> dict:
    """
    从 CSV 文件导入 ESG 数据。

    预期 CSV 格式:
    ticker, company_name, msci_rating, sustainalytics_risk, sp_global_score, e_score, s_score, g_score

    返回:
        dict: 标准化的 ESG 数据
    """
    import csv

    data = {
        "source": f"CSV文件: {file_path}",
        "fetch_time": datetime.now().isoformat(),
        "companies": []
    }

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company_data = {
                "ticker": row.get("ticker", ""),
                "company_name": row.get("company_name", ""),
                "fetch_time": datetime.now().isoformat(),
                "data_available": True,
                "esg_scores": {
                    "MSCI评级": row.get("msci_rating", "N/A"),
                    "Sustainalytics风险分": row.get("sustainalytics_risk", "N/A"),
                    "S&P Global得分": row.get("sp_global_score", "N/A"),
                },
                "environmental": {"E得分": row.get("e_score", "N/A")},
                "social": {"S得分": row.get("s_score", "N/A")},
                "governance": {"G得分": row.get("g_score", "N/A")},
            }
            data["companies"].append(company_data)

    return data


def fetch_from_excel(file_path: str) -> dict:
    """
    从 Excel 文件导入 ESG 数据。

    返回:
        dict: 标准化的 ESG 数据
    """
    try:
        import pandas as pd
    except ImportError:
        print("错误: 需要 pandas 和 openpyxl 库。请运行: pip install pandas openpyxl")
        sys.exit(1)

    df = pd.read_excel(file_path)

    data = {
        "source": f"Excel文件: {file_path}",
        "fetch_time": datetime.now().isoformat(),
        "companies": []
    }

    # 尝试自动映射常见列名
    col_map = {}
    for col in df.columns:
        col_lower = col.lower().strip()
        if "ticker" in col_lower or "代码" in col_lower:
            col_map["ticker"] = col
        elif "company" in col_lower or "公司" in col_lower or "名称" in col_lower:
            col_map["company_name"] = col
        elif "msci" in col_lower:
            col_map["msci"] = col
        elif "sustain" in col_lower:
            col_map["sustainalytics"] = col
        elif "sp" in col_lower or "s&p" in col_lower:
            col_map["sp_global"] = col

    for _, row in df.iterrows():
        company_data = {
            "ticker": str(row.get(col_map.get("ticker", ""), "")),
            "company_name": str(row.get(col_map.get("company_name", ""), "")),
            "fetch_time": datetime.now().isoformat(),
            "data_available": True,
            "esg_scores": {}
        }
        if "msci" in col_map:
            company_data["esg_scores"]["MSCI评级"] = str(row[col_map["msci"]])
        if "sustainalytics" in col_map:
            company_data["esg_scores"]["Sustainalytics风险分"] = str(row[col_map["sustainalytics"]])
        if "sp_global" in col_map:
            company_data["esg_scores"]["S&P Global得分"] = str(row[col_map["sp_global"]])

        data["companies"].append(company_data)

    return data


def compare_esg(tickers: list, output_format: str = "dict") -> dict:
    """
    对比多个公司的 ESG 表现。

    参数:
        tickers: 股票代码列表
        output_format: 输出格式 ("dict", "json")

    返回:
        dict: 多公司 ESG 对比数据
    """
    comparison = {
        "comparison_date": datetime.now().isoformat(),
        "source": "Yahoo Finance",
        "companies": []
    }

    for ticker in tickers:
        data = fetch_yahoo_esg(ticker)
        comparison["companies"].append(data)

    if output_format == "json":
        return json.dumps(comparison, ensure_ascii=False, indent=2)

    return comparison


def main():
    parser = argparse.ArgumentParser(description="ESG 数据获取工具")
    parser.add_argument("--ticker", type=str, help="股票代码（如 AAPL）")
    parser.add_argument("--tickers", type=str, nargs="+", help="多个股票代码（用于对比）")
    parser.add_argument("--file", type=str, help="本地数据文件路径（CSV 或 Excel）")
    parser.add_argument("--source", choices=["yahoo", "csv", "excel"], default="yahoo",
                        help="数据源（默认: yahoo）")
    parser.add_argument("--output", choices=["json", "text"], default="json",
                        help="输出格式（默认: json）")

    args = parser.parse_args()

    if args.tickers:
        result = compare_esg(args.tickers, args.output)
    elif args.ticker and args.source == "yahoo":
        result = fetch_yahoo_esg(args.ticker)
    elif args.file and args.source == "csv":
        result = fetch_from_csv(args.file)
    elif args.file and args.source == "excel":
        result = fetch_from_excel(args.file)
    else:
        parser.print_help()
        sys.exit(1)

    if args.output == "json" or args.source == "yahoo":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(result)


if __name__ == "__main__":
    main()
