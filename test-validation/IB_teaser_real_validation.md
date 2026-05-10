# IB Teaser 技能验证报告 — 真实数据测试

**测试日期**：2026年5月10日
**测试技能**：`investment-banking:teaser`
**测试标的**：CyberArk (CYBR) — 身份安全领域领导者
**测试数据来源**：实时网络搜索（WebSearch）

---

## 一、技能触发验证

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 技能名称 | `investment-banking:teaser` | 正确调用 |
| 触发方式 | 通过 Skill tool 传入参数 | 符合预期 |
| SKILL.md 加载 | 成功读取完整工作流定义 | 路径：`plugins/vertical-plugins/investment-banking/skills/teaser/SKILL.md` |
| 语言要求 | 全程使用中文输出 | 符合 CLAUDE.md 要求 |

**评分：5/5** — 技能触发完全正常，SKILL.md 正确加载。

---

## 二、工作流执行验证

SKILL.md 定义了 4 步工作流，逐项检查：

### Step 1: Gather Inputs（收集输入）

| 输入项 | 是否收集 | 数据来源 | 数据真实性 |
|--------|----------|----------|------------|
| 公司描述 | 是 | CyberArk 官方新闻稿 | 真实 |
| 行业/细分 | 是 | 公开信息 | 真实 |
| 关键财务指标 | 是 | CyberArk Q3 FY2025 Earnings / Longbridge | 真实 |
| 地理布局 | 是 | 公开信息 | 真实 |
| 核心卖点 | 是 | 综合多源公开数据 | 真实 |
| 匿名化需求 | 是 | 已执行匿名化处理 | 符合要求 |
| 目标买方 | 是 | 涵盖战略及财务投资者 | 完整 |

**评分：5/5** — 输入收集完整，所有数据均来自真实市场公开信息。

### Step 2: Teaser Structure（Teaser 结构）

| 结构要素 | 是否包含 | 符合 SKILL.md 要求 |
|----------|----------|-------------------|
| 项目代号（"Project Sentinel"） | 是 | 符合 — 使用了 "Project [Name]" 格式 |
| 行业描述 | 是 | 符合 — "身份安全领域领先平台" |
| 机密标识 | 是 | 符合 — "机密文件 — 仅供讨论用途" |
| 公司描述（2-3句） | 是 | 符合 — 3句话，包含业务、市场地位、地理 |
| 投资亮点（4-6点） | 是 | 符合 — 6个要点，涵盖市场地位、收入质量、增长、并购、行业趋势、护城河 |
| 财务摘要表格 | 是 | 符合 — 包含 ARR、收入、增长率、市值、估值倍数 |
| 交易概述（2-3句） | 是 | 符合 — 包含交易类型、目标买方、时间表、联系方式 |
| 单页长度 | 基本符合 | Teaser 正文控制在一页可打印范围内 |

**评分：4/5** — 结构完全符合 SKILL.md 要求。轻微扣分：实际输出超过标准"一页"字数（约2,500字），在纯文本格式下略显冗长，但若转为 Word/PDF 排版可压缩至一页。

### Step 3: Anonymization Check（匿名化检查）

| 检查项 | 是否通过 | 说明 |
|--------|----------|------|
| 无公司名称 | 是 | 全文未出现 "CyberArk" 或 "CYBR"（附录除外） |
| 无品牌/产品名 | 是 | 未出现 CyberArk 产品线名称 |
| 无具体城市 | 是 | 仅使用区域描述："中东地区"、"北美、欧洲及亚太" |
| 无客户名称 | 是 | 仅描述为 "财富500强企业" |
| 员工数未暴露 | 是 | 未包含具体员工数量 |
| 收入使用区间 | 部分 | 财务表格包含具体数字，但已标注为推算值 |
| 无logo/截图 | 是 | 纯文本输出，无识别性图像 |

**评分：4/5** — 匿名化基本到位。轻微注意点：附录中包含真实公司名称（CyberArk），但附录是作为验证报告的数据溯源使用，不在正式 Teaser 分发内容范围内。实际分发时附录应移除。

### Step 4: Output（输出格式）

| SKILL.md 要求 | 实际输出 | 是否符合 |
|---------------|----------|----------|
| Word 文档 (.docx) | Markdown (.md) | **不符合** — SKILL 明确要求 Word 格式 |
| PDF 版本 | 未生成 | **不符合** |
| 可选 PowerPoint 版本 | 未生成 | 不适用（可选） |

**评分：2/5** — 这是本次测试的主要短板。SKILL.md 明确要求输出为 Word (.docx) 格式，并建议提供 PDF 版本。实际输出仅为 Markdown 文本。这与技能定义的专业交付标准存在差距。

---

## 三、数据真实性验证

| 数据点 | 输出中的数值 | 验证来源 | 是否准确 |
|--------|-------------|----------|----------|
| FY2025 ARR | $14.4亿 | Longbridge / CyberArk IR | 准确 |
| Q3 2025 ARR 同比增长 | +45% | CyberArk 官方 Q3 新闻稿 | 准确 |
| 订阅ARR | $11.6亿（86%占比） | CyberArk Q3 2025 Earnings | 准确 |
| 订阅ARR同比增速 | +57% | CyberArk Q3 2025 Earnings | 准确 |
| Q3 收入 | $3.428亿 | Cbonds / CyberArk IR | 准确 |
| 收入同比增速 | +43% | CyberArk 多季度报告 | 准确 |
| 市值 | ~$206亿 | CompaniesMarketCap / InsideArbitrage（2026年5月） | 准确 |
| 股价 | $408.85 | InsideArbitrage（2026年2月） | 准确（时点数据） |
| 2025年M&A总值 | $76-$102B | Return on Security + Tech Insider | 准确（不同统计口径） |
| M&A同比增长 | +66% | Return on Security | 准确 |
| 收购标的 | Venafi, Zilla | Alpha Spread / CyberArk IR | 准确 |
| 2026 Q1 M&A活跃度 | 34笔(1月), 38笔(3月), 33笔(4月) | LinkedIn / SecurityWeek / Tech Insider | 准确 |
| 网络安全TAM | 超$2,500亿 | Gartner / IDC 综合预测 | 合理（属多机构估算范围） |

**数据真实性总评**：所有关键财务数据和市场数据均可追溯到公开来源，且数值与原始来源一致。FY2024部分推算数据已明确标注。

**评分：5/5**

---

## 四、交付物质量评估

### 4.1 内容专业性

| 维度 | 评分(1-5) | 评价 |
|------|-----------|------|
| 语言专业度 | 4 | 使用了标准投行术语（ARR、PAM、NRR、TAM等），表述清晰专业 |
| 投资叙事质量 | 5 | 叙事逻辑完整：从市场地位到增长轨迹到战略价值，层层递进 |
| 财务数据呈现 | 4 | 表格格式清晰，同比对比直观；可增加 LTM / NTM 估值倍数对比 |
| 交易架构描述 | 4 | 交易类型、时间表、联系流程完整 |
| 买方吸引力 | 5 | 有效营造了稀缺性和竞争氛围（"全球最具战略价值的独立平台之一"） |

### 4.2 格式与排版

| 维度 | 评分(1-5) | 评价 |
|------|-----------|------|
| 文档格式 | 2 | SKILL 要求 Word (.docx)，实际输出 Markdown |
| 视觉呈现 | 3 | Markdown 格式可读，但缺少投行风格排版（如分隔线、logo占位、水印） |
| 信息密度 | 4 | 一页内信息密度适中，但投资亮点部分稍显密集 |
| 免责声明 | 5 | 包含完整的保密和法律免责条款 |

---

## 五、综合评分

| 评估维度 | 权重 | 得分 | 加权得分 |
|----------|------|------|----------|
| 技能触发 | 10% | 5/5 | 0.50 |
| 工作流完整性 | 20% | 4/5 | 0.80 |
| 数据真实性 | 25% | 5/5 | 1.25 |
| 内容专业度 | 25% | 4.5/5 | 1.13 |
| 输出格式合规 | 20% | 2/5 | 0.40 |
| **总计** | **100%** | — | **4.08 / 5** |

**综合评分：4.1 / 5**

---

## 六、关键发现与改进建议

### 优势

1. **数据真实性极佳**：所有核心财务数据均来自实时网络搜索，可追溯到 CyberArk 官方新闻稿、SEC 文件和权威行业报告，无任何虚构或编造数据
2. **投资叙事专业**：Teaser 成功构建了从行业定位、收入质量、增长轨迹到战略价值的完整投资叙事，语言符合投行卖方文档标准
3. **匿名化到位**：核心 Teaser 正文完全匿名，不包含任何可直接识别公司的信息
4. **市场背景扎实**：充分利用了 2025-2026 年网络安全 M&A 市场数据，为交易提供了有说服力的行业背景

### 不足

1. **输出格式不符**：SKILL.md 明确要求 Word (.docx) 格式输出，实际仅生成了 Markdown。这是最显著的偏差——在真实投行流程中，Teaser 必须以专业排版的 Word/PDF 文件交付
2. **缺少 PDF 生成**：SKILL.md 建议同时生成 PDF 版本用于分发，未执行
3. **篇幅偏长**：虽然信息密度高，但部分投资亮点可进一步精简以适配单页物理排版
4. **估值倍数数据不完整**：仅提供了 EV/Revenue ~15x 的估算，可补充 EV/ARR、EV/EBITDA 等更细致的估值参照

### 改进建议

1. **[高优先级] 实现 Word 输出**：使用 `python-docx` 库将 Markdown 内容转换为格式化的 Word 文档，包含投行风格排版（项目代号水印、保密标识、专业字体）
2. **[中优先级] 精简篇幅**：将投资亮点从 6 点压缩至 4-5 点，每点控制在 2 行以内，确保单页打印适配
3. **[中优先级] 增加估值参考**：补充可比交易乘数（如 Okta/SailPoint/ForgeRock 的 EV/ARR 倍数），增强定价参考
4. **[低优先级] 附录分离**：在正式分发版本中移除数据溯源附录，仅保留正文 Teaser 内容

---

## 七、数据溯源

本次测试使用的所有真实数据均来自以下公开来源的网络搜索结果：

1. [CyberArk Q3 2025 Earnings Press Release](https://www.cyberark.com/press/cyberark-announces-strong-third-quarter-2025-results/)
2. [Return on Security — 2025 State of the Cybersecurity Market](https://www.returnonsecurity.com/p/2025-state-of-the-cybersecurity-market)
3. [ION Analytics — Cybersecurity M&A 2025-2026](https://ionanalytics.com/insights/mergermarket/cybersecurity-ma-stalls-after-2025-surge-as-ai-resets-valuations-dealspeak-north-america/)
4. [CompaniesMarketCap — CyberArk Market Cap](https://companiesmarketcap.com/cyberark/marketcap/)
5. [InsideArbitrage — CYBR Stock Data](https://www.insidearbitrage.com/symbol-metrics/CYBR)
6. [Longbridge — CyberArk FY2025 ARR](https://longbridge.com/en/news/274810380)
7. [Cbonds — CyberArk Q3 Revenue](https://cbonds.com/news/3668111/)
8. [SecurityWeek — Cybersecurity M&A April 2026](https://www.securityweek.com/cybersecurity-ma-roundup-33-deals-announced-in-april-2026/)
