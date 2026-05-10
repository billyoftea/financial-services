"""
云计算基础设施行业竞争格局分析 PPTX 生成脚本
AWS vs Azure vs Google Cloud
使用真实财务数据
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData
import os

# ── 颜色方案 ──────────────────────────────────────────
NAVY      = RGBColor(0x1B, 0x2A, 0x4A)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MED_GRAY  = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY= RGBColor(0xCC, 0xCC, 0xCC)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT1   = RGBColor(0xE8, 0x6C, 0x00)   # 橙色强调
ACCENT2   = RGBColor(0x2E, 0x75, 0xB6)   # 蓝色
ACCENT3   = RGBColor(0x00, 0xA6, 0x5A)   # 绿色

AWS_COLOR   = RGBColor(0xFF, 0x99, 0x00)
AZURE_COLOR = RGBColor(0x00, 0x89, 0xD6)
GCP_COLOR   = RGBColor(0x42, 0x85, 0xF4)

BG_LIGHT   = RGBColor(0xF5, 0xF5, 0xF5)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

# ── 工具函数 ──────────────────────────────────────────
def add_blank_slide():
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)

def set_slide_bg(slide, color=BG_LIGHT):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=14,
                bold=False, color=DARK_GRAY, alignment=PP_ALIGN.LEFT,
                font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_multi_text(slide, left, top, width, height, lines, default_size=14,
                   default_color=DARK_GRAY, line_spacing=1.15):
    """lines: list of (text, size, bold, color)"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(lines):
        text, sz, bld, clr = item
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(sz)
        p.font.bold = bld
        p.font.color.rgb = clr
        p.font.name = 'Calibri'
        p.space_after = Pt(4)
    return txBox

def add_source_line(slide, text, top=None):
    if top is None:
        top = H - Inches(0.45)
    add_textbox(slide, Inches(0.5), top, Inches(12), Inches(0.35),
                text, font_size=10, color=MED_GRAY)

def add_slide_title(slide, title, subtitle=None):
    """标题栏 + 可选副标题"""
    # 标题背景条
    shape = slide.shapes.add_shape(
        1, Inches(0), Inches(0), W, Inches(1.0))  # MSO_SHAPE.RECTANGLE
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()

    add_textbox(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.65),
                title, font_size=28, bold=True, color=WHITE)

    if subtitle:
        add_textbox(slide, Inches(0.5), Inches(0.75), Inches(12), Inches(0.3),
                    subtitle, font_size=14, color=RGBColor(0xBB, 0xCC, 0xDD))

def add_table(slide, left, top, width, height, headers, rows,
              header_color=NAVY, col_widths=None):
    """创建标准表格"""
    n_rows = len(rows) + 1
    n_cols = len(headers)
    table_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    table = table_shape.table

    # 列宽
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    # 表头
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = 'Calibri'
            p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_color
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    # 数据行
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = DARK_GRAY
                p.font.name = 'Calibri'
                if c == 0:
                    p.alignment = PP_ALIGN.LEFT
                else:
                    p.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF0, 0xF0, 0xF0)

    return table_shape

def add_kpi_box(slide, left, top, width, height, label, value, color=NAVY):
    """KPI卡片"""
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = LIGHT_GRAY
    shape.line.width = Pt(1)
    shape.shadow.inherit = False

    # 标签
    add_textbox(slide, left + Inches(0.1), top + Inches(0.05),
                width - Inches(0.2), Inches(0.3),
                label, font_size=11, color=MED_GRAY)
    # 数值
    add_textbox(slide, left + Inches(0.1), top + Inches(0.3),
                width - Inches(0.2), Inches(0.5),
                value, font_size=22, bold=True, color=color)

# ══════════════════════════════════════════════════════
# Slide 1: 封面
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide, NAVY)

add_textbox(slide, Inches(1), Inches(1.8), Inches(11), Inches(1.2),
            "云计算基础设施行业竞争格局分析",
            font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1), Inches(3.2), Inches(11), Inches(0.6),
            "AWS  vs  Azure  vs  Google Cloud",
            font_size=24, bold=False, color=ACCENT1, alignment=PP_ALIGN.CENTER)

# 三色横条
for i, (clr, name) in enumerate([(AWS_COLOR, "AWS"), (AZURE_COLOR, "Azure"), (GCP_COLOR, "GCP")]):
    x = Inches(3.5) + Inches(i * 2.2)
    shape = slide.shapes.add_shape(1, x, Inches(4.1), Inches(1.8), Inches(0.12))
    shape.fill.solid()
    shape.fill.fore_color.rgb = clr
    shape.line.fill.background()
    add_textbox(slide, x, Inches(4.3), Inches(1.8), Inches(0.4),
                name, font_size=14, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1), Inches(5.5), Inches(11), Inches(0.4),
            "分析日期：2026年5月10日  |  数据截止：FY2025 / Q1 CY2025  |  投资专业版",
            font_size=14, color=RGBColor(0xAA, 0xBB, 0xCC), alignment=PP_ALIGN.CENTER)

add_source_line(slide, "数据来源：Amazon IR FY2025, Microsoft IR FY25 Q3, Alphabet IR Q1 2026, Synergy Research (2025.11)")

# ══════════════════════════════════════════════════════
# Slide 2: 市场概况
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "全球云市场突破4,000亿美元，AI成为核心增长引擎")

# KPI卡片
add_kpi_box(slide, Inches(0.5), Inches(1.3), Inches(2.8), Inches(0.9),
            "2025年市场规模", "~$4,190亿", NAVY)
add_kpi_box(slide, Inches(3.5), Inches(1.3), Inches(2.8), Inches(0.9),
            "YoY增长率", "~20-22%", ACCENT3)
add_kpi_box(slide, Inches(6.5), Inches(1.3), Inches(2.8), Inches(0.9),
            "三巨头合计份额", "63%", ACCENT1)
add_kpi_box(slide, Inches(9.5), Inches(1.3), Inches(2.8), Inches(0.9),
            "预计2027年规模", "~$5,500-6,000亿", NAVY)

# 市场份额饼图
chart_data = CategoryChartData()
chart_data.categories = ['AWS', 'Azure', 'GCP', '其他']
chart_data.add_series('市场份额', (30, 20, 13, 37))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.PIE, Inches(0.5), Inches(2.5), Inches(5.5), Inches(4.3),
    chart_data
)
chart = chart_frame.chart
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.RIGHT
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(12)

plot = chart.plots[0]
plot.has_data_labels = True
data_labels = plot.data_labels
data_labels.font.size = Pt(12)
data_labels.font.bold = True
data_labels.font.color.rgb = WHITE
data_labels.number_format = '0"%"'

# 饼图颜色
series = chart.series[0]
colors = [AWS_COLOR, AZURE_COLOR, GCP_COLOR, LIGHT_GRAY]
for i, clr in enumerate(colors):
    point = series.points[i]
    point.format.fill.solid()
    point.format.fill.fore_color.rgb = clr

# 右侧增长驱动力
lines = [
    ("增长驱动力", 18, True, NAVY),
    ("", 8, False, DARK_GRAY),
    ("1. AI/生成式AI工作负载 — 最大的增量需求来源", 14, False, DARK_GRAY),
    ("   GPU基础设施和AI平台消费爆发式增长", 12, False, MED_GRAY),
    ("", 8, False, DARK_GRAY),
    ("2. 企业数字化转型 — 持续结构性趋势", 14, False, DARK_GRAY),
    ("   传统IT向云迁移仍在加速中", 12, False, MED_GRAY),
    ("", 8, False, DARK_GRAY),
    ("3. 混合云/多云策略 — 扩大总可触达市场", 14, False, DARK_GRAY),
    ("   企业采用多云架构推动整体市场扩容", 12, False, MED_GRAY),
    ("", 8, False, DARK_GRAY),
    ("4. 边缘计算 — 新兴增长点", 14, False, DARK_GRAY),
    ("   IoT和实时应用驱动边缘云需求", 12, False, MED_GRAY),
]
add_multi_text(slide, Inches(6.5), Inches(2.5), Inches(6), Inches(4.5), lines)

add_source_line(slide, "来源：Synergy Research Group (2025.11); Gartner; 行业共识估算")

# ══════════════════════════════════════════════════════
# Slide 3: 三巨头关键指标对比
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "AWS规模领先但增速放缓，GCP增速爆发、Azure最为均衡")

headers = ["指标", "AWS (AMZN)", "Azure (MSFT)", "Google Cloud (GOOGL)"]
rows = [
    ["FY2025云营收", "$1,287亿", "~$750亿+", "~$450亿(年化)"],
    ["最新季度营收", "$356亿 (Q4'25)", "$309亿 (IC, FY25Q3)", "$200.3亿 (Q1'26)"],
    ["YoY增长率", "+20% (全年) / +24% (Q4)", "+33-34%", "+63%"],
    ["运营利润率", "~35.9%", "~45% (IC segment)", "~33%"],
    ["市场份额", "~29-30%", "~20%", "~13%"],
    ["AI对增长贡献", "未单独披露", "16个百分点", "显著但未量化"],
    ["P/E (TTM)", "~28.2x", "~29.6x", "~21.7x"],
    ["自研芯片", "Graviton4, Trainium2", "Maia 100", "TPU v5p"],
]

add_table(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(4.5),
          headers, rows,
          col_widths=[Inches(2.5), Inches(3.2), Inches(3.2), Inches(3.4)])

add_source_line(slide, "来源：Amazon IR FY2025; Microsoft IR FY25 Q3; Alphabet IR Q1 2026; Synergy Research (2025.11)")

# ══════════════════════════════════════════════════════
# Slide 4: 营收规模对比图
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "AWS营收规模约为GCP的2.9倍，但增速差距正在缩小")

# 营收柱状图
chart_data = CategoryChartData()
chart_data.categories = ['AWS', 'Azure', 'Google Cloud']
chart_data.add_series('年云营收（亿美元）', (1287, 750, 450))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1.3), Inches(5.8), Inches(4.5),
    chart_data
)
chart = chart_frame.chart
chart.has_legend = False
chart.value_axis.major_gridlines.format.line.color.rgb = LIGHT_GRAY
chart.value_axis.has_title = True
chart.value_axis.axis_title.text_frame.paragraphs[0].text = "亿美元"
chart.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(11)

series = chart.series[0]
# 设置各柱颜色
colors = [AWS_COLOR, AZURE_COLOR, GCP_COLOR]
for i, clr in enumerate(colors):
    pt = series.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = clr

series.has_data_labels = True
series.data_labels.font.size = Pt(13)
series.data_labels.font.bold = True
series.data_labels.number_format = '#,##0'

# 增长率柱状图
chart_data2 = CategoryChartData()
chart_data2.categories = ['AWS', 'Azure', 'Google Cloud']
chart_data2.add_series('YoY增长率 (%)', (20, 33.5, 63))

chart_frame2 = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(6.8), Inches(1.3), Inches(5.8), Inches(4.5),
    chart_data2
)
chart2 = chart_frame2.chart
chart2.has_legend = False
chart2.value_axis.major_gridlines.format.line.color.rgb = LIGHT_GRAY
chart2.value_axis.has_title = True
chart2.value_axis.axis_title.text_frame.paragraphs[0].text = "%"
chart2.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(11)

series2 = chart2.series[0]
for i, clr in enumerate(colors):
    pt = series2.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = clr

series2.has_data_labels = True
series2.data_labels.font.size = Pt(13)
series2.data_labels.font.bold = True
series2.data_labels.number_format = '0"%"'

add_source_line(slide, "来源：Amazon IR FY2025; Microsoft IR FY25 Q3; Alphabet IR Q1 2026")

# ══════════════════════════════════════════════════════
# Slide 5: AWS 深度分析
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "AWS：利润机器稳健运转，但增速落后于AI时代的竞争者")

# 左侧指标
headers = ["指标", "数值"]
rows = [
    ["FY2025营收", "$1,287亿"],
    ["YoY增长", "+20% / Q4 +24%"],
    ["运营利润率", "~35.9%"],
    ["年化运行率", "~$1,420亿"],
    ["市场份额", "~29-30%"],
    ["数据中心", "33区域 / 105可用区"],
    ["自研芯片", "Graviton4, Trainium2"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(5.0), Inches(3.8),
          headers, rows, col_widths=[Inches(2.2), Inches(2.8)])

# 右侧定性
lines = [
    ("核心优势", 16, True, ACCENT3),
    ("  - 最早进入者，生态最成熟（200+服务）", 13, False, DARK_GRAY),
    ("  - 运营利润率行业最高（35.9%）", 13, False, DARK_GRAY),
    ("  - 自研芯片战略降低成本", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("核心劣势", 16, True, RGBColor(0xCC, 0x33, 0x33)),
    ("  - 增速在三巨头中最低（+20%）", 13, False, DARK_GRAY),
    ("  - 缺乏原生SaaS应用层绑定", 13, False, DARK_GRAY),
    ("  - 无自研基础大模型（依赖Anthropic）", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("当前战略重点", 16, True, ACCENT2),
    ("  - AI基础设施扩张（Trainium芯片）", 13, False, DARK_GRAY),
    ("  - 自研Nova大模型系列", 13, False, DARK_GRAY),
    ("  - 企业级客户深化与Bedrock平台", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(6.0), Inches(1.3), Inches(6.5), Inches(5.0), lines)

add_source_line(slide, "来源：Amazon IR FY2025年报; Synergy Research (2025.11)")

# ══════════════════════════════════════════════════════
# Slide 6: Azure 深度分析
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "Azure：AI变现的最佳平台，OpenAI+Copilot构建独特护城河")

headers = ["指标", "数值"]
rows = [
    ["Azure年营收", ">$750亿"],
    ["Azure YoY增长", "+34%"],
    ["AI对增长贡献", "16个百分点"],
    ["智能云营收(FY25Q3)", "$309亿, +21% YoY"],
    ["Cloud毛利率", "69% (同比-3pp)"],
    ["市场份额", "~20%"],
    ["数据中心", "60+区域"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(5.0), Inches(3.8),
          headers, rows, col_widths=[Inches(2.5), Inches(2.5)])

lines = [
    ("核心优势", 16, True, ACCENT3),
    ("  - 企业客户关系最深（M365生态绑定）", 13, False, DARK_GRAY),
    ("  - OpenAI独家合作，最强AI能力接入", 13, False, DARK_GRAY),
    ("  - 混合云能力领先（Azure Arc）", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("核心劣势", 16, True, RGBColor(0xCC, 0x33, 0x33)),
    ("  - 毛利率同比下降3个百分点", 13, False, DARK_GRAY),
    ("  - 对OpenAI关系依赖度较高", 13, False, DARK_GRAY),
    ("  - 纯IaaS市场心智份额低于AWS", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("当前战略重点", 16, True, ACCENT2),
    ("  - Copilot全面整合M365/Dynamics", 13, False, DARK_GRAY),
    ("  - AI Foundry企业AI应用平台", 13, False, DARK_GRAY),
    ("  - Maia自研AI芯片降低成本", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(6.0), Inches(1.3), Inches(6.5), Inches(5.0), lines)

add_source_line(slide, "来源：Microsoft IR FY25 Q3; Synergy Research (2025.11)")

# ══════════════════════════════════════════════════════
# Slide 7: GCP 深度分析
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "GCP：增速爆发的追赶者，从亏损到盈利的质变时刻")

headers = ["指标", "数值"]
rows = [
    ["Q1 2026营收", "$200.3亿"],
    ["YoY增长", "+63%"],
    ["运营利润", "$66亿 (同期$22亿)"],
    ["运营利润率", "~33%"],
    ["市场份额", "~13%"],
    ["年化运行率", "~$800亿"],
    ["自研芯片", "TPU v5p"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(5.0), Inches(3.8),
          headers, rows, col_widths=[Inches(2.2), Inches(2.8)])

lines = [
    ("核心优势", 16, True, ACCENT3),
    ("  - AI/ML技术基因最强（Gemini + TPU）", 13, False, DARK_GRAY),
    ("  - 数据分析栈领先（BigQuery, Looker）", 13, False, DARK_GRAY),
    ("  - 增速最快（+63%），利润率快速提升", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("核心劣势", 16, True, RGBColor(0xCC, 0x33, 0x33)),
    ("  - 市场份额仍小（13%）", 13, False, DARK_GRAY),
    ("  - 企业销售能力弱于Microsoft", 13, False, DARK_GRAY),
    ("  - 生态合作伙伴网络不足", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("当前战略重点", 16, True, ACCENT2),
    ("  - AI平台差异化（Vertex AI + Gemini）", 13, False, DARK_GRAY),
    ("  - 企业客户拓展（Salesforce/SAP合作）", 13, False, DARK_GRAY),
    ("  - TPU芯片成本优势深化", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(6.0), Inches(1.3), Inches(6.5), Inches(5.0), lines)

add_source_line(slide, "来源：Alphabet IR Q1 2026; Synergy Research (2025.11)")

# ══════════════════════════════════════════════════════
# Slide 8: AI战略对比
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "AI已成为云竞争的核心战场，三者路径分化明显")

headers = ["AI维度", "AWS", "Azure", "GCP"]
rows = [
    ["基础模型", "Nova（自研）+ Anthropic", "GPT（OpenAI）+ Phi", "Gemini（自研）"],
    ["AI芯片", "Trainium2, Inferentia", "Maia 100", "TPU v5p"],
    ["AI平台", "Bedrock, SageMaker", "Azure AI Foundry", "Vertex AI"],
    ["AI营收贡献", "未单独披露", "16个百分点", "显著但未量化"],
    ["差异化定位", "最广泛的模型选择", "企业AI应用领先", "技术/成本领先"],
    ["AI合作伙伴", "Anthropic ($40亿)", "OpenAI ($130亿+)", "自研为主"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(3.5),
          headers, rows,
          col_widths=[Inches(2.0), Inches(3.3), Inches(3.5), Inches(3.5)])

# 底部洞察
lines = [
    ("关键洞察", 18, True, NAVY),
    ("", 6, False, DARK_GRAY),
    ("  - Azure通过OpenAI合作实现了AI变现的最快路径，Copilot正从概念走向产品化", 13, False, DARK_GRAY),
    ("  - AWS选择'模型超市'策略（Bedrock），避免对单一模型厂商的依赖", 13, False, DARK_GRAY),
    ("  - GCP凭借TPU和Gemini实现技术差异化，垂直整合程度最高（芯片-模型-平台）", 13, False, DARK_GRAY),
    ("  - 三家均在大幅增加AI资本开支：Amazon计划$2,000亿总capex", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(0.5), Inches(5.0), Inches(12.3), Inches(2.0), lines)

add_source_line(slide, "来源：各公司财报电话会议; 行业研究报告")

# ══════════════════════════════════════════════════════
# Slide 9: 竞争力矩阵（雷达图用表格呈现）
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "AWS以规模和利润率领先，Azure生态绑定最深，GCP增速与技术突出")

headers = ["维度", "AWS (AMZN)", "Azure (MSFT)", "GCP (GOOGL)"]
rows = [
    ["规模", "●●● $1,287亿", "●●○ ~$750亿", "●○○ ~$450亿"],
    ["增速", "●○○ +20%", "●●● +33-34%", "●●● +63%"],
    ["利润率", "●●● 35.9%", "●●● ~45% (IC)", "●●○ 33%"],
    ["AI能力", "●●○ Anthropic合作", "●●● OpenAI/Copilot", "●●● Gemini/TPU"],
    ["生态深度", "●●● 最广", "●●● Office/M365", "●○○ 建设中"],
    ["企业销售", "●●● 强", "●●● 最强", "●○○ 弱"],
    ["开发者心智", "●●● 领先", "●●○ 强", "●●○ Kubernetes"],
    ["估值吸引力", "●○○ 28.2x", "●○○ 29.6x", "●●● 21.7x"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(4.8),
          headers, rows,
          col_widths=[Inches(2.0), Inches(3.3), Inches(3.5), Inches(3.5)])

add_source_line(slide, "来源：综合分析; 各公司财报; Synergy Research")

# ══════════════════════════════════════════════════════
# Slide 10: 护城河评估
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "护城河评估：AWS与Azure具有持久优势，GCP护城河正在加深")

headers = ["护城河维度", "AWS", "Azure", "GCP"]
rows = [
    ["网络效应", "强 — 最大用户基础", "强 — M365生态飞轮", "中等 — K8s生态"],
    ["转换成本", "强 — 深度架构集成", "极强 — AD/M365绑定", "中等 — 技术标准化"],
    ["规模经济", "极强 — 最低单位成本", "强 — 第二大规模", "中等 — 改善中"],
    ["无形资产", "强 — 品牌认知第一", "强 — 企业信任度最高", "强 — AI/ML技术品牌"],
    ["综合评级", "强", "强-极强", "中等-强"],
]
add_table(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(3.0),
          headers, rows,
          col_widths=[Inches(2.0), Inches(3.3), Inches(3.5), Inches(3.5)])

# 底部总结
lines = [
    ("持久优势与结构性脆弱", 18, True, NAVY),
    ("", 6, False, DARK_GRAY),
    ("AWS — 稳健的现金牛，规模护城河最深，但缺乏应用层绑定，增速持续放缓", 13, False, DARK_GRAY),
    ("Azure — 企业AI变现最佳定位，M365绑定创造最高转换成本，但毛利率受AI投资侵蚀", 13, False, DARK_GRAY),
    ("GCP — 增速最快的追赶者，技术差异化（TPU/Gemini）独特，估值最具吸引力（P/E 21.7x）", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.5), lines)

add_source_line(slide, "来源：综合分析; 各公司财报; 投资研究报告")

# ══════════════════════════════════════════════════════
# Slide 11: 估值对比
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "GOOGL估值最具吸引力（P/E 21.7x），AMZN与MSFT估值相当")

# 估值对比柱状图
chart_data = CategoryChartData()
chart_data.categories = ['AWS (AMZN)', 'Azure (MSFT)', 'GCP (GOOGL)']
chart_data.add_series('P/E (TTM)', (28.2, 29.6, 21.7))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1.3), Inches(5.8), Inches(4.5),
    chart_data
)
chart = chart_frame.chart
chart.has_legend = False
chart.value_axis.major_gridlines.format.line.color.rgb = LIGHT_GRAY
chart.value_axis.has_title = True
chart.value_axis.axis_title.text_frame.paragraphs[0].text = "P/E 倍数"
chart.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(11)

series = chart.series[0]
for i, clr in enumerate(colors):
    pt = series.points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = clr

series.has_data_labels = True
series.data_labels.font.size = Pt(14)
series.data_labels.font.bold = True
series.data_labels.number_format = '0.0"x"'

# 右侧估值分析
lines = [
    ("估值关键观察", 18, True, NAVY),
    ("", 8, False, DARK_GRAY),
    ("GOOGL (P/E 21.7x)", 16, True, GCP_COLOR),
    ("  - 三者中估值最低，反映市场对其AI变现路径的不确定性", 13, False, DARK_GRAY),
    ("  - 但Cloud增速+63%远超预期，可能存在重估空间", 13, False, DARK_GRAY),
    ("  - 风险回报比最佳", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("AMZN (P/E 28.2x)", 16, True, AWS_COLOR),
    ("  - P/E已从2023年的48.4x压缩至28.2x", 13, False, DARK_GRAY),
    ("  - EV/Revenue 4.0x反映AWS的规模价值", 13, False, DARK_GRAY),
    ("  - EPS预计2025-2027年增长31%", 13, False, DARK_GRAY),
    ("", 8, False, DARK_GRAY),
    ("MSFT (P/E 29.6x)", 16, True, AZURE_COLOR),
    ("  - 最高估值反映Azure AI变现预期", 13, False, DARK_GRAY),
    ("  - 溢价来自Copilot和OpenAI独家优势", 13, False, DARK_GRAY),
    ("  - 约30%上行空间（分析师共识）", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(6.8), Inches(1.3), Inches(6.0), Inches(5.0), lines)

add_source_line(slide, "来源：Yahoo Finance; FinanceCharts; TipRanks; 各公司财报")

# ══════════════════════════════════════════════════════
# Slide 12: 情景分析
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "情景分析：AI需求持续性是三者的共同关键变量")

# AWS情景
lines_aws = [
    ("AWS (AMZN) 情景分析", 16, True, AWS_COLOR),
    ("", 6, False, DARK_GRAY),
    ("乐观 (25%) — AI加速增长，利润率扩张至38%+，Q4 +24%趋势延续", 12, False, DARK_GRAY),
    ("基准 (50%) — 维持+18-22%稳态增长，份额缓降至27-28%，利润率35-36%", 12, False, DARK_GRAY),
    ("悲观 (25%) — AI需求不及预期，份额被蚕食，利润率压缩至32-33%", 12, False, DARK_GRAY),
]
add_multi_text(slide, Inches(0.5), Inches(1.2), Inches(6.0), Inches(2.0), lines_aws)

# Azure情景
lines_az = [
    ("Azure (MSFT) 情景分析", 16, True, AZURE_COLOR),
    ("", 6, False, DARK_GRAY),
    ("乐观 (30%) — Copilot全面渗透，Azure增速维持30%+，AI营收占比突破20%", 12, False, DARK_GRAY),
    ("基准 (45%) — 增速逐步放缓至25-30%，利润率在AI投资和规模效应间平衡", 12, False, DARK_GRAY),
    ("悲观 (25%) — OpenAI关系生变，AI投入过度致利润率下降，变现慢于预期", 12, False, DARK_GRAY),
]
add_multi_text(slide, Inches(6.8), Inches(1.2), Inches(6.0), Inches(2.0), lines_az)

# GCP情景
lines_gcp = [
    ("Google Cloud (GOOGL) 情景分析", 16, True, GCP_COLOR),
    ("", 6, False, DARK_GRAY),
    ("乐观 (30%) — +60%增速持续2-3年，TPU/Gemini技术优势兑现，份额突破15%", 12, False, DARK_GRAY),
    ("基准 (45%) — 增速回归至35-40%，份额稳定在13-14%，利润率维持30-35%", 12, False, DARK_GRAY),
    ("悲观 (25%) — 增速快速回落至25%以下（基数效应+竞争），亏损风险再现", 12, False, DARK_GRAY),
]
add_multi_text(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(2.0), lines_gcp)

# 底部投资建议
lines_bottom = [
    ("投资启示", 18, True, NAVY),
    ("", 6, False, DARK_GRAY),
    ("  - 风险规避型投资者 → AWS（最稳健的利润机器，35.9%运营利润率）", 13, False, DARK_GRAY),
    ("  - 平衡型投资者 → Azure（AI变现最佳路径，但估值已反映部分预期）", 13, False, DARK_GRAY),
    ("  - 高回报偏好投资者 → GCP（最佳风险回报比，P/E 21.7x，增速+63%）", 13, False, DARK_GRAY),
]
add_multi_text(slide, Inches(0.5), Inches(5.3), Inches(12.3), Inches(2.0), lines_bottom)

add_source_line(slide, "来源：综合分析; 各公司财报; 分析师共识估算")

# ══════════════════════════════════════════════════════
# Slide 13: 总结与关键结论
# ══════════════════════════════════════════════════════
slide = add_blank_slide()
set_slide_bg(slide)
add_slide_title(slide, "云计算三巨头各具特色，AI将成为决定最终格局的关键变量")

# 三列总结
for i, (name, clr, bullets) in enumerate([
    ("AWS", AWS_COLOR, [
        ("规模之王", 16, True, clr),
        ("", 4, False, DARK_GRAY),
        ("营收$1,287亿，份额30%", 13, False, DARK_GRAY),
        ("利润率35.9%行业最高", 13, False, DARK_GRAY),
        ("稳健的现金流生成器", 13, False, DARK_GRAY),
        ("风险：增速放缓至+20%", 13, False, RGBColor(0xCC, 0x33, 0x33)),
    ]),
    ("Azure", AZURE_COLOR, [
        ("AI变现之王", 16, True, clr),
        ("", 4, False, DARK_GRAY),
        ("增速+33%，AI贡献16pp", 13, False, DARK_GRAY),
        ("M365生态绑定最深", 13, False, DARK_GRAY),
        ("Copilot驱动企业AI落地", 13, False, DARK_GRAY),
        ("风险：毛利率承压", 13, False, RGBColor(0xCC, 0x33, 0x33)),
    ]),
    ("GCP", GCP_COLOR, [
        ("增速之王", 16, True, clr),
        ("", 4, False, DARK_GRAY),
        ("增速+63%，利润率33%", 13, False, DARK_GRAY),
        ("TPU/Gemini技术领先", 13, False, DARK_GRAY),
        ("估值最低 P/E 21.7x", 13, False, DARK_GRAY),
        ("风险：份额小(13%)", 13, False, RGBColor(0xCC, 0x33, 0x33)),
    ]),
]):
    x = Inches(0.5) + Inches(i * 4.2)
    add_multi_text(slide, x, Inches(1.5), Inches(3.8), Inches(4.5), bullets)

# 底部核心结论
shape = slide.shapes.add_shape(1, Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.3))
shape.fill.solid()
shape.fill.fore_color.rgb = NAVY
shape.line.fill.background()

add_textbox(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.0),
            "核心结论：AI正在重塑云计算竞争格局。AWS以规模和利润率防守，Azure以生态和AI应用进攻，"
            "GCP以技术和增速追赶。未来2-3年，AI变现能力和基础设施投入的平衡将决定最终座次。"
            "从估值角度看，GOOGL提供最佳风险回报比（P/E 21.7x vs AMZN 28.2x vs MSFT 29.6x）。",
            font_size=14, bold=False, color=WHITE)

add_source_line(slide, "分析日期：2026年5月10日 | 数据来源：Amazon IR, Microsoft IR, Alphabet IR, Synergy Research")

# ── 保存 ──────────────────────────────────────────────
output_path = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\FA_competitive_analysis_real_output.pptx"
prs.save(output_path)
print(f"PPTX已保存至: {output_path}")
print(f"共 {len(prs.slides)} 张幻灯片")
