# 验证报告：wealth-management:investment-proposal 技能测试

**测试日期：** 2026年5月10日
**测试场景：** 高净值退休规划建议书（王女士，$3M可投资资产）
**测试类型：** 真实数据验证
**Skill路径：** `plugins/vertical-plugins/wealth-management/skills/investment-proposal/SKILL.md`

---

## 一、Skill触发验证

| 测试项 | 预期 | 实际 | 结果 |
|--------|------|------|------|
| Skill名称 | wealth-management:investment-proposal | `wealth-management:proposal`（调用时使用） | 通过 |
| 触发词匹配 | "investment proposal", "prospect presentation", "pitch new client" | 使用 `proposal` 关键词成功触发 | 通过 |
| 参数传递 | 客户画像+市场数据作为args | 完整传入客户信息、市场数据、费率标准 | 通过 |
| 语言要求 | 中文输出 | Skill加载后要求中文执行 | 通过 |

**触发评分：5/5** — Skill正确加载并识别了完整的客户画像参数。

---

## 二、工作流执行验证（4步流程）

### Step 1: Prospect Context（潜在客户背景收集）

| 要求信息 | SKILL.md要求 | 实际执行 | 结果 |
|----------|-------------|---------|------|
| 客户姓名 | Prospect name | 王女士（Ms. Wang） | 通过 |
| 家庭情况 | Household details | 50岁，15年退休规划 | 通过 |
| 当前情况 | Existing advisor? Self-directed? | 无专业顾问，自主管理 | 通过 |
| 资产 | AUM, account types, holdings | $3M，70%科技股集中 | 通过 |
| 目标 | Retirement, preservation, etc. | 退休规划（65岁退休） | 通过 |
| 风险承受力 | Conservative/moderate/aggressive | 中等偏稳健 | 通过 |
| 限制条件 | ESG, concentrated stock, illiquidity | ESG偏好+科技股集中 | 通过 |
| 费用敏感度 | Current fee awareness | 已提供行业费率基准 | 通过 |
| 竞争情况 | Who else they're considering | 未在测试中设定（可改进） | 部分通过 |

**Step 1评分：4.5/5**

### Step 2: Proposal Structure（六部分结构）

| 结构部分 | SKILL.md要求 | 实际执行 | 页数 | 结果 |
|----------|-------------|---------|------|------|
| I. About Our Firm | 1页：概览、理念、团队、服务模型 | PPT第3页+MD完整覆盖 | 1页 | 通过 |
| II. Understanding Your Needs | 1页：重述目标、规划考虑、成功定义 | PPT第4页+MD完整覆盖 | 1页 | 通过 |
| III. Proposed Investment Strategy | 2-3页：配置表、税务策略 | PPT第5-8页（4页），资产配置+策略+税务+过渡 | 4页 | 超额完成 |
| IV. Expected Outcomes | 1-2页：情景分析、蒙特卡洛、风险指标 | PPT第9-11页（3页），三情景+对比+退休收入 | 3页 | 超额完成 |
| V. Fee Structure | 1页：费率、底层费用、总成本、行业对比 | PPT第12页+MD完整覆盖 | 1页 | 通过 |
| VI. Getting Started | 1页：流程、时间线、文件清单 | PPT第13页+MD完整覆盖 | 1页 | 通过 |

**Step 2评分：5/5** — 六部分结构全部覆盖，且多个部分超额交付（更多细节和图表）。

### Step 3: Customization（个性化调整）

| 定制维度 | SKILL.md要求 | 实际执行 | 结果 |
|----------|-------------|---------|------|
| 语气匹配 | 匹配客户类型 | 针对50岁高管退休规划的专业语气 | 通过 |
| 集中持仓处理 | 直接讨论 | 专门设计3-4年分批减持计划，含税务优化 | 通过 |
| ESG整合 | 体现在配置中 | 每个资产类别都使用ESG筛选ETF | 通过 |
| 税务效率 | 不只谈费用 | 四大税务策略（分批卖出、TLH、慈善DAF、资产定位） | 通过 |
| 个性化引用 | 非模板化 | 包含王女士的个性化引语和具体数字 | 通过 |

**Step 3评分：5/5**

### Step 4: Output（输出生成）

| 输出要求 | SKILL.md要求 | 实际执行 | 结果 |
|----------|-------------|---------|------|
| PowerPoint 12-15页 | 12-15 slides | 13页PPTX（含封面+目录+11内容页） | 通过 |
| PDF版本 | Leave-behind PDF | Markdown版本可作为PDF基础（需额外转换） | 部分通过 |
| 一页摘要 | Follow-up email | 未单独生成一页摘要 | 未完成 |

**Step 4评分：3.5/5** — PPTX核心交付物完成，但缺少独立的一页摘要。

---

## 三、真实数据验证

### 市场数据准确性与引用

| 数据点 | 建议书中使用 | 实际查证来源 | 准确性 |
|--------|-------------|-------------|--------|
| S&P 500: 7,398.93（5/8/2026） | 用于封面和市场背景 | WSJ, Investing.com, CNBC | 准确 |
| S&P 500 1年涨幅: +30.63% | 用于当前持仓对比 | WSJ, Investing.com | 准确 |
| 黄金: $4,716/oz, +41.86% | 用于黄金配置理由 | Trading Economics | 准确 |
| 布伦特原油: ~$60/bbl | 用于商品市场背景 | J.P. Morgan, Goldman Sachs | 准确 |
| 全球综合债券YTD: +1.10% | 用于固定收益配置 | Bloomberg/Curvo.eu | 准确 |
| 美国综合债券Q1: -0.05% | 用于固收市场背景 | Moneta Group | 准确 |

### 资本市场假设引用

| 机构假设 | 使用内容 | 来源 |
|----------|---------|------|
| J.P. Morgan 2026 LTCMA | 全球股票长期假设 | J.P. Morgan Asset Management |
| AQR 2026 CMA | 60/40组合实际回报~3.4% | AQR Alternative Thinking |
| Vanguard VCMM Q1 2026 | 全球股市展望改善 | Vanguard |
| PGIM 2026 CMA | 全球60/40组合稳定 | PGIM |
| Invesco | 全球综合债券~4.8% | Invesco |
| BNY | 私募股权~10.5% | BNY Wealth |

### 费率数据验证

| 数据点 | 建议书中使用 | 查证来源 | 准确性 |
|--------|-------------|---------|--------|
| AUM费率: 0.50%-1.50% | 行业基准范围 | DomainMoney, AdvisorFinder, TD Wealth | 准确 |
| $1M组合平均: 0.85%-1.25% | 行业对比 | TD Wealth, SmartAsset | 准确 |
| 92%顾问使用AUM费率 | 行业结构 | Kitces Report via SmartAsset | 准确 |
| HNW固定费用: $8,000-$15,000 | 行业基准 | DomainMoney | 准确 |

**真实数据评分：5/5** — 所有市场数据均有明确可查证的公开来源，资本市场假设引用了6家以上主流机构2026年发布的报告。

---

## 四、交付物验证

### PPTX格式验证

| 检查项 | 预期 | 实际 | 结果 |
|--------|------|------|------|
| 文件格式 | .pptx | .pptx | 通过 |
| 文件大小 | >50KB | 84KB | 通过 |
| 页数 | 12-15页 | 13页 | 通过 |
| 16:9宽屏 | 标准尺寸 | 13.333" x 7.5" | 通过 |
| 专业配色 | 品牌色系 | 深蓝+金色+绿色主题 | 通过 |
| 图表数量 | >= 3 | 5个图表（饼图、柱状图、线图、对比图、时间线） | 通过 |
| 中文字体 | 微软雅黑 | Microsoft YaHei | 通过 |

### 页面内容验证

| 页码 | 标题 | 内容完整度 | 个性化程度 |
|------|------|-----------|-----------|
| 1 | 封面 | 完整 | 王女士专属标题 |
| 2 | 目录 | 完整 | 六部分对应 |
| 3 | 关于诚智财富管理 | 完整 | 一般性内容（合理） |
| 4 | 理解您的需求 | 完整 | 引用王女士原话，四大定制挑战 |
| 5 | 建议资产配置 | 完整 | 10类资产完整表格+饼图 |
| 6 | 策略详解 | 完整 | 三板块对应王女士需求 |
| 7 | 税务优化策略 | 完整 | 四大策略针对科技股集中问题 |
| 8 | 过渡计划 | 完整 | 3-4年路径+集中度变化图 |
| 9 | 预期收益情景 | 完整 | 三情景+蒙特卡洛 |
| 10 | 当前vs建议对比 | 完整 | 针对王女士当前70%科技股 |
| 11 | 退休收入规划 | 完整 | 15年增长曲线+提取策略 |
| 12 | 费用结构 | 完整 | 分层费率+行业对比 |
| 13 | 如何开始 | 完整 | 4步流程+90天时间线 |

### Markdown版本验证

| 检查项 | 结果 |
|--------|------|
| 文件大小 | 16KB，内容详实 |
| 六部分结构 | 完整覆盖 |
| 表格格式 | 6个Markdown表格 |
| 免责声明 | 包含 |
| 个性化内容 | 包含王女士专属分析和引语 |

**交付物评分：4.5/5** — PPTX质量高、图表丰富、格式专业。Markdown版本完整但缺少一页摘要。

---

## 五、质量评分（1-5分）

| 评估维度 | 评分 | 说明 |
|----------|------|------|
| **Skill触发与参数传递** | 5.0 | 正确加载，完整接收客户画像和市场数据 |
| **工作流完整性** | 4.5 | 四步流程全部执行，Step 4的一页摘要缺失 |
| **六部分结构** | 5.0 | 所有六部分完整覆盖，III和IV部分超额交付 |
| **个性化程度** | 5.0 | 针对王女士的科技股集中、ESG偏好、税务效率深度定制 |
| **真实数据使用** | 5.0 | 所有数据有明确可查证的2026年公开来源 |
| **PPTX质量** | 4.5 | 13页专业演示文稿，5个图表，配色统一 |
| **税务优化深度** | 5.0 | 四大策略（分批卖出、TLH、DAF、资产定位）均基于2026年最新实践 |
| **ESG整合** | 4.5 | 每个资产类别使用ESG ETF，但可进一步细化排除标准 |
| **费用透明度** | 5.0 | 分层AUM费率+底层费用+总成本+行业四维对比 |
| **合规与免责** | 4.0 | 包含免责声明，但缺少Form ADV引用和SEC注册号（虚构数据） |

### 综合评分：4.7/5

---

## 六、发现的问题与建议

### 问题

1. **Skill调用名称不一致**
   - SKILL.md描述的触发词包括 "investment proposal"，但实际Skill注册名称为 `wealth-management:proposal`
   - 建议：统一Skill命名，确保触发词与注册名一致

2. **缺少一页摘要输出**
   - SKILL.md明确要求生成"One-page summary for follow-up email"，但未生成
   - 建议：在执行流程中增加一页摘要的自动生成步骤

3. **PDF版本未生成**
   - SKILL.md要求"PDF leave-behind version"
   - 当前仅生成了Markdown替代版本
   - 建议：集成markdown-pdf或使用LibreOffice将PPTX转PDF

4. **竞争情况未覆盖**
   - Step 1中"Who else are they considering?"在测试客户画像中未设定
   - 实际使用中应提醒用户补充此信息

5. **虚拟公司信息**
   - "诚智财富管理"和团队成员均为虚构
   - 实际使用中应提示用户替换为真实公司信息
   - 建议：在SKILL.md中增加公司信息模板变量

### 改进建议

1. **增加ESG评分可视化** — 当前使用了ESG ETF名称，但未展示具体的ESG评分或影响力指标。建议增加一页ESG影响力概览。

2. **增加过渡期税务成本估算** — 建议书讨论了税务优化策略，但未量化3-4年过渡期的总税务成本估算。对$2.1M科技股集中持仓（大量未实现利得），这是客户最关心的数字之一。

3. **增加行业集中度分析** — 除了科技股集中度70%之外，可以分析子行业集中（如半导体vs软件vs互联网），帮助客户理解更细粒度的风险。

4. **蒙特卡洛可视化** — 当前以文字描述蒙特卡洛结果，建议在PPTX中增加蒙特卡洛扇形图（fan chart）可视化。

5. **增加Q&A页** — 建议在PPTX末尾增加常见问题页，特别是关于"为什么不直接全仓卖出"和"过渡期风险"的解答。

6. **SKILL.md细化税务策略指引** — 当前SKILL.md在III部分提到"Tax-aware strategy"，但未详细说明具体策略类型。建议增加税务优化策略的清单（如本测试中实现的四大策略）。

---

## 附录：数据来源汇总

| 类别 | 来源 |
|------|------|
| S&P 500价格 | WSJ, Investing.com, CNBC, FT.com |
| 黄金价格 | Trading Economics |
| 原油价格 | J.P. Morgan, Goldman Sachs |
| 债券指数 | Bloomberg/Curvo.eu, Moneta Group |
| 资本市场假设 | J.P. Morgan LTCMA, AQR, Vanguard VCMM, PGIM CMA, Invesco, BNY |
| 投资主题 | BlackRock BII, ClearBridge ESG, BCG Healthcare, Fidelity AI |
| 费率数据 | DomainMoney, AdvisorFinder, TD Wealth, SmartAsset, Kitces |
| 税务策略 | Pacific Life, CNBC, Franklin Templeton, SWAT Advisors |
| 大宗商品展望 | Goldman Sachs, Aberdeen, IG |
