"""
构建AI行业投资主题演示文稿
使用 python-pptx 生成6页投资主题PPTX
数据来源: WebSearch 实时搜索结果 (2026年5月)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE
from pptx.chart.data import CategoryChartData
import os
from datetime import datetime

# ============================================================
# 配置
# ============================================================
OUTPUT_DIR = "C:/Users/Lenovo/Desktop/financial-services-fork/financial-services/test-validation"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "FA_pptx_author_real_output.pptx")
MD_FILE = os.path.join(OUTPUT_DIR, "FA_pptx_author_real_output.md")

# 颜色方案
DARK_BLUE = RGBColor(0x1B, 0x3A, 0x5C)      # 深蓝 - 标题背景
MEDIUM_BLUE = RGBColor(0x2C, 0x5F, 0x8A)     # 中蓝 - 次要背景
LIGHT_BLUE = RGBColor(0x3A, 0x86, 0xC8)      # 浅蓝 - 强调
ACCENT_GREEN = RGBColor(0x27, 0xAE, 0x60)    # 绿色 - 正面指标
ACCENT_RED = RGBColor(0xE7, 0x4C, 0x3C)      # 红色 - 风险
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF0, 0xF0, 0xF0)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
GOLD = RGBColor(0xD4, 0xA5, 0x17)            # 金色 - 高亮


# ============================================================
# 辅助函数
# ============================================================

def set_slide_bg(slide, color):
    """设置幻灯片背景色"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape_with_text(slide, left, top, width, height, text, font_size=12,
                        font_color=DARK_GRAY, bold=False, bg_color=None,
                        alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    """添加带文本的矩形框"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()  # 无边框
    if bg_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
    else:
        shape.fill.background()  # 透明背景

    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=12,
                 font_color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri"):
    """添加纯文本框"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multiline_text(slide, left, top, width, height, lines, font_size=12,
                       font_color=DARK_GRAY, bold=False, alignment=PP_ALIGN.LEFT,
                       font_name="Calibri", line_spacing=1.2):
    """添加多行文本框，lines可以是字符串列表"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = font_color
        p.font.bold = bold
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(font_size * (line_spacing - 1) * 2)
    return txBox


def add_table(slide, left, top, width, height, rows, cols, data, col_widths=None):
    """添加表格
    data: 二维列表, data[0]为表头
    """
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # 设置列宽
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    # 填充数据
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c])

            # 设置单元格样式
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(10)
                paragraph.font.name = "Calibri"
                if r == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
                    paragraph.alignment = PP_ALIGN.CENTER
                else:
                    paragraph.font.color.rgb = DARK_GRAY
                    if c == 0:
                        paragraph.alignment = PP_ALIGN.LEFT
                    else:
                        paragraph.alignment = PP_ALIGN.CENTER

            # 表头背景色
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE

    return table_shape


def add_title_bar(slide, title_text, subtitle_text=None):
    """在幻灯片顶部添加标题栏"""
    # 标题背景条
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        Inches(13.333), Inches(1.2)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

    # 标题文字
    add_text_box(slide, Inches(0.6), Inches(0.15), Inches(12), Inches(0.7),
                 title_text, font_size=28, font_color=WHITE, bold=True)

    # 副标题/日期
    if subtitle_text:
        add_text_box(slide, Inches(0.6), Inches(0.75), Inches(12), Inches(0.4),
                     subtitle_text, font_size=12, font_color=RGBColor(0xBB, 0xCC, 0xDD))

    # 底部金色装饰线
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(1.2),
        Inches(13.333), Inches(0.04)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = GOLD
    line.line.fill.background()


def add_footer(slide, page_num, total_pages):
    """添加页脚"""
    add_text_box(slide, Inches(0.5), Inches(7.2), Inches(5), Inches(0.3),
                 "机密 | 仅供内部使用 | AI行业投资主题分析",
                 font_size=8, font_color=RGBColor(0x99, 0x99, 0x99))
    add_text_box(slide, Inches(11), Inches(7.2), Inches(2), Inches(0.3),
                 f"第 {page_num} / {total_pages} 页",
                 font_size=8, font_color=RGBColor(0x99, 0x99, 0x99),
                 alignment=PP_ALIGN.RIGHT)


# ============================================================
# 创建演示文稿
# ============================================================

prs = Presentation()
# 宽屏16:9
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

TOTAL_PAGES = 8  # 封面 + 6页内容 + 尾页

# ============================================================
# 第1页：封面
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
set_slide_bg(slide1, DARK_BLUE)

# 主标题
add_text_box(slide1, Inches(1.5), Inches(1.8), Inches(10), Inches(1.2),
             "AI行业投资主题分析",
             font_size=44, font_color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# 金色分隔线
line = slide1.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(4.5), Inches(3.1), Inches(4.333), Inches(0.05)
)
line.fill.solid()
line.fill.fore_color.rgb = GOLD
line.line.fill.background()

# 副标题
add_text_box(slide1, Inches(1.5), Inches(3.4), Inches(10), Inches(0.8),
             "Artificial Intelligence Sector — Investment Thesis & Outlook",
             font_size=20, font_color=RGBColor(0xBB, 0xCC, 0xDD),
             alignment=PP_ALIGN.CENTER)

# 关键信息
info_lines = [
    "聚焦标的：NVIDIA (NVDA) | Microsoft (MSFT) | Alphabet (GOOGL)",
    "报告日期：2026年5月10日",
    "数据来源：Grand View Research, Statista, Yahoo Finance, Reuters"
]
add_multiline_text(slide1, Inches(2.5), Inches(4.6), Inches(8), Inches(1.5),
                   info_lines, font_size=14, font_color=RGBColor(0xDD, 0xDD, 0xDD),
                   alignment=PP_ALIGN.CENTER, line_spacing=1.5)

# 机密标识
add_text_box(slide1, Inches(4), Inches(6.5), Inches(5), Inches(0.4),
             "CONFIDENTIAL — FOR INTERNAL USE ONLY",
             font_size=10, font_color=RGBColor(0x88, 0x88, 0x88),
             alignment=PP_ALIGN.CENTER)

# ============================================================
# 第2页：AI市场概览
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide2, "全球AI市场规模 — 万亿级增长赛道",
              "市场规模从2025年$391B预计增长至2033年$3.5T+，CAGR 30.6%")

# 左侧：市场规模表格
market_data = [
    ["年份", "市场规模 (十亿美元)", "同比增长率"],
    ["2023", "$189B", "—"],
    ["2024", "$280B (估)", "~48%"],
    ["2025", "$391B", "~40%"],
    ["2026F", "$510B (估)", "~30%"],
    ["2028F", "$860B (估)", "~30%"],
    ["2030F", "$1,450B (估)", "~30%"],
    ["2033F", "$3,497B", "CAGR 30.6%"],
]
add_table(slide2, Inches(0.6), Inches(1.6), Inches(5.5), Inches(3.5),
          len(market_data), 3, market_data,
          col_widths=[Inches(1.5), Inches(2.2), Inches(1.8)])

# 右侧：关键驱动因素
add_text_box(slide2, Inches(6.8), Inches(1.6), Inches(6), Inches(0.4),
             "关键增长驱动因素", font_size=16, font_color=DARK_BLUE, bold=True)

drivers = [
    "1. 生成式AI爆发：ChatGPT/Copilot等应用推动企业级AI采用率飙升",
    "2. 云基础设施投资：超大规模云厂商资本支出2025年超$3,000亿",
    "3. 企业数字化转型：AI嵌入ERP/CRM/供应链等核心业务流程",
    "4. AI芯片需求：GPU/TPU/AI加速器供不应求，NVIDIA独占鳌头",
    "5. 政策推动：各国AI战略和监管框架逐步落地，消除不确定性",
]
add_multiline_text(slide2, Inches(6.8), Inches(2.1), Inches(6), Inches(3.0),
                   drivers, font_size=11, font_color=DARK_GRAY, line_spacing=1.4)

# 底部注释
add_text_box(slide2, Inches(0.6), Inches(5.5), Inches(12), Inches(0.8),
             "数据来源：Grand View Research (2026), Statista, UNCTAD, MarketsandMarkets | 注：2026F及之后为预测值",
             font_size=8, font_color=RGBColor(0x99, 0x99, 0x99))

# 市场规模柱状图（使用pptx原生图表）
chart_data = CategoryChartData()
chart_data.categories = ['2023', '2024E', '2025', '2026F', '2028F', '2030F', '2033F']
chart_data.add_series('市场规模 ($B)', (189, 280, 391, 510, 860, 1450, 3497))

chart_frame = slide2.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.6), Inches(5.8), Inches(12), Inches(1.4),
    chart_data
)
chart = chart_frame.chart
chart.has_legend = False
chart.has_title = False

# 美化图表
plot = chart.plots[0]
series = plot.series[0]
series.format.fill.solid()
series.format.fill.fore_color.rgb = LIGHT_BLUE

# 设置分类轴标签字体大小
cat_axis = chart.category_axis
cat_axis.tick_labels.font.size = Pt(8)
val_axis = chart.value_axis
val_axis.tick_labels.font.size = Pt(8)

add_footer(slide2, 2, TOTAL_PAGES)

# ============================================================
# 第3页：主要玩家
# ============================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide3, "AI三巨头核心数据对比",
              "NVIDIA、Microsoft、Alphabet — 2026年AI价值链核心标的")

# 核心数据对比表格
company_data = [
    ["指标", "NVIDIA (NVDA)", "Microsoft (MSFT)", "Alphabet (GOOGL)"],
    ["市值 (2026年5月)", "~$3.6-4.6T", "~$3.0T (估)", "~$3.99T"],
    ["市盈率 (TTM P/E)", "43.5x", "24.5x", "29.2x"],
    ["Forward P/E", "23.9x", "~25x", "~28x"],
    ["最新季度营收", "$68.1B (Q4 FY26)", ">$70B (估)", ">$90B (估)"],
    ["YoY营收增长", "+20%", "~15%", "~14%"],
    ["AI相关资本支出", "—", "$91-93B (FY25)", "$70-72B (+81% YoY)"],
    ["核心AI优势", "GPU/AI芯片垄断", "Azure云+Copilot", "Gemini+Google Cloud"],
    ["AI收入增长亮点", "数据中心收入暴涨", "云增长26%", "云增长48%"],
]
add_table(slide3, Inches(0.6), Inches(1.5), Inches(12), Inches(3.8),
          len(company_data), 4, company_data,
          col_widths=[Inches(2.5), Inches(3.0), Inches(3.25), Inches(3.25)])

# 分析要点
add_text_box(slide3, Inches(0.6), Inches(5.6), Inches(12), Inches(0.4),
             "核心洞察", font_size=14, font_color=DARK_BLUE, bold=True)

insights = [
    "NVIDIA：AI算力基础设施绝对龙头，Forward P/E仅23.9x，估值相对增速具有吸引力",
    "Microsoft：企业AI落地最佳平台，Azure+Copilot构成闭环生态，P/E最低(24.5x)估值最具性价比",
    "Alphabet：Google Cloud增长48%领跑，Gemini模型能力持续提升，市值有望超越NVIDIA",
]
add_multiline_text(slide3, Inches(0.6), Inches(6.0), Inches(12), Inches(1.2),
                   insights, font_size=10, font_color=DARK_GRAY, line_spacing=1.3)

add_footer(slide3, 3, TOTAL_PAGES)

# ============================================================
# 第4页：投资论点
# ============================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide4, "AI投资核心论点 — 三大关键驱动因素",
              "结构性增长、盈利可见性、估值重估空间")

# 三个驱动因素卡片
card_width = Inches(3.8)
card_height = Inches(4.5)
card_top = Inches(1.6)
card_gap = Inches(0.4)

cards_info = [
    {
        "title": "驱动因素一：AI基础设施\n支出周期远未结束",
        "color": LIGHT_BLUE,
        "items": [
            "超大规模云厂商2025年AI相关",
            "资本支出合计超$2,500亿",
            "",
            "Microsoft FY25 Capex指引：",
            "$91-93B (同比+60%+)",
            "",
            "Alphabet Capex：$70-72B",
            "(同比+81%)",
            "",
            "NVIDIA数据中心收入持续创",
            "历史新高，供需缺口仍在",
        ]
    },
    {
        "title": "驱动因素二：AI从实验\n到规模化盈利转换",
        "color": ACCENT_GREEN,
        "items": [
            "企业AI采用率从试点走向",
            "生产级部署，ROI逐步验证",
            "",
            "Copilot/Gemini等AI助手",
            "推动SaaS ARPU提升",
            "",
            "AI赋能广告、搜索、云服务",
            "三大收入支柱同时受益",
            "",
            "Google Cloud 48%增速验证",
            "AI变现的加速度",
        ]
    },
    {
        "title": "驱动因素三：估值仍有\n重估空间",
        "color": MEDIUM_BLUE,
        "items": [
            "NVIDIA Forward P/E 23.9x",
            "远低于3年均值79x",
            "",
            "Microsoft P/E 24.5x，在AI",
            "受益标的中估值最低",
            "",
            "AI市场CAGR 30.6%远超",
            "传统科技增长水平",
            "",
            "盈利增速持续超越股价涨幅",
            "估值被动压缩带来配置窗口",
        ]
    },
]

for i, card in enumerate(cards_info):
    left = Inches(0.6) + i * (card_width + card_gap)

    # 卡片背景
    bg = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, card_top, card_width, card_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = WHITE
    bg.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    bg.line.width = Pt(1)

    # 顶部色条
    stripe = slide4.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left, card_top, card_width, Inches(0.08)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = card["color"]
    stripe.line.fill.background()

    # 卡片标题
    add_text_box(slide4, left + Inches(0.2), card_top + Inches(0.2),
                 card_width - Inches(0.4), Inches(0.9),
                 card["title"], font_size=13, font_color=DARK_BLUE, bold=True)

    # 卡片内容
    add_multiline_text(slide4, left + Inches(0.2), card_top + Inches(1.2),
                       card_width - Inches(0.4), Inches(3.0),
                       card["items"], font_size=10, font_color=DARK_GRAY,
                       line_spacing=1.2)

add_footer(slide4, 4, TOTAL_PAGES)

# ============================================================
# 第5页：估值比较
# ============================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide5, "估值比较 — NVIDIA vs Microsoft vs Alphabet",
              "基于2026年最新市场数据的估值矩阵分析")

# 估值对比表格
valuation_data = [
    ["估值指标", "NVIDIA", "Microsoft", "Alphabet", "行业中位数"],
    ["市盈率 (TTM P/E)", "43.5x", "24.5x", "29.2x", "~30x"],
    ["Forward P/E", "23.9x", "~25x", "~28x", "~28x"],
    ["P/E vs 3年均值", "远低于79x均值", "略低于均值", "高于10年中位数27.75x", "—"],
    ["营收增速", "+20%", "+15%", "+14%", "~10%"],
    ["PEG比率 (估)", "~1.2x", "~1.6x", "~2.0x", "~2.0x"],
    ["AI Capex强度", "—", "$91-93B", "$70-72B", "—"],
    ["市值区间", "$3.6-4.6T", "~$3.0T", "~$3.99T", "—"],
]
add_table(slide5, Inches(0.6), Inches(1.5), Inches(12), Inches(3.2),
          len(valuation_data), 5, valuation_data,
          col_widths=[Inches(2.5), Inches(2.4), Inches(2.4), Inches(2.4), Inches(2.3)])

# 估值雷达图（用表格+文字模拟，因为pptx原生图表不支持雷达图在所有版本）
add_text_box(slide5, Inches(0.6), Inches(5.0), Inches(12), Inches(0.4),
             "估值结论", font_size=14, font_color=DARK_BLUE, bold=True)

valuation_conclusions = [
    "NVIDIA：Forward P/E 23.9x最具吸引力，PEG ~1.2x表明增长未被充分定价，但需关注AI芯片周期性风险",
    "Microsoft：P/E 24.5x为三者最低，企业AI护城河深厚，Azure+Copilot组合提供最佳风险回报比",
    "Alphabet：P/E 29.2x相对合理，Google Cloud 48%增长提供上行催化剂，但广告业务AI替代风险需关注",
]
add_multiline_text(slide5, Inches(0.6), Inches(5.4), Inches(12), Inches(1.5),
                   valuation_conclusions, font_size=10, font_color=DARK_GRAY, line_spacing=1.3)

# 估值柱状图
chart_data2 = CategoryChartData()
chart_data2.categories = ['TTM P/E', 'Forward P/E', 'PEG (估)']
chart_data2.add_series('NVIDIA', (43.5, 23.9, 1.2))
chart_data2.add_series('Microsoft', (24.5, 25.0, 1.6))
chart_data2.add_series('Alphabet', (29.2, 28.0, 2.0))

chart_frame2 = slide5.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.6), Inches(6.2), Inches(6), Inches(1.0),
    chart_data2
)
chart2 = chart_frame2.chart
chart2.has_title = False
cat_axis2 = chart2.category_axis
cat_axis2.tick_labels.font.size = Pt(8)
val_axis2 = chart2.value_axis
val_axis2.tick_labels.font.size = Pt(8)

# 着色各系列
colors = [LIGHT_BLUE, ACCENT_GREEN, GOLD]
for idx, color in enumerate(colors):
    series = chart2.plots[0].series[idx]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = color

add_footer(slide5, 5, TOTAL_PAGES)

# ============================================================
# 第6页：风险因素
# ============================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide6, "关键风险因素",
              "AI投资面临的主要下行风险和不确定性")

risks = [
    {
        "title": "1. 监管风险",
        "level": "高",
        "color": ACCENT_RED,
        "desc": [
            "EU AI Act 2026年进入全面实施阶段，",
            "高风险AI系统面临严格合规要求",
            "69%的企业预计AI将引发合规问题",
            "美欧监管分歧增加跨国运营复杂度",
        ]
    },
    {
        "title": "2. 基础设施瓶颈",
        "level": "中高",
        "color": RGBColor(0xE6, 0x7E, 0x22),
        "desc": [
            "数据中心电力需求激增，部分地区",
            "电力供应面临瓶颈",
            "AI芯片产能扩张需要时间，供需",
            "平衡点尚不确定",
            "高杠杆AI生态对资本市场依赖度高",
        ]
    },
    {
        "title": "3. 估值回调风险",
        "level": "中",
        "color": GOLD,
        "desc": [
            "NVIDIA市值波动区间大",
            "($3.6-4.6T)，市场情绪敏感",
            "AI主题投资拥挤度升高，短期",
            "获利了结压力存在",
            "利率环境变化影响成长股估值",
        ]
    },
    {
        "title": "4. 技术迭代风险",
        "level": "中",
        "color": LIGHT_BLUE,
        "desc": [
            "AI模型架构快速演进可能改变",
            "算力需求结构",
            "新进入者（如Anthropic $380B）",
            "可能颠覆现有格局",
            "开源模型崛起压缩商业模型利润",
        ]
    },
]

for i, risk in enumerate(risks):
    row = i // 2
    col = i % 2
    left = Inches(0.6) + col * Inches(6.3)
    top = Inches(1.5) + row * Inches(2.8)

    # 风险卡片背景
    card = slide6.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, Inches(5.9), Inches(2.5)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    card.line.width = Pt(1)

    # 左侧色条
    stripe = slide6.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left, top, Inches(0.06), Inches(2.5)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = risk["color"]
    stripe.line.fill.background()

    # 风险标题 + 等级
    add_text_box(slide6, left + Inches(0.2), top + Inches(0.15),
                 Inches(4.0), Inches(0.4),
                 risk["title"], font_size=13, font_color=DARK_BLUE, bold=True)

    # 风险等级标签
    level_shape = add_shape_with_text(
        slide6, left + Inches(4.5), top + Inches(0.15),
        Inches(1.0), Inches(0.35),
        f"风险: {risk['level']}", font_size=9,
        font_color=WHITE, bold=True, bg_color=risk["color"],
        alignment=PP_ALIGN.CENTER
    )

    # 风险描述
    add_multiline_text(slide6, left + Inches(0.2), top + Inches(0.65),
                       Inches(5.4), Inches(1.7),
                       risk["desc"], font_size=10, font_color=DARK_GRAY,
                       line_spacing=1.2)

add_footer(slide6, 6, TOTAL_PAGES)

# ============================================================
# 第7页：结论与建议
# ============================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_bar(slide7, "投资结论与配置建议",
              "基于综合分析的投资策略建议")

# 建议表格
recommendation_data = [
    ["标的", "评级", "目标逻辑", "配置权重建议", "关键催化剂"],
    ["NVIDIA", "增持", "AI算力垄断地位+估值压缩后", "35%", "下一代GPU发布; 数据中心收入超预期"],
    ["", "", "配置窗口打开", "", ""],
    ["Microsoft", "增持", "企业AI闭环生态+估值最低", "35%", "Copilot付费用户增长; Azure增速加速"],
    ["", "", "风险回报比最优", "", ""],
    ["Alphabet", "中性偏多", "Cloud增速领跑+搜索AI化", "30%", "Cloud维持40%+增速; Gemini突破"],
    ["", "", "但广告AI替代风险需监测", "", ""],
]
# 简化为5行（合并描述行）
recommendation_data_clean = [
    ["标的", "评级", "核心逻辑", "配置权重", "关键催化剂"],
    ["NVIDIA", "增持", "AI算力垄断+Forward P/E 23.9x\n估值压缩后配置窗口打开", "35%", "下一代GPU发布;\n数据中心收入超预期"],
    ["Microsoft", "增持", "企业AI闭环生态+P/E 24.5x\n风险回报比最优", "35%", "Copilot付费转化率;\nAzure增速维持26%+"],
    ["Alphabet", "中性偏多", "Cloud增速48%领跑+搜索AI化\n广告AI替代风险需监测", "30%", "Cloud维持40%+增速;\nGemini模型能力突破"],
]
add_table(slide7, Inches(0.6), Inches(1.5), Inches(12), Inches(2.5),
          len(recommendation_data_clean), 5, recommendation_data_clean,
          col_widths=[Inches(1.5), Inches(1.2), Inches(4.0), Inches(1.3), Inches(4.0)])

# 总结要点
add_text_box(slide7, Inches(0.6), Inches(4.3), Inches(12), Inches(0.4),
             "核心结论", font_size=14, font_color=DARK_BLUE, bold=True)

conclusions = [
    "市场判断：AI仍处于早期增长阶段，市场规模CAGR 30.6%为十年级别确定性机会",
    "估值观点：三巨头Forward P/E均处于历史低位区间，盈利增速远超估值水平",
    "配置建议：NVDA+MSFT为核心仓(70%)，GOOGL为卫星仓(30%)，注重再平衡纪律",
    "时间窗口：2026年Q2-Q3为政策真空期+财报季窗口，适合逐步建仓",
    "风控要点：设置15%止损线，关注AI Capex增速拐点和监管政策变化",
]
add_multiline_text(slide7, Inches(0.6), Inches(4.7), Inches(12), Inches(2.2),
                   conclusions, font_size=11, font_color=DARK_GRAY, line_spacing=1.3)

add_footer(slide7, 7, TOTAL_PAGES)

# ============================================================
# 第8页：免责声明/尾页
# ============================================================
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide8, DARK_BLUE)

add_text_box(slide8, Inches(1.5), Inches(1.5), Inches(10), Inches(0.8),
             "免责声明",
             font_size=28, font_color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

disclaimer_lines = [
    "本报告仅供内部参考，不构成任何投资建议。",
    "报告中的数据来源于公开市场信息和第三方研究机构，",
    "包括但不限于 Grand View Research、Statista、Yahoo Finance、",
    "Reuters、Motley Fool、AllInvestView 等。",
    "",
    "所有预测性陈述基于当前市场条件和公开信息，",
    "实际结果可能与预测存在重大差异。",
    "投资者应基于自身情况独立做出投资决策。",
    "",
    "数据截止日期：2026年5月10日",
    "",
    "CONFIDENTIAL — FOR INTERNAL USE ONLY",
]
add_multiline_text(slide8, Inches(2), Inches(2.8), Inches(9), Inches(3.5),
                   disclaimer_lines, font_size=12, font_color=RGBColor(0xBB, 0xCC, 0xDD),
                   alignment=PP_ALIGN.CENTER, line_spacing=1.3)

# ============================================================
# 保存文件
# ============================================================
prs.save(OUTPUT_FILE)
print(f"PPTX已保存至: {OUTPUT_FILE}")

# ============================================================
# 生成MD版本
# ============================================================
md_content = """# AI行业投资主题分析

## 第1页：封面
- 标题：AI行业投资主题分析
- 副标题：Artificial Intelligence Sector — Investment Thesis & Outlook
- 聚焦标的：NVIDIA (NVDA) | Microsoft (MSFT) | Alphabet (GOOGL)
- 报告日期：2026年5月10日

---

## 第2页：全球AI市场规模
### 万亿级增长赛道

| 年份 | 市场规模 (十亿美元) | 同比增长率 |
|------|---------------------|------------|
| 2023 | $189B | — |
| 2024 | $280B (估) | ~48% |
| 2025 | $391B | ~40% |
| 2026F | $510B (估) | ~30% |
| 2028F | $860B (估) | ~30% |
| 2030F | $1,450B (估) | ~30% |
| 2033F | $3,497B | CAGR 30.6% |

**关键增长驱动因素：**
1. 生成式AI爆发：ChatGPT/Copilot等应用推动企业级AI采用率飙升
2. 云基础设施投资：超大规模云厂商资本支出2025年超$3,000亿
3. 企业数字化转型：AI嵌入ERP/CRM/供应链等核心业务流程
4. AI芯片需求：GPU/TPU/AI加速器供不应求
5. 政策推动：各国AI战略和监管框架逐步落地

> 数据来源：Grand View Research (2026), Statista, UNCTAD, MarketsandMarkets

---

## 第3页：AI三巨头核心数据对比

| 指标 | NVIDIA (NVDA) | Microsoft (MSFT) | Alphabet (GOOGL) |
|------|---------------|-------------------|-------------------|
| 市值 (2026年5月) | ~$3.6-4.6T | ~$3.0T (估) | ~$3.99T |
| 市盈率 (TTM P/E) | 43.5x | 24.5x | 29.2x |
| Forward P/E | 23.9x | ~25x | ~28x |
| 最新季度营收 | $68.1B (Q4 FY26) | >$70B (估) | >$90B (估) |
| YoY营收增长 | +20% | ~15% | ~14% |
| AI相关资本支出 | — | $91-93B (FY25) | $70-72B (+81% YoY) |
| 核心AI优势 | GPU/AI芯片垄断 | Azure云+Copilot | Gemini+Google Cloud |
| AI收入增长亮点 | 数据中心收入暴涨 | 云增长26% | 云增长48% |

**核心洞察：**
- NVIDIA：AI算力基础设施绝对龙头，Forward P/E仅23.9x，估值相对增速具有吸引力
- Microsoft：企业AI落地最佳平台，Azure+Copilot构成闭环生态，P/E最低估值最具性价比
- Alphabet：Google Cloud增长48%领跑，Gemini模型能力持续提升，市值有望超越NVIDIA

---

## 第4页：投资论点 — 三大关键驱动因素

### 驱动因素一：AI基础设施支出周期远未结束
- 超大规模云厂商2025年AI相关资本支出合计超$2,500亿
- Microsoft FY25 Capex指引：$91-93B (同比+60%+)
- Alphabet Capex：$70-72B (同比+81%)
- NVIDIA数据中心收入持续创历史新高

### 驱动因素二：AI从实验到规模化盈利转换
- 企业AI采用率从试点走向生产级部署，ROI逐步验证
- Copilot/Gemini等AI助手推动SaaS ARPU提升
- AI赋能广告、搜索、云服务三大收入支柱同时受益
- Google Cloud 48%增速验证AI变现的加速度

### 驱动因素三：估值仍有重估空间
- NVIDIA Forward P/E 23.9x远低于3年均值79x
- Microsoft P/E 24.5x，在AI受益标的中估值最低
- AI市场CAGR 30.6%远超传统科技增长水平
- 盈利增速持续超越股价涨幅，估值被动压缩带来配置窗口

---

## 第5页：估值比较

| 估值指标 | NVIDIA | Microsoft | Alphabet | 行业中位数 |
|----------|--------|-----------|----------|------------|
| 市盈率 (TTM P/E) | 43.5x | 24.5x | 29.2x | ~30x |
| Forward P/E | 23.9x | ~25x | ~28x | ~28x |
| P/E vs 历史均值 | 远低于79x均值 | 略低于均值 | 高于10年中位数 | — |
| 营收增速 | +20% | +15% | +14% | ~10% |
| PEG比率 (估) | ~1.2x | ~1.6x | ~2.0x | ~2.0x |

**估值结论：**
- NVIDIA：Forward P/E 23.9x最具吸引力，PEG ~1.2x表明增长未被充分定价
- Microsoft：P/E 24.5x为三者最低，企业AI护城河深厚，最佳风险回报比
- Alphabet：P/E 29.2x相对合理，Google Cloud 48%增长提供上行催化剂

---

## 第6页：关键风险因素

### 1. 监管风险 [高]
- EU AI Act 2026年进入全面实施阶段
- 69%的企业预计AI将引发合规问题
- 美欧监管分歧增加跨国运营复杂度

### 2. 基础设施瓶颈 [中高]
- 数据中心电力需求激增
- AI芯片产能扩张需要时间
- 高杠杆AI生态对资本市场依赖度高

### 3. 估值回调风险 [中]
- NVIDIA市值波动区间大($3.6-4.6T)
- AI主题投资拥挤度升高
- 利率环境变化影响成长股估值

### 4. 技术迭代风险 [中]
- AI模型架构快速演进
- 新进入者（如Anthropic $380B）可能颠覆格局
- 开源模型崛起压缩商业模型利润

---

## 第7页：投资结论与配置建议

| 标的 | 评级 | 核心逻辑 | 配置权重 | 关键催化剂 |
|------|------|----------|----------|------------|
| NVIDIA | 增持 | AI算力垄断+Forward P/E 23.9x | 35% | 下一代GPU发布; 数据中心收入超预期 |
| Microsoft | 增持 | 企业AI闭环生态+P/E 24.5x | 35% | Copilot付费转化率; Azure增速维持26%+ |
| Alphabet | 中性偏多 | Cloud增速48%领跑+搜索AI化 | 30% | Cloud维持40%+增速; Gemini突破 |

**核心结论：**
1. 市场判断：AI仍处于早期增长阶段，CAGR 30.6%为十年级别确定性机会
2. 估值观点：三巨头Forward P/E均处于历史低位区间
3. 配置建议：NVDA+MSFT为核心仓(70%)，GOOGL为卫星仓(30%)
4. 时间窗口：2026年Q2-Q3为政策真空期+财报季窗口
5. 风控要点：设置15%止损线，关注AI Capex增速拐点

---

## 第8页：免责声明

本报告仅供内部参考，不构成任何投资建议。报告中的数据来源于公开市场信息和第三方研究机构，包括但不限于 Grand View Research、Statista、Yahoo Finance、Reuters、Motley Fool、AllInvestView 等。所有预测性陈述基于当前市场条件和公开信息，实际结果可能与预测存在重大差异。

数据截止日期：2026年5月10日

CONFIDENTIAL — FOR INTERNAL USE ONLY
"""

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"MD版本已保存至: {MD_FILE}")

print("\\n=== 生成完成 ===")
print(f"PPTX: {OUTPUT_FILE}")
print(f"MD:   {MD_FILE}")
