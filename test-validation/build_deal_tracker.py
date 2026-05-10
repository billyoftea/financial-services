"""
Deal Tracker Excel 生成脚本
生成包含管线总览、里程碑追踪、行动事项清单的工作簿
数据来源：2022-2026年真实M&A交易公开信息
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

wb = Workbook()

# ===== 样式定义 =====
HEADER_FONT = Font(name='Microsoft YaHei', bold=True, size=11, color='FFFFFF')
HEADER_FILL = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
SUBHEADER_FILL = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
COMPLETE_FILL = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
AT_RISK_FILL = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
IN_PROGRESS_FILL = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
TITLE_FONT = Font(name='Microsoft YaHei', bold=True, size=14, color='2F5496')
SECTION_FONT = Font(name='Microsoft YaHei', bold=True, size=12, color='2F5496')
NORMAL_FONT = Font(name='Microsoft YaHei', size=10)
BOLD_FONT = Font(name='Microsoft YaHei', bold=True, size=10)
THIN_BORDER = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
CENTER_ALIGN = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT_ALIGN = Alignment(horizontal='left', vertical='center', wrap_text=True)


def apply_header_style(ws, row, cols):
    """应用表头样式"""
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER_ALIGN
        cell.border = THIN_BORDER


def apply_data_style(ws, row, cols):
    """应用数据行样式"""
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = NORMAL_FONT
        cell.alignment = LEFT_ALIGN
        cell.border = THIN_BORDER


def auto_width(ws, cols, min_w=12, max_w=40):
    """自动调整列宽"""
    for col in range(1, cols + 1):
        max_len = min_w
        for row in ws.iter_rows(min_col=col, max_col=col, values_only=False):
            for cell in row:
                if cell.value:
                    # 中文按2字符宽度计算
                    val = str(cell.value)
                    length = sum(2 if ord(c) > 127 else 1 for c in val)
                    max_len = max(max_len, min(length + 4, max_w))
        ws.column_dimensions[get_column_letter(col)].width = max_len


# =====================================================================
# Tab 1: 管线总览 (Pipeline Overview)
# =====================================================================
ws1 = wb.active
ws1.title = "管线总览"

# 标题
ws1.merge_cells('A1:K1')
ws1['A1'] = '交易管线总览 — Deal Pipeline Overview'
ws1['A1'].font = TITLE_FONT
ws1['A1'].alignment = Alignment(horizontal='center', vertical='center')

ws1.merge_cells('A2:K2')
ws1['A2'] = f'生成日期：2026年5月10日 | 管线总规模：~$128B | 已完成交易：3笔'
ws1['A2'].font = Font(name='Microsoft YaHei', size=10, italic=True, color='666666')
ws1['A2'].alignment = Alignment(horizontal='center')

# 表头
headers = ['交易代号', '收购方', '目标公司', '交易类型', '交易规模($B)',
           '对价结构', '阶段', '状态', '宣布日期', '完成日期', '总历时(月)']
row = 4
for col, h in enumerate(headers, 1):
    ws1.cell(row=row, column=col, value=h)
apply_header_style(ws1, row, len(headers))

# 数据
deals = [
    ['Project Bridge', 'Broadcom (AVGO)', 'VMware (VMW)', 'Buy-side', '$61B',
     '现金+股票', 'Close', '已完成', '2022-05-26', '2023-11-22', '18'],
    ['Project Symphony', 'Synopsys (SNPS)', 'Ansys (ANSS)', 'Buy-side', '$35B',
     '现金+股票', 'Close', '已完成', '2024-01-16', '2025-07-17', '18'],
    ['Project Guardian', 'Alphabet/Google', 'Wiz, Inc.', 'Buy-side', '$32B',
     '100%现金', 'Close', '已完成', '2025-03-18', '2026-03-11', '12'],
]

for i, deal in enumerate(deals):
    r = row + 1 + i
    for col, val in enumerate(deal, 1):
        ws1.cell(row=r, column=col, value=val)
    apply_data_style(ws1, r, len(headers))
    # 已完成行用绿色底色
    for col in range(1, len(headers) + 1):
        ws1.cell(row=r, column=col).fill = COMPLETE_FILL

# 汇总区域
summary_row = row + len(deals) + 2
ws1.cell(row=summary_row, column=1, value='管线汇总').font = SECTION_FONT
summaries = [
    ['活跃交易', 0],
    ['已完成交易', 3],
    ['管线总金额', '~$128B'],
    ['本季度预期交割', 0],
    ['有风险交易', 0],
]
for i, (label, val) in enumerate(summaries):
    r = summary_row + 1 + i
    ws1.cell(row=r, column=1, value=label).font = BOLD_FONT
    ws1.cell(row=r, column=2, value=val).font = NORMAL_FONT
    ws1.cell(row=r, column=1).border = THIN_BORDER
    ws1.cell(row=r, column=2).border = THIN_BORDER

auto_width(ws1, len(headers))

# =====================================================================
# Tab 2: 里程碑追踪 (Milestone Tracking)
# =====================================================================
ws2 = wb.create_sheet("里程碑追踪")

ws2.merge_cells('A1:F1')
ws2['A1'] = '里程碑追踪 — Milestone Tracking'
ws2['A1'].font = TITLE_FONT
ws2['A1'].alignment = Alignment(horizontal='center')

# --- Project Bridge ---
r = 3
ws2.merge_cells(f'A{r}:F{r}')
ws2.cell(row=r, column=1, value='Project Bridge — Broadcom收购VMware (~$61B)').font = SECTION_FONT
r += 1
milestone_headers = ['里程碑', '目标日期', '实际日期', '状态', '备注']
for col, h in enumerate(milestone_headers, 1):
    ws2.cell(row=r, column=col, value=h)
apply_header_style(ws2, r, len(milestone_headers))

bridge_milestones = [
    ['签署最终协议', '2022-05', '2022-05-26', '已完成', '现金+股票交易，~$61B'],
    ['股东投票权登记日', '2022-Q3', '2022-09-30', '已完成', 'VMware股东投票权登记'],
    ['HSR等待期届满（美国）', '2022-Q3', '2022-Q3', '已完成', 'FTC未采取行动'],
    ['EU Phase II调查启动', '-', '2022-12-20', '延迟', 'EU委员会启动深度调查'],
    ['UK CMA批准', '2023-Q2', '2023-07-12', '已完成', '无条件批准'],
    ['EU批准（有条件）', '2023-Q2', '2023-07-19', '延迟完成', '需行为性救济措施'],
    ['中国SAMR批准', '2023-Q3', '2023-08', '已完成', '附条件批准'],
    ['交易交割完成', '2023-Q4', '2023-11-22', '已完成', 'VMware退市'],
    ['协同效应实现（3年目标）', '2026-11', '进行中', '进行中', '目标：$8.5B EBITDA增量'],
]

for i, ms in enumerate(bridge_milestones):
    rr = r + 1 + i
    for col, val in enumerate(ms, 1):
        ws2.cell(row=rr, column=col, value=val)
    apply_data_style(ws2, rr, len(milestone_headers))
    # 状态列颜色
    status_cell = ws2.cell(row=rr, column=4)
    if '完成' in str(ms[3]) or ms[3] == '已完成':
        status_cell.fill = COMPLETE_FILL
    elif '延迟' in str(ms[3]):
        status_cell.fill = AT_RISK_FILL
    elif ms[3] == '进行中':
        status_cell.fill = IN_PROGRESS_FILL

# --- Project Symphony ---
r = r + len(bridge_milestones) + 2
ws2.merge_cells(f'A{r}:F{r}')
ws2.cell(row=r, column=1, value='Project Symphony — Synopsys收购Ansys (~$35B)').font = SECTION_FONT
r += 1
for col, h in enumerate(milestone_headers, 1):
    ws2.cell(row=r, column=col, value=h)
apply_header_style(ws2, r, len(milestone_headers))

symphony_milestones = [
    ['签署最终协议', '2024-01', '2024-01-16', '已完成', '现金+股票，~$35B'],
    ['Ansys股东批准', '2024-Q2', '2024-05-22', '已完成', '股东大会投票通过'],
    ['EU反垄断审查（报道）', '2024-Q4', '2024-12-23', '已完成', 'Reuters报道EU将附条件批准'],
    ['EU正式批准（Phase 1）', '2025-Q1', '2025-01-10', '已完成', 'Phase 1即获批准，附条件（需剥离软件资产）'],
    ['UK CMA批准', '2025-Q1', '2025-03-05', '已完成', '无条件批准'],
    ['EU批准剥离资产买方', '2025-Q2', '2025-05-23', '已完成', '剥离资产买方获EU单独批准'],
    ['中国SAMR批准', '2025-Q3', '2025-07-14', '已完成', '最后重大监管障碍'],
    ['交易交割完成', '2025-H1', '2025-07-17', '已完成', '设计与仿真软件行业史上最大并购'],
]

for i, ms in enumerate(symphony_milestones):
    rr = r + 1 + i
    for col, val in enumerate(ms, 1):
        ws2.cell(row=rr, column=col, value=val)
    apply_data_style(ws2, rr, len(milestone_headers))
    ws2.cell(row=rr, column=4).fill = COMPLETE_FILL

# --- Project Guardian ---
r = r + len(symphony_milestones) + 2
ws2.merge_cells(f'A{r}:F{r}')
ws2.cell(row=r, column=1, value='Project Guardian — Alphabet/Google收购Wiz ($32B)').font = SECTION_FONT
r += 1
for col, h in enumerate(milestone_headers, 1):
    ws2.cell(row=r, column=col, value=h)
apply_header_style(ws2, r, len(milestone_headers))

guardian_milestones = [
    ['首次接触', '2024-Q2', '2024-06', '已完成', 'Google首次接触Wiz，Wiz倾向IPO'],
    ['谈判重启', '2025-Q1', '2025-01', '已完成', '特朗普就职后谈判加速'],
    ['签署最终协议', '2025-Q1', '2025-03-18', '已完成', '全现金交易，$32B'],
    ['监管分手费协议', '2025-03', '2025-03', '已完成', '$3.2B分手费（如监管否决）'],
    ['美国DOJ批准', '2025-Q4', '2025-11', '已完成', 'DOJ提前结束审查，无条件批准'],
    ['EU无条件批准', '2026-Q1', '2026-02-10', '已完成', 'EU无条件批准'],
    ['其他地区审批', '2026-Q1', '2026-02/03', '已完成', '以色列、UK、澳洲'],
    ['交易交割完成', '2026-Q1', '2026-03-11', '已完成', 'Google史上最大收购完成'],
    ['集成启动', '2026-Q2', '2026-03', '进行中', 'Wiz整合进Google Cloud'],
]

for i, ms in enumerate(guardian_milestones):
    rr = r + 1 + i
    for col, val in enumerate(ms, 1):
        ws2.cell(row=rr, column=col, value=val)
    apply_data_style(ws2, rr, len(milestone_headers))
    status_cell = ws2.cell(row=rr, column=4)
    if ms[3] == '已完成':
        status_cell.fill = COMPLETE_FILL
    elif ms[3] == '进行中':
        status_cell.fill = IN_PROGRESS_FILL

auto_width(ws2, len(milestone_headers))

# =====================================================================
# Tab 3: 行动事项清单 (Action Items)
# =====================================================================
ws3 = wb.create_sheet("行动事项清单")

ws3.merge_cells('A1:G1')
ws3['A1'] = '行动事项清单 — Action Items'
ws3['A1'].font = TITLE_FONT
ws3['A1'].alignment = Alignment(horizontal='center')

# 已归档区域
r = 3
ws3.cell(row=r, column=1, value='已归档行动事项（历史记录）').font = SECTION_FONT
r += 1
action_headers = ['#', '行动事项', '关联交易', '负责人', '截止日期', '优先级', '状态']
for col, h in enumerate(action_headers, 1):
    ws3.cell(row=r, column=col, value=h)
apply_header_style(ws3, r, len(action_headers))

archived_actions = [
    [1, '准备Broadcom-VMware交易交割文件', 'Project Bridge', 'Legal Team', '2023-11-15', 'P0', '已完成'],
    [2, '跟进EU对VMware交易的Phase II调查进展', 'Project Bridge', 'VP / Associate', '2023-06', 'P1', '已完成'],
    [3, '协调中国SAMR对VMware交易的审批策略', 'Project Bridge', 'MD / Legal', '2023-08', 'P0', '已完成'],
    [4, '准备Synopsys-Ansys交易股东沟通材料', 'Project Symphony', 'Analyst', '2024-05', 'P1', '已完成'],
    [5, '跟进EU对Ansys交易的剥离资产买方审批', 'Project Symphony', 'VP', '2025-05', 'P0', '已完成'],
    [6, '跟进中国SAMR对Ansys交易的审批进度', 'Project Symphony', 'MD / Legal', '2025-07', 'P0', '已完成'],
    [7, '准备Google-Wiz交易的HSR申报文件', 'Project Guardian', 'Legal / Analyst', '2025-04', 'P0', '已完成'],
    [8, '监控EU对Wiz交易的反垄断审查进展', 'Project Guardian', 'VP / Legal', '2026-01', 'P0', '已完成'],
    [9, '协调Wiz交易的全球多地区审批', 'Project Guardian', 'MD / Legal', '2026-02', 'P0', '已完成'],
]

for i, action in enumerate(archived_actions):
    rr = r + 1 + i
    for col, val in enumerate(action, 1):
        ws3.cell(row=rr, column=col, value=val)
    apply_data_style(ws3, rr, len(action_headers))
    for col in range(1, len(action_headers) + 1):
        ws3.cell(row=rr, column=col).fill = COMPLETE_FILL

# 活跃行动事项
r = r + len(archived_actions) + 2
ws3.cell(row=r, column=1, value='当前活跃行动事项').font = SECTION_FONT
r += 1
for col, h in enumerate(action_headers, 1):
    ws3.cell(row=r, column=col, value=h)
apply_header_style(ws3, r, len(action_headers))

active_actions = [
    [10, '跟踪Broadcom-VMware协同效应实现进度（$8.5B EBITDA目标）', 'Project Bridge', 'VP / Analyst', '2026-11', 'P1', '进行中'],
    [11, '监控Wiz与Google Cloud集成进展', 'Project Guardian', 'Associate', '2026-Q2', 'P2', '进行中'],
    [12, '准备已关闭交易的收费确认和发票', '全部', 'Analyst', '2026-05-15', 'P1', '进行中'],
    [13, '归档已关闭交易的全部文档', '全部', 'Analyst', '2026-05-31', 'P2', '待启动'],
]

for i, action in enumerate(active_actions):
    rr = r + 1 + i
    for col, val in enumerate(action, 1):
        ws3.cell(row=rr, column=col, value=val)
    apply_data_style(ws3, rr, len(action_headers))
    status_cell = ws3.cell(row=rr, column=7)
    if action[6] == '进行中':
        status_cell.fill = IN_PROGRESS_FILL
    elif action[6] == '待启动':
        status_cell.fill = PatternFill(start_color='BDD7EE', end_color='BDD7EE', fill_type='solid')

auto_width(ws3, len(action_headers))

# =====================================================================
# Tab 4: 每周评审 (Weekly Review)
# =====================================================================
ws4 = wb.create_sheet("每周评审")

ws4.merge_cells('A1:E1')
ws4['A1'] = '每周交易评审 — Weekly Deal Review'
ws4['A1'].font = TITLE_FONT
ws4['A1'].alignment = Alignment(horizontal='center')

ws4.merge_cells('A2:E2')
ws4['A2'] = '评审日期：2026年5月10日'
ws4['A2'].font = Font(name='Microsoft YaHei', size=10, italic=True, color='666666')
ws4['A2'].alignment = Alignment(horizontal='center')

r = 4
review_headers = ['交易', '一行状态', '本周关键进展', '未来两周里程碑', '风险/障碍']
for col, h in enumerate(review_headers, 1):
    ws4.cell(row=r, column=col, value=h)
apply_header_style(ws4, r, len(review_headers))

reviews = [
    ['Project Bridge\n(Broadcom/VMware)',
     '已于2023-11-22完成交割，处于整合后期',
     '继续跟踪协同效应实现情况',
     '无（交易已关闭）',
     '协同效应$8.5B EBITDA目标实现进度需持续监控，2026年11月为3年期限'],
    ['Project Symphony\n(Synopsys/Ansys)',
     '已于2025-07-17完成交割，集成进展顺利',
     '已完成全部监管流程和交易文件归档',
     '无（交易已关闭）',
     'EU要求的资产剥离已全部完成，无遗留风险'],
    ['Project Guardian\n(Google/Wiz)',
     '已于2026-03-11完成交割，Wiz整合进Google Cloud中',
     'Wiz产品保持多云兼容性，Google Cloud安全能力增强',
     '集成进度检查（2026年5月底）',
     '集成中的人才保留风险、多云兼容性承诺执行'],
]

for i, rev in enumerate(reviews):
    rr = r + 1 + i
    for col, val in enumerate(rev, 1):
        ws4.cell(row=rr, column=col, value=val)
    apply_data_style(ws4, rr, len(review_headers))
    ws4.cell(row=rr, column=1).font = BOLD_FONT
    ws4.row_dimensions[rr].height = 60

# 管线汇总
r = r + len(reviews) + 2
ws4.cell(row=r, column=1, value='管线汇总').font = SECTION_FONT
r += 1
summary_headers2 = ['指标', '数值']
for col, h in enumerate(summary_headers2, 1):
    ws4.cell(row=r, column=col, value=h)
apply_header_style(ws4, r, 2)

pipeline_summary = [
    ['活跃交易', 0],
    ['已完成交易', 3],
    ['管线总金额', '~$128B'],
    ['本季度预期交割', 0],
    ['有风险交易', 0],
    ['新mandate / Pitch', '待确认'],
    ['归档进度', '进行中'],
]

for i, (label, val) in enumerate(pipeline_summary):
    rr = r + 1 + i
    ws4.cell(row=rr, column=1, value=label)
    ws4.cell(row=rr, column=2, value=val)
    apply_data_style(ws4, rr, 2)

# 关键风险提示
r = r + len(pipeline_summary) + 2
ws4.cell(row=r, column=1, value='关键风险提示').font = SECTION_FONT
risks = [
    '1. Project Bridge协同效应风险：$8.5B EBITDA增量目标需在2026年11月前验证',
    '2. Project Guardian集成风险：Wiz独立品牌定位与Google Cloud整合可能存在张力',
    '3. 行业趋势：大型科技并购监管环境变化，需关注FTC/DOJ政策走向',
]
for i, risk in enumerate(risks):
    rr = r + 1 + i
    ws4.merge_cells(f'A{rr}:E{rr}')
    ws4.cell(row=rr, column=1, value=risk).font = NORMAL_FONT
    ws4.cell(row=rr, column=1).fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')

auto_width(ws4, len(review_headers), min_w=15, max_w=50)

# =====================================================================
# Tab 5: 顾问信息 (Advisors)
# =====================================================================
ws5 = wb.create_sheet("顾问信息")

ws5.merge_cells('A1:E1')
ws5['A1'] = '交易顾问信息 — Deal Advisors'
ws5['A1'].font = TITLE_FONT
ws5['A1'].alignment = Alignment(horizontal='center')

r = 3
advisor_headers = ['交易', '收购方财务顾问', '目标方财务顾问', '收购方法律顾问', '目标方法律顾问']
for col, h in enumerate(advisor_headers, 1):
    ws5.cell(row=r, column=col, value=h)
apply_header_style(ws5, r, len(advisor_headers))

advisors = [
    ['Project Bridge', 'BofA Securities等', 'Goldman Sachs, JPMorgan',
     'Wachtell Lipton, O\'Melveny, Cleary Gottlieb', 'Gibson Dunn'],
    ['Project Symphony', 'Evercore（独家）', '[未公开]',
     'Goodwin Procter等', '[未公开]'],
    ['Project Guardian', 'BofA Securities', '[未公开]',
     'Freshfields, Cleary Gottlieb', 'Fenwick & West, Cravath'],
]

for i, adv in enumerate(advisors):
    rr = r + 1 + i
    for col, val in enumerate(adv, 1):
        ws5.cell(row=rr, column=col, value=val)
    apply_data_style(ws5, rr, len(advisor_headers))

auto_width(ws5, len(advisor_headers), min_w=15, max_w=45)

# =====================================================================
# 保存文件
# =====================================================================
output_path = r'C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\IB_deal_tracker_real_output.xlsx'
wb.save(output_path)
print(f"Excel文件已保存到：{output_path}")
print(f"包含 {len(wb.sheetnames)} 个工作表：{', '.join(wb.sheetnames)}")
