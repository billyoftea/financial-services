#!/usr/bin/env python3
"""
NVIDIA (NVDA) Strip Profile Generator
按照 SKILL.md 工作流生成4:3比例的投行级单页公司概况幻灯片
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ========================================
# NVIDIA 品牌色系（来自官方品牌指南）
# ========================================
NVIDIA_GREEN = RGBColor(0x76, 0xB9, 0x00)  # NVIDIA 主品牌绿色
NVIDIA_DARK = RGBColor(0x1A, 0x1A, 0x1A)   # 深黑
HEADER_BLUE = RGBColor(0x00, 0x33, 0x66)    # 深蓝色标题
DARK_TEXT = RGBColor(0x33, 0x33, 0x33)       # 正文深灰
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)     # 表格边框
TABLE_HEADER_BG = RGBColor(0x00, 0x33, 0x66) # 表头背景
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# ========================================
# 创建4:3幻灯片
# ========================================
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

slide_layout = prs.slide_layouts[6]  # 空白布局
slide = prs.slides.add_slide(slide_layout)

# ========================================
# 标题区域 (y=0.15)
# ========================================
# NVIDIA绿色装饰线
slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0.3), Inches(0.15), Inches(9.4), Inches(0.04),
).fill.solid()
slide.shapes[-1].fill.fore_color.rgb = NVIDIA_GREEN
slide.shapes[-1].line.fill.background()

# 公司名称和Ticker
title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.22), Inches(7.5), Inches(0.4))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
run = p.add_run()
run.text = "NVIDIA Corporation (NVDA)"
run.font.size = Pt(22)
run.font.bold = True
run.font.color.rgb = NVIDIA_DARK
run.font.name = "Arial"

# 副标题：行业标签
sub_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.58), Inches(7.5), Inches(0.22))
tf = sub_box.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Semiconductors & AI Computing  |  NASDAQ  |  Market Cap: $5.22T (#1 Global)"
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
run.font.name = "Arial"

# ========================================
# 分隔线 (顶部/底部象限之间)
# ========================================
def add_divider(y_pos):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.3), Inches(y_pos), Inches(9.4), Inches(0.008),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_GRAY
    shape.line.fill.background()

# 顶部象限和底部象限之间的分隔线
add_divider(3.65)

# ========================================
# 辅助函数：添加象限头部（带绿色竖条）
# ========================================
def add_quadrant_header(x, y, text):
    """添加带绿色竖条的象限标题"""
    # 绿色竖条
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(0.06), Inches(0.22),
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NVIDIA_GREEN
    bar.line.fill.background()

    # 标题文字
    tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y - 0.02), Inches(4.3), Inches(0.28))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = HEADER_BLUE
    run.font.name = "Arial"

# ========================================
# 辅助函数：添加要点内容
# ========================================
def add_bullets(x, y, w, h, bullets, font_size=9):
    """添加要点列表，每个bullet一行"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True

    for i, bullet_text in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        run = p.add_run()
        run.text = bullet_text
        run.font.size = Pt(font_size)
        run.font.color.rgb = DARK_TEXT
        run.font.name = "Arial"
        p.space_after = Pt(2)
        p.space_before = Pt(1)

    return tb

# ========================================
# 象限1：公司概况 (左上, x=0.3, y=0.85, w=4.7, h=2.7)
# ========================================
add_quadrant_header(0.3, 0.85, "Company Overview")

q1_bullets = [
    "HQ: Santa Clara, CA; Founded: 1993; ~36,000 employees",
    "CEO: Jensen Huang (co-founder); CFO: Colette Kress",
    "Market Cap: $5.22T — #1 globally by market capitalization",
    "Enterprise Value: ~$5.10T; Ticker: NASDAQ: NVDA",
    "Core Business: GPU & AI chip design; CUDA software ecosystem",
    "Key Products: H100/H200/B200 GPUs, DGX systems, NVIDIA AI Enterprise",
    "Competitive Moat: CUDA ecosystem (20M+ developers), 80%+ AI training market share",
    "Geographic Mix: US ~45%, China ~12%, Taiwan ~10%, Other ~33%",
]

add_bullets(0.42, 1.15, 4.5, 2.35, q1_bullets, font_size=8.5)

# ========================================
# 象限2：业务与定位 (右上, x=5.0, y=0.85, w=4.7, h=2.7)
# ========================================
add_quadrant_header(5.0, 0.85, "Business & Positioning")

q2_bullets = [
    "Primary Driver: Data Center AI (89.8% of revenue, $193.7B in FY26)",
    "Gaming: 7.4% ($16.0B) — GeForce RTX series, GeForce NOW cloud gaming",
    "Professional Visualization: 1.5% ($3.2B) — Quadro/RTX workstation GPUs",
    "Automotive: 1.3% ($2.8B) — DRIVE platform for autonomous vehicles (+72% YoY)",
    "Blackwell Ultra (B200) architecture in full production, driving data center demand",
    "Networking: InfiniBand & Ethernet (14.4% of DC revenue); Mellanox acquisition integration",
    "AI inference market growing rapidly; NVIDIA positioned across training + inference",
    "Top customers: Hyperscalers (Microsoft, Google, Meta, Amazon) collectively >40% of DC revenue",
]

add_bullets(5.12, 1.15, 4.5, 2.35, q2_bullets, font_size=8.5)

# ========================================
# 象限3：核心财务数据 (左下, x=0.3, y=3.75, w=4.7, h=3.5)
# 使用表格展示
# ========================================
add_quadrant_header(0.3, 3.75, "Key Financials & Valuation")

# 构建表格数据
table_data = [
    ["Metric",       "FY24 (Jan'24)", "FY25 (Jan'25)", "FY26 (Jan'26)"],
    ["Revenue",      "$60.9B",        "$130.5B",       "$215.9B"],
    ["Revenue Growth", "+126% YoY",   "+114% YoY",    "+65% YoY"],
    ["EBITDA",       "$25.6B",        "~$80.0B",      "~$140.0B"],
    ["EBITDA Margin", "~42%",         "~61%",         "~65%"],
    ["Net Income",   "$29.8B",        "$72.9B",       "~$95.0B"],
    ["EPS",          "$1.20",         "$2.95",        "$3.90"],
    ["Free Cash Flow", "~$20.0B",    "~$60.0B",      "~$90.0B"],
    ["P/E Ratio",    "—",            "—",            "37.98x"],
    ["EV/EBITDA",    "—",            "—",            "~36x"],
    ["EV/Revenue",   "—",            "—",            "~24x"],
]

rows = len(table_data)
cols = len(table_data[0])
table = slide.shapes.add_table(
    rows, cols,
    Inches(0.42), Inches(4.05),
    Inches(4.5), Inches(3.1)
).table

# 设置列宽
table.columns[0].width = Inches(1.35)
table.columns[1].width = Inches(1.05)
table.columns[2].width = Inches(1.05)
table.columns[3].width = Inches(1.05)

# 填充表格
for r_idx, row_data in enumerate(table_data):
    for c_idx, cell_text in enumerate(row_data):
        cell = table.cell(r_idx, c_idx)
        cell.text = cell_text

        # 设置单元格格式
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(8)
            paragraph.font.name = "Arial"
            paragraph.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

            if r_idx == 0:
                # 表头样式
                paragraph.font.bold = True
                paragraph.font.color.rgb = WHITE
                paragraph.font.size = Pt(8)

        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

        # 表头背景色
        if r_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = TABLE_HEADER_BG
        elif r_idx % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE

# ========================================
# 象限4：股权结构与近期动态 (右下, x=5.0, y=3.75, w=4.7, h=3.5)
# ========================================
add_quadrant_header(5.0, 3.75, "Ownership & Recent Developments")

# 分为两个子区域：上部为股东信息，下部为近期动态
# 股东信息
owner_title = slide.shapes.add_textbox(Inches(5.12), Inches(4.05), Inches(4.5), Inches(0.2))
tf = owner_title.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Top Shareholders:"
run.font.size = Pt(8.5)
run.font.bold = True
run.font.color.rgb = DARK_TEXT
run.font.name = "Arial"

owner_bullets = [
    "Vanguard Group: 7.5%  |  BlackRock: 6.8%  |  FMR (Fidelity): 4.5%",
    "State Street: 3.5%  |  Geode Capital: 2.5%  |  Jensen Huang (CEO): ~3.5%",
    "Institutional Ownership: ~65% of total shares outstanding",
]

add_bullets(5.12, 4.25, 4.5, 0.7, owner_bullets, font_size=8)

# 近期动态标题
dev_title = slide.shapes.add_textbox(Inches(5.12), Inches(4.95), Inches(4.5), Inches(0.2))
tf = dev_title.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Recent Developments (90 Days):"
run.font.size = Pt(8.5)
run.font.bold = True
run.font.color.rgb = DARK_TEXT
run.font.name = "Arial"

dev_bullets = [
    "Q4 FY26 revenue $68.1B, record high (+73% YoY); FY26 total $215.9B (+65% YoY)",
    "Q1 FY27 revenue guidance ~$78B (±2%), indicating continued strong momentum",
    "US govt shifts H200/MI325X export policy to case-by-case review for China",
    "Blackwell Ultra (B200) architecture in full mass production driving DC demand",
    "Long-term revenue outlook exceeds $500B target; FY27 consensus ~$323.3B",
    "37 analysts maintain consensus 'Buy' rating; avg price target ~$272",
]

add_bullets(5.12, 5.15, 4.5, 1.6, dev_bullets, font_size=8)

# ========================================
# 一致预期数据（放在象限4底部小框）
# ========================================
est_title = slide.shapes.add_textbox(Inches(5.12), Inches(6.65), Inches(4.5), Inches(0.18))
tf = est_title.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Consensus Estimates:"
run.font.size = Pt(8)
run.font.bold = True
run.font.color.rgb = DARK_TEXT
run.font.name = "Arial"

est_text = slide.shapes.add_textbox(Inches(5.12), Inches(6.82), Inches(4.5), Inches(0.35))
tf = est_text.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
run = p.add_run()
run.text = "FY27E Revenue: ~$323.3B (+50% YoY) | FY27E EPS: raised ~14% | NTM EV/Revenue: ~16x"
run.font.size = Pt(7.5)
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
run.font.name = "Arial"

# ========================================
# 页脚/数据来源
# ========================================
footer_box = slide.shapes.add_textbox(Inches(0.3), Inches(7.15), Inches(9.4), Inches(0.25))
tf = footer_box.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "Sources: NVIDIA IR, Yahoo Finance, Macrotrends, SEC EDGAR, Analyst Reports  |  Data as of May 2026  |  All amounts in USD"
run.font.size = Pt(7)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.font.name = "Arial"
p.alignment = PP_ALIGN.LEFT

# ========================================
# 保存文件
# ========================================
output_path = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\IB_strip_profile_real_output.pptx"
prs.save(output_path)
print(f"PPTX 已保存到: {output_path}")
