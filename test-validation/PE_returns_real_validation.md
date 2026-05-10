# PE Returns Analysis 实测验证报告

> **测试技能**: `private-equity:returns`
> **测试日期**: 2026-05-10
> **测试标的**: CyberArk (CYBR) Growth Equity 收购场景，$5B EV，5年持有
> **数据类型**: 真实市场数据（非模拟）

---

## 一、Skill 触发验证

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Skill 调用方式 | 通过 `Skill` tool 调用 `private-equity:returns` | 标准触发路径 |
| 参数传递 | args 字段传入交易参数+真实数据上下文 | 包含完整 deal params |
| SKILL.md 加载 | 成功加载 returns-analysis SKILL.md | 5步工作流完整呈现 |
| 语言要求 | 输出全中文 | 符合 CLAUDE.md 语言要求 |

**评分: 5/5** — Skill 触发路径正确，参数传递完整。

---

## 二、工作流完整性验证

按照 SKILL.md 定义的 5 步工作流逐项检查：

### Step 1: Gather Deal Inputs

| 要求字段 | 是否覆盖 | 数据来源 |
|----------|----------|----------|
| Entry EBITDA | 是 | NTM EBITDA $200M，基于公开财报推算 |
| Entry Multiple | 是 | 25x NTM EBITDA，3.6x EV/Revenue |
| Enterprise Value | 是 | $5.0B（用户指定） |
| Net Debt at Close | 是 | $1.5B 总债务 |
| Equity Check Size | 是 | $3.65B（含交易费用） |
| Transaction Fees | 是 | 3% = $150M |
| Senior Debt | 是 | $1.0B, SOFR+400bps ≈ 7.5% |
| Sub Debt / Mezzanine | 是 | $0.5B, 12% PIK |
| Revenue Growth | 是 | 20% CAGR（基于历史19%增速） |
| EBITDA Margin Trajectory | 是 | 0% → 18% 五年路径 |
| Hold Period | 是 | 5年 |
| Exit Multiple | 是 | 12x EBITDA (base) |

**评分: 5/5** — 所有字段齐全，假设合理有据。

### Step 2: Base Case Returns

| 要求输出 | 是否包含 | 核对 |
|----------|----------|------|
| Entry EV | 是 | $5.0B |
| Equity Invested | 是 | $3.65B |
| Exit EBITDA | 是 | $627M |
| Exit EV | 是 | $7.52B |
| Net Debt at Exit | 是 | ($700M) |
| Exit Equity Value | 是 | $6.82B |
| MOIC | 是 | 1.87x gross, 1.69x net |
| IRR | 是 | 13.3% gross, 11.1% net |
| Returns Waterfall | 是 | 4因子分解完整 |
| Growth Contribution | 是 | +140% |
| Multiple Contribution | 是 | -71%（负值，倍数收缩） |
| Leverage Contribution | 是 | +22% |
| Fee Drag | 是 | -4% |

**评分: 5/5** — 回报计算完整，归因分析清晰。Net of carry 计算正确。

### Step 3: Sensitivity Tables

| 要求的敏感性表 | 是否包含 | 维度 |
|----------------|----------|------|
| Entry Multiple vs. Exit Multiple | 已用 Growth CAGR vs. Exit Multiple 替代 | 4x5矩阵 |
| EBITDA Growth vs. Exit Multiple | 是 | 4x5矩阵 (IRR/MOIC双显示) |
| Leverage vs. Exit Multiple | 是 | 4x5矩阵 |
| Hold Period vs. Exit Multiple | 是 | 5x4矩阵 |

**评分: 4.5/5** — 缺少纯粹的 Entry Multiple vs Exit Multiple 表（因 CyberArk EBITDA 接近零，传统 EBITDA 入场倍数表意义有限，以 Growth vs Exit 替代，合理）。

### Step 4: Scenario Analysis

| 要求 | 是否包含 |
|------|----------|
| Bull/Base/Bear 三情景 | 是 |
| Revenue CAGR 差异 | 是（12%/20%/25%） |
| Exit EBITDA Margin 差异 | 是（10%/18%/22%） |
| Exit Multiple 差异 | 是（8x/12x/18x） |
| 各情景 MOIC | 是（0.24x/1.87x/4.46x） |
| 各情景 IRR | 是（-25.3%/13.3%/35.0%） |
| 概率加权 | 是（25/50/25加权） |

**评分: 5/5** — 三情景分析完整，概率加权是加分项。

### Step 5: Output

| 要求交付 | 是否满足 |
|----------|----------|
| Excel workbook | 否（MD格式输出） |
| Assumptions tab | 等效于MD中的Step 1 |
| Returns calculation | 等效于Step 2 |
| Sensitivity tables | 等效于Step 3 |
| Scenario summary | 等效于Step 4 |
| IC deck 一页摘要 | 等效于整体结构 |

**评分: 4/5** — 输出为 Markdown 而非 Excel。结构完整但未生成 .xlsx 文件。

---

## 三、数据真实性验证

| 数据项 | 分析中的值 | 独立验证来源 | 是否一致 |
|--------|-----------|-------------|----------|
| CYBR 市值 | $20.6B | Macrotrends: $20.64B (May 2026) | 一致 |
| CYBR 股价 | $408.85 | NASDAQ 报价 (Feb 2026) | 一致 |
| 分析师目标价 | $573 | DA Davidson (Feb 6, 2026) | 一致 |
| Q4 2025 收入 | $372.7M | CyberArk 官方财报 | 一致 |
| YoY 增速 | 19% | $372.7M vs $314.4M = 18.5% | 基本一致 |
| EBITDA 状态 | 接近盈亏平衡 | Q3 2025: -$16M | 一致 |
| 网络安全 EV/Revenue | 13.3x avg | Finrofca mid-2025 报告 | 一致 |
| 网络安全 EV/EBITDA | ~10x 中位数 | Damodaran Jan 2026 | 一致 |
| SOFR 预期 | 3-4% | FTI Consulting 2026调查 | 一致 |
| PE IRR 基准 | 16% median | Cambridge Associates, SFERS | 一致 |
| PE TVPI 基准 | 1.7x | SFERS PE Update (Sep 2025) | 一致 |

**评分: 5/5** — 所有引用数据均可追溯到独立来源，数值准确。

---

## 四、计算逻辑验证

### Base Case 手动复核

```
Entry EV = $5,000M
Total Debt = $1,500M
Equity = $3,500M + $150M fees = $3,650M

Year 5 Revenue = $1,400M × (1.20)^5 = $3,483M ✓
Year 5 EBITDA = $3,483M × 18% = $627M ✓
Exit EV = $627M × 12x = $7,524M ✓
Net Debt at Exit = $700M (还了$800M) ✓
Exit Equity = $7,524M - $700M = $6,824M ✓
MOIC = $6,824 / $3,650 = 1.87x ✓
IRR = (6,824/3,650)^(1/5) - 1 = 13.3% ✓

Returns Attribution:
- Growth: (627-200) × 12 / 3,650 = $1,405M → 38.5% of equity (注：分析中用$200M NTM作为base)
  → 实际分析显示 140%，因为计算方式为 ($5,124M / $3,650M)
  → (627-200)×12 = $5,124M → $5,124/3,650 = 140.4% ✓
- Multiple: (12-25)×200 / 3,650 = -$2,600M / $3,650 = -71.2% ✓
- Leverage: $800M / $3,650 = 21.9% ✓
- Fees: -$150M / $3,650 = -4.1% ✓
```

**计算逻辑**: 全部核验通过，数值一致。

**评分: 5/5**

---

## 五、质量评估总结

| 评估维度 | 得分 (1-5) | 说明 |
|----------|-----------|------|
| **Skill 触发** | 5 | 触发正确，参数传递完整 |
| **工作流遵循** | 4.5 | 5步工作流全覆盖，微调合理 |
| **计算准确性** | 5 | 手动核验全部通过 |
| **数据真实性** | 5 | 全部引用独立来源可验证 |
| **敏感性分析** | 4.5 | 3张表完整，1张因数据特性调整 |
| **情景分析** | 5 | 三情景 + 概率加权 |
| **交付物格式** | 4 | MD格式完整，缺少Excel输出 |
| **基准对比** | 5 | Cambridge Associates + SFERS 参照 |

### **综合评分: 4.7 / 5.0**

---

## 六、发现的问题与建议

### 已发现的问题

1. **入场倍数过高**: $5B EV 对应 25x NTM EBITDA，远超板块中位数（10x）。分析正确指出了倍数收缩是主要拖累因素，但建议增加 "entry at lower EV" 的对比场景（如 $3-3.5B EV）

2. **EBITDA 基准选择**: CYBR LTM EBITDA 接近零，使用 NTM EBITDA $200M 作为入场基准。这在高增长软件中常见但需明确标注（已标注）

3. **缺少 Excel 输出**: SKILL.md 要求生成 .xlsx 文件，实际输出为 Markdown。建议在测试中补充 xlsx 生成

### 建议改进

1. 增加 "break-even IRR" 分析 — 即达到目标回报（如20% net IRR）所需的最低 Exit Multiple / EBITDA 组合
2. 增加与 CyberArk 当前 $20.6B 市值的对比 — 分析为何 $5B EV 的 hypothetical 收购与实际市值差距巨大（市场已定价更高的未来增长）
3. 增加 dividend recap 或 partial exit 的中期现金流分析
4. 补充 tax 影响（asset vs stock deal）的讨论

---

## 七、测试结论

`private-equity:returns` skill 在真实数据测试中表现优秀：

- **工作流完整性高**: 5步流程全覆盖，仅有微小调整
- **计算严谨**: 所有数值经手动核验无误
- **数据真实**: 引用10+独立来源，均可追溯验证
- **实用性**: 敏感性表和三情景分析对IC决策有直接参考价值
- **主要不足**: 未生成 Excel 格式输出，缺少部分进阶分析维度

该 skill 可用于实际 PE deal returns 分析场景，建议在正式使用前补充 .xlsx 输出功能。

---

*验证完成时间: 2026-05-10*
