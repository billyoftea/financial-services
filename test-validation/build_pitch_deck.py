"""
CyberShield Technologies Pitch Deck - PowerPoint Generator
使用 python-pptx 创建投资银行Pitch Book
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# 颜色定义
DARK_BLUE = RGBColor(0x00, 0x2B, 0x5C)      # 深蓝 - 主色
MEDIUM_BLUE = RGBColor(0x00, 0x4E, 0x8C)     # 中蓝 - 副色
LIGHT_BLUE = RGBColor(0x00, 0x7B, 0xC0)      # 浅蓝 - 强调
ACCENT_ORANGE = RGBColor(0xE6, 0x7E, 0x22)   # 橙色 - 点缀
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
MED_GRAY = RGBColor(0x99, 0x99, 0x99)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_footer(slide, sources="", notes=""):
    """添加页脚来源栏"""
    footer = slide.shapes.add_textbox(
        Inches(0.5), Inches(6.8), Inches(12.3), Inches(0.5)
    )
    tf = footer.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.font.size = Pt(8)
    p.font.italic = True
    p.font.color.rgb = MED_GRAY
    if sources:
        run = p.add_run()
        run.text = sources
    if notes:
        p2 = tf.add_paragraph()
        p2.font.size = Pt(8)
        p2.font.italic = True
        p2.font.color.rgb = MED_GRAY
        run2 = p2.add_run()
        run2.text = notes

def add_title_bar(slide, title_text, subtitle_text=""):
    """添加标题栏"""
    # 深蓝背景条
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

    # 标题文字
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12), Inches(0.7))
    tf = title.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title_text
    run.font.size = Pt(32)
    run.font.bold = True
    run.font.color.rgb = WHITE

    if subtitle_text:
        sub = slide.shapes.add_textbox(Inches(0.5), Inches(0.75), Inches(12), Inches(0.4))
        tf2 = sub.text_frame
        p2 = tf2.paragraphs[0]
        run2 = p2.add_run()
        run2.text = subtitle_text
        run2.font.size = Pt(16)
        run2.font.color.rgb = RGBColor(0xCC, 0xDD, 0xEE)

def add_table(slide, data, left, top, width, height, col_widths=None):
    """添加格式化表格"""
    rows = len(data)
    cols = len(data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    for row_idx, row_data in enumerate(data):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(cell_text)

            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(10)
                if row_idx == 0:  # Header row
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
                    paragraph.font.size = Pt(10)
                elif "中位数" in str(cell_text) or "平均值" in str(cell_text) or "共识" in str(cell_text):
                    paragraph.font.bold = True
                    paragraph.font.size = Pt(10)
                else:
                    paragraph.font.color.rgb = DARK_GRAY

                # 数字列右对齐
                if col_idx > 0 and row_idx > 0:
                    try:
                        float(str(cell_text).replace('$','').replace('B','').replace('x','').replace('~','').replace(',',''))
                        paragraph.alignment = PP_ALIGN.CENTER
                    except:
                        pass

            # Header row background
            if row_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
            elif row_idx == len(data) - 1 and ("中位数" in str(row_data[0]) or "共识" in str(row_data[0])):
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xE8, 0xEE, 0xF4)
            elif row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY

    return table


# =============================================
# Slide 1: 封面页
# =============================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

# 全幅深蓝背景
bg = slide1.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
)
bg.fill.solid()
bg.fill.fore_color.rgb = DARK_BLUE
bg.line.fill.background()

# 分隔线
line = slide1.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1), Inches(2.8), Inches(2), Inches(0.05)
)
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_ORANGE
line.line.fill.background()

# 主标题
title_box = slide1.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(1.3))
tf = title_box.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "CyberShield Technologies"
run.font.size = Pt(44)
run.font.bold = True
run.font.color.rgb = WHITE

# 副标题
sub_box = slide1.shapes.add_textbox(Inches(1), Inches(3.0), Inches(11), Inches(1.5))
tf2 = sub_box.text_frame
p2 = tf2.paragraphs[0]
run2 = p2.add_run()
run2.text = "战略选择评估"
run2.font.size = Pt(28)
run2.font.color.rgb = WHITE

p3 = tf2.add_paragraph()
run3 = p3.add_run()
run3.text = "机密卖方顾问Pitch Book"
run3.font.size = Pt(18)
run3.font.color.rgb = RGBColor(0xCC, 0xDD, 0xEE)

# 底部信息
bottom = slide1.shapes.add_textbox(Inches(1), Inches(5.5), Inches(11), Inches(1.5))
tf3 = bottom.text_frame
p4 = tf3.paragraphs[0]
run4 = p4.add_run()
run4.text = "Sterling Capital Advisors"
run4.font.size = Pt(16)
run4.font.bold = True
run4.font.color.rgb = ACCENT_ORANGE

p5 = tf3.add_paragraph()
run5 = p5.add_run()
run5.text = "2026年5月  |  严格保密"
run5.font.size = Pt(12)
run5.font.color.rgb = RGBColor(0x99, 0xAA, 0xBB)


# =============================================
# Slide 2: 目录
# =============================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide2, "目  录")

toc_items = [
    ("01", "行业概览 — 市场定义"),
    ("02", "行业概览 — 市场规模与增长（TAM）"),
    ("03", "可比上市公司分析"),
    ("04", "可比M&A交易分析"),
    ("05", "卖方流程概述"),
    ("06", "初步估值范围分析"),
    ("07", "为什么选择 Sterling Capital"),
]

y_start = 1.6
for i, (num, title) in enumerate(toc_items):
    # 编号
    num_box = slide2.shapes.add_textbox(Inches(1), Inches(y_start + i * 0.7), Inches(0.6), Inches(0.5))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    run_num = p_num.add_run()
    run_num.text = num
    run_num.font.size = Pt(20)
    run_num.font.bold = True
    run_num.font.color.rgb = ACCENT_ORANGE

    # 标题
    title_box = slide2.shapes.add_textbox(Inches(1.8), Inches(y_start + i * 0.7), Inches(8), Inches(0.5))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    run_title = p_title.add_run()
    run_title.text = title
    run_title.font.size = Pt(16)
    run_title.font.color.rgb = DARK_GRAY


# =============================================
# Slide 3: 市场定义
# =============================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide3, "行业概览 — 市场定义", "全球网络安全行业")

# 定义文本
def_box = slide3.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(12.3), Inches(0.6))
tf = def_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
run = p.add_run()
run.text = "定义：全球网络安全行业涵盖为保护企业IT基础设施、云环境、端点设备、网络通信及数据资产免受网络威胁而提供的软件、硬件及服务解决方案。"
run.font.size = Pt(11)
run.font.color.rgb = DARK_GRAY

# 包含范围 - 左侧
inc_label = slide3.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(5.8), Inches(0.4))
tf = inc_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "市场范围 — 包含"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

inc_items = [
    "云安全（Cloud Security）— Wiz, PANW, CrowdStrike",
    "端点安全（Endpoint Security）— CrowdStrike, SentinelOne",
    "网络安全（Network Security）— Fortinet, PANW, Cisco",
    "身份与访问管理（IAM）— CyberArk, Okta",
    "安全运营（SecOps）— Splunk, PANW, IBM",
    "数据安全（Data Security）— Varonis, Rubrik",
]

inc_box = slide3.shapes.add_textbox(Inches(0.5), Inches(2.7), Inches(5.8), Inches(3.5))
tf = inc_box.text_frame
tf.word_wrap = True
for i, item in enumerate(inc_items):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = item
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(4)

# 不包含范围 - 右侧
exc_label = slide3.shapes.add_textbox(Inches(6.8), Inches(2.2), Inches(5.8), Inches(0.4))
tf = exc_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "市场范围 — 不包含"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

exc_items = [
    "消费级安全软件（面向个人用户）",
    "IT基础设施硬件（非安全类）",
    "纯IT服务/外包（非安全相关）",
]

exc_box = slide3.shapes.add_textbox(Inches(6.8), Inches(2.7), Inches(5.8), Inches(3.5))
tf = exc_box.text_frame
tf.word_wrap = True
for i, item in enumerate(exc_items):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = item
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(4)

add_footer(slide3,
    "Sources: MarketsandMarkets (2025), Mordor Intelligence (2025), Gartner (2025).",
    "Notes: (1) 市场定义基于Gartner、IDC等主要研究机构的方法论；(2) 细分市场划分参照MarketsandMarkets网络安全报告框架。"
)


# =============================================
# Slide 4: 市场规模与增长 (TAM)
# =============================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide4, "行业概览 — 市场规模与增长", "全球网络安全市场 TAM 分析")

# 关键指标卡片
metrics = [
    ("2025年市场规模", "~$228B"),
    ("2030年预测", "~$352B"),
    ("共识CAGR", "9-12%"),
    ("2025年M&A总额", "$84-102B"),
]

for i, (label, value) in enumerate(metrics):
    x = 0.5 + i * 3.2
    card = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(2.8), Inches(1.0)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0xE8, 0xEE, 0xF4)
    card.line.color.rgb = MEDIUM_BLUE
    card.line.width = Pt(1)

    val_box = slide4.shapes.add_textbox(Inches(x + 0.1), Inches(1.55), Inches(2.6), Inches(0.5))
    tf = val_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = value
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = DARK_BLUE

    lbl_box = slide4.shapes.add_textbox(Inches(x + 0.1), Inches(2.0), Inches(2.6), Inches(0.4))
    tf2 = lbl_box.text_frame
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = label
    run2.font.size = Pt(10)
    run2.font.color.rgb = MED_GRAY

# 数据表格
tam_data = [
    ["来源", "基准年规模", "CAGR", "目标年预测"],
    ["MarketsandMarkets", "$228B (2025)", "9.1%", "$352B (2030)"],
    ["Mordor Intelligence", "$236B (2025)", "12.3%", "$264B (2026)"],
    ["Fortune Business Insights", "$248B (2026)", "13.8%", "$699B (2034)"],
    ["Grand View Research", "$210B (2024E)", "11.9%", "$663B (2033)"],
    ["BCC Research", "$208B (2023)", "11.6%", "$397B (2029)"],
    ["共识（范围）", "$228-248B", "9-14%", "$352-663B"],
]

add_table(slide4, tam_data,
    Inches(0.5), Inches(2.8), Inches(8), Inches(3.2),
    col_widths=[Inches(2.5), Inches(1.8), Inches(1.2), Inches(2.5)]
)

# 增长驱动因素 - 右侧
driver_label = slide4.shapes.add_textbox(Inches(9), Inches(2.8), Inches(4), Inches(0.4))
tf = driver_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "关键增长驱动因素"
run.font.size = Pt(13)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

drivers = [
    "AI驱动的网络威胁升级",
    "云迁移加速（CAGR ~16%）",
    "全球监管合规要求收紧",
    "零信任架构广泛采用",
    "远程/混合办公常态化",
]

driver_box = slide4.shapes.add_textbox(Inches(9), Inches(3.3), Inches(4), Inches(2.5))
tf = driver_box.text_frame
tf.word_wrap = True
for i, d in enumerate(drivers):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = d
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(6)

add_footer(slide4,
    "Sources: MarketsandMarkets (2025), Fortune Business Insights (2026), Mordor Intelligence (2026), Grand View Research (2025), BCC Research (2024).",
    "Notes: (1) 各机构市场定义和统计口径略有差异；(2) 共识范围为全数据源最小-最大区间。"
)


# =============================================
# Slide 5: 可比公司分析
# =============================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide5, "可比上市公司分析", "网络安全行业可比公司估值")

comps_data = [
    ["公司", "代码", "市值", "EV", "收入", "收入增速", "EBITDA利润率", "EV/Revenue", "EV/EBITDA"],
    ["Palo Alto Networks", "PANW", "$168.6B", "$164.0B", "$9.2B", "+15%", "~22%", "16.6x", "74.2x"],
    ["CrowdStrike", "CRWD", "$111.5B", "$111.0B", "$5.0B", "+30%", "~3%", "22.2x", "N/A"],
    ["Fortinet", "FTNT", "$80.0B", "$78.0B", "$6.6B", "+16%", "~36%", "11.8x", "26.9x"],
    ["中位数", "", "", "", "", "+16%", "~22%", "16.6x", "50.6x"],
]

add_table(slide5, comps_data,
    Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.5),
    col_widths=[Inches(2.2), Inches(0.8), Inches(1.3), Inches(1.3), Inches(1.1), Inches(1.1), Inches(1.5), Inches(1.5), Inches(1.5)]
)

# 定位分析
pos_label = slide5.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(6), Inches(0.4))
tf = pos_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "CyberShield 相对定位"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

pos_items = [
    "收入增速 ~25%，显著高于行业中位数 +16%",
    "聚焦云安全 + 零信任两个最高增速赛道",
    "EBITDA利润率 ~20%，与行业中位数持平",
    "较小收入规模需考虑规模折价，但高增速可部分抵消",
]

pos_box = slide5.shapes.add_textbox(Inches(0.5), Inches(4.7), Inches(6), Inches(2.0))
tf = pos_box.text_frame
tf.word_wrap = True
for i, item in enumerate(pos_items):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = item
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(4)

add_footer(slide5,
    "Sources: Yahoo Finance (2026年5月), GuruFocus (2026年5月), ValueInvesting.io (2026年5月), 各公司年报/10-Q.",
    "Notes: (1) 收入为最近完整财年数据；(2) CRWD EBITDA利润率受SBC影响较大；(3) EV/EBITDA对CRWD不具参考性。"
)


# =============================================
# Slide 6: 可比M&A交易分析
# =============================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide6, "可比M&A交易分析", "2024-2025年网络安全行业重大交易")

ma_data = [
    ["日期", "收购方", "标的", "交易价值", "标的收入/ARR", "EV/Revenue", "EV/EBITDA"],
    ["2025年3月", "Google/Alphabet", "Wiz", "$32.0B", "~$600M ARR", "~53x", "N/M"],
    ["2025年", "Palo Alto Networks", "CyberArk", "$25.0B", "~$800M", "~31x", "~130x"],
    ["2024-2025年", "HPE", "Juniper Networks", "$14.0B", "~$5.6B", "~2.5x", "~14x"],
    ["2024年", "Thoma Bravo", "Darktrace", "$5.3B", "~$750M", "~7.1x", "~30x"],
    ["中位数", "", "", "", "", "~19x", "~30x"],
]

add_table(slide6, ma_data,
    Inches(0.5), Inches(1.5), Inches(12.3), Inches(3.0),
    col_widths=[Inches(1.3), Inches(2.0), Inches(2.0), Inches(1.5), Inches(1.8), Inches(1.5), Inches(1.5)]
)

# 交易洞察
insight_label = slide6.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(6), Inches(0.4))
tf = insight_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "关键交易洞察"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

insights = [
    "2025年网络安全M&A创纪录，总交易额 $84-102B",
    "大型战略收购（Google/Wiz）享有显著溢价（EV/Rev 53x）",
    "PE收购倍数更为理性（Darktrace 7.1x）",
    "CyberShield作为中端标的，估值应参考PE交易倍数+增长溢价",
]

insight_box = slide6.shapes.add_textbox(Inches(0.5), Inches(5.3), Inches(12), Inches(1.5))
tf = insight_box.text_frame
tf.word_wrap = True
for i, item in enumerate(insights):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = item
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(4)

add_footer(slide6,
    "Sources: Momentum Cyber (2025), SecurityWeek (2025), InfoSecurity Magazine (2025), Forbes (2026), TechCrunch (2025).",
    "Notes: (1) Wiz为Pre-profit公司，EV/EBITDA不具意义；(2) CyberArk收入和EBITDA为估计值；(3) HPE/Juniper含硬件业务，倍数偏低。"
)


# =============================================
# Slide 7: 卖方流程概述
# =============================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide7, "卖方流程概述", "推荐交易流程与时间线")

phases = [
    ("阶段1", "准备与定位", "第1-4周", [
        "深入尽职调查与材料准备",
        "CIM撰写与财务模型优化",
        "买家画像分析与分级",
    ]),
    ("阶段2", "市场推广", "第5-10周", [
        "定向接触潜在买家",
        "NDA管理与CIM分发",
        "收集第一轮意向函（IOI）",
    ]),
    ("阶段3", "深度尽职调查", "第11-16周", [
        "数据室管理与协调",
        "收集最终报价函（FO）",
        "核心条款谈判支持",
    ]),
    ("阶段4", "交割执行", "第17-20周", [
        "SPA/合并协议审核",
        "监管审批支持",
        "交割与资金结算",
    ]),
]

for i, (phase, name, timeline, items) in enumerate(phases):
    x = 0.5 + i * 3.15

    # 阶段编号和名称
    phase_box = slide7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(2.8), Inches(0.6)
    )
    phase_box.fill.solid()
    phase_box.fill.fore_color.rgb = DARK_BLUE if i < 3 else ACCENT_ORANGE
    phase_box.line.fill.background()

    ptf = phase_box.text_frame
    ptf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    prun = ptf.paragraphs[0].add_run()
    prun.text = f"{phase}: {name}"
    prun.font.size = Pt(12)
    prun.font.bold = True
    prun.font.color.rgb = WHITE

    # 时间线
    tl_box = slide7.shapes.add_textbox(Inches(x), Inches(2.2), Inches(2.8), Inches(0.3))
    tf = tl_box.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = timeline
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = ACCENT_ORANGE

    # 活动列表
    act_box = slide7.shapes.add_textbox(Inches(x + 0.1), Inches(2.6), Inches(2.6), Inches(2.0))
    tf = act_box.text_frame
    tf.word_wrap = True
    for j, item in enumerate(items):
        if j == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = item
        run.font.size = Pt(10)
        run.font.color.rgb = DARK_GRAY
        p.space_after = Pt(6)

    # 箭头（除最后一个阶段外）
    if i < 3:
        arrow = slide7.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.85), Inches(1.6), Inches(0.3), Inches(0.4)
        )
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = ACCENT_ORANGE
        arrow.line.fill.background()

# 总时间线
total_box = slide7.shapes.add_textbox(Inches(0.5), Inches(5.0), Inches(12), Inches(0.6))
tf = total_box.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "预计总时间线：约4-5个月"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

add_footer(slide7,
    "注：若涉及大型战略买家，需考虑额外的监管审批时间（如反垄断/CFIUS审查）。",
    ""
)


# =============================================
# Slide 8: 初步估值范围
# =============================================
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide8, "初步估值范围分析", "CyberShield Technologies 指示性估值")

# 估值矩阵
val_data = [
    ["估值方法", "关键假设", "低端", "高端"],
    ["可比公司（EV/Revenue）", "16.0x - 25.0x x $800M", "$12.8B", "$20.0B"],
    ["可比交易（EV/Revenue）", "10.0x - 18.0x x $800M", "$8.0B", "$14.4B"],
    ["可比交易（EV/EBITDA）", "20.0x - 30.0x x $160M", "$3.2B", "$4.8B"],
    ["DCF（WACC 11%）", "5年预测, 终值15x EBITDA", "$10.0B", "$16.0B"],
]

add_table(slide8, val_data,
    Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.5),
    col_widths=[Inches(3.0), Inches(4.0), Inches(2.5), Inches(2.5)]
)

# 综合估值范围 - 高亮显示
summary_box = slide8.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2), Inches(4.3), Inches(9), Inches(1.5)
)
summary_box.fill.solid()
summary_box.fill.fore_color.rgb = RGBColor(0xE8, 0xEE, 0xF4)
summary_box.line.color.rgb = DARK_BLUE
summary_box.line.width = Pt(2)

sum_title = slide8.shapes.add_textbox(Inches(2.3), Inches(4.4), Inches(8.5), Inches(0.4))
tf = sum_title.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "综合估值范围"
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

sum_val = slide8.shapes.add_textbox(Inches(2.3), Inches(4.9), Inches(8.5), Inches(0.5))
tf2 = sum_val.text_frame
p2 = tf2.paragraphs[0]
p2.alignment = PP_ALIGN.CENTER
run2 = p2.add_run()
run2.text = "$8.0B — $16.0B（中值 ~$12.0B）"
run2.font.size = Pt(24)
run2.font.bold = True
run2.font.color.rgb = ACCENT_ORANGE

sum_detail = slide8.shapes.add_textbox(Inches(2.3), Inches(5.4), Inches(8.5), Inches(0.3))
tf3 = sum_detail.text_frame
p3 = tf3.paragraphs[0]
p3.alignment = PP_ALIGN.CENTER
run3 = p3.add_run()
run3.text = "隐含 EV/Revenue: 10.0x - 20.0x  |  隐含 EV/EBITDA: 50x - 100x"
run3.font.size = Pt(11)
run3.font.color.rgb = MED_GRAY

add_footer(slide8,
    "Sources: Yahoo Finance (2026年5月), Momentum Cyber (2025), MarketsandMarkets (2025).",
    "Notes: (1) 以上为初步指示性估值，仅供讨论之用；(2) 最终估值将根据详细尽职调查和当时市场条件确定。"
)


# =============================================
# Slide 9: 为什么选择我们
# =============================================
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide9, "为什么选择 Sterling Capital", "专业能力与差异化优势")

# 左侧 - 核心优势
adv_label = slide9.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(6), Inches(0.4))
tf = adv_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "核心差异化优势"
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

advantages = [
    ("行业专注", "100%聚焦科技/网络安全，非综合投行的一般性覆盖"),
    ("买家网络", "与所有主要战略买家和顶级PE保持活跃对话"),
    ("执行能力", "从CIM撰写到交割完成的全流程执行经验"),
    ("估值专长", "深入理解网络安全行业特有估值逻辑"),
    ("团队友好", "注重保护管理层利益，协助实现平稳过渡"),
]

for i, (title, desc) in enumerate(advantages):
    y = 2.1 + i * 0.7

    num_box = slide9.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(y), Inches(0.4), Inches(0.4)
    )
    num_box.fill.solid()
    num_box.fill.fore_color.rgb = ACCENT_ORANGE
    num_box.line.fill.background()
    ntf = num_box.text_frame
    ntf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ntf.vertical_anchor = MSO_ANCHOR.MIDDLE
    nrun = ntf.paragraphs[0].add_run()
    nrun.text = str(i+1)
    nrun.font.size = Pt(12)
    nrun.font.bold = True
    nrun.font.color.rgb = WHITE

    adv_box = slide9.shapes.add_textbox(Inches(1.1), Inches(y), Inches(5.5), Inches(0.6))
    tf = adv_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = DARK_BLUE
    run2 = p.add_run()
    run2.text = f" — {desc}"
    run2.font.size = Pt(11)
    run2.font.color.rgb = DARK_GRAY

# 右侧 - 代表交易
deal_label = slide9.shapes.add_textbox(Inches(7), Inches(1.5), Inches(6), Inches(0.4))
tf = deal_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "最近代表交易"
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

deal_data = [
    ["年份", "交易", "角色", "价值"],
    ["2025", "云安全公司SaaS合并", "卖方顾问", "$3.2B"],
    ["2025", "零信任方案提供商出售予PE", "卖方顾问", "$1.8B"],
    ["2024", "端点安全公司战略出售", "卖方顾问", "$5.1B"],
    ["2024", "IAM公司PE重组", "财务顾问", "$2.4B"],
]

add_table(slide9, deal_data,
    Inches(7), Inches(2.0), Inches(5.8), Inches(2.5),
    col_widths=[Inches(0.8), Inches(2.5), Inches(1.2), Inches(1.3)]
)

# 关键数据
stats_label = slide9.shapes.add_textbox(Inches(7), Inches(4.8), Inches(5.8), Inches(0.4))
tf = stats_label.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "行业覆盖数据"
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

stats = [
    "2024-2025年完成 12+ 网络安全行业交易",
    "累计交易总额超过 $45B（网络安全领域）",
    "与全球 50+ 家网络安全企业建立长期关系",
]

stats_box = slide9.shapes.add_textbox(Inches(7), Inches(5.3), Inches(5.8), Inches(1.3))
tf = stats_box.text_frame
tf.word_wrap = True
for i, s in enumerate(stats):
    if i == 0:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    run = p.add_run()
    run.text = s
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    p.space_after = Pt(6)

add_footer(slide9,
    "注：代表交易信息仅用于说明团队经验，不构成对未来交易结果的保证。",
    ""
)


# =============================================
# 保存文件
# =============================================
output_path = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\IB_pitch_deck_output.pptx"
prs.save(output_path)
print(f"Pitch Deck 已保存到: {output_path}")
print(f"共 {len(prs.slides)} 页幻灯片")
