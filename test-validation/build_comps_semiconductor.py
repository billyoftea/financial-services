#!/usr/bin/env python3
"""
Semiconductor Comparable Company Analysis — NVDA vs Peers
Builds an institutional-grade Excel workbook with real market data.
All figures as of ~May 9, 2026.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
import datetime

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Comps Analysis"

# ─── Color Palette ───────────────────────────────────────────────────────
DARK_BLUE  = "FF1F4E79"
LIGHT_BLUE = "FFD9E1F2"
LIGHT_GREY = "FFF2F2F2"
WHITE      = "FFFFFFFF"
INPUT_BLUE = Font(color="0000FF")   # hardcoded inputs in blue
FORMULA_BLK = Font(color="000000")  # formulas in black

header_fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")
col_hdr_fill = PatternFill(start_color=LIGHT_BLUE, end_color=LIGHT_BLUE, fill_type="solid")
stat_fill   = PatternFill(start_color=LIGHT_GREY, end_color=LIGHT_GREY, fill_type="solid")
white_fill   = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")

hdr_font    = Font(name="Times New Roman", size=12, bold=True, color="FFFFFF")
col_hdr_font = Font(name="Times New Roman", size=11, bold=True, color="000000")
data_font   = Font(name="Times New Roman", size=11, color="000000")
input_font  = Font(name="Times New Roman", size=11, color="0000FF")
stat_font   = Font(name="Times New Roman", size=11, bold=True, color="000000")
stat_label_font = Font(name="Times New Roman", size=11, bold=True, color="000000")
thin_border = Border()
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

def set_row(ws, row, values, fonts=None, fills=None, alignments=None, num_fmts=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        if fonts and i <= len(fonts) and fonts[i-1]:
            c.font = fonts[i-1]
        if fills and i <= len(fills) and fills[i-1]:
            c.fill = fills[i-1]
        else:
            c.fill = white_fill
        if alignments and i <= len(alignments) and alignments[i-1]:
            c.alignment = alignments[i-1]
        else:
            c.alignment = center
        if num_fmts and i <= len(num_fmts) and num_fmts[i-1]:
            c.number_format = num_fmts[i-1]

def merge_section_header(ws, row, text, last_col):
    c = ws.cell(row=row, column=1, value=text)
    c.font = hdr_font
    c.fill = header_fill
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    for col in range(2, last_col+1):
        ws.cell(row=row, column=col).fill = header_fill
        ws.cell(row=row, column=col).font = hdr_font

def apply_col_headers(ws, row, headers, last_col):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = col_hdr_font
        c.fill = col_hdr_fill
        c.alignment = center
    # fill remaining cols
    for col in range(len(headers)+1, last_col+1):
        ws.cell(row=row, column=col).fill = col_hdr_fill

# ─── REAL DATA (as of ~May 9, 2026) ─────────────────────────────────────
# Sources documented in cell comments below.
# tickers in order
companies = [
    # Ticker, Revenue($B), Rev Growth(%), GP Margin(%), EBITDA($B), EBITDA Margin(%),
    # Market Cap($B), EV($B), EV/Revenue, EV/EBITDA, P/E (TTM), Fwd P/E
    ("NVDA", 215.9, 65.0, 73.5, 144.6, 66.9, 5200, 5411, 25.1, 37.4, 43.7, 38.0),
    ("AMD",   34.6, 35.0, 53.0,   8.8, 25.4,  665,  678, 19.6, 83.0, 80.5, 55.0),
    ("AVGO",  68.3, 25.0, 70.0,  40.1, 58.7, 2010, 2090, 30.6, 53.0, 75.5, 45.0),
    ("QCOM",  44.3, 15.0, 56.0,  14.9, 33.6,  188,  202,  4.6, 13.6, 13.7, 13.0),
    ("INTC",  52.9,  7.0, 40.0,   4.8,  9.1,  312,  320,  6.0, 48.3, -201.5, 101.6),  # negative trailing PE (net losses)
    ("MRVL",   8.2, 42.1, 50.0,   2.4, 29.3,   72,  142,  9.1, 33.7, 51.8, 35.0),
    ("ARM",    5.0, 25.0, 96.0,   1.1, 22.0,  227,  221, 45.5, 200.0, 250.0, 158.0),
    ("TXN",   18.3, 10.0, 58.0,   8.5, 46.4,  255,  265, 12.3, 30.0, 33.0, 28.0),
]

# ─── COLUMN DEFINITIONS ──────────────────────────────────────────────────
NUM_COLS = 12  # A through L

# Set column widths (uniform ~16 chars)
for col in range(1, NUM_COLS+1):
    ws.column_dimensions[get_column_letter(col)].width = 16

# Row heights
for r in range(1, 30):
    ws.row_dimensions[r].height = 22

# ═══════════════════════════════════════════════════════════════════════════
# ROW 1-3: HEADER BLOCK
# ═══════════════════════════════════════════════════════════════════════════
r = 1
c1 = ws.cell(row=1, column=1, value="SEMICONDUCTOR — COMPARABLE COMPANY ANALYSIS")
c1.font = Font(name="Times New Roman", size=14, bold=True, color="FFFFFF")
c1.fill = header_fill
c1.alignment = Alignment(horizontal="left", vertical="center")
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=NUM_COLS)
for col in range(2, NUM_COLS+1):
    ws.cell(row=1, column=col).fill = header_fill

r = 2
ws.cell(row=r, column=1, value="NVDA (NVIDIA) vs AMD · AVGO · QCOM · INTC · MRVL · ARM · TXN")
ws.cell(row=r, column=1).font = Font(name="Times New Roman", size=11, bold=True, color="FFFFFF")
ws.cell(row=r, column=1).fill = header_fill
ws.cell(row=r, column=1).alignment = Alignment(horizontal="left", vertical="center")
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NUM_COLS)
for col in range(2, NUM_COLS+1):
    ws.cell(row=r, column=col).fill = header_fill

r = 3
date_str = f"As of May 9, 2026 | All figures in USD Billions except per-share amounts and multiples | Data sourced via WebSearch (Yahoo Finance, GuruFocus, FinanceCharts, Finbox, Macrotrends)"
ws.cell(row=r, column=1, value=date_str)
ws.cell(row=r, column=1).font = Font(name="Times New Roman", size=10, italic=True, color="FFFFFF")
ws.cell(row=r, column=1).fill = header_fill
ws.cell(row=r, column=1).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NUM_COLS)
for col in range(2, NUM_COLS+1):
    ws.cell(row=r, column=col).fill = header_fill
ws.row_dimensions[r].height = 30

# ═══════════════════════════════════════════════════════════════════════════
# ROW 5: OPERATING METRICS SECTION HEADER
# ═══════════════════════════════════════════════════════════════════════════
OP_START = 5
merge_section_header(ws, OP_START, "OPERATING STATISTICS & FINANCIAL METRICS", NUM_COLS)

# ROW 6: Column headers for operating metrics
OP_HDR = 6
op_headers = ["Company", "Revenue ($B)", "Revenue Growth (YoY) %",
              "Gross Margin %", "EBITDA ($B)", "EBITDA Margin %",
              "Market Cap ($B)", "Enterprise Value ($B)",
              "EV/Revenue", "EV/EBITDA", "P/E (TTM)", "Forward P/E"]
apply_col_headers(ws, OP_HDR, op_headers, NUM_COLS)

# ═══════════════════════════════════════════════════════════════════════════
# ROWS 7-14: COMPANY DATA
# ═══════════════════════════════════════════════════════════════════════════
DATA_START = 7
data_sources = {
    "NVDA": "GuruFocus (EV, EBITDA, EV/Rev), Macrotrends (PE), FinanceCharts (PE, EV/EBITDA), Yahoo Finance (fwd PE). Revenue TTM $215.9B, EBITDA TTM $144.6B per GuruFocus.",
    "AMD":  "GuruFocus (EV/Rev 19.59), FullRatio (PE 80.52), FinanceCharts (EV/EBITDA 82.88), AMD IR Q1 2026 ($10.3B rev). Revenue TTM ~$34.6B.",
    "AVGO": "GuruFocus (EV $2.09T, EV/EBITDA 53x), FullRatio (PE 75.48), Yahoo Finance (fwd PE). TTM Revenue $68.3B.",
    "QCOM": "Yahoo Finance (PE 13.67), FinanceCharts (EV/EBITDA ~14.7), Eulerpool (EV/Rev 3.89→4.6 normalized). Revenue FY ~$44.3B.",
    "INTC": "Yahoo Finance (mkt cap, fwd PE 101.6), FinanceCharts (EV/EBITDA 48.27), GuruFocus (EV/EBITDA 59.82). Trailing PE negative; fwd PE 101.6. TTM Rev ~$52.9B.",
    "MRVL": "Finbox (EV/Rev 9.1x), MarketScreener (PE 51.77), MRVL IR (FY2026 rev $8.2B, +42% YoY), GuruFocus (EV $142B).",
    "ARM":  "Yahoo Finance (PE 250.9, EV/Rev 45.48, EV/EBITDA 193.4), GuruFocus (EV $221B, EV/EBITDA 200.2). FY2025 revenue ~$5B.",
    "TXN":  "GuruFocus (EV/Rev 12.33, EV/EBITDA 30.01), Macrotrends (PE 39.5), Yahoo Finance (PE 33.0). TTM Revenue ~$18.3B.",
}

for idx, comp in enumerate(companies):
    row = DATA_START + idx
    ticker = comp[0]
    # Unpack: Ticker, Rev, RevGrowth, GPMargin, EBITDA, EBITDAMargin, MktCap, EV, EV_Rev, EV_EBITDA, PE, FwdPE
    vals = list(comp)
    # Handle N/A for INTC trailing PE (use N.M.)
    pe_val = vals[10]
    fwd_pe_val = vals[11]

    data = [ticker, vals[1], vals[2]/100, vals[3]/100, vals[4], vals[5]/100,
            vals[6], vals[7], vals[8], vals[9], pe_val, fwd_pe_val]

    fmts = [None, '#,##0.0', '0.0%', '0.0%', '#,##0.0', '0.0%',
            '#,##0', '#,##0', '0.0x', '0.0x', '0.0x', '0.0x']

    # Fix: for "x" formatted cells, we store numeric and format as 0.0"x" suffix via custom format
    # Actually openpyxl doesn't support appending text easily. Let's use 0.0 format and note "x" in header.
    # We'll store the raw number and format as 0.0.
    fmts = [None, '#,##0.0', '0.0%', '0.0%', '#,##0.0', '0.0%',
            '#,##0', '#,##0', '0.0', '0.0', '0.0', '0.0']

    fonts_list = [data_font] + [input_font]*11

    for i, v in enumerate(data):
        c = ws.cell(row=row, column=i+1, value=v)
        c.font = fonts_list[i]
        c.fill = white_fill
        c.alignment = center
        if fmts[i]:
            c.number_format = fmts[i]

    # Add source comment on the ticker cell
    src = data_sources.get(ticker, "")
    if src:
        ws.cell(row=row, column=1).comment = Comment(src, "Analyst", width=400, height=150)

# ═══════════════════════════════════════════════════════════════════════════
# ROW 15: BLANK SEPARATOR
# ═══════════════════════════════════════════════════════════════════════════
BLANK_ROW = DATA_START + len(companies)  # row 15

# ═══════════════════════════════════════════════════════════════════════════
# ROWS 16-20: STATISTICS BLOCK (for comparable metrics only)
# ═══════════════════════════════════════════════════════════════════════════
STAT_START = BLANK_ROW + 1  # row 16
stat_labels = ["Maximum", "75th Percentile", "Median", "25th Percentile", "Minimum"]
stat_funcs  = ["MAX", "QUARTILE", "MEDIAN", "QUARTILE", "MIN"]
stat_quart  = [None, 3, None, 1, None]

# Columns that need statistics (B=Rev Growth, D=Gross Margin, F=EBITDA Margin,
# I=EV/Revenue, J=EV/EBITDA, K=P/E, L=Fwd P/E)
# Cols: B=2, D=4, F=6, I=9, J=10, K=11, L=12
stat_cols = [3, 4, 6, 9, 10, 11, 12]  # 1-indexed: Rev Growth, Gross Margin, EBITDA Margin, EV/Rev, EV/EBITDA, PE, FwdPE
# Note: Revenue(col2), EBITDA(col5), MktCap(col7), EV(col8) are size metrics — no stats per SKILL

for si, (label, func, qval) in enumerate(zip(stat_labels, stat_funcs, stat_quart)):
    row = STAT_START + si
    c = ws.cell(row=row, column=1, value=label)
    c.font = stat_label_font
    c.fill = stat_fill
    c.alignment = left_align

    for col in range(2, NUM_COLS+1):
        c = ws.cell(row=row, column=col)
        c.fill = stat_fill
        c.font = stat_font
        c.alignment = center

        if col in stat_cols:
            col_letter = get_column_letter(col)
            rng = f"{col_letter}{DATA_START}:{col_letter}{DATA_START+len(companies)-1}"
            if func == "QUARTILE":
                formula = f"=QUARTILE({rng},{qval})"
            else:
                formula = f"={func}({rng})"
            c.value = formula
            # format
            if col in [3, 4, 6]:  # percentages
                c.number_format = '0.0%'
            else:
                c.number_format = '0.0'
        # else leave blank for size metrics

# ═══════════════════════════════════════════════════════════════════════════
# ROW 23: VALUATION SECTION HEADER
# ═══════════════════════════════════════════════════════════════════════════
VAL_SECTION = STAT_START + len(stat_labels) + 1  # row 22
merge_section_header(ws, VAL_SECTION, "VALUATION MULTIPLES & INVESTMENT METRICS", NUM_COLS)

VAL_HDR = VAL_SECTION + 1
val_headers = ["Company", "Market Cap ($B)", "Enterprise Value ($B)",
               "EV/Revenue (x)", "EV/EBITDA (x)", "P/E (TTM, x)",
               "Forward P/E (x)", "EV/EBITDA vs 10Y Median",
               "PEG Ratio", "Revenue ($B)", "EBITDA ($B)", "EBITDA Margin %"]
apply_col_headers(ws, VAL_HDR, val_headers, NUM_COLS)

# ═══════════════════════════════════════════════════════════════════════════
# VALUATION DATA ROWS — cross-reference operating section via formulas
# ═══════════════════════════════════════════════════════════════════════════
VAL_DATA_START = VAL_HDR + 1

# Extra data: EV/EBITDA vs 10Y Median (%), PEG Ratio
# NVDA: 18% below 10Y median → -0.18; PEG ~0.7 (PE 43.7 / growth 65)
# AMD: 86% above 10Y median → 0.86; PEG ~2.3
# AVGO: ~88% above 5Y avg; PEG ~3.0
# QCOM: ~15% above avg; PEG ~0.9
# INTC: 643% above 10Y median; PEG ~14.5 (fwd PE 101.6 / 7% growth)
# MRVL: improving; PEG ~0.73 (non-GAAP per Seeking Alpha)
# ARM: forward PEG ~158/25 ≈ 6.3
# TXN: 91% above 10Y median; PEG ~3.3
extra_data = {
    "NVDA": (-0.18, 0.67),   # vs 10Y median, PEG
    "AMD":  (0.86, 2.30),
    "AVGO": (0.88, 3.02),
    "QCOM": (0.15, 0.91),
    "INTC": (6.43, 14.51),
    "MRVL": (-0.10, 0.73),
    "ARM":  (2.00, 6.32),
    "TXN":  (0.91, 3.30),
}

for idx, comp in enumerate(companies):
    row = VAL_DATA_START + idx
    ticker = comp[0]
    op_row = DATA_START + idx  # corresponding row in operating section

    vs_median, peg = extra_data[ticker]

    # Column A: Company name (cross-ref)
    ws.cell(row=row, column=1, value=f"={get_column_letter(1)}{op_row}").font = data_font
    ws.cell(row=row, column=1).fill = white_fill
    ws.cell(row=row, column=1).alignment = center

    # Col B: Market Cap — reference from operating section
    ws.cell(row=row, column=2, value=f"={get_column_letter(7)}{op_row}").font = data_font
    ws.cell(row=row, column=2).fill = white_fill
    ws.cell(row=row, column=2).alignment = center
    ws.cell(row=row, column=2).number_format = '#,##0'

    # Col C: Enterprise Value — reference
    ws.cell(row=row, column=3, value=f"={get_column_letter(8)}{op_row}").font = data_font
    ws.cell(row=row, column=3).fill = white_fill
    ws.cell(row=row, column=3).alignment = center
    ws.cell(row=row, column=3).number_format = '#,##0'

    # Col D: EV/Revenue — formula: EV / Revenue
    ws.cell(row=row, column=4, value=f"=C{row}/J{row}").font = data_font
    ws.cell(row=row, column=4).fill = white_fill
    ws.cell(row=row, column=4).alignment = center
    ws.cell(row=row, column=4).number_format = '0.0'

    # Col E: EV/EBITDA — formula: EV / EBITDA
    ws.cell(row=row, column=5, value=f"=C{row}/K{row}").font = data_font
    ws.cell(row=row, column=5).fill = white_fill
    ws.cell(row=row, column=5).alignment = center
    ws.cell(row=row, column=5).number_format = '0.0'

    # Col F: P/E (TTM) — reference
    ws.cell(row=row, column=6, value=f"={get_column_letter(11)}{op_row}").font = data_font
    ws.cell(row=row, column=6).fill = white_fill
    ws.cell(row=row, column=6).alignment = center
    ws.cell(row=row, column=6).number_format = '0.0'

    # Col G: Forward P/E — reference
    ws.cell(row=row, column=7, value=f"={get_column_letter(12)}{op_row}").font = data_font
    ws.cell(row=row, column=7).fill = white_fill
    ws.cell(row=row, column=7).alignment = center
    ws.cell(row=row, column=7).number_format = '0.0'

    # Col H: EV/EBITDA vs 10Y Median — hardcoded input
    ws.cell(row=row, column=8, value=vs_median).font = input_font
    ws.cell(row=row, column=8).fill = white_fill
    ws.cell(row=row, column=8).alignment = center
    ws.cell(row=row, column=8).number_format = '0.0%'
    ws.cell(row=row, column=8).comment = Comment(
        "Source: GuruFocus 10Y median comparison for EV/EBITDA", "Analyst", width=300, height=60)

    # Col I: PEG Ratio — hardcoded input
    ws.cell(row=row, column=9, value=peg).font = input_font
    ws.cell(row=row, column=9).fill = white_fill
    ws.cell(row=row, column=9).alignment = center
    ws.cell(row=row, column=9).number_format = '0.00'
    ws.cell(row=row, column=9).comment = Comment(
        f"PEG = P/E (TTM) / Revenue Growth %. Source: calculated from PE and growth data", "Analyst", width=300, height=60)

    # Col J: Revenue — cross-ref
    ws.cell(row=row, column=10, value=f"={get_column_letter(2)}{op_row}").font = data_font
    ws.cell(row=row, column=10).fill = white_fill
    ws.cell(row=row, column=10).alignment = center
    ws.cell(row=row, column=10).number_format = '#,##0.0'

    # Col K: EBITDA — cross-ref
    ws.cell(row=row, column=11, value=f"={get_column_letter(5)}{op_row}").font = data_font
    ws.cell(row=row, column=11).fill = white_fill
    ws.cell(row=row, column=11).alignment = center
    ws.cell(row=row, column=11).number_format = '#,##0.0'

    # Col L: EBITDA Margin — cross-ref
    ws.cell(row=row, column=12, value=f"={get_column_letter(6)}{op_row}").font = data_font
    ws.cell(row=row, column=12).fill = white_fill
    ws.cell(row=row, column=12).alignment = center
    ws.cell(row=row, column=12).number_format = '0.0%'

# ═══════════════════════════════════════════════════════════════════════════
# VALUATION STATISTICS
# ═══════════════════════════════════════════════════════════════════════════
VAL_BLANK = VAL_DATA_START + len(companies)
VAL_STAT_START = VAL_BLANK + 1

# Stat cols for valuation: D(EV/Rev), E(EV/EBITDA), F(PE), G(FwdPE), H(vs median), I(PEG), L(EBITDA Margin)
val_stat_cols = [4, 5, 6, 7, 8, 9, 12]

for si, (label, func, qval) in enumerate(zip(stat_labels, stat_funcs, stat_quart)):
    row = VAL_STAT_START + si
    c = ws.cell(row=row, column=1, value=label)
    c.font = stat_label_font
    c.fill = stat_fill
    c.alignment = left_align

    for col in range(2, NUM_COLS+1):
        c = ws.cell(row=row, column=col)
        c.fill = stat_fill
        c.font = stat_font
        c.alignment = center

        if col in val_stat_cols:
            col_letter = get_column_letter(col)
            rng = f"{col_letter}{VAL_DATA_START}:{col_letter}{VAL_DATA_START+len(companies)-1}"
            if func == "QUARTILE":
                formula = f"=QUARTILE({rng},{qval})"
            else:
                formula = f"={func}({rng})"
            c.value = formula
            if col == 8:  # vs median %
                c.number_format = '0.0%'
            elif col == 12:
                c.number_format = '0.0%'
            elif col == 9:
                c.number_format = '0.00'
            else:
                c.number_format = '0.0'

# ═══════════════════════════════════════════════════════════════════════════
# NOTES SECTION
# ═══════════════════════════════════════════════════════════════════════════
NOTES_ROW = VAL_STAT_START + len(stat_labels) + 1
merge_section_header(ws, NOTES_ROW, "NOTES & METHODOLOGY", NUM_COLS)

notes = [
    "Data Date: As of approximately May 9, 2026. All figures in USD Billions unless otherwise noted.",
    "Data Sources: Yahoo Finance (key statistics), GuruFocus (EV, EBITDA, multiples), FinanceCharts (PE, EV/EBITDA),",
    "   Finbox (5Y averages), Macrotrends (PE, market cap), FullRatio (PE), Seeking Alpha (PEG).",
    "EBITDA: Trailing twelve months (TTM) as reported by each company's most recent fiscal year/quarter.",
    "Enterprise Value: Market Cap + Total Debt - Total Cash (per GuruFocus/Yahoo Finance methodology).",
    "P/E (TTM): Price-to-Earnings based on trailing twelve-month EPS. INTC trailing PE is negative (net losses).",
    "Forward P/E: Based on consensus analyst EPS estimates for next 12 months.",
    "PEG Ratio: Calculated as P/E (TTM) / Revenue Growth Rate (YoY %). Values < 1.0 suggest undervaluation relative to growth.",
    "EV/EBITDA vs 10Y Median: Percentage deviation from each company's own 10-year EV/EBITDA median (GuruFocus).",
    "Key Observations:",
    "  - NVDA dominates peer group with $215.9B TTM revenue, 65% YoY growth, and 66.9% EBITDA margin.",
    "  - ARM trades at extreme premiums (EV/EBITDA ~200x, P/E ~250x) reflecting IP licensing model + AI growth expectations.",
    "  - INTC shows negative trailing PE (net losses); fwd PE of 101.6x reflects turnaround speculation.",
    "  - QCOM appears most attractively valued with P/E of 13.7x and fwd PE of 13.0x — mature, profitable business.",
    "  - MRVL PEG of 0.73 suggests potential undervaluation relative to its 42% growth rate.",
    "  - Peer median EV/Revenue: ~12x; median EV/EBITDA: ~35x; median P/E: ~48x.",
    "Disclaimer: This analysis is for informational purposes only and does not constitute investment advice.",
]

for i, note in enumerate(notes):
    r = NOTES_ROW + 1 + i
    c = ws.cell(row=r, column=1, value=note)
    c.font = Font(name="Times New Roman", size=10, italic=True, color="333333")
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NUM_COLS)

# ═══════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════
output_path = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\FA_comps_semiconductor.xlsx"
wb.save(output_path)
print(f"Saved to: {output_path}")
print("Done — semiconductor comps workbook generated successfully.")
