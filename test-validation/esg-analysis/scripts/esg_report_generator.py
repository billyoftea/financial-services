#!/usr/bin/env python3
"""
ESG 分析报告生成器 - 将 ESG 数据转化为标准化分析报告

支持输出格式:
1. Markdown 报告
2. Excel 工作簿

用法:
    python esg_report_generator.py --input esg_data.json --output report.md
    python esg_report_generator.py --input esg_data.json --output report.xlsx
    python esg_report_generator.py --input esg_data.json --output report.md --compare
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


# ESG 风险评级函数
def get_risk_level(sustainalytics_score: float) -> str:
    """根据 Sustainalytics 风险分判定风险等级"""
    if sustainalytics_score <= 10:
        return "可忽略 (Negligible)"
    elif sustainalytics_score <= 20:
        return "低风险 (Low)"
    elif sustainalytics_score <= 30:
        return "中等风险 (Medium)"
    elif sustainalytics_score <= 40:
        return "高风险 (High)"
    else:
        return "严重风险 (Severe)"


def get_msci_quality(rating: str) -> str:
    """根据 MSCI 评级判定质量水平"""
    quality_map = {
        "AAA": "领先 (Leader)", "AA": "领先 (Leader)",
        "A": "平均 (Average)",
        "BBB": "平均 (Average)",
        "BB": "滞后 (Laggard)", "B": "滞后 (Laggard)", "CCC": "滞后 (Laggard)",
    }
    return quality_map.get(rating.upper(), "未知")


def generate_markdown_report(esg_data: dict, is_comparison: bool = False) -> str:
    """生成 Markdown 格式的 ESG 分析报告"""
    timestamp = datetime.now().strftime("%Y年%m月%d日")

    lines = []
    if is_comparison and "companies" in esg_data:
        # 多公司对比报告
        lines.append(f"# ESG 对比分析报告")
        lines.append(f"\n> 报告生成日期: {timestamp}\n")

        companies = esg_data.get("companies", [])
        lines.append("## 一、概览对比表\n")
        lines.append("| 公司 | 代码 | ESG 总分 | 环境得分 | 社会得分 | 治理得分 |")
        lines.append("|------|------|---------|---------|---------|---------|")

        for c in companies:
            name = c.get("company_name", c.get("ticker", "N/A"))
            ticker = c.get("ticker", "N/A")
            scores = c.get("esg_scores", {})
            total = scores.get("ESG总分", scores.get("totalEsg", "N/A"))
            e = c.get("environmental", {}).get("environmentScore", c.get("environmental", {}).get("E得分", "N/A"))
            s = c.get("social", {}).get("socialScore", c.get("social", {}).get("S得分", "N/A"))
            g = c.get("governance", {}).get("governanceScore", c.get("governance", {}).get("G得分", "N/A"))
            lines.append(f"| {name} | {ticker} | {total} | {e} | {s} | {g} |")

        # 维度分析
        lines.append("\n## 二、各维度分析\n")
        for c in companies:
            name = c.get("company_name", c.get("ticker", "N/A"))
            lines.append(f"### {name}\n")
            env = c.get("environmental", {})
            soc = c.get("social", {})
            gov = c.get("governance", {})
            lines.append(f"- **环境 (E)**: {env}")
            lines.append(f"- **社会 (S)**: {soc}")
            lines.append(f"- **治理 (G)**: {gov}\n")

    else:
        # 单公司报告
        ticker = esg_data.get("ticker", "N/A")
        lines.append(f"# ESG 分析报告: {ticker}")
        lines.append(f"\n> 报告生成日期: {timestamp}\n")

        scores = esg_data.get("esg_scores", {})
        lines.append("## 一、ESG 综合评分\n")
        lines.append("```")
        for key, val in scores.items():
            lines.append(f"  {key}: {val}")
        lines.append("```\n")

        # 维度详情
        for dim_name, dim_key in [("环境", "environmental"), ("社会", "social"), ("治理", "governance")]:
            dim_data = esg_data.get(dim_key, {})
            if dim_data:
                lines.append(f"## {['一','二','三','四','五'][['一','二','三','四','五'].index('二') + [{'environmental':0,'social':1,'governance':2}.get(dim_key,0)]]} + 2、{dim_name}维度详情\n")
                for k, v in dim_data.items():
                    lines.append(f"- **{k}**: {v}")
                lines.append("")

        # 争议分析
        controversy = esg_data.get("controversy", {})
        if controversy:
            lines.append("## 五、争议事件分析\n")
            for k, v in controversy.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")

    # 总结
    lines.append("---\n")
    lines.append(f"*报告由 ESG 分析工具自动生成 | {timestamp}*")

    return "\n".join(lines)


def generate_excel_report(esg_data: dict, output_path: str, is_comparison: bool = False):
    """生成 Excel 格式的 ESG 分析报告"""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    except ImportError:
        print("错误: 需要 openpyxl 库。请运行: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.Workbook()

    # 定义样式
    header_font = Font(name="微软雅黑", size=12, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    title_font = Font(name="微软雅黑", size=16, bold=True)
    cell_font = Font(name="微软雅黑", size=10)
    border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # 概览工作表
    ws = wb.active
    ws.title = "ESG概览"
    ws.merge_cells('A1:F1')
    ws['A1'] = "ESG 分析报告"
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal='center')

    # 写入 ESG 评分
    row = 3
    headers = ["指标", "数值"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        cell.border = border

    if is_comparison and "companies" in esg_data:
        # 多公司对比
        companies = esg_data.get("companies", [])
        row = 4
        for c in companies:
            name = c.get("company_name", c.get("ticker", "N/A"))
            ws.cell(row=row, column=1, value=name).font = cell_font
            scores = c.get("esg_scores", {})
            score_str = " | ".join([f"{k}: {v}" for k, v in scores.items()])
            ws.cell(row=row, column=2, value=score_str).font = cell_font
            row += 1
    else:
        # 单公司
        scores = esg_data.get("esg_scores", {})
        row = 4
        for key, val in scores.items():
            ws.cell(row=row, column=1, value=key).font = cell_font
            ws.cell(row=row, column=2, value=str(val)).font = cell_font
            ws.cell(row=row, column=1).border = border
            ws.cell(row=row, column=2).border = border
            row += 1

    # E/S/G 维度工作表
    for dim_name, dim_key in [("环境E", "environmental"), ("社会S", "social"), ("治理G", "governance")]:
        ws_dim = wb.create_sheet(title=dim_name)
        ws_dim.merge_cells('A1:B1')
        ws_dim['A1'] = f"{dim_name} 维度详情"
        ws_dim['A1'].font = title_font

        ws_dim.cell(row=3, column=1, value="指标").font = header_font
        ws_dim.cell(row=3, column=1).fill = header_fill
        ws_dim.cell(row=3, column=2, value="数值").font = header_font
        ws_dim.cell(row=3, column=2).fill = header_fill

        dim_data = esg_data.get(dim_key, {})
        r = 4
        for k, v in dim_data.items():
            ws_dim.cell(row=r, column=1, value=k).font = cell_font
            ws_dim.cell(row=r, column=2, value=str(v)).font = cell_font
            ws_dim.cell(row=r, column=1).border = border
            ws_dim.cell(row=r, column=2).border = border
            r += 1

    wb.save(output_path)
    print(f"Excel 报告已保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="ESG 分析报告生成器")
    parser.add_argument("--input", required=True, help="ESG 数据 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出报告路径（.md 或 .xlsx）")
    parser.add_argument("--compare", action="store_true", help="生成对比报告模式")

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        esg_data = json.load(f)

    if args.output.endswith('.xlsx'):
        generate_excel_report(esg_data, args.output, args.compare)
    elif args.output.endswith('.md'):
        report = generate_markdown_report(esg_data, args.compare)
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"Markdown 报告已保存至: {args.output}")
    else:
        print("错误: 输出文件必须为 .md 或 .xlsx 格式")
        sys.exit(1)


if __name__ == "__main__":
    main()
