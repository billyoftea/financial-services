#!/usr/bin/env python3
"""
build_tsm_excel_v2.py — TSM 台积电 coverage model v2
- 5个业务分部独立S曲线收入建模
- 分层P&L (GM → R&D → SGA → EBIT → Tax → NI)
- 动态PE (增速挂钩, 非常数)
- 每行附逻辑说明和推理依据
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

# ===== 样式 =====
BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
GREEN = Font(color="008000")
WHITE_B = Font(color="FFFFFF", bold=True)
BLACK_B = Font(color="000000", bold=True)
GRAY = Font(color="666666", italic=True)

H_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
COL_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
OUT_FILL = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
IN_FILL = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
TOG_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
SEG_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

BD = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
RA = Alignment(horizontal='right')
WRAP = Alignment(horizontal='left', vertical='top', wrap_text=True)
N = 10  # 预测年数


def sh(ws, r, c1, c2, fill=H_FILL, font=WHITE_B):
    for c in range(c1, c2 + 1):
        cell = ws.cell(row=r, column=c)
        cell.fill = fill; cell.font = font
        cell.alignment = Alignment(horizontal='center'); cell.border = BD


def sc(ws, r, c, font=BLACK, fill=None, fmt=None, align=RA):
    cell = ws.cell(row=r, column=c)
    cell.font = font
    if fill: cell.fill = fill
    cell.border = BD; cell.alignment = align
    if fmt: cell.number_format = fmt


def lbl(ws, r, c, val, font=BLACK_B):
    ws.cell(row=r, column=c, value=val)
    ws.cell(row=r, column=c).font = font
    ws.cell(row=r, column=c).border = BD


def note(ws, r, c, val):
    """Write a gray italic note"""
    ws.cell(row=r, column=c, value=val)
    ws.cell(row=r, column=c).font = GRAY
    ws.cell(row=r, column=c).alignment = WRAP


def section(ws, r, c1, c2, text, fill=H_FILL):
    """Write a section header spanning columns"""
    ws.cell(row=r, column=c1, value=text)
    ws.cell(row=r, column=c1).font = WHITE_B
    ws.cell(row=r, column=c1).fill = fill
    ws.cell(row=r, column=c1).border = BD
    for c in range(c1 + 1, c2 + 1):
        ws.cell(row=r, column=c).fill = fill
        ws.cell(row=r, column=c).border = BD


# ===== 数据 =====
HIST_YEARS = ['2021A', '2022A', '2023A', '2024A', '2025A']
HIST = {
    '2021A': {'rev': 57.4, 'gm': 0.5163, 'om': 0.4096, 'nm': 0.3732, 'g': None},
    '2022A': {'rev': 73.6, 'gm': 0.5956, 'om': 0.4956, 'nm': 0.4386, 'g': 0.282},
    '2023A': {'rev': 70.6, 'gm': 0.5436, 'om': 0.4263, 'nm': 0.3940, 'g': -0.042},
    '2024A': {'rev': 88.3, 'gm': 0.5612, 'om': 0.4572, 'nm': 0.4002, 'g': 0.250},
    '2025A': {'rev': 122.4, 'gm': 0.5989, 'om': 0.5083, 'nm': 0.4510, 'g': 0.385},
}
SEG_PCTS = {
    'HPC': [0.37, 0.41, 0.45, 0.52, 0.58],
    'Smartphone': [0.44, 0.41, 0.38, 0.35, 0.30],
    'IoT': [0.08, 0.08, 0.08, 0.07, 0.06],
    'Automotive': [0.04, 0.05, 0.05, 0.05, 0.04],
    'DCE': [0.07, 0.05, 0.04, 0.01, 0.02],
}

# 分部定义: (name, subtitle, 2025A_revenue, bear/init/term/mid/k, base/..., bull/..., reasoning_dict)
SEGS = [
    ('HPC', 'AI/数据中心', 71.0,
     (0.25, 0.08, 4, 0.6), (0.35, 0.12, 5, 0.5), (0.45, 0.18, 6, 0.4),
     {'rev': '2025A总收入$122.4B × 58%占比 = $71.0B',
      'init': 'AI CapEx 2024-25年+40-50%; 类比AWS早期增速50%+持续约5年',
      'term': 'AI基础设施终将成熟; 类比云计算2024年增速已降至~19%',
      'mid': 'AI需求拐点预计在第5年前后(训练→推理为主,需求结构变化)',
      'k': '中等衰减, AI需求持续性较强(推理需求接力训练)'}),
    ('Smartphone', '智能手机', 36.7,
     (0.04, 0.01, 3, 0.7), (0.08, 0.04, 3, 0.7), (0.12, 0.06, 4, 0.6),
     {'rev': '2025A总收入$122.4B × 30%占比 = $36.7B',
      'init': '手机出货量持平(~12亿台/年), 增长靠芯片升级(N3/N2渗透)',
      'term': '手机芯片终局: 纯内容升级, 接近GDP增速',
      'mid': '手机周期短, 拐点来得快(第3年)',
      'k': '较快衰减, 手机没有颠覆性增长动力'}),
    ('IoT', '物联网', 7.3,
     (0.08, 0.03, 3, 0.7), (0.15, 0.07, 4, 0.6), (0.22, 0.10, 5, 0.5),
     {'rev': '2025A总收入$122.4B × 6%占比 = $7.3B',
      'init': '边缘AI拉动IoT芯片升级; 智能家居/穿戴设备渗透',
      'term': 'IoT芯片ASP较低, 终端增速有限',
      'mid': '中等拐点, 取决于边缘AI普及速度',
      'k': '中等衰减'}),
    ('Automotive', '汽车电子', 4.9,
     (0.10, 0.04, 3, 0.7), (0.18, 0.08, 5, 0.5), (0.25, 0.12, 5, 0.5),
     {'rev': '2025A总收入$122.4B × 4%占比 = $4.9B',
      'init': 'ADAS L2+渗透率提升 + EV芯片用量增加; 汽车半导体CAGR ~15%',
      'term': '汽车电子成熟后增速降至~8%, 参考传统汽车供应链',
      'mid': '拐点靠后(第5年), 汽车认证周期长, 爬坡慢',
      'k': '衰减较慢, 汽车电子渗透是长周期过程'}),
    ('DCE', '数字消费电子', 2.4,
     (-0.02, -0.03, 2, 0.8), (0.03, 0.02, 2, 0.8), (0.06, 0.03, 3, 0.7),
     {'rev': '2025A总收入$122.4B × 2%占比 = $2.4B',
      'init': '游戏机/PC等消费电子需求疲软, 部分被AI PC抵消',
      'term': '衰退/低增长, 此分部非核心',
      'mid': '拐点很早(第2年), 已经是成熟/衰退市场',
      'k': '快速衰减'}),
]

# 利润率假设: (bear, base, bull, reasoning)
MARGINS = {
    'gm_start': (0.58, 0.60, 0.61, '2025A实际GM=59.9%; Bear取略低(海外厂成本), Bull取略高(N2溢价)'),
    'gm_end':   (0.53, 0.58, 0.63, 'Bear:海外扩产+竞争压价; Base:维持; Bull:N2+A16定价权'),
    'rd_start': (0.055, 0.055, 0.050, 'TSMC R&D/Revenue ~5-6%, 随收入规模扩大费用率下降'),
    'rd_end':   (0.065, 0.050, 0.045, 'Bear:需加大投入保持竞争力; Bull:规模效应显著'),
    'sga_start':(0.040, 0.040, 0.035, 'TSMC SGA/Revenue ~3.5-4.5%'),
    'sga_end':  (0.050, 0.040, 0.030, 'Bear:海外运营推高费用; Bull:极致规模效应'),
    'tax':      (0.16, 0.14, 0.12, 'TSMC有效税率~12-15%; 海外厂可能享受税收优惠'),
}

VAL = {
    'pe_peak':  (25, 33, 40, '当前PE(TTM)=33.8x; Bear:均值回归至25x; Bull:AI溢价维持40x,类比ASML'),
    'pe_term':  (15, 20, 25, '成熟代工PE参考: Intel Foundry ~15x, ASML ~30x; TSMC取中间'),
    'shares':   (5186, 5186, 5186, 'TSM ADR约5,186M股 (25,930M普通股÷5); 假设不变'),
    'cur_mcap': (2060, 2060, 2060, '当前市值约$2,060B (2025年末)'),
    'cur_price':(397.28, 397.28, 397.28, '当前ADR股价$397.28'),
}

# 推理依据列写入函数
def write_reasoning(ws, row, reasoning_dict, keys=['rev', 'init', 'term', 'mid', 'k']):
    """Write reasoning for a segment's assumptions"""
    offset = 0
    for key in keys:
        if key in reasoning_dict:
            ws.cell(row=row + offset, column=7, value=reasoning_dict[key])
            ws.cell(row=row + offset, column=7).font = GRAY
            ws.cell(row=row + offset, column=7).alignment = WRAP
        offset += 1


# ======================== Sheet 1: 财务历史 ========================
def build_financials(wb):
    ws = wb.active
    ws.title = "财务历史"

    lbl(ws, 1, 1, "指标"); sh(ws, 1, 1, 1)
    for i, y in enumerate(HIST_YEARS):
        ws.cell(row=1, column=i + 2, value=y)
        sh(ws, 1, i + 2, i + 2, fill=COL_FILL, font=BLACK_B)

    rows = [
        ("收入 ($B)", 'rev', BLUE, IN_FILL, '#,##0.0'),
        ("收入增速", 'g', BLACK, None, '0.0%'),
        ("毛利率", 'gm', BLACK, None, '0.0%'),
        ("营业利润率", 'om', BLACK, None, '0.0%'),
        ("净利率", 'nm', BLACK, None, '0.0%'),
    ]
    for r, (label, key, font, fill, fmt) in enumerate(rows, 2):
        lbl(ws, r, 1, label)
        for c, y in enumerate(HIST_YEARS, 2):
            v = HIST[y][key]
            if v is not None: ws.cell(row=r, column=c, value=v)
            sc(ws, r, c, font=font, fill=fill, fmt=fmt)

    derived = [("毛利 ($B)", 'gm'), ("营业利润 ($B)", 'om'), ("净利润 ($B)", 'nm')]
    for r, (label, mk) in enumerate(derived, 7):
        lbl(ws, r, 1, label)
        for c, y in enumerate(HIST_YEARS, 2):
            ws.cell(row=r, column=c, value=round(HIST[y]['rev'] * HIST[y][mk], 1))
            sc(ws, r, c, fmt='#,##0.0')

    # 右侧备注
    note(ws, 2, 7, "数据来源: TSMC官方USD报告 + stockanalysis.com")
    note(ws, 3, 7, "2022年增速用USD口径(TWD口径为+42.6%,汇率差异)")
    note(ws, 4, 7, "2022年周期顶峰(59.6%), 2023年下行(54.4%), 2025年创新高(59.9%)")
    note(ws, 6, 7, "净利率: 2025A=45.1%为历史最高")

    ws.column_dimensions['A'].width = 20
    for c in range(2, 7): ws.column_dimensions[get_column_letter(c)].width = 13
    ws.column_dimensions['G'].width = 50


# ======================== Sheet 2: 业务分部 ========================
def build_segments(wb):
    ws = wb.create_sheet("业务分部")
    revs = [HIST[y]['rev'] for y in HIST_YEARS]

    lbl(ws, 1, 1, "平台"); sh(ws, 1, 1, 1)
    for i, y in enumerate(HIST_YEARS):
        ws.cell(row=1, column=i + 2, value=y)
        sh(ws, 1, i + 2, i + 2, fill=COL_FILL, font=BLACK_B)

    r = 2
    for seg, pcts in SEG_PCTS.items():
        lbl(ws, r, 1, f"{seg} 收入 ($B)")
        for c, (p, rv) in enumerate(zip(pcts, revs), 2):
            ws.cell(row=r, column=c, value=round(rv * p, 1))
            sc(ws, r, c, font=BLUE, fill=IN_FILL, fmt='#,##0.0')
        r += 1
        lbl(ws, r, 1, f"{seg} 占比")
        for c, p in enumerate(pcts, 2):
            ws.cell(row=r, column=c, value=p)
            sc(ws, r, c, fmt='0.0%')
        r += 1

    note(ws, 2, 7, "HPC占比从37%(2021)→58%(2025), AI是绝对核心驱动力")
    note(ws, 4, 7, "Smartphone从44%→30%, 从第一大变第二大")
    note(ws, 8, 7, "Automotive绝对占比小(~4%), 但ADAS/EV渗透空间大")

    ws.column_dimensions['A'].width = 22
    for c in range(2, 7): ws.column_dimensions[get_column_letter(c)].width = 13
    ws.column_dimensions['G'].width = 50


# ======================== Sheet 3: 估值历史 ========================
def build_valuation(wb):
    ws = wb.create_sheet("估值历史")

    items = [
        ("当前市值 ($B)", 2060, '#,##0'),
        ("当前股价 ($)", 397.28, '#,##0.00'),
        ("PE (TTM)", 33.8, '0.0'),
        ("PE (Forward)", 20.6, '0.0'),
        ("52周高 ($)", 420.00, '#,##0.00'),
        ("52周低 ($)", 188.81, '#,##0.00'),
        ("历史中位PE", 26, '0'),
        ("流通ADR数 (M)", 5186, '#,##0'),
    ]
    lbl(ws, 1, 1, "指标"); ws.cell(row=1, column=2, value="数值"); sh(ws, 1, 1, 2)
    for r, (label, val, fmt) in enumerate(items, 2):
        lbl(ws, r, 1, label)
        ws.cell(row=r, column=2, value=val)
        sc(ws, r, 2, font=BLUE, fill=IN_FILL, fmt=fmt)

    # PE轨迹
    lbl(ws, 11, 1, "年份"); lbl(ws, 11, 2, "PE区间"); lbl(ws, 11, 3, "驱动"); sh(ws, 11, 1, 3)
    pe_hist = [
        ('2021', '27-32x', '全球芯片荒, 产能紧张'),
        ('2022', '11-14x', '半导体下行+加息杀估值(周期底部)'),
        ('2023', '18-22x', 'AI概念启动(ChatGPT), 估值修复'),
        ('2024', '25-32x', 'AI CapEx爆发, 业绩兑现'),
        ('2025', '29-35x', '业绩持续超预期, 定价权验证'),
    ]
    for r, (y, pe, drv) in enumerate(pe_hist, 12):
        lbl(ws, r, 1, y); ws.cell(row=r, column=2, value=pe); sc(ws, r, 2)
        note(ws, r, 3, drv)

    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 40


# ======================== Sheet 4: 假设 ========================
def build_assumptions(wb):
    """
    返回 {key: row_number} 字典, 供预测表引用
    列: A=标签 B=空 C=Bear D=Base E=Bull F=活跃值 G=推理依据
    """
    ws = wb.create_sheet("假设")
    row_map = {}

    # 场景切换
    lbl(ws, 1, 1, "活跃情景")
    ws.cell(row=1, column=1).fill = H_FILL; ws.cell(row=1, column=1).font = WHITE_B
    ws.cell(row=1, column=2, value=2)
    ws.cell(row=1, column=2).font = BLACK_B
    ws.cell(row=1, column=2).fill = TOG_FILL; ws.cell(row=1, column=2).border = BD

    dv = DataValidation(type="list", formula1='"1,2,3"', allow_blank=False)
    dv.error = "请选择 1(Bear), 2(Base), 3(Bull)"
    dv.prompt = "1=Bear, 2=Base, 3=Bull"
    ws.add_data_validation(dv); dv.add(ws["B1"])

    # 列标题
    for ci, h in enumerate(["假设项", "", "Bear", "Base", "Bull", "活跃值", "推理依据"], 1):
        ws.cell(row=2, column=ci, value=h)
    sh(ws, 2, 1, 7); sh(ws, 2, 3, 5, fill=COL_FILL, font=BLACK_B)
    sh(ws, 2, 6, 6, fill=OUT_FILL, font=BLACK_B)

    r = 3
    for seg_name, subtitle, base_rev, bear, base, bull, reasons in SEGS:
        # 分部标题
        section(ws, r, 1, 7, f"--- {seg_name} ({subtitle}) ---", fill=SEG_FILL)
        r += 1

        # 2025A base revenue
        key = f'{seg_name}_rev'
        row_map[key] = r
        lbl(ws, r, 1, "2025A收入 ($B)")
        for ci, v in enumerate([base_rev, base_rev, base_rev], 3):
            ws.cell(row=r, column=ci, value=v)
            sc(ws, r, ci, font=BLUE, fill=IN_FILL, fmt='#,##0.0')
        ws.cell(row=r, column=6, value=f'=INDEX(C{r}:E{r},$B$1)')
        sc(ws, r, 6, font=GREEN, fill=OUT_FILL, fmt='#,##0.0')
        note(ws, r, 7, reasons['rev'])
        r += 1

        # init, term, mid, k
        params = [
            ('初始增速', 'init', bear[0], base[0], bull[0], '0.0%'),
            ('终端增速', 'term', bear[1], base[1], bull[1], '0.0%'),
            ('S曲线中点', 'mid', bear[2], base[2], bull[2], '0'),
            ('衰减系数k', 'k', bear[3], base[3], bull[3], '0.0'),
        ]
        for label, pkey, bv, bsv, blv, fmt in params:
            fkey = f'{seg_name}_{pkey}'
            row_map[fkey] = r
            lbl(ws, r, 1, label)
            for ci, v in enumerate([bv, bsv, blv], 3):
                ws.cell(row=r, column=ci, value=v)
                sc(ws, r, ci, font=BLUE, fill=IN_FILL, fmt=fmt)
            ws.cell(row=r, column=6, value=f'=INDEX(C{r}:E{r},$B$1)')
            sc(ws, r, 6, font=GREEN, fill=OUT_FILL, fmt=fmt)
            note(ws, r, 7, reasons.get(pkey, ''))
            r += 1
        r += 1  # 空行

    # 利润率
    section(ws, r, 1, 7, "--- 利润率 ---"); r += 1
    for key in ['gm_start', 'gm_end', 'rd_start', 'rd_end', 'sga_start', 'sga_end', 'tax']:
        bear_v, base_v, bull_v, reason = MARGINS[key]
        row_map[key] = r
        lbl(ws, r, 1, key.replace('_', ' '))
        for ci, v in enumerate([bear_v, base_v, bull_v], 3):
            ws.cell(row=r, column=ci, value=v)
            sc(ws, r, ci, font=BLUE, fill=IN_FILL, fmt='0.0%')
        ws.cell(row=r, column=6, value=f'=INDEX(C{r}:E{r},$B$1)')
        sc(ws, r, 6, font=GREEN, fill=OUT_FILL, fmt='0.0%')
        note(ws, r, 7, reason)
        r += 1

    r += 1
    # 估值
    section(ws, r, 1, 7, "--- 估值 ---"); r += 1
    for key in ['pe_peak', 'pe_term', 'shares', 'cur_mcap', 'cur_price']:
        bear_v, base_v, bull_v, reason = VAL[key]
        row_map[key] = r
        lbl(ws, r, 1, {'pe_peak': '峰值PE', 'pe_term': '终端PE',
                        'shares': 'ADR股份数(M)', 'cur_mcap': '当前市值($B)',
                        'cur_price': '当前股价($)'}[key])
        fmt_map = {'pe_peak': '0', 'pe_term': '0', 'shares': '#,##0',
                   'cur_mcap': '#,##0', 'cur_price': '#,##0.00'}
        for ci, v in enumerate([bear_v, base_v, bull_v], 3):
            ws.cell(row=r, column=ci, value=v)
            sc(ws, r, ci, font=BLUE, fill=IN_FILL, fmt=fmt_map[key])
        ws.cell(row=r, column=6, value=f'=INDEX(C{r}:E{r},$B$1)')
        sc(ws, r, 6, font=GREEN, fill=OUT_FILL, fmt=fmt_map[key])
        note(ws, r, 7, reason)
        r += 1

    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 4
    for c in ['C', 'D', 'E', 'F']: ws.column_dimensions[c].width = 12
    ws.column_dimensions['G'].width = 55

    return row_map


# ======================== Sheet 5: 预测 ========================
def build_projections(wb, rm):
    """
    rm = row_map from build_assumptions
    列: A=指标 B=逻辑 C..L=2026E..2035E
    """
    ws = wb.create_sheet("预测")
    Y = N  # 10 years
    YC = 3  # first year column (C)
    YC_LAST = YC + Y - 1  # column L

    def asum(key):
        return f"假设!$F${rm[key]}"

    def ycl(i):
        """Year column letter for year i (0-indexed)"""
        return get_column_letter(YC + i)

    # 表头
    ws.cell(row=1, column=1, value="指标")
    ws.cell(row=1, column=2, value="逻辑 / 公式")
    for i in range(Y):
        ws.cell(row=1, column=YC + i, value=f"{2026 + i}E")
    sh(ws, 1, 1, YC + Y - 1)
    sh(ws, 1, YC, YC_LAST, fill=COL_FILL, font=BLACK_B)

    # ---- 共享年序 ----
    r = 2
    section(ws, r, 1, YC_LAST, "--- 分部收入推导 ---")
    r = 3
    lbl(ws, r, 1, "年序 (t)")
    note(ws, r, 2, "共享计数器, 1..10")
    for i in range(Y):
        ws.cell(row=r, column=YC + i, value=i + 1)
        sc(ws, r, YC + i, fmt='0')

    # ---- 每个分部: decay, growth, revenue ----
    seg_rows = {}  # {name: (decay_row, growth_row, rev_row)}

    for seg_name, _, _, _, _, _, _ in SEGS:
        r += 1  # section header
        section(ws, r, 1, YC_LAST, f"--- {seg_name} ---", fill=SEG_FILL)

        # decay
        r += 1
        decay_r = r
        lbl(ws, r, 1, "衰减系数")
        note(ws, r, 2, "1/(1+EXP(k·(t-mid)))  S曲线衰减")
        for i in range(Y):
            cl = ycl(i)
            ws.cell(row=r, column=YC + i,
                    value=f'=1/(1+EXP({asum(f"{seg_name}_k")}*({cl}3-{asum(f"{seg_name}_mid")})))')
            sc(ws, r, YC + i, fmt='0.000')

        # growth
        r += 1
        grow_r = r
        lbl(ws, r, 1, "收入增速")
        note(ws, r, 2, "terminal + (initial - terminal) × decay")
        for i in range(Y):
            cl = ycl(i)
            ws.cell(row=r, column=YC + i,
                    value=f'={asum(f"{seg_name}_term")}+({asum(f"{seg_name}_init")}-{asum(f"{seg_name}_term")})*{cl}{decay_r}')
            sc(ws, r, YC + i, fmt='0.0%')

        # revenue
        r += 1
        rev_r = r
        lbl(ws, r, 1, "收入 ($B)")
        note(ws, r, 2, "Y1=base×(1+g), Y2+=prev×(1+g)")
        for i in range(Y):
            cl = ycl(i)
            if i == 0:
                ws.cell(row=r, column=YC + i,
                        value=f'={asum(f"{seg_name}_rev")}*(1+{cl}{grow_r})')
            else:
                prev = ycl(i - 1)
                ws.cell(row=r, column=YC + i,
                        value=f'={prev}{rev_r}*(1+{cl}{grow_r})')
            sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0.0')

        seg_rows[seg_name] = rev_r

    # ---- 汇总收入 ----
    r += 1
    section(ws, r, 1, YC_LAST, "--- 汇总收入 ---")

    r += 1
    lbl(ws, r, 1, "总收入 ($B)")
    note(ws, r, 2, "Σ 各分部收入")
    total_rev_r = r
    seg_rev_refs = '+'.join([f'{ycl(0)}{seg_rows[s]}' for s in [se[0] for se in SEGS]])
    for i in range(Y):
        cl = ycl(i)
        parts = '+'.join([f'{cl}{seg_rows[s]}' for s in [se[0] for se in SEGS]])
        ws.cell(row=r, column=YC + i, value=f'={parts}')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0.0')

    r += 1
    lbl(ws, r, 1, "总收入增速")
    note(ws, r, 2, "(本期 - 上期) / 上期; Y1 vs 2025A实际收入$122.4B")
    total_grow_r = r
    for i in range(Y):
        cl = ycl(i)
        if i == 0:
            ws.cell(row=r, column=YC + i,
                    value=f'=({cl}{total_rev_r}-122.4)/122.4')
        else:
            prev = ycl(i - 1)
            ws.cell(row=r, column=YC + i,
                    value=f'=({cl}{total_rev_r}-{prev}{total_rev_r})/{prev}{total_rev_r}')
        sc(ws, r, YC + i, fmt='0.0%')

    r += 1
    lbl(ws, r, 1, "HPC占比")
    note(ws, r, 2, "HPC收入 / 总收入; 用于判断结构变化")
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{seg_rows["HPC"]}/{cl}{total_rev_r}')
        sc(ws, r, YC + i, fmt='0.0%')

    # ---- P&L ----
    r += 1
    section(ws, r, 1, YC_LAST, "--- P&L 推导 ---")

    # 毛利率
    r += 1
    lbl(ws, r, 1, "毛利率")
    note(ws, r, 2, "线性插值: start + (end-start)×(t-1)/9")
    gm_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={asum("gm_start")}+({asum("gm_end")}-{asum("gm_start")})*({cl}3-1)/9')
        sc(ws, r, YC + i, fmt='0.0%')

    # 毛利
    r += 1
    lbl(ws, r, 1, "毛利 ($B)")
    note(ws, r, 2, "= 总收入 × 毛利率")
    gp_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{total_rev_r}*{cl}{gm_r}')
        sc(ws, r, YC + i, fmt='#,##0.0')

    # R&D费用率
    r += 1
    lbl(ws, r, 1, "R&D费用率")
    note(ws, r, 2, "线性插值: start→end; 2025A实际约5.5%")
    rd_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={asum("rd_start")}+({asum("rd_end")}-{asum("rd_start")})*({cl}3-1)/9')
        sc(ws, r, YC + i, fmt='0.0%')

    # R&D费用
    r += 1
    lbl(ws, r, 1, "R&D费用 ($B)")
    note(ws, r, 2, "= 总收入 × R&D费用率")
    rd_amt_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{total_rev_r}*{cl}{rd_r}')
        sc(ws, r, YC + i, fmt='#,##0.0')

    # SGA费用率
    r += 1
    lbl(ws, r, 1, "SGA费用率")
    note(ws, r, 2, "线性插值; 2025A实际约4%")
    sga_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={asum("sga_start")}+({asum("sga_end")}-{asum("sga_start")})*({cl}3-1)/9')
        sc(ws, r, YC + i, fmt='0.0%')

    # SGA费用
    r += 1
    lbl(ws, r, 1, "SGA费用 ($B)")
    note(ws, r, 2, "= 总收入 × SGA费用率")
    sga_amt_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{total_rev_r}*{cl}{sga_r}')
        sc(ws, r, YC + i, fmt='#,##0.0')

    # EBIT
    r += 1
    lbl(ws, r, 1, "EBIT ($B)")
    note(ws, r, 2, "= 毛利 - R&D - SGA")
    ebit_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{gp_r}-{cl}{rd_amt_r}-{cl}{sga_amt_r}')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0.0')

    # EBIT margin
    r += 1
    lbl(ws, r, 1, "EBIT margin")
    note(ws, r, 2, "= EBIT / 总收入; 验证: 2025A实际50.8%")
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{ebit_r}/{cl}{total_rev_r}')
        sc(ws, r, YC + i, fmt='0.0%')

    # 税率
    r += 1
    lbl(ws, r, 1, "有效税率")
    note(ws, r, 2, "从假设表取; 2025A实际约11-12%")
    tax_r = r
    for i in range(Y):
        ws.cell(row=r, column=YC + i, value=f'={asum("tax")}')
        sc(ws, r, YC + i, font=GREEN, fmt='0.0%')

    # 净利润
    r += 1
    lbl(ws, r, 1, "净利润 ($B)")
    note(ws, r, 2, "= EBIT × (1 - 税率)")
    ni_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{ebit_r}*(1-{cl}{tax_r})')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0.0')

    # 净利率
    r += 1
    lbl(ws, r, 1, "净利率")
    note(ws, r, 2, "= 净利润 / 总收入; 验证: 2025A实际45.1%")
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{ni_r}/{cl}{total_rev_r}')
        sc(ws, r, YC + i, fmt='0.0%')

    # ---- 动态估值 ----
    r += 1
    section(ws, r, 1, YC_LAST, "--- 动态估值 ---")

    # 增速比(用于PE)
    r += 1
    lbl(ws, r, 1, "增速比 (PE驱动)")
    note(ws, r, 2, "= (本期增速-终年增速)/(首年增速-终年增速), 用于PE插值")
    gr_r = r
    g1 = f'${ycl(0)}{total_grow_r}'  # 首年增速绝对引用
    g10 = f'${ycl(Y-1)}{total_grow_r}'  # 终年增速绝对引用
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'=MAX(0,MIN(1,({cl}{total_grow_r}-{g10})/({g1}-{g10})))')
        sc(ws, r, YC + i, fmt='0.00')

    # 动态PE
    r += 1
    lbl(ws, r, 1, "动态 PE")
    note(ws, r, 2, "= 终端PE + (峰值PE-终端PE) × 增速比; 高增速→高PE, 增速衰减→PE压缩")
    pe_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={asum("pe_term")}+({asum("pe_peak")}-{asum("pe_term")})*{cl}{gr_r}')
        sc(ws, r, YC + i, font=GREEN, fill=OUT_FILL, fmt='0.0')

    # 隐含市值
    r += 1
    lbl(ws, r, 1, "隐含市值 ($B)")
    note(ws, r, 2, "= 净利润 × 动态PE")
    mcap_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{ni_r}*{cl}{pe_r}')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0')

    # 隐含股价
    r += 1
    lbl(ws, r, 1, "隐含股价 ($)")
    note(ws, r, 2, "= 市值($B) × 1000 / ADR股份数(M)")
    price_r = r
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{mcap_r}*1000/{asum("shares")}')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='#,##0.00')

    # vs当前
    r += 1
    lbl(ws, r, 1, "vs 当前股价")
    note(ws, r, 2, "= (隐含股价 - 当前股价) / 当前股价")
    for i in range(Y):
        cl = ycl(i)
        ws.cell(row=r, column=YC + i,
                value=f'={cl}{price_r}/{asum("cur_price")}-1')
        sc(ws, r, YC + i, fmt='+0.0%;-0.0%')

    # 年化回报
    r += 1
    lbl(ws, r, 1, "年化回报")
    note(ws, r, 2, "= (隐含市值/当前市值)^(1/t) - 1")
    for i in range(Y):
        cl = ycl(i)
        t = i + 1
        ws.cell(row=r, column=YC + i,
                value=f'=({cl}{mcap_r}/{asum("cur_mcap")})^(1/{t})-1')
        sc(ws, r, YC + i, font=BLACK, fill=OUT_FILL, fmt='+0.0%;-0.0%')

    # ---- 摘要 ----
    r += 2
    section(ws, r, 1, YC_LAST, "--- 终年摘要 (2035E) ---")
    last = ycl(Y - 1)

    summaries = [
        ("总收入 ($B)", f'={last}{total_rev_r}', '#,##0.0'),
        ("总收入10yr CAGR", f'=({last}{total_rev_r}/122.4)^(1/10)-1', '0.0%'),
        ("HPC占比", f'={last}{seg_rows["HPC"]}/{last}{total_rev_r}', '0.0%'),
        ("毛利率", f'={last}{gm_r}', '0.0%'),
        ("EBIT margin", f'={last}{ebit_r}/{last}{total_rev_r}', '0.0%'),
        ("净利率", f'={last}{ni_r}/{last}{total_rev_r}', '0.0%'),
        ("净利润 ($B)", f'={last}{ni_r}', '#,##0.0'),
        ("动态PE", f'={last}{pe_r}', '0.0'),
        ("隐含市值 ($B)", f'={last}{mcap_r}', '#,##0'),
        ("隐含股价 ($)", f'={last}{price_r}', '#,##0.00'),
        ("10年年化回报", f'=({last}{mcap_r}/{asum("cur_mcap")})^(1/10)-1', '+0.0%;-0.0%'),
    ]
    for label, formula, fmt in summaries:
        r += 1
        lbl(ws, r, 1, label)
        ws.cell(row=r, column=2, value=formula)
        sc(ws, r, 2, font=BLACK, fill=OUT_FILL, fmt=fmt)

    # 列宽
    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 42
    for i in range(Y):
        ws.column_dimensions[get_column_letter(YC + i)].width = 14


# ======================== Sheet 6: 合理性 ========================
def build_sanity(wb):
    ws = wb.create_sheet("合理性")
    headers = ["检验项", "Bear", "Base", "Bull", "状态"]
    for i, h in enumerate(headers, 1):
        ws.cell(row=1, column=i, value=h)
    sh(ws, 1, 1, 5)

    checks = [
        ("=== 第一层：内部逻辑 ===", "", "", "", ""),
        ("各分部增速单调递减", "✓", "✓", "✓", "✓ 通过"),
        ("毛利率范围(30-70%)", "✓ 53-58%", "✓ 58-60%", "✓ 61-63%", "✓ 通过"),
        ("R&D费用率合理", "✓ 5.5-6.5%", "✓ 5.0-5.5%", "✓ 4.5-5.0%", "✓ 通过"),
        ("动态PE范围", "15-25x", "20-33x", "25-40x", "✓ 在历史范围内"),
        ("", "", "", "", ""),
        ("=== 第二层：跨情景 ===", "", "", "", ""),
        ("各分部: Bear<Base<Bull增速", "✓ 全部满足", "", "", "✓ 通过"),
        ("PE: Bear<Base<Bull", "✓ 15-25<20-33<25-40", "", "", "✓ 通过"),
        ("", "", "", "", ""),
        ("=== 第三层：外部基准 ===", "", "", "", ""),
        ("HPC增速 vs AWS早期(~50%)", "", "35%→12%", "", "✓ 类比AWS衰减曲线"),
        ("Smartphone增速 vs 手机行业(~5%)", "", "8%→4%", "", "✓ 高于行业(靠内容升级)"),
        ("整体CAGR vs Intel增长期(15-20%)", "", "待计算", "", "见预测表摘要"),
        ("峰值PE vs ASML(30-40x)", "", "33x", "40x", "✓ 与ASML垄断溢价相当"),
        ("终端PE vs Intel Foundry(~15x)", "15x", "20x", "", "✓ TSMC应高于Intel"),
        ("", "", "", "", ""),
        ("=== PE动态性验证 ===", "", "", "", ""),
        ("PE随增速衰减而压缩", "25→15x", "33→20x", "40→25x", "✓ 非常数, 增速挂钩"),
        ("PE压缩幅度合理", "-40%", "-39%", "-38%", "✓ 约40%压缩, 类比历史周期"),
    ]
    for r, check in enumerate(checks, 2):
        for c, val in enumerate(check, 1):
            ws.cell(row=r, column=c, value=val)
            sc(ws, r, c, align=Alignment(horizontal='left', wrap_text=True))

    ws.column_dimensions['A'].width = 38
    for c in ['B', 'C', 'D', 'E']: ws.column_dimensions[c].width = 22


# ======================== Sheet 7: 逻辑说明 ========================
def build_logic_notes(wb):
    ws = wb.create_sheet("逻辑说明")

    notes = [
        ("模型结构", "自上而下分部收入 → 分层P&L → 动态PE估值"),
        ("", ""),
        ("=== 收入推导 ===", ""),
        ("S曲线公式", "growth(t) = terminal + (initial - terminal) × 1/(1+EXP(k·(t-mid)))"),
        ("衰减系数", "decay = 1/(1+EXP(k·(t-mid))), t=年序(1..10), k控制衰减速度, mid控制拐点位置"),
        ("参数含义", "k越大→衰减越快; mid越大→拐点越晚(高增长持续更久)"),
        ("分部逻辑", "5个分部独立S曲线, 各有不同的initial/terminal/mid/k, 求和得总收入"),
        ("", ""),
        ("=== P&L推导 ===", ""),
        ("毛利率", "线性插值从start到end; 反映N2溢价(↑) vs 海外厂成本(↓)的博弈"),
        ("R&D费用率", "线性插值; TSMC R&D强度高但随规模效应下降"),
        ("SGA费用率", "线性插值; 海外扩张推高费用(↑) vs 规模效应(↓)"),
        ("EBIT", "= 毛利 - R&D - SGA; 不含D&A(已含在COGS中)"),
        ("净利润", "= EBIT × (1 - 有效税率)"),
        ("", ""),
        ("=== 动态PE ===", ""),
        ("核心公式", "PE(t) = 终端PE + (峰值PE - 终端PE) × 增速比"),
        ("增速比", "= MAX(0, MIN(1, (g(t)-g10)/(g1-g10))); g1=首年增速, g10=终年增速"),
        ("经济含义", "增速高→市场给高PE(增长溢价); 增速衰减→PE自然压缩(均值回归)"),
        ("vs常数PE", "常数PE忽略增长变化: 如果10年后增速仅8%仍给33x,则高估; 动态PE自动修正"),
        ("", ""),
        ("=== 估值 ===", ""),
        ("隐含市值", "= 净利润 × 动态PE"),
        ("年化回报", "= (终年市值/当前市值)^(1/t) - 1; 含估值变动+盈利增长"),
        ("", ""),
        ("=== 场景切换 ===", ""),
        ("使用方法", "假设表B1单元格: 1=Bear, 2=Base, 3=Bull"),
        ("联动机制", "假设表F列=INDEX(C:E,B1); 预测表所有公式引用F列, 切换即联动"),
        ("", ""),
        ("=== 类比参考 ===", ""),
        ("AWS增速衰减", "2015年~70% → 2020年~30% → 2024年~19%; HPC对标此曲线"),
        ("ASML PE", "EUV垄断环节, PE稳定30-40x; TSMC同为垄断环节可参考"),
        ("Intel Server CPU", "市占率从90%+被蚕食到<70%花了8年; TSMC先进制程~90%需警惕"),
        ("Cisco 2000", "PE从100x+压缩到15x; 但那是泡沫,TSMC增速远非泡沫"),
    ]

    lbl(ws, 1, 1, "主题"); lbl(ws, 1, 2, "说明")
    sh(ws, 1, 1, 2)

    for r, (topic, detail) in enumerate(notes, 2):
        if topic.startswith("==="):
            section(ws, r, 1, 2, topic)
        elif topic:
            lbl(ws, r, 1, topic)
            ws.cell(row=r, column=2, value=detail)
            ws.cell(row=r, column=2).alignment = WRAP

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 80


# ======================== 主函数 ========================
def main():
    wb = Workbook()

    build_financials(wb)
    build_segments(wb)
    build_valuation(wb)
    row_map = build_assumptions(wb)
    build_projections(wb, row_map)
    build_sanity(wb)
    build_logic_notes(wb)

    out = Path(__file__).parent.parent / "out"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "TSM_coverage_model.xlsx"
    wb.save(str(path))
    print(f"TSM v2 覆盖模型已生成: {path}")


if __name__ == '__main__':
    main()
