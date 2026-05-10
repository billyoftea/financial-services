#!/usr/bin/env python3
"""Generate CyberArk CIM Word document using python-docx."""
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\Lenovo\Desktop\financial-services-fork\financial-services\test-validation\IB_cim_builder_real_output.docx"

doc = Document()

# Default style
style = doc.styles["Normal"]
style.font.name = "SimSun"
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)


def shade(cell, color):
    s = OxmlElement("w:shd")
    s.set(qn("w:fill"), color)
    s.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(s)


def add_table(headers, rows, hc="1F4E79"):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(255, 255, 255)
        shade(c, hc)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = t.rows[ri + 1].cells[ci]
            c.text = str(val)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    return t


def heading1(text):
    h = doc.add_heading(text, level=1)
    for r in h.runs:
        r.font.color.rgb = RGBColor(31, 78, 121)


def heading2(text):
    doc.add_heading(text, level=2)


def bold_para(label, text=""):
    p = doc.add_paragraph()
    r = p.add_run(label)
    r.font.bold = True
    if text:
        p.add_run(text)


def para(text):
    doc.add_paragraph(text)


def bullet(text):
    doc.add_paragraph(text, style="List Bullet")


def pb():
    doc.add_page_break()


# ── COVER ──
for _ in range(6):
    doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("严格保密")
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(192, 0, 0)
r.font.bold = True

doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("机密信息备忘录")
r.font.size = Pt(28)
r.font.bold = True
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Confidential Information Memorandum")
r.font.size = Pt(16)
r.font.color.rgb = RGBColor(89, 89, 89)

doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CyberArk Software Ltd.")
r.font.size = Pt(22)
r.font.bold = True
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("NASDAQ: CYBR")
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(89, 89, 89)

doc.add_paragraph("")
doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("项目代号：Project Shield")
r.font.size = Pt(12)
r.font.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("编制日期：2026年5月")
r.font.size = Pt(12)

doc.add_paragraph("")
doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("本文件包含高度机密信息。未经事先书面同意，不得复制、分发或向任何第三方披露。")
r.font.size = Pt(9)
r.font.italic = True
r.font.color.rgb = RGBColor(128, 128, 128)

pb()

# ── DISCLAIMER ──
heading1("免责声明")
for t in [
    "本备忘录由卖方财务顾问编制，仅供合格潜在收购方评估对CyberArk Software Ltd.的潜在收购交易之用。",
    "本备忘录包含机密信息，未经公司或顾问事先书面同意，收件人不得复制、分发或向任何第三方披露本备忘录的全部或部分内容。",
    "本备忘录中的信息基于公司管理层提供的数据和公开可获取的信息，顾问未对信息的完整性和准确性进行独立验证。本备忘录不构成任何形式的要约或招揽。",
    "收件人应自行进行独立尽职调查，并咨询其法律、税务和财务顾问。",
]:
    para(t)
pb()

# ── TOC ──
heading1("目录")
for num, title, pages in [
    ("I.", "执行摘要", "1-3"),
    ("II.", "公司概况", "4-8"),
    ("III.", "行业概况", "9-13"),
    ("IV.", "增长机会", "14-16"),
    ("V.", "客户与销售", "17-21"),
    ("VI.", "运营", "22-25"),
    ("VII.", "财务概况", "26-33"),
    ("VIII.", "附录", "34-40"),
]:
    p = doc.add_paragraph()
    r = p.add_run(f"{num}  {title}")
    r.font.size = Pt(12)
    r.font.bold = True
    r = p.add_run(f"  ......  {pages}")
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(128, 128, 128)
pb()

# ═══════════════════════════════════════
# I. EXECUTIVE SUMMARY
# ═══════════════════════════════════════
heading1("I. 执行摘要")
heading2("1.1 公司简介")

para(
    "CyberArk Software Ltd.（NASDAQ: CYBR）是全球领先的身份安全平台公司，"
    "专注于特权访问管理（PAM）和身份威胁检测与响应（ITDR）领域。"
    "公司成立于1999年，总部位于美国马萨诸塞州Newton市，同时在以色列Petah Tikva设有研发中心。"
)
para(
    "CyberArk提供业界最全面的身份安全平台，覆盖人类身份和机器身份的全生命周期管理。"
    "公司已成功从传统许可模式转型为以SaaS订阅为核心的商业模式，FY2025订阅收入占总收入比例超过81%。"
)

bold_para("核心数据速览")
add_table(
    ["指标", "数值"],
    [
        ["FY2025 总收入", "$13.61亿"],
        ["收入同比增长", "36%"],
        ["FY2025 总ARR", "$14.4亿"],
        ["Non-GAAP营业利润率", "18%"],
        ["全球员工数", "~3,793人"],
        ["财富500强覆盖率", ">50%"],
        ["全球覆盖", "15+国家"],
    ],
)

heading2("1.2 投资亮点")
highlights = [
    ("1. 市场领导地位与品牌壁垒",
     "Gartner魔力象限PAM领域连续多年领导者象限。全球PAM市场份额第一，客户覆盖超过50%的财富500强企业。"),
    ("2. 强劲的收入增长轨迹",
     "FY2023至FY2025收入CAGR达34.4%。ARR从FY2022的$5.7亿增长至FY2025的$14.4亿。"),
    ("3. SaaS转型基本完成",
     "订阅收入FY2025达$11.05亿，占总收入81%+。订阅ARR占比约85%。"),
    ("4. 利润率持续改善",
     "Non-GAAP营业利润率从15%（FY2024）提升至18%（FY2025），营业利润增长63%。"),
    ("5. 战略收购构建全平台",
     "FY2024以$15.4亿收购Venafi；FY2025以$1.75亿收购Zilla Security。"),
    ("6. 巨大的TAM",
     "IAM市场2025年约$260亿（CAGR 10.4%）；数字身份解决方案约$470亿。"),
    ("7. 零信任与AI的结构性顺风",
     "全球企业加速采用零信任架构，AI/GenAI带来新的身份管理挑战和机遇。"),
]
for title, desc in highlights:
    bold_para(title + " — ", desc)

heading2("1.3 财务摘要")
add_table(
    ["指标", "FY2023", "FY2024", "FY2025"],
    [
        ["总收入", "$7.52亿", "$10.01亿", "$13.61亿"],
        ["收入同比增长", "27%", "33%", "36%"],
        ["总ARR", "$7.74亿", "$11.70亿", "$14.40亿"],
        ["订阅收入占比", "~60%", "~78%", "~81%"],
        ["Non-GAAP营业利润", "$0.63亿", "$1.51亿", "$2.47亿"],
        ["Non-GAAP营业利润率", "8.4%", "15.1%", "18.1%"],
    ],
)

heading2("1.4 交易概况")
add_table(
    ["项目", "描述"],
    [
        ["交易标的", "CyberArk Software Ltd. 100%股权"],
        ["交易结构", "待定（现金/股票混合或全部现金）"],
        ["指示性时间表", "第一轮报价截止：2026年Q3"],
        ["财务顾问", "[卖方顾问名称]"],
        ["法律顾问", "[法律顾问名称]"],
    ],
)
pb()

# ═══════════════════════════════════════
# II. COMPANY OVERVIEW
# ═══════════════════════════════════════
heading1("II. 公司概况")
heading2("2.1 历史沿革")
para("CyberArk由现任首席执行官Udi Mokady于1999年在以色列创立。公司最初专注于特权账户密码管理。")

bold_para("发展里程碑")
add_table(
    ["时间", "里程碑事件"],
    [
        ["1999", "Udi Mokady在以色列创立CyberArk"],
        ["2005", "推出Enterprise Password Vault"],
        ["2014", "纳斯达克IPO（CYBR），募资约$1.76亿"],
        ["2020", "加速SaaS转型，推出Privilege Cloud"],
        ["2024", "以$15.4亿收购Venafi"],
        ["2025", "以$1.75亿收购Zilla Security"],
        ["2025", "年收入突破$13.6亿，ARR达$14.4亿"],
    ],
)

heading2("2.2 使命与价值主张")
bold_para("使命：", '"保障全球领先组织免受网络攻击，通过全面保护人类和机器身份，消除最关键的安全漏洞。"')
for v in [
    "全面覆盖：唯一同时保护人类身份和机器身份的平台",
    "深度防御：从特权发现到威胁检测的端到端防护",
    "云原生架构：SaaS优先部署，支持混合云和多云",
    "生态集成：与100+安全工具和IT平台深度集成",
]:
    bullet(v)

heading2("2.3 产品与服务")
para("CyberArk Identity Security Platform产品组合：")

products = [
    ("Privileged Access Manager (PAM)", "旗舰产品，凭证保管、会话隔离、审计追踪"),
    ("Secrets Manager, SaaS", "云原生密钥管理，保护容器和CI/CD管道"),
    ("Machine Identity Security (原Venafi)", "TLS证书管理、代码签名、机器身份自动化"),
    ("Identity Governance (原Zilla Security)", "IGA平台，访问治理、合规审计"),
    ("Endpoint Privilege Manager", "端点最小权限管理、应用控制"),
    ("ITDR", "AI身份威胁检测、实时监控、自动响应"),
]
for name, desc in products:
    bold_para(f"{name} — ", desc)

heading2("2.4 商业模式与收入来源")
add_table(
    ["收入类型", "FY2023", "FY2024", "FY2025"],
    [
        ["订阅收入", "~$4.5亿 (60%)", "~$7.8亿 (78%)", "~$11.1亿 (81%)"],
        ["许可+维护", "~$2.2亿 (29%)", "~$1.5亿 (15%)", "~$1.4亿 (10%)"],
        ["专业服务", "~$0.8亿 (11%)", "~$0.7亿 (7%)", "~$1.1亿 (9%)"],
        ["总计", "$7.52亿", "$10.01亿", "$13.61亿"],
    ],
)

heading2("2.5 核心竞争优势")
for c in [
    "技术领先：80+项专利，20+年威胁情报积累",
    "市场定义者：创造PAM细分市场，Gartner连续多年领导者",
    "最完整产品线：PAM + 机器身份 + IGA + ITDR 四合一平台",
    "全球化运营：15+国家覆盖，30+语言支持",
]:
    bullet(c)
pb()

# ═══════════════════════════════════════
# III. INDUSTRY
# ═══════════════════════════════════════
heading1("III. 行业概况")
heading2("3.1 市场规模（TAM）")
add_table(
    ["市场细分", "2025年规模", "2030年预测", "CAGR"],
    [
        ["IAM", "~$260亿", "~$426亿", "10.4%"],
        ["PAM", "~$35亿", "~$65亿", "13.2%"],
        ["机器身份管理", "~$30亿", "~$60亿", "14.9%"],
        ["IGA", "~$80亿", "~$140亿", "11.8%"],
        ["ITDR", "~$20亿", "~$50亿", "20.1%"],
        ["身份安全总TAM", "~$470亿", "~$800亿+", "~11.5%"],
    ],
)

heading2("3.2 核心增长驱动因素")
for d in [
    "网络攻击损失超$9.5万亿，80%+勒索攻击涉及凭证盗窃",
    "零信任架构全球部署，身份是核心第一层",
    "机器身份数量已超人类45:1",
    "AI/GenAI带来新身份管理挑战",
    "NIS2、DORA、SEC合规要求持续推动",
]:
    bullet(d)

heading2("3.3 竞争格局")
add_table(
    ["竞争对手", "核心产品", "目标市场", "PAM份额", "优势", "劣势"],
    [
        ["CyberArk", "Identity Platform", "大型企业", "~30%", "产品最全、品牌最强", "价格较高"],
        ["BeyondTrust", "Privilege Mgmt", "中大型", "~15%", "端点管理强", "产品线较窄"],
        ["Delinea", "Secret Server", "中型市场", "~10%", "性价比高", "大企业能力不足"],
        ["Okta", "IAM/SSO", "中大型", "~5%", "生态强大", "PAM能力浅"],
        ["One Identity", "Active Roles", "大型企业", "~8%", "Quest整合", "策略不聚焦"],
    ],
)

heading2("3.4 进入壁垒")
for b in [
    "技术壁垒：PAM技术复杂度高，需多年研发积累",
    "客户切换成本：部署后切换成本极高",
    "合规认证壁垒：SOC 2、ISO 27001、FedRAMP认证周期长",
    "品牌信任壁垒：20+年安全运营记录",
]:
    bullet(b)
pb()

# ═══════════════════════════════════════
# IV. GROWTH OPPORTUNITIES
# ═══════════════════════════════════════
heading1("IV. 增长机会")
heading2("4.1 有机增长杠杆")
for t, d in [
    ("IGA新赛道", "市场规模$80亿，CAGR 11.8%，交叉销售转化率25-35%"),
    ("ITDR", "增长最快子市场（CAGR ~20%），防御+检测闭环"),
    ("AI身份安全", "AI代理身份管理是新市场空白，2026-2028年贡献收入"),
    ("地域扩张", "NIS2驱动欧洲、亚太政府项目"),
    ("定价优化", "增值模块、消费型定价、平台打包提升ARPU"),
]:
    bold_para(f"{t} — ", d)

heading2("4.2 收购机会")
add_table(
    ["方向", "市场规模", "战略价值", "预计交易规模"],
    [
        ["CIEM", "~$15亿", "多云权限管理", "$3-8亿"],
        ["IDV", "~$140亿", "用户身份验证", "$2-5亿"],
        ["ZTNA", "~$50亿", "完整零信任方案", "$5-10亿"],
        ["AI安全", "~$100亿", "AI工作负载保护", "$3-8亿"],
    ],
)

heading2("4.3 管理层预测")
add_table(
    ["指标（$M）", "FY2025A", "FY2026E", "FY2027E", "FY2028E"],
    [
        ["总收入", "$1,361", "$1,770", "$2,240", "$2,780"],
        ["增长率", "36%", "30%", "27%", "24%"],
        ["Non-GAAP OP", "$247", "$354", "$493", "$667"],
        ["OP利润率", "18%", "20%", "22%", "24%"],
        ["FCF", "$250", "$320", "$430", "$580"],
    ],
)
pb()

# ═══════════════════════════════════════
# V. CUSTOMERS & SALES
# ═══════════════════════════════════════
heading1("V. 客户与销售")
heading2("5.1 客户概况")
add_table(
    ["指标", "数据"],
    [
        ["总客户数", "~8,000+"],
        ["财富500强覆盖", ">50%（约260家）"],
        ["客户留存率", ">95%"],
        ["净留存率（NRR）", ">120%"],
    ],
)

heading2("5.2 行业分布")
add_table(
    ["行业", "占比", "代表客户"],
    [
        ["金融服务", "25%", "银行、保险、资管"],
        ["科技", "20%", "大型科技、SaaS"],
        ["政府/国防", "15%", "联邦机构、情报部门"],
        ["医疗健康", "12%", "医院、制药"],
        ["制造业", "10%", "工业4.0、汽车"],
        ["零售", "8%", "全球零售品牌"],
        ["能源", "6%", "电力、油气"],
    ],
)

heading2("5.3 匿名化大客户")
add_table(
    ["代号", "行业", "地区", "产品", "年合同价值"],
    [
        ["A", "金融", "北美", "PAM+Secrets+ITDR", "$5M+"],
        ["B", "科技", "北美", "Privilege Cloud+MI", "$4M+"],
        ["C", "政府", "EMEA", "全平台", "$3.5M+"],
        ["D", "医疗", "北美", "PAM+EPM", "$3M+"],
        ["E", "制造", "亚太", "PC+Secrets", "$2.5M+"],
        ["F", "能源", "EMEA", "PAM+MI", "$2M+"],
        ["G", "零售", "北美", "PAM+IGA", "$2M+"],
        ["H", "金融", "EMEA", "全平台", "$4.5M+"],
    ],
)
para("前10大客户占比<15%，最大单客<3%，无客户集中风险。")

heading2("5.4 销售周期与GTM")
add_table(
    ["客户类型", "周期", "ACV", "胜率"],
    [
        ["大企业(新)", "6-12月", "$50-200万", "35-45%"],
        ["大企业(扩展)", "3-6月", "$20-100万", "60-70%"],
        ["中型(新)", "3-6月", "$10-50万", "40-50%"],
        ["中型(扩展)", "1-3月", "$5-20万", "65-75%"],
    ],
)
for c in [
    "直销(55%)：大企业和政府",
    "渠道(30%)：Accenture/Deloitte/IBM",
    "云市场(10%)：AWS/Azure Marketplace",
    "数字(5%)：中小企业自助",
]:
    bullet(c)
pb()

# ═══════════════════════════════════════
# VI. OPERATIONS
# ═══════════════════════════════════════
heading1("VI. 运营")
heading2("6.1 全球布局")
add_table(
    ["地区", "办公室", "功能", "员工(估)"],
    [
        ["北美", "Newton, MA", "总部、销售", "~800"],
        ["北美", "San Jose", "销售、售前", "~200"],
        ["北美", "Herndon, VA", "联邦政府", "~150"],
        ["以色列", "Petah Tikva", "研发总部", "~1,000"],
        ["以色列", "Beer Sheva", "研发", "~200"],
        ["欧洲", "London", "EMEA总部", "~200"],
        ["亚太", "Singapore/Tokyo", "亚太销售", "~240"],
    ],
)

heading2("6.2 关键管理人员")
add_table(
    ["姓名", "职位", "任职时间", "背景"],
    [
        ["Udi Mokady", "CEO兼董事长", "1999至今", "创始人，Unit 8200出身"],
        ["Josh Siegel", "CFO", "2023年", "前Tesla财务高管"],
    ],
)

heading2("6.3 安全认证")
for c in ["SOC 2 Type II", "ISO 27001", "FedRAMP", "PCI DSS", "GDPR"]:
    bullet(c)
pb()

# ═══════════════════════════════════════
# VII. FINANCIAL OVERVIEW
# ═══════════════════════════════════════
heading1("VII. 财务概况")
heading2("7.1 历史利润表")
add_table(
    ["指标($M)", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],
    [
        ["总收入", "$464", "$503", "$592", "$752", "$1,001", "$1,361"],
        ["增长率", "7.0%", "8.3%", "17.7%", "27.1%", "33.1%", "36.0%"],
        ["毛利率", "~80%", "~81%", "~81%", "~82%", "~83%", "~84%"],
        ["Non-GAAP OP", "-", "-", "-", "$63", "$151", "$247"],
        ["OP利润率", "-", "-", "-", "8.4%", "15.1%", "18.1%"],
    ],
)

heading2("7.2 ARR分析")
add_table(
    ["指标($M)", "FY2022", "FY2023", "FY2024", "FY2025"],
    [
        ["期末ARR", "$570", "$774", "$1,170", "$1,440"],
        ["YoY增长", "-", "36%", "51%", "23%"],
        ["订阅ARR占比", "-", "~70%", "~84%", "~85%"],
    ],
)

heading2("7.3 利润率趋势")
add_table(
    ["指标", "FY2023", "FY2024", "FY2025"],
    [
        ["毛利率", "~82%", "~83%", "~84%"],
        ["研发费率", "~22.5%", "~22.0%", "~21.3%"],
        ["销售费率", "~43.4%", "~38.6%", "~35.6%"],
        ["管理费率", "~13.0%", "~11.2%", "~10.3%"],
        ["OP利润率", "~8.4%", "~15.1%", "~18.1%"],
    ],
)

heading2("7.4 现金流量")
add_table(
    ["指标($M)", "FY2023", "FY2024", "FY2025"],
    [
        ["经营现金流", "~$120", "~$200", "~$300"],
        ["资本支出", "~($30)", "~($40)", "~($50)"],
        ["自由现金流", "~$90", "~$160", "~$250"],
        ["FCF利润率", "~12%", "~16%", "~18%"],
    ],
)

heading2("7.5 管理层预测")
add_table(
    ["指标($M)", "FY2025A", "FY2026E", "FY2027E", "FY2028E"],
    [
        ["总收入", "$1,361", "$1,770", "$2,240", "$2,780"],
        ["增长率", "36%", "30%", "27%", "24%"],
        ["Non-GAAP OP", "$247", "$354", "$493", "$667"],
        ["OP利润率", "18%", "20%", "22%", "24%"],
    ],
)
pb()

# ═══════════════════════════════════════
# VIII. APPENDIX
# ═══════════════════════════════════════
heading1("VIII. 附录")

heading2("附录A：收入CAGR")
add_table(
    ["期间", "CAGR"],
    [
        ["FY2020-2025(5年)", "24.0%"],
        ["FY2022-2025(3年)", "32.1%"],
        ["FY2023-2025(2年)", "34.6%"],
    ],
)

heading2("附录B：产品目录")
add_table(
    ["产品", "类别", "部署", "核心功能"],
    [
        ["Privilege Cloud", "PAM", "SaaS", "凭证保管、会话隔离"],
        ["PAM Self-Hosted", "PAM", "本地", "密码保管库"],
        ["Secrets Manager", "密钥管理", "SaaS", "容器密钥"],
        ["Machine Identity", "机器身份", "混合", "TLS证书管理"],
        ["EPM", "端点安全", "混合", "最小权限"],
        ["ITDR", "威胁检测", "SaaS", "AI威胁检测"],
        ["Identity Governance", "IGA", "SaaS", "访问治理"],
    ],
)

heading2("附录C：数据来源")
for s in [
    "CyberArk官方新闻稿 (cyberark.com/press)",
    "Macrotrends (macrotrends.net)",
    "Yahoo Finance (finance.yahoo.com)",
    "MarketsandMarkets IAM报告",
    "Precedence Research",
    "Gartner MQ PAM",
    "SEC 10-K/10-Q",
]:
    bullet(s)

doc.add_paragraph("")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("— 本备忘录结束 —")
r.font.size = Pt(12)
r.font.bold = True
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("严格保密 — 未经书面授权不得复制或分发")
r.font.color.rgb = RGBColor(192, 0, 0)
r.font.bold = True

doc.save(OUTPUT)
print(f"Saved: {OUTPUT}")
print(f"Size: {os.path.getsize(OUTPUT)} bytes")
