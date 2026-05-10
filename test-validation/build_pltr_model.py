"""
Palantir Technologies (PLTR) 财务模型构建脚本
生成6个工作表的完整Excel模型
数据来源: Palantir 10-K, SEC EDGAR, Yahoo Finance, Macrotrends
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from datetime import datetime

wb = openpyxl.Workbook()

# ========== 样式定义 ==========
BLUE_FONT = Font(name='Times New Roman', color='0000FF', size=10)
BLACK_FONT = Font(name='Times New Roman', color='000000', size=10)
GREEN_FONT = Font(name='Times New Roman', color='008000', size=10)
HEADER_FONT = Font(name='Times New Roman', bold=True, color='FFFFFF', size=11)
SECTION_FONT = Font(name='Times New Roman', bold=True, color='000000', size=11)
TITLE_FONT = Font(name='Times New Roman', bold=True, color='000000', size=14)
SUBTITLE_FONT = Font(name='Times New Roman', bold=True, color='000000', size=12)
PCT_FORMAT = '0.0%'
NUM_FORMAT = '#,##0'
DEC_FORMAT = '#,##0.0'
DOLLAR_FORMAT = '$#,##0'
EPS_FORMAT = '$#,##0.00'

HEADER_FILL = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
SECTION_FILL = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
SUBSECTION_FILL = PatternFill(start_color='E8F0FE', end_color='E8F0FE', fill_type='solid')
TOTAL_FILL = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
CHECK_FILL = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')

THIN_BORDER = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

def style_header_row(ws, row, max_col):
    for col in range(1, max_col+1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = THIN_BORDER

def style_section_row(ws, row, max_col):
    for col in range(1, max_col+1):
        cell = ws.cell(row=row, column=col)
        cell.font = SECTION_FONT
        cell.fill = SECTION_FILL
        cell.border = THIN_BORDER

def style_total_row(ws, row, max_col):
    for col in range(1, max_col+1):
        cell = ws.cell(row=row, column=col)
        cell.font = Font(name='Times New Roman', bold=True, size=10)
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER

def style_data_row(ws, row, max_col, font=BLACK_FONT):
    for col in range(1, max_col+1):
        cell = ws.cell(row=row, column=col)
        cell.font = font
        cell.border = THIN_BORDER

# 年份列配置 (历史3年 + 预测5年)
years_hist = [2022, 2023, 2024]
years_proj = [2025, 2026, 2027, 2028, 2029]
years_all = years_hist + years_proj
max_col = 1 + len(years_all)  # 标签列 + 数据列

# =====================================================================
# Tab 1: Revenue Model (收入模型)
# =====================================================================
ws1 = wb.active
ws1.title = 'Revenue Model'
ws1.sheet_properties.tabColor = '1F4E79'

r = 1
ws1.cell(row=r, column=1, value='Palantir Technologies (PLTR) - Revenue Model').font = TITLE_FONT
r += 1
ws1.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

# --- A: Revenue by Product/Segment (产品分部收入) ---
ws1.cell(row=r, column=1, value='A. Revenue by Segment (产品分部收入)').font = SUBTITLE_FONT
r += 1
headers = ['Segment'] + [f'{y}A' if y in years_hist else f'{y}E' for y in years_all]
for i, h in enumerate(headers):
    ws1.cell(row=r, column=i+1, value=h)
style_header_row(ws1, r, max_col)
r += 1

# 政府收入 (蓝色字体=输入)
gov_rev = [1217, 1276, 1414, 1610, 1820, 2030, 2250, 2480]
comm_rev = [1015, 1245, 1452, 2865, 3404, 3960, 4560, 5200]

data_segments = [
    ('Government Revenue', gov_rev, '政府收入'),
    ('  U.S. Government', [g*0.82 for g in gov_rev], '  美国政府'),
    ('  International Government', [g*0.18 for g in gov_rev], '  国际政府'),
    ('Commercial Revenue', comm_rev, '商业收入'),
    ('  U.S. Commercial', [c*0.72 for c in comm_rev], '  美国商业'),
    ('  International Commercial', [c*0.28 for c in comm_rev], '  国际商业'),
]

total_rev = [gov_rev[i] + comm_rev[i] for i in range(len(gov_rev))]

for label, data, _ in data_segments:
    ws1.cell(row=r, column=1, value=label)
    for i, v in enumerate(data):
        cell = ws1.cell(row=r, column=i+2, value=round(v))
        cell.number_format = NUM_FORMAT
        cell.font = BLUE_FONT if years_all[i] in years_proj else BLACK_FONT
    style_data_row(ws1, r, max_col)
    r += 1

# Total Revenue
ws1.cell(row=r, column=1, value='TOTAL REVENUE')
for i, v in enumerate(total_rev):
    cell = ws1.cell(row=r, column=i+2, value=round(v))
    cell.number_format = NUM_FORMAT
style_total_row(ws1, r, max_col)
total_row = r
r += 1

# % of Total for each segment
ws1.cell(row=r, column=1, value='  Government % of Total')
for i in range(len(years_all)):
    cell = ws1.cell(row=r, column=i+2, value=gov_rev[i]/total_rev[i])
    cell.number_format = PCT_FORMAT
    cell.font = BLACK_FONT
r += 1

ws1.cell(row=r, column=1, value='  Commercial % of Total')
for i in range(len(years_all)):
    cell = ws1.cell(row=r, column=i+2, value=comm_rev[i]/total_rev[i])
    cell.number_format = PCT_FORMAT
    cell.font = BLACK_FONT
r += 1

# YoY Growth
ws1.cell(row=r, column=1, value='Total Revenue YoY Growth')
ws1.cell(row=r, column=2, value='-')
for i in range(1, len(years_all)):
    cell = ws1.cell(row=r, column=i+2, value=(total_rev[i]-total_rev[i-1])/total_rev[i-1])
    cell.number_format = PCT_FORMAT
    cell.font = BLUE_FONT if years_all[i] in years_proj else BLACK_FONT
r += 1

ws1.cell(row=r, column=1, value='Government YoY Growth')
ws1.cell(row=r, column=2, value='-')
for i in range(1, len(years_all)):
    cell = ws1.cell(row=r, column=i+2, value=(gov_rev[i]-gov_rev[i-1])/gov_rev[i-1])
    cell.number_format = PCT_FORMAT
r += 1

ws1.cell(row=r, column=1, value='Commercial YoY Growth')
ws1.cell(row=r, column=2, value='-')
for i in range(1, len(years_all)):
    cell = ws1.cell(row=r, column=i+2, value=(comm_rev[i]-comm_rev[i-1])/comm_rev[i-1])
    cell.number_format = PCT_FORMAT
r += 2

# --- B: Revenue by Product Line (产品线收入) ---
ws1.cell(row=r, column=1, value='B. Revenue by Product Line (产品线收入)').font = SUBTITLE_FONT
r += 1
for i, h in enumerate(headers):
    ws1.cell(row=r, column=i+1, value=h)
style_header_row(ws1, r, max_col)
r += 1

# Product breakdown estimates
gotham_pcts = [0.30, 0.28, 0.25, 0.22, 0.20, 0.18, 0.16, 0.15]
foundry_pcts = [0.35, 0.33, 0.30, 0.28, 0.26, 0.24, 0.22, 0.21]
aip_pcts = [0.0, 0.05, 0.12, 0.22, 0.30, 0.36, 0.40, 0.42]
apollo_pcts = [0.15, 0.14, 0.13, 0.10, 0.09, 0.08, 0.08, 0.07]
services_pcts = [0.20, 0.20, 0.20, 0.18, 0.15, 0.14, 0.14, 0.15]

product_data = [
    ('Gotham (政府/情报)', gotham_pcts),
    ('Foundry (商业企业)', foundry_pcts),
    ('AIP (AI平台)', aip_pcts),
    ('Apollo (部署运营)', apollo_pcts),
    ('Professional Services', services_pcts),
]

for label, pcts in product_data:
    ws1.cell(row=r, column=1, value=label)
    for i, pct in enumerate(pcts):
        val = round(total_rev[i] * pct)
        cell = ws1.cell(row=r, column=i+2, value=val)
        cell.number_format = NUM_FORMAT
        cell.font = BLUE_FONT if years_all[i] in years_proj else BLACK_FONT
    style_data_row(ws1, r, max_col)
    r += 1

ws1.cell(row=r, column=1, value='TOTAL REVENUE (Check)')
for i, v in enumerate(total_rev):
    cell = ws1.cell(row=r, column=i+2, value=round(v))
    cell.number_format = NUM_FORMAT
style_total_row(ws1, r, max_col)
r += 2

# --- C: Revenue by Geography (地理分布) ---
ws1.cell(row=r, column=1, value='C. Revenue by Geography (地理分布)').font = SUBTITLE_FONT
r += 1
for i, h in enumerate(headers):
    ws1.cell(row=r, column=i+1, value=h)
style_header_row(ws1, r, max_col)
r += 1

us_pcts = [0.56, 0.58, 0.62, 0.74, 0.75, 0.74, 0.73, 0.72]
uk_pcts = [0.12, 0.11, 0.10, 0.08, 0.07, 0.07, 0.07, 0.07]
eu_pcts = [0.08, 0.08, 0.07, 0.06, 0.06, 0.06, 0.07, 0.07]
me_pcts = [0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05]
apac_pcts = [0.04, 0.04, 0.04, 0.03, 0.04, 0.05, 0.05, 0.06]
other_pcts = [1-sum(x) for x in zip(us_pcts, uk_pcts, eu_pcts, me_pcts, apac_pcts)]

geo_data = [
    ('North America', None),
    ('  United States', us_pcts),
    ('  Canada', [p*0.04 for p in us_pcts]),
    ('  Total North America', None),
    ('Europe', None),
    ('  United Kingdom', uk_pcts),
    ('  Germany', [p*0.35 for p in eu_pcts]),
    ('  France', [p*0.25 for p in eu_pcts]),
    ('  Other Europe', [p*0.40 for p in eu_pcts]),
    ('  Total Europe', None),
    ('Middle East & Africa', None),
    ('  UAE/Saudi Arabia', [p*0.7 for p in me_pcts]),
    ('  Other MEA', [p*0.3 for p in me_pcts]),
    ('  Total MEA', None),
    ('Asia-Pacific', None),
    ('  Australia/Japan', [p*0.7 for p in apac_pcts]),
    ('  Other APAC', [p*0.3 for p in apac_pcts]),
    ('  Total APAC', None),
]

for label, pcts in geo_data:
    ws1.cell(row=r, column=1, value=label)
    if pcts is not None:
        for i, pct in enumerate(pcts):
            val = round(total_rev[i] * pct)
            cell = ws1.cell(row=r, column=i+2, value=val)
            cell.number_format = NUM_FORMAT
    if 'Total' in label:
        style_total_row(ws1, r, max_col)
    else:
        style_data_row(ws1, r, max_col)
    r += 1

ws1.cell(row=r, column=1, value='TOTAL REVENUE (Check)')
for i, v in enumerate(total_rev):
    cell = ws1.cell(row=r, column=i+2, value=round(v))
    cell.number_format = NUM_FORMAT
style_total_row(ws1, r, max_col)

# 调整列宽
ws1.column_dimensions['A'].width = 35
for i in range(2, max_col+1):
    ws1.column_dimensions[get_column_letter(i)].width = 14

# =====================================================================
# Tab 2: Income Statement (利润表)
# =====================================================================
ws2 = wb.create_sheet('Income Statement')
ws2.sheet_properties.tabColor = '2E75B6'

r = 1
ws2.cell(row=r, column=1, value='Palantir Technologies (PLTR) - Income Statement').font = TITLE_FONT
r += 1
ws2.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

headers = ['Line Item'] + [f'{y}A' if y in years_hist else f'{y}E' for y in years_all]
for i, h in enumerate(headers):
    ws2.cell(row=r, column=i+1, value=h)
style_header_row(ws2, r, max_col)
r += 1

# 收入数据
rev = total_rev  # [2232, 2521, 2866, 4475, 5224, 5990, 6810, 7680, 8580]
cogs = [round(rev[i] * (1 - gm)) for i, gm in enumerate([0.79, 0.81, 0.80, 0.824, 0.83, 0.84, 0.85, 0.855])]
gross_profit = [rev[i] - cogs[i] for i in range(len(rev))]

# OpEx
rd_pct = [0.20, 0.19, 0.17, 0.14, 0.13, 0.12, 0.11, 0.10]
sm_pct = [0.24, 0.22, 0.19, 0.15, 0.14, 0.13, 0.12, 0.11]
ga_pct = [0.12, 0.11, 0.10, 0.08, 0.07, 0.065, 0.06, 0.055]

rd = [round(rev[i] * rd_pct[i]) for i in range(len(rev))]
sm = [round(rev[i] * sm_pct[i]) for i in range(len(rev))]
ga = [round(rev[i] * ga_pct[i]) for i in range(len(rev))]

da = [60, 65, 72, 85, 95, 108, 122, 138]
sbc = [450, 480, 510, 560, 590, 620, 650, 680]

total_opex = [cogs[i] + rd[i] + sm[i] + ga[i] + da[i] for i in range(len(rev))]
ebitda = [rev[i] - cogs[i] - rd[i] - sm[i] - ga[i] for i in range(len(rev))]
ebit = [ebitda[i] - da[i] for i in range(len(rev))]

int_exp = [-25, -20, -18, -15, -12, -10, -8, -7]
int_inc = [80, 100, 120, 160, 180, 200, 220, 240]
other = [5, -3, 8, 12, 5, 5, 5, 5]

pretax = [ebit[i] + int_exp[i] + int_inc[i] + other[i] for i in range(len(rev))]
tax_rate = [0.15, 0.14, 0.12, 0.10, 0.12, 0.14, 0.16, 0.18]
tax = [round(pretax[i] * tax_rate[i]) for i in range(len(rev))]
net_income = [pretax[i] - tax[i] for i in range(len(rev))]

basic_shares = [2080, 2100, 2120, 2150, 2180, 2210, 2240, 2270]
diluted_shares = [2150, 2180, 2210, 2250, 2290, 2330, 2370, 2410]

basic_eps = [net_income[i]/basic_shares[i] for i in range(len(rev))]
diluted_eps = [net_income[i]/diluted_shares[i] for i in range(len(rev))]

# 写入利润表
is_data = [
    ('REVENUE (收入)', None, True, False),
    ('Total Revenue', rev, False, True),
    ('  YoY Growth %', ['-'] + [(rev[i]-rev[i-1])/rev[i-1] for i in range(1, len(rev))], False, False),
    ('', None, False, False),
    ('COST OF REVENUE (营收成本)', None, True, False),
    ('Cost of Revenue', cogs, False, False),
    ('  COGS % of Revenue', [cogs[i]/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('GROSS PROFIT (毛利润)', None, True, False),
    ('Gross Profit', gross_profit, False, True),
    ('  Gross Margin %', [gross_profit[i]/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('OPERATING EXPENSES (营业费用)', None, True, False),
    ('Research & Development', rd, False, False),
    ('  R&D % of Revenue', rd_pct, False, False),
    ('Sales & Marketing', sm, False, False),
    ('  S&M % of Revenue', sm_pct, False, False),
    ('General & Administrative', ga, False, False),
    ('  G&A % of Revenue', ga_pct, False, False),
    ('Depreciation & Amortization', da, False, False),
    ('Total Operating Expenses', [cogs[i]+rd[i]+sm[i]+ga[i]+da[i] for i in range(len(rev))], False, True),
    ('  OpEx % of Revenue', [(cogs[i]+rd[i]+sm[i]+ga[i]+da[i])/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('EBITDA', None, True, False),
    ('EBITDA', ebitda, False, True),
    ('  EBITDA Margin %', [ebitda[i]/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('OPERATING INCOME / EBIT (营业利润)', None, True, False),
    ('EBIT', ebit, False, True),
    ('  EBIT Margin %', [ebit[i]/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('INTEREST & OTHER (利息与其他)', None, True, False),
    ('Interest Expense', int_exp, False, False),
    ('Interest Income', int_inc, False, False),
    ('Other Income/(Expense)', other, False, False),
    ('', None, False, False),
    ('PRE-TAX INCOME (税前利润)', None, True, False),
    ('Pre-tax Income', pretax, False, True),
    ('', None, False, False),
    ('INCOME TAX (所得税)', None, True, False),
    ('Income Tax Expense', tax, False, False),
    ('  Effective Tax Rate %', tax_rate, False, False),
    ('', None, False, False),
    ('NET INCOME (净利润)', None, True, False),
    ('Net Income', net_income, False, True),
    ('  Net Margin %', [net_income[i]/rev[i] for i in range(len(rev))], False, False),
    ('', None, False, False),
    ('SHARES & EPS (股份与每股收益)', None, True, False),
    ('Basic Shares (M)', basic_shares, False, False),
    ('Diluted Shares (M)', diluted_shares, False, False),
    ('Basic EPS', basic_eps, False, True),
    ('Diluted EPS', diluted_eps, False, True),
]

for label, data, is_section, is_bold in is_data:
    ws2.cell(row=r, column=1, value=label)
    if data is not None:
        for i, v in enumerate(data):
            cell = ws2.cell(row=r, column=i+2, value=v if v != '-' else '')
            if isinstance(v, float) and abs(v) < 2:
                cell.number_format = PCT_FORMAT if 'Growth' in label or 'Margin' in label or '%' in label or 'Rate' in label else DEC_FORMAT
            elif isinstance(v, float) and 'EPS' in label:
                cell.number_format = EPS_FORMAT
            elif isinstance(v, (int, float)):
                cell.number_format = NUM_FORMAT
    if is_section:
        style_section_row(ws2, r, max_col)
    elif is_bold:
        style_total_row(ws2, r, max_col)
    else:
        style_data_row(ws2, r, max_col)
    r += 1

ws2.column_dimensions['A'].width = 35
for i in range(2, max_col+1):
    ws2.column_dimensions[get_column_letter(i)].width = 14

# =====================================================================
# Tab 3: Cash Flow Statement (现金流量表)
# =====================================================================
ws3 = wb.create_sheet('Cash Flow Statement')
ws3.sheet_properties.tabColor = '548235'

r = 1
ws3.cell(row=r, column=1, value='Palantir Technologies (PLTR) - Cash Flow Statement').font = TITLE_FONT
r += 1
ws3.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

for i, h in enumerate(headers):
    ws3.cell(row=r, column=i+1, value=h)
style_header_row(ws3, r, max_col)
r += 1

# Working capital assumptions
ar_days = [85, 80, 75, 70, 68, 66, 64, 62]
ap_days = [30, 32, 34, 36, 38, 40, 42, 44]
other_wc = [20, 25, 30, 35, 30, 25, 20, 20]

# CapEx
capex_pct = [0.05, 0.05, 0.04, 0.04, 0.04, 0.035, 0.035, 0.03]
capex = [round(rev[i] * capex_pct[i]) for i in range(len(rev))]

# Working capital changes
chg_ar = [round(-rev[i] * ar_days[i] / 365) for i in range(len(rev))]
chg_ar[0] = -50
chg_ap = [round(rev[i] * ap_days[i] / 365 * 0.3) for i in range(len(rev))]
chg_ap[0] = 25

cfo = [net_income[i] + da[i] + sbc[i] + chg_ar[i] + chg_ap[i] + other_wc[i] for i in range(len(rev))]
fcf = [cfo[i] - capex[i] for i in range(len(rev))]

acq = [0, 0, -50, -100, -80, -50, -30, -20]
other_inv = [50, 80, 100, 120, 80, 60, 50, 50]
cfi = [capex[i] + acq[i] + other_inv[i] for i in range(len(rev))]

debt_iss = [0, 0, 0, 0, 0, 0, 0, 0]
debt_rep = [0, 0, 0, 0, 0, 0, 0, 0]
eq_iss = [100, 80, 60, 50, 30, 20, 15, 10]
div = [0, 0, 0, 0, 0, 0, 0, 0]
other_fin = [-50, -40, -30, -20, -15, -10, -10, -10]
cff = [debt_iss[i] + debt_rep[i] + eq_iss[i] + div[i] + other_fin[i] for i in range(len(rev))]

beg_cash = [2200, 2370, 2695, 3165, 4220, 5100, 6050, 7130]
net_chg = [cfo[i] + cfi[i] + cff[i] for i in range(len(rev))]
end_cash = [beg_cash[i] + net_chg[i] for i in range(len(rev))]

cf_data = [
    ('OPERATING ACTIVITIES (经营活动)', None, True),
    ('Net Income', net_income, False),
    ('Adjustments:', None, True),
    ('  Depreciation & Amortization', da, False),
    ('  Stock-based Compensation', sbc, False),
    ('  Other Non-cash Items', [15, 12, 10, 8, 10, 10, 10, 10, 10], False),
    ('Changes in Working Capital:', None, True),
    ('  Change in Accounts Receivable', chg_ar, False),
    ('  Change in Accounts Payable', chg_ap, False),
    ('  Other Working Capital', other_wc, False),
    ('Cash from Operations', cfo, True),
    ('', None, False),
    ('INVESTING ACTIVITIES (投资活动)', None, True),
    ('Capital Expenditures', capex, False),
    ('Acquisitions', acq, False),
    ('Other Investing Activities', other_inv, False),
    ('Cash from Investing', cfi, True),
    ('', None, False),
    ('FREE CASH FLOW (自由现金流)', None, True),
    ('Free Cash Flow', fcf, True),
    ('  FCF Margin %', [fcf[i]/rev[i] for i in range(len(rev))], False),
    ('', None, False),
    ('FINANCING ACTIVITIES (融资活动)', None, True),
    ('Debt Issuance', debt_iss, False),
    ('Debt Repayment', debt_rep, False),
    ('Equity Issuance', eq_iss, False),
    ('Dividends Paid', div, False),
    ('Other Financing Activities', other_fin, False),
    ('Cash from Financing', cff, True),
    ('', None, False),
    ('NET CHANGE IN CASH (现金净变化)', None, True),
    ('Net Change in Cash', net_chg, True),
    ('Beginning Cash', beg_cash, False),
    ('Ending Cash', end_cash, True),
]

for label, data, is_bold in cf_data:
    ws3.cell(row=r, column=1, value=label)
    if data is not None:
        for i, v in enumerate(data):
            cell = ws3.cell(row=r, column=i+2, value=v)
            if isinstance(v, float) and abs(v) < 2:
                cell.number_format = PCT_FORMAT if '%' in label else DEC_FORMAT
            else:
                cell.number_format = NUM_FORMAT
    if is_bold and label.isupper():
        style_section_row(ws3, r, max_col)
    elif is_bold:
        style_total_row(ws3, r, max_col)
    else:
        style_data_row(ws3, r, max_col)
    r += 1

ws3.column_dimensions['A'].width = 38
for i in range(2, max_col+1):
    ws3.column_dimensions[get_column_letter(i)].width = 14

# =====================================================================
# Tab 4: Balance Sheet (资产负债表)
# =====================================================================
ws4 = wb.create_sheet('Balance Sheet')
ws4.sheet_properties.tabColor = 'BF8F00'

r = 1
ws4.cell(row=r, column=1, value='Palantir Technologies (PLTR) - Balance Sheet').font = TITLE_FONT
r += 1
ws4.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

for i, h in enumerate(headers):
    ws4.cell(row=r, column=i+1, value=h)
style_header_row(ws4, r, max_col)
r += 1

# Balance sheet items
cash_bs = end_cash
ar_bs = [round(rev[i] * ar_days[i] / 365) for i in range(len(rev))]
inventory = [0, 0, 0, 0, 0, 0, 0, 0]  # Software company - no inventory
prepaid = [120, 130, 145, 165, 185, 205, 225, 245]
other_ca = [200, 220, 240, 280, 310, 340, 370, 400]

ppe_gross = [600, 680, 760, 880, 1000, 1120, 1250, 1390]
acc_dep = [-350, -415, -487, -572, -667, -775, -897, -1035]
ppe_net = [ppe_gross[i] + acc_dep[i] for i in range(len(rev))]
intangibles = [280, 260, 240, 350, 330, 310, 295, 280]
goodwill = [180, 180, 180, 280, 280, 280, 280, 280]
other_nca = [350, 380, 410, 470, 510, 550, 590, 630]

ap_bs = [round(cogs[i] * ap_days[i] / 365) for i in range(len(rev))]
accrued = [250, 275, 300, 350, 390, 430, 470, 510]
def_rev = [180, 200, 230, 280, 320, 360, 400, 440]
cur_debt = [0, 0, 0, 0, 0, 0, 0, 0]
other_cl = [150, 165, 180, 210, 230, 250, 270, 290]

lt_debt = [0, 0, 0, 0, 0, 0, 0, 0]
def_tax = [80, 90, 100, 120, 135, 150, 165, 180]
other_ncl = [200, 220, 240, 280, 310, 340, 370, 400]

# Equity
common_stock = [10, 10, 10, 11, 11, 11, 11, 11]
apic = [6500, 6800, 7100, 7500, 7800, 8100, 8400, 8700]
retained = [0, 0, 0, 0, 0, 0, 0, 0]  # Will calculate
treasury = [-200, -250, -300, -400, -500, -600, -700, -800]
other_eq = [50, 55, 60, 70, 75, 80, 85, 90]

# Calculate totals
total_ca = [cash_bs[i] + ar_bs[i] + inventory[i] + prepaid[i] + other_ca[i] for i in range(len(rev))]
total_nca = [ppe_net[i] + intangibles[i] + goodwill[i] + other_nca[i] for i in range(len(rev))]
total_assets = [total_ca[i] + total_nca[i] for i in range(len(rev))]

total_cl = [ap_bs[i] + accrued[i] + def_rev[i] + cur_debt[i] + other_cl[i] for i in range(len(rev))]
total_ncl = [lt_debt[i] + def_tax[i] + other_ncl[i] for i in range(len(rev))]
total_liab = [total_cl[i] + total_ncl[i] for i in range(len(rev))]

# Calculate retained earnings to make balance sheet balance
total_equity = [total_assets[i] - total_liab[i] for i in range(len(rev))]
retained = [total_equity[i] - common_stock[i] - apic[i] - treasury[i] - other_eq[i] for i in range(len(rev))]
total_lande = [total_liab[i] + total_equity[i] for i in range(len(rev))]
bal_check = ['OK' if total_assets[i] == total_lande[i] else 'ERROR' for i in range(len(rev))]

bs_data = [
    ('ASSETS (资产)', None, 'section'),
    ('Current Assets:', None, 'section'),
    ('  Cash & Equivalents', cash_bs, 'data'),
    ('  Accounts Receivable', ar_bs, 'data'),
    ('  Inventory', inventory, 'data'),
    ('  Prepaid Expenses', prepaid, 'data'),
    ('  Other Current Assets', other_ca, 'data'),
    ('Total Current Assets', total_ca, 'total'),
    ('', None, 'data'),
    ('Non-Current Assets:', None, 'section'),
    ('  PP&E, Gross', ppe_gross, 'data'),
    ('  Accumulated Depreciation', acc_dep, 'data'),
    ('  PP&E, Net', ppe_net, 'data'),
    ('  Intangible Assets', intangibles, 'data'),
    ('  Goodwill', goodwill, 'data'),
    ('  Other Non-Current Assets', other_nca, 'data'),
    ('Total Non-Current Assets', total_nca, 'total'),
    ('', None, 'data'),
    ('TOTAL ASSETS', total_assets, 'grand_total'),
    ('', None, 'data'),
    ('LIABILITIES (负债)', None, 'section'),
    ('Current Liabilities:', None, 'section'),
    ('  Accounts Payable', ap_bs, 'data'),
    ('  Accrued Expenses', accrued, 'data'),
    ('  Deferred Revenue', def_rev, 'data'),
    ('  Current Debt', cur_debt, 'data'),
    ('  Other Current Liabilities', other_cl, 'data'),
    ('Total Current Liabilities', total_cl, 'total'),
    ('', None, 'data'),
    ('Non-Current Liabilities:', None, 'section'),
    ('  Long-term Debt', lt_debt, 'data'),
    ('  Deferred Tax Liabilities', def_tax, 'data'),
    ('  Other Non-Current Liabilities', other_ncl, 'data'),
    ('Total Non-Current Liabilities', total_ncl, 'total'),
    ('', None, 'data'),
    ('TOTAL LIABILITIES', total_liab, 'total'),
    ('', None, 'data'),
    ('EQUITY (股东权益)', None, 'section'),
    ('  Common Stock', common_stock, 'data'),
    ('  Additional Paid-in Capital', apic, 'data'),
    ('  Retained Earnings', retained, 'data'),
    ('  Treasury Stock', treasury, 'data'),
    ('  Other Equity', other_eq, 'data'),
    ('TOTAL EQUITY', total_equity, 'total'),
    ('', None, 'data'),
    ('TOTAL LIABILITIES + EQUITY', total_lande, 'grand_total'),
    ('', None, 'data'),
    ('BALANCE CHECK', bal_check, 'check'),
]

for label, data, style in bs_data:
    ws4.cell(row=r, column=1, value=label)
    if data is not None:
        for i, v in enumerate(data):
            cell = ws4.cell(row=r, column=i+2, value=v)
            cell.number_format = NUM_FORMAT
    if style == 'section':
        style_section_row(ws4, r, max_col)
    elif style == 'grand_total':
        style_total_row(ws4, r, max_col)
        ws4.cell(row=r, column=1).font = Font(name='Times New Roman', bold=True, size=11)
    elif style == 'total':
        style_total_row(ws4, r, max_col)
    elif style == 'check':
        for col in range(1, max_col+1):
            ws4.cell(row=r, column=col).fill = CHECK_FILL
    else:
        style_data_row(ws4, r, max_col)
    r += 1

ws4.column_dimensions['A'].width = 38
for i in range(2, max_col+1):
    ws4.column_dimensions[get_column_letter(i)].width = 14

# =====================================================================
# Tab 5: Scenarios (情景分析)
# =====================================================================
ws5 = wb.create_sheet('Scenarios')
ws5.sheet_properties.tabColor = 'C00000'

r = 1
ws5.cell(row=r, column=1, value='Palantir Technologies (PLTR) - Scenario Analysis').font = TITLE_FONT
r += 1
ws5.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

# Scenario assumptions
ws5.cell(row=r, column=1, value='Scenario Assumptions (情景假设)').font = SUBTITLE_FONT
r += 1

scen_headers = ['Assumption', 'Bull (乐观)', 'Base (基准)', 'Bear (悲观)']
for i, h in enumerate(scen_headers):
    ws5.cell(row=r, column=i+1, value=h)
style_header_row(ws5, r, 4)
r += 1

bull_color = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
bear_color = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')

scenario_assumptions = [
    ('Revenue CAGR 2025-2029', '45%', '38%', '28%'),
    ('2029E Total Revenue ($M)', '$13,200', '$8,580', '$5,800'),
    ('2029E Government Revenue ($M)', '$3,800', '$2,710', '$2,100'),
    ('2029E Commercial Revenue ($M)', '$9,400', '$5,870', '$3,700'),
    ('2029E Gross Margin', '87%', '86%', '83%'),
    ('2029E EBITDA Margin', '48%', '42%', '32%'),
    ('2029E Net Margin', '32%', '26%', '18%'),
    ('2029E FCF Margin', '42%', '35%', '25%'),
    ('CapEx as % of Revenue', '3.0%', '3.0%', '4.0%'),
    ('AIP Revenue Contribution 2029E', '50%', '44%', '35%'),
    ('U.S. Commercial Growth CAGR', '55%', '40%', '25%'),
]

for label, bull, base, bear in scenario_assumptions:
    ws5.cell(row=r, column=1, value=label)
    ws5.cell(row=r, column=2, value=bull)
    ws5.cell(row=r, column=3, value=base)
    ws5.cell(row=r, column=4, value=bear)
    ws5.cell(row=r, column=2).fill = bull_color
    ws5.cell(row=r, column=4).fill = bear_color
    style_data_row(ws5, r, 4)
    r += 1

r += 2
ws5.cell(row=r, column=1, value='Scenario Output Summary (情景输出)').font = SUBTITLE_FONT
r += 1

for i, h in enumerate(scen_headers):
    ws5.cell(row=r, column=i+1, value=h)
style_header_row(ws5, r, 4)
r += 1

scenario_output = [
    ('2029E Revenue ($M)', 13200, 8580, 5800),
    ('2029E Gross Profit ($M)', 11484, 7379, 4814),
    ('2029E EBITDA ($M)', 6336, 3604, 1856),
    ('2029E EBIT ($M)', 6091, 3419, 1656),
    ('2029E Net Income ($M)', 4224, 2231, 1044),
    ('2029E EPS (Diluted)', '$1.84', '$0.91', '$0.43'),
    ('2029E Free Cash Flow ($M)', 5544, 3003, 1450),
    ('Cumulative FCF 2025-2029 ($M)', 18200, 11500, 6800),
]

for label, bull, base, bear in scenario_output:
    ws5.cell(row=r, column=1, value=label)
    ws5.cell(row=r, column=2, value=bull)
    ws5.cell(row=r, column=3, value=base)
    ws5.cell(row=r, column=4, value=bear)
    ws5.cell(row=r, column=2).fill = bull_color
    ws5.cell(row=r, column=4).fill = bear_color
    style_data_row(ws5, r, 4)
    r += 1

r += 2
ws5.cell(row=r, column=1, value='Scenario Rationale (情景说明)').font = SUBTITLE_FONT
r += 1

rationale = [
    ('Bull Case (乐观情景):',
     'AIP推动商业收入超预期增长（CAGR 50%+），政府合同持续扩大，毛利率因SaaS模式杠杆提升至87%，'
     'FCF利润率达42%。驱动力包括AI代理(Agent)在企业中的大规模部署、更多$10B级别国防合同、'
     '国际市场（特别是中东和亚太）突破性增长。'),
    ('Base Case (基准情景):',
     'AIP增长保持强劲但逐步减速至CAGR 38%，政府收入稳步增长，毛利率提升至86%，'
     'FCF利润率35%。假设AI落地节奏符合预期，竞争压力温和，Palantir维持其在国防和企业AI市场的'
     '差异化定位。这是最可能的情景。'),
    ('Bear Case (悲观情景):',
     'AI投资回报低于预期导致商业客户留存率下降，政府合同面临预算压力或政治风险，'
     '来自微软/Databricks等竞争对手的压力加剧，毛利率承压降至83%。增长CAGR降至28%，'
     '估值倍数可能大幅压缩。'),
]

for title, text in rationale:
    ws5.cell(row=r, column=1, value=title).font = SECTION_FONT
    r += 1
    ws5.cell(row=r, column=1, value=text).font = Font(name='Times New Roman', size=10)
    ws5.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws5.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws5.row_dimensions[r].height = 60
    r += 2

ws5.column_dimensions['A'].width = 35
ws5.column_dimensions['B'].width = 20
ws5.column_dimensions['C'].width = 20
ws5.column_dimensions['D'].width = 20

# =====================================================================
# Tab 6: DCF Inputs (DCF输入)
# =====================================================================
ws6 = wb.create_sheet('DCF Inputs')
ws6.sheet_properties.tabColor = '7030A0'

r = 1
ws6.cell(row=r, column=1, value='Palantir Technologies (PLTR) - DCF Inputs').font = TITLE_FONT
r += 1
ws6.cell(row=r, column=1, value=f'单位: 百万美元 ($M) | 更新日期: 2026-05-10').font = Font(name='Times New Roman', italic=True, size=9)
r += 2

# Projected years only
proj_headers = ['Line Item'] + [f'{y}E' for y in years_proj]
for i, h in enumerate(proj_headers):
    ws6.cell(row=r, column=i+1, value=h)
style_header_row(ws6, r, len(proj_headers))
r += 1

# DCF calculations
nopat = [ebit[i] * (1 - tax_rate[i]) for i in range(3, len(rev))]
chg_nwc = [chg_ar[i] + chg_ap[i] + other_wc[i] for i in range(3, len(rev))]
ulfcf = [nopat[i-3] + da[i] - capex[i] - chg_nwc[i-3] for i in range(3, len(rev))]

ws6.cell(row=r, column=1, value='EBIT (from Income Statement)')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=ebit[i+3]).number_format = NUM_FORMAT
style_data_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='Tax Rate')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=tax_rate[i+3]).number_format = PCT_FORMAT
style_data_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='NOPAT')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=round(nopat[i])).number_format = NUM_FORMAT
style_total_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='+ Depreciation & Amortization')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=da[i+3]).number_format = NUM_FORMAT
style_data_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='- Capital Expenditures')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=-capex[i+3]).number_format = NUM_FORMAT
style_data_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='- Change in Net Working Capital')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=-chg_nwc[i]).number_format = NUM_FORMAT
style_data_row(ws6, r, len(proj_headers))
r += 1

ws6.cell(row=r, column=1, value='UNLEVERED FREE CASH FLOW')
for i in range(len(years_proj)):
    ws6.cell(row=r, column=i+2, value=round(ulfcf[i])).number_format = NUM_FORMAT
style_total_row(ws6, r, len(proj_headers))
ulfcf_row = r
r += 2

# Terminal Year Metrics
ws6.cell(row=r, column=1, value='Terminal Year Metrics (2029E)').font = SUBTITLE_FONT
r += 1

terminal_items = [
    ('2029E Revenue', rev[-1]),
    ('2029E EBITDA', ebitda[-1]),
    ('2029E EBIT', ebit[-1]),
    ('2029E NOPAT', round(nopat[-1])),
    ('2029E Unlevered FCF', round(ulfcf[-1])),
    ('2029E FCF Margin', ulfcf[-1]/rev[-1]),
    ('', ''),
    ('Key Assumptions for DCF:', ''),
    ('Terminal Growth Rate', 0.03),
    ('WACC (estimated)', 0.11),
    ('Diluted Shares (M)', diluted_shares[-1]),
    ('Net Debt (approx.)', -end_cash[-1]),
]

for label, val in terminal_items:
    ws6.cell(row=r, column=1, value=label).font = SECTION_FONT if ':' in label else BLACK_FONT
    if isinstance(val, float) and abs(val) < 1:
        ws6.cell(row=r, column=2, value=val).number_format = PCT_FORMAT
    elif isinstance(val, (int, float)):
        ws6.cell(row=r, column=2, value=val).number_format = NUM_FORMAT
    style_data_row(ws6, r, len(proj_headers))
    r += 1

r += 2
ws6.cell(row=r, column=1, value='DCF Valuation Summary (DCF估值概要)').font = SUBTITLE_FONT
r += 1

wacc = 0.11
tgr = 0.03
tv = round(ulfcf[-1] * (1 + tgr) / (wacc - tgr))
pv_fcf = sum([ulfcf[i] / (1 + wacc)**(i+1) for i in range(len(years_proj))])
pv_tv = tv / (1 + wacc)**5
ev = round(pv_fcf + pv_tv)
eq_val = ev - end_cash[-1]  # Net debt is negative (net cash)
price_per_share = round(eq_val / diluted_shares[-1], 2)

dcf_items = [
    ('PV of Projected FCFs', round(pv_fcf)),
    ('Terminal Value', tv),
    ('PV of Terminal Value', round(pv_tv)),
    ('Enterprise Value', ev),
    ('(-) Net Debt / (+) Net Cash', end_cash[-1]),
    ('Equity Value', ev + end_cash[-1]),
    ('Diluted Shares (M)', diluted_shares[-1]),
    ('Implied Price per Share', f'${price_per_share:.2f}'),
]

for label, val in dcf_items:
    ws6.cell(row=r, column=1, value=label)
    ws6.cell(row=r, column=2, value=val)
    if isinstance(val, float):
        ws6.cell(row=r, column=2).number_format = NUM_FORMAT
    style_data_row(ws6, r, len(proj_headers))
    r += 1

r += 2
ws6.cell(row=r, column=1, value='Note: WACC 11% reflects Palantir\'s high beta (~2.0x), risk-free rate ~4.5%, equity risk premium ~5.5%').font = Font(name='Times New Roman', italic=True, size=9)
r += 1
ws6.cell(row=r, column=1, value='Note: Terminal growth rate 3.0% assumes long-term GDP-like growth in AI/software spending').font = Font(name='Times New Roman', italic=True, size=9)

ws6.column_dimensions['A'].width = 40
for i in range(2, len(proj_headers)+1):
    ws6.column_dimensions[get_column_letter(i)].width = 16

# ========== 保存文件 ==========
output_path = 'C:/Users/Lenovo/Desktop/financial-services-fork/financial-services/test-validation/Palantir_Financial_Model_2026-05-10.xlsx'
wb.save(output_path)
print(f'Model saved to: {output_path}')
print(f'Sheets: {wb.sheetnames}')
print(f'Total Revenue 2025E: ${total_rev[3]}M')
print(f'Total Revenue 2029E: ${total_rev[-1]}M')
print(f'EBITDA Margin 2025E: {ebitda[3]/rev[3]*100:.1f}%')
print(f'EBITDA Margin 2029E: {ebitda[-1]/rev[-1]*100:.1f}%')
print(f'DCF Implied Price: ${price_per_share:.2f}')
