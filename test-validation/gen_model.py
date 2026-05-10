# -*- coding: utf-8 -*-
"""
AAPL 三表联动模型 Excel 生成脚本
按照 xlsx-author SKILL.md 规范：
  - 蓝色 = 硬编码输入
  - 黑色 = 公式
  - 绿色 = 跨表引用
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()

# ========== 颜色定义 ==========
BLUE_FONT = Font(color="0000FF")
BLACK_FONT = Font(color="000000")
BLACK_BOLD = Font(color="000000", bold=True)
GREEN_FONT = Font(color="008000")
HEADER_FONT = Font(color="000000", bold=True, size=11)
TITLE_FONT = Font(color="000000", bold=True, size=14)
SECTION_FONT = Font(color="000000", bold=True, size=11)
NOTE_FONT = Font(italic=True, color="666666")

HEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
TITLE_FILL = PatternFill(start_color="B4C6E7", end_color="B4C6E7", fill_type="solid")

thin_border = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin")
)

NUM_FMT = "#,##0"
NUM_FMT_DEC = "#,##0.00"
PCT_FMT = "0.0%"


def sc(ws, row, col, value=None, font=None, fill=None, fmt=None):
    """Style a cell with value, font, fill, number format, and border."""
    cell = ws.cell(row=row, column=col, value=value)
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    cell.border = thin_border
    return cell


def header_row(ws, row, labels, start_col=2):
    """Write a header row."""
    for i, label in enumerate(labels):
        sc(ws, row, start_col + i, label, HEADER_FONT, HEADER_FILL)


def set_widths(ws, widths):
    """Set column widths from a dict {col_letter: width}."""
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


# ================================================================
# 标签页 1: Inputs
# ================================================================
ws_inp = wb.active
ws_inp.title = "Inputs"
set_widths(ws_inp, {"A": 3, "B": 32, "C": 18, "D": 18, "E": 18})

# 标题
sc(ws_inp, 1, 2, "AAPL 三表联动模型 - 输入数据", TITLE_FONT, TITLE_FILL)
for c in (3, 4, 5):
    sc(ws_inp, 1, c, None, TITLE_FONT, TITLE_FILL)
ws_inp.merge_cells("B1:E1")

sc(ws_inp, 2, 2, "单位：百万美元（股数为百万股，EPS为美元）", NOTE_FONT)
ws_inp.merge_cells("B2:E2")

# --- 利润表输入 ---
sc(ws_inp, 4, 2, "[利润表]", SECTION_FONT, HEADER_FILL)
for c in (3, 4, 5):
    sc(ws_inp, 4, c, None, SECTION_FONT, HEADER_FILL)
header_row(ws_inp, 5, ["项目", "FY2023", "FY2024", "FY2025"])

income_items = [
    ("收入 (Revenue)", 383285, 391035, 416178),
    ("营业成本 (COGS)", 214138, 210352, 133088),
]
r = 6
for label, v23, v24, v25 in income_items:
    sc(ws_inp, r, 2, label)
    sc(ws_inp, r, 3, v23, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 4, v24, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 5, v25, BLUE_FONT, fmt=NUM_FMT)
    r += 1

# --- 资产负债表输入 ---
r += 1  # r=9
sc(ws_inp, r, 2, "[资产负债表]", SECTION_FONT, HEADER_FILL)
for c in (3, 4, 5):
    sc(ws_inp, r, c, None, SECTION_FONT, HEADER_FILL)
r += 1  # r=10
header_row(ws_inp, r, ["项目", "FY2023", "FY2024", "FY2025"])

bs_items = [
    ("总资产 (Total Assets)", 352583, 364980, 359241),
    ("总负债 (Total Liabilities)", 290437, 308030, 285508),
]
r += 1  # r=11
for label, v23, v24, v25 in bs_items:
    sc(ws_inp, r, 2, label)
    sc(ws_inp, r, 3, v23, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 4, v24, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 5, v25, BLUE_FONT, fmt=NUM_FMT)
    r += 1
# r=13 after loop

# --- 现金流量表输入 ---
r += 1  # r=14
sc(ws_inp, r, 2, "[现金流量表]", SECTION_FONT, HEADER_FILL)
for c in (3, 4, 5):
    sc(ws_inp, r, c, None, SECTION_FONT, HEADER_FILL)
r += 1  # r=15
header_row(ws_inp, r, ["项目", "FY2023", "FY2024", "FY2025"])

cf_items = [
    ("经营现金流 (Operating CF)", 118254, 111482, 140222),
    ("资本支出 (CapEx)", -10959, -9445, -12720),
]
r += 1  # r=16
for label, v23, v24, v25 in cf_items:
    sc(ws_inp, r, 2, label)
    sc(ws_inp, r, 3, v23, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 4, v24, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 5, v25, BLUE_FONT, fmt=NUM_FMT)
    r += 1
# r=18 after loop

# --- 其他指标输入 ---
r += 1  # r=19
sc(ws_inp, r, 2, "[其他指标]", SECTION_FONT, HEADER_FILL)
for c in (3, 4, 5):
    sc(ws_inp, r, c, None, SECTION_FONT, HEADER_FILL)
r += 1  # r=20
header_row(ws_inp, r, ["项目", "FY2023", "FY2024", "FY2025"])

other_items = [
    ("稀释股数 (百万)", 15813, 15408, 14939),
    ("净利润 (Net Income)", 96995, 93736, 112010),
]
r += 1  # r=21
for label, v23, v24, v25 in other_items:
    sc(ws_inp, r, 2, label)
    sc(ws_inp, r, 3, v23, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 4, v24, BLUE_FONT, fmt=NUM_FMT)
    sc(ws_inp, r, 5, v25, BLUE_FONT, fmt=NUM_FMT)
    r += 1
# r=23 after loop

# Inputs 关键行号映射:
# Revenue:        row 6   (C6/D6/E6)
# COGS:           row 7   (C7/D7/E7)
# Total Assets:   row 11  (C11/D11/E11)
# Total Liab:     row 12  (C12/D12/E12)
# Operating CF:   row 16  (C16/D16/E16)
# CapEx:          row 17  (C17/D17/E17)
# Shares:         row 21  (C21/D21/E21)
# Net Income:     row 22  (C22/D22/E22)

# ================================================================
# 标签页 2: 利润表
# ================================================================
ws_is = wb.create_sheet("利润表")
set_widths(ws_is, {"A": 3, "B": 35, "C": 18, "D": 18, "E": 18, "F": 18})

sc(ws_is, 1, 2, "苹果公司 (AAPL) - 利润表", TITLE_FONT, TITLE_FILL)
for c in (3, 4, 5, 6):
    sc(ws_is, 1, c, None, TITLE_FONT, TITLE_FILL)
ws_is.merge_cells("B1:F1")

sc(ws_is, 2, 2, "单位：百万美元", NOTE_FONT)
ws_is.merge_cells("B2:F2")

header_row(ws_is, 4, ["项目", "FY2023", "FY2024", "FY2025", "FY2025同比"])

# 收入
r = 5
sc(ws_is, r, 2, "收入 (Revenue)")
sc(ws_is, r, 3, "=Inputs!C6", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, "=Inputs!D6", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, "=Inputs!E6", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 6, "=(E5-D5)/D5", BLACK_FONT, fmt=PCT_FMT)

# 营业成本
r = 6
sc(ws_is, r, 2, "营业成本 (COGS)")
sc(ws_is, r, 3, "=Inputs!C7", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, "=Inputs!D7", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, "=Inputs!E7", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 6, "=(E6-D6)/D6", BLACK_FONT, fmt=PCT_FMT)

# 毛利润
r = 7
sc(ws_is, r, 2, "毛利润 (Gross Profit)", BLACK_BOLD)
sc(ws_is, r, 3, "=C5-C6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, "=D5-D6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, "=E5-E6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_is, r, 6, "=(E7-D7)/D7", BLACK_FONT, fmt=PCT_FMT)

# 毛利率
r = 8
sc(ws_is, r, 2, "毛利率 (Gross Margin)")
sc(ws_is, r, 3, "=C7/C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 4, "=D7/D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 5, "=E7/E5", BLACK_FONT, fmt=PCT_FMT)

# 营业利润 (硬编码输入，因为Inputs中没有单独行)
r = 10
sc(ws_is, r, 2, "营业利润 (Operating Income)", BLACK_BOLD)
sc(ws_is, r, 3, 114725, BLUE_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, 123487, BLUE_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, 133157, BLUE_FONT, fmt=NUM_FMT)
sc(ws_is, r, 6, "=(E10-D10)/D10", BLACK_FONT, fmt=PCT_FMT)

# 营业利润率
r = 11
sc(ws_is, r, 2, "营业利润率 (Operating Margin)")
sc(ws_is, r, 3, "=C10/C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 4, "=D10/D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 5, "=E10/E5", BLACK_FONT, fmt=PCT_FMT)

# 净利润
r = 13
sc(ws_is, r, 2, "净利润 (Net Income)", BLACK_BOLD)
sc(ws_is, r, 3, "=Inputs!C22", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, "=Inputs!D22", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, "=Inputs!E22", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 6, "=(E13-D13)/D13", BLACK_FONT, fmt=PCT_FMT)

# 净利润率
r = 14
sc(ws_is, r, 2, "净利润率 (Net Margin)")
sc(ws_is, r, 3, "=C13/C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 4, "=D13/D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_is, r, 5, "=E13/E5", BLACK_FONT, fmt=PCT_FMT)

# 稀释股数
r = 16
sc(ws_is, r, 2, "稀释股数 (百万股)")
sc(ws_is, r, 3, "=Inputs!C21", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 4, "=Inputs!D21", GREEN_FONT, fmt=NUM_FMT)
sc(ws_is, r, 5, "=Inputs!E21", GREEN_FONT, fmt=NUM_FMT)

# EPS
r = 17
sc(ws_is, r, 2, "稀释EPS (美元/股)", BLACK_BOLD)
sc(ws_is, r, 3, "=C13/C16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_is, r, 4, "=D13/D16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_is, r, 5, "=E13/E16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_is, r, 6, "=(E17-D17)/D17", BLACK_FONT, fmt=PCT_FMT)

# ================================================================
# 标签页 3: 资产负债表
# ================================================================
ws_bs = wb.create_sheet("资产负债表")
set_widths(ws_bs, {"A": 3, "B": 38, "C": 18, "D": 18, "E": 18, "F": 18})

sc(ws_bs, 1, 2, "苹果公司 (AAPL) - 资产负债表", TITLE_FONT, TITLE_FILL)
for c in (3, 4, 5, 6):
    sc(ws_bs, 1, c, None, TITLE_FONT, TITLE_FILL)
ws_bs.merge_cells("B1:F1")

sc(ws_bs, 2, 2, "单位：百万美元", NOTE_FONT)
ws_bs.merge_cells("B2:F2")

header_row(ws_bs, 4, ["项目", "FY2023", "FY2024", "FY2025", "FY2025同比"])

# 总资产
r = 5
sc(ws_bs, r, 2, "总资产 (Total Assets)", BLACK_BOLD)
sc(ws_bs, r, 3, "=Inputs!C11", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 4, "=Inputs!D11", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 5, "=Inputs!E11", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 6, "=(E5-D5)/D5", BLACK_FONT, fmt=PCT_FMT)

# 总负债
r = 6
sc(ws_bs, r, 2, "总负债 (Total Liabilities)")
sc(ws_bs, r, 3, "=Inputs!C12", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 4, "=Inputs!D12", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 5, "=Inputs!E12", GREEN_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 6, "=(E6-D6)/D6", BLACK_FONT, fmt=PCT_FMT)

# 股东权益 = 总资产 - 总负债
r = 7
sc(ws_bs, r, 2, "股东权益 (Shareholders Equity)", BLACK_BOLD)
sc(ws_bs, r, 3, "=C5-C6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 4, "=D5-D6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 5, "=E5-E6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 6, "=(E7-D7)/D7", BLACK_FONT, fmt=PCT_FMT)

# 校验行: 负债+权益
r = 9
sc(ws_bs, r, 2, "负债 + 权益（校验）", Font(italic=True, color="666666"))
sc(ws_bs, r, 3, "=C6+C7", BLACK_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 4, "=D6+D7", BLACK_FONT, fmt=NUM_FMT)
sc(ws_bs, r, 5, "=E6+E7", BLACK_FONT, fmt=NUM_FMT)

# 资产负债率
r = 11
sc(ws_bs, r, 2, "资产负债率")
sc(ws_bs, r, 3, "=C6/C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 4, "=D6/D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 5, "=E6/E5", BLACK_FONT, fmt=PCT_FMT)

# ROE
r = 12
sc(ws_bs, r, 2, "ROE (净利润/股东权益)")
sc(ws_bs, r, 3, "=利润表!C13/C7", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 4, "=利润表!D13/D7", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 5, "=利润表!E13/E7", BLACK_FONT, fmt=PCT_FMT)

# ROA
r = 13
sc(ws_bs, r, 2, "ROA (净利润/总资产)")
sc(ws_bs, r, 3, "=利润表!C13/C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 4, "=利润表!D13/D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_bs, r, 5, "=利润表!E13/E5", BLACK_FONT, fmt=PCT_FMT)

# ================================================================
# 标签页 4: 现金流量表
# ================================================================
ws_cf = wb.create_sheet("现金流量表")
set_widths(ws_cf, {"A": 3, "B": 38, "C": 18, "D": 18, "E": 18, "F": 18})

sc(ws_cf, 1, 2, "苹果公司 (AAPL) - 现金流量表", TITLE_FONT, TITLE_FILL)
for c in (3, 4, 5, 6):
    sc(ws_cf, 1, c, None, TITLE_FONT, TITLE_FILL)
ws_cf.merge_cells("B1:F1")

sc(ws_cf, 2, 2, "单位：百万美元", NOTE_FONT)
ws_cf.merge_cells("B2:F2")

header_row(ws_cf, 4, ["项目", "FY2023", "FY2024", "FY2025", "FY2025同比"])

# 经营现金流
r = 5
sc(ws_cf, r, 2, "经营现金流 (Operating CF)")
sc(ws_cf, r, 3, "=Inputs!C16", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 4, "=Inputs!D16", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 5, "=Inputs!E16", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 6, "=(E5-D5)/D5", BLACK_FONT, fmt=PCT_FMT)

# 资本支出
r = 6
sc(ws_cf, r, 2, "资本支出 (CapEx)")
sc(ws_cf, r, 3, "=Inputs!C17", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 4, "=Inputs!D17", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 5, "=Inputs!E17", GREEN_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 6, "=(E6-D6)/D6", BLACK_FONT, fmt=PCT_FMT)

# 自由现金流 = 经营CF + CapEx
r = 7
sc(ws_cf, r, 2, "自由现金流 (FCF)", BLACK_BOLD)
sc(ws_cf, r, 3, "=C5+C6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 4, "=D5+D6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 5, "=E5+E6", BLACK_FONT, fmt=NUM_FMT)
sc(ws_cf, r, 6, "=(E7-D7)/D7", BLACK_FONT, fmt=PCT_FMT)

# FCF利润率
r = 8
sc(ws_cf, r, 2, "FCF利润率 (FCF/Revenue)")
sc(ws_cf, r, 3, "=C7/利润表!C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_cf, r, 4, "=D7/利润表!D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_cf, r, 5, "=E7/利润表!E5", BLACK_FONT, fmt=PCT_FMT)

# CapEx/Revenue
r = 9
sc(ws_cf, r, 2, "CapEx/Revenue")
sc(ws_cf, r, 3, "=C6/利润表!C5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_cf, r, 4, "=D6/利润表!D5", BLACK_FONT, fmt=PCT_FMT)
sc(ws_cf, r, 5, "=E6/利润表!E5", BLACK_FONT, fmt=PCT_FMT)

# ================================================================
# 标签页 5: Checks
# ================================================================
ws_ck = wb.create_sheet("Checks")
set_widths(ws_ck, {"A": 3, "B": 45, "C": 18, "D": 18, "E": 18, "F": 12})

sc(ws_ck, 1, 2, "苹果公司 (AAPL) - 平衡校验", TITLE_FONT, TITLE_FILL)
for c in (3, 4, 5, 6):
    sc(ws_ck, 1, c, None, TITLE_FONT, TITLE_FILL)
ws_ck.merge_cells("B1:F1")

sc(ws_ck, 2, 2, "所有校验项应为 TRUE（差值为0）", NOTE_FONT)
ws_ck.merge_cells("B2:F2")

header_row(ws_ck, 4, ["校验项目", "FY2023", "FY2024", "FY2025", "通过?"])

# 校验1: 资产 = 负债 + 权益
r = 5
sc(ws_ck, r, 2, "资产 = 负债 + 权益（差值=0）")
sc(ws_ck, r, 3, "=资产负债表!C5-资产负债表!C9", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 4, "=资产负债表!D5-资产负债表!D9", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 5, "=资产负债表!E5-资产负债表!E9", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 6, "=AND(C5=0,D5=0,E5=0)", BLACK_FONT)

# 校验2: 毛利润 = 收入 - COGS
r = 6
sc(ws_ck, r, 2, "毛利润 = 收入 - COGS（差值=0）")
sc(ws_ck, r, 3, "=利润表!C7-(利润表!C5-利润表!C6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 4, "=利润表!D7-(利润表!D5-利润表!D6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 5, "=利润表!E7-(利润表!E5-利润表!E6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 6, "=AND(C6=0,D6=0,E6=0)", BLACK_FONT)

# 校验3: FCF = 经营CF + CapEx
r = 7
sc(ws_ck, r, 2, "FCF = 经营CF + CapEx（差值=0）")
sc(ws_ck, r, 3, "=现金流量表!C7-(现金流量表!C5+现金流量表!C6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 4, "=现金流量表!D7-(现金流量表!D5+现金流量表!D6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 5, "=现金流量表!E7-(现金流量表!E5+现金流量表!E6)", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 6, "=AND(C7=0,D7=0,E7=0)", BLACK_FONT)

# 校验4: EPS一致性
r = 8
sc(ws_ck, r, 2, "EPS一致性（计算EPS - 公式EPS，应=0）")
sc(ws_ck, r, 3, "=利润表!C17-利润表!C13/利润表!C16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_ck, r, 4, "=利润表!D17-利润表!D13/利润表!D16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_ck, r, 5, "=利润表!E17-利润表!E13/利润表!E16", BLACK_FONT, fmt=NUM_FMT_DEC)
sc(ws_ck, r, 6, "=AND(ABS(C8)<0.05,ABS(D8)<0.05,ABS(E8)<0.05)", BLACK_FONT)

# 校验5: 经营CF/净利润 > 80%
r = 9
sc(ws_ck, r, 2, "盈利质量：经营CF/净利润 > 80%")
sc(ws_ck, r, 3, "=现金流量表!C5/利润表!C13", BLACK_FONT, fmt=PCT_FMT)
sc(ws_ck, r, 4, "=现金流量表!D5/利润表!D13", BLACK_FONT, fmt=PCT_FMT)
sc(ws_ck, r, 5, "=现金流量表!E5/利润表!E13", BLACK_FONT, fmt=PCT_FMT)
sc(ws_ck, r, 6, "=AND(C9>0.8,D9>0.8,E9>0.8)", BLACK_FONT)

# 校验6: 净利润一致性
r = 10
sc(ws_ck, r, 2, "净利润一致性（利润表 = Inputs）")
sc(ws_ck, r, 3, "=利润表!C13-Inputs!C22", BLACK_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 4, "=利润表!D13-Inputs!D22", GREEN_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 5, "=利润表!E13-Inputs!E22", GREEN_FONT, fmt=NUM_FMT)
sc(ws_ck, r, 6, "=AND(C10=0,D10=0,E10=0)", BLACK_FONT)

# ================================================================
# 保存
# ================================================================
output_path = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\FA_xlsx_author_real_output.xlsx"
wb.save(output_path)
print("Excel saved to:", output_path)
print("Sheets:", wb.sheetnames)
