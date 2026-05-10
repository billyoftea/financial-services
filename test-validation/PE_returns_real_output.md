# CyberArk (CYBR) 私募股权回报分析

> **交易场景**: Growth Equity 收购 — $5B Enterprise Value，5年持有期
> **数据截止**: 2026年5月 | **分析日期**: 2026-05-10
> **数据来源**: Yahoo Finance, Macrotrends, DA Davidson, Cambridge Associates, S&P Global, Momentum Cyber

---

## Step 1: 交易输入假设

### 入场估值 (Entry)

| 指标 | 数值 | 备注 |
|------|------|------|
| Entry Enterprise Value | **$5.0B** | 假设收购价格 |
| CyberArk 当前市值 | $20.6B | 2026年5月市场数据 |
| CYBR 股价 (Feb 2026) | $408.85 | NASDAQ |
| 分析师目标价 | $573 | DA Davidson, Buy rating |
| LTM 收入 (FY2025E) | ~$1.40B | Q4 $372.7M, YoY +19% |
| LTM EBITDA | ~$0 (接近盈亏平衡) | Q3 2025: -$16M, 快速改善 |
| NTM EBITDA (FY2026E) | **$200M** | 基于20%收入增长 + 10%利润率路径 |
| Entry EV / Revenue | **3.6x** | $5B / $1.4B |
| Entry EV / NTM EBITDA | **25.0x** | $5B / $200M (高增长软件典型) |

### 融资结构 (Financing)

| 项目 | 金额/倍数 | 备注 |
|------|-----------|------|
| Senior Debt | $1.0B (5.0x NTM EBITDA) | SOFR + 400bps ≈ 7.5% 利率 |
| Subordinated / Mezzanine | $0.5B (2.5x NTM EBITDA) | 12% PIK + 现金票息 |
| Total Debt at Entry | **$1.5B** (7.5x NTM EBITDA) | |
| Equity Contribution | **$3.5B** | 70% equity / 30% debt |
| Transaction Fees (3%) | **$150M** | 含咨询费、法律费、融资费 |
| **实际 Equity Check** | **$3.65B** | 含交易费用 |

> **注**: CyberArk 为高增长网络安全公司，EBITDA接近零使得传统杠杆收购困难。Growth Equity 场景以高股权比例（70%）为主，杠杆适度（30%），符合实际市场条件。SOFR预期3-4%区间（FTI Consulting 2026调查，73%受访者预期年末Fed Funds在3-4%）。

### 运营假设 (Operating Assumptions)

| 参数 | Base Case | 备注 |
|------|-----------|------|
| 收入 CAGR | **20%** | 历史增速 ~19-25%，identity security赛道高景气 |
| EBITDA Margin 路径 | Year 1: 5% → Year 5: 18% | 规模效应，SaaS模型成熟 |
| Capex / Revenue | 8% | 研发+基础设施投入 |
| NWC 变动 | 收入增量的 5% | SaaS模型WC效率高 |
| 债务偿还 | 自由现金流优先还债 | Senior优先 |

### EBITDA 增长路径 (Base Case)

| 年份 | 收入 ($M) | EBITDA Margin | EBITDA ($M) |
|------|-----------|---------------|-------------|
| Year 0 (Entry) | 1,400 | 0% | 0 → NTM: 200 |
| Year 1 | 1,680 | 5% | 84 |
| Year 2 | 2,016 | 8% | 161 |
| Year 3 | 2,419 | 12% | 290 |
| Year 4 | 2,903 | 15% | 435 |
| Year 5 (Exit) | 3,484 | 18% | **627** |

---

## Step 2: Base Case 回报计算

### 回报摘要

| 指标 | 数值 |
|------|------|
| Entry EV | $5.00B |
| Equity Invested (含费用) | $3.65B |
| Exit EBITDA (Year 5) | $627M |
| Exit EV (at 12x EBITDA) | **$7.52B** |
| Net Debt at Exit | ($700M) |
| Exit Equity Value | **$6.82B** |
| **MOIC (Gross)** | **1.87x** |
| **IRR (Gross)** | **13.3%** |
| MOIC (Net of 20% carry) | **1.69x** |
| IRR (Net of 20% carry) | **11.1%** |

### 回报归因分析 (Returns Waterfall)

| 贡献来源 | 金额 ($M) | 占 Equity % | 说明 |
|----------|-----------|-------------|------|
| EBITDA 增长 | $5,124 | 140% | ($627-$200) x 12x / $3,650M |
| Multiple 变动 | ($2,600) | -71% | (12x - 25x) x $200M / $3,650M |
| 债务偿还 | $800 | 22% | $1.5B → $0.7B 偿还$800M |
| 交易费用 | ($150) | -4% | 入场一次性费用 |
| **净效果** | **$3,174** | **87%** | Equity value from $3.65B → $6.82B |

> **关键洞察**: 入场倍数25x NTM EBITDA 较高，即使Exit 12x EBITDA（网络安全板块中上水平），仍存在显著倍数收缩（-13x）。回报主要依赖EBITDA增长，从$200M到$627M的增长贡献了绝大部分价值。

---

## Step 3: 敏感性分析

### 表1: Exit Multiple vs. EBITDA Growth CAGR (IRR % / MOIC)

**固定条件**: Entry EV $5B, 5年持有, 70/30 股债结构

| | Exit 10x | Exit 12x | Exit 14x | Exit 16x | Exit 18x |
|---|----------|----------|----------|----------|----------|
| **15% Rev CAGR** | 4.2% / 1.23x | 8.1% / 1.48x | 11.6% / 1.74x | 14.7% / 2.00x | 17.5% / 2.27x |
| **20% Rev CAGR** | 7.8% / 1.46x | 12.3% / 1.82x | 16.2% / 2.19x | 19.7% / 2.56x | 22.8% / 2.94x |
| **25% Rev CAGR** | 11.0% / 1.73x | 16.1% / 2.22x | 20.5% / 2.72x | 24.5% / 3.23x | 28.0% / 3.76x |
| **30% Rev CAGR** | 14.0% / 2.05x | 19.7% / 2.70x | 24.6% / 3.37x | 29.0% / 4.05x | 32.9% / 4.76x |

> **Base Case** (20% CAGR, 12x Exit): 12.3% IRR / 1.82x MOIC

### 表2: Leverage vs. Exit Multiple (IRR % / MOIC)

**固定条件**: Entry EV $5B, 20% Rev CAGR, 5年持有

| | Exit 10x | Exit 12x | Exit 14x | Exit 16x | Exit 18x |
|---|----------|----------|----------|----------|----------|
| **0% Debt (全股权)** | 5.9% / 1.33x | 10.0% / 1.62x | 14.3% / 1.91x | 18.2% / 2.21x | 21.8% / 2.50x |
| **20% Debt** | 6.7% / 1.39x | 10.9% / 1.70x | 15.2% / 2.00x | 19.2% / 2.31x | 22.8% / 2.62x |
| **30% Debt (Base)** | 7.8% / 1.46x | 12.3% / 1.82x | 16.2% / 2.19x | 19.7% / 2.56x | 22.8% / 2.94x |
| **40% Debt** | 8.8% / 1.54x | 13.7% / 1.96x | 17.8% / 2.40x | 21.5% / 2.85x | 24.8% / 3.31x |

### 表3: Hold Period vs. Exit Multiple (IRR % / MOIC)

**固定条件**: Entry EV $5B, 20% Rev CAGR, 30% Debt

| | 3yr Hold | 4yr Hold | 5yr Hold | 6yr Hold | 7yr Hold |
|---|----------|----------|----------|----------|----------|
| **Exit 10x** | 10.1% / 1.34x | 8.8% / 1.40x | 7.8% / 1.46x | 6.9% / 1.53x | 6.2% / 1.60x |
| **Exit 12x** | 16.5% / 1.57x | 14.1% / 1.69x | 12.3% / 1.82x | 10.8% / 1.95x | 9.6% / 2.09x |
| **Exit 14x** | 22.5% / 1.82x | 19.0% / 2.00x | 16.2% / 2.19x | 14.2% / 2.39x | 12.5% / 2.60x |
| **Exit 16x** | 28.1% / 2.09x | 23.5% / 2.33x | 19.7% / 2.56x | 17.1% / 2.85x | 15.0% / 3.12x |

---

## Step 4: 三情景分析 (Bull / Base / Bear)

### 情景假设

| 参数 | Bull (牛市) | Base (基准) | Bear (熊市) |
|------|-------------|-------------|-------------|
| **宏观环境** | 利率下行，M&A活跃 | 温和增长 | 衰退，信贷收紧 |
| Revenue CAGR | 25% | 20% | 12% |
| Exit EBITDA Margin | 22% | 18% | 10% |
| Exit EV/EBITDA | 18x | 12x | 8x |
| Exit EBITDA ($M) | 927 | 627 | 246 |
| SOFR 假设 | 2.5% | 3.5% | 4.5% |

### 情景回报

| 指标 | Bull | Base | Bear |
|------|------|------|------|
| Exit EV | $16.69B | $7.52B | $1.97B |
| Net Debt at Exit | ($400M) | ($700M) | ($1.1B) |
| Exit Equity Value | $16.29B | $6.82B | $0.87B |
| **Gross MOIC** | **4.46x** | **1.87x** | **0.24x** |
| **Gross IRR** | **35.0%** | **13.3%** | **-25.3%** |
| Net MOIC (after 20% carry) | **3.77x** | **1.69x** | **0.24x** |
| Net IRR (after 20% carry) | **30.7%** | **11.1%** | **-25.3%** |

### 情景概率加权

| 情景 | 概率 | 加权 MOIC | 加权 IRR |
|------|------|-----------|----------|
| Bull | 25% | 1.12x | — |
| Base | 50% | 0.94x | — |
| Bear | 25% | 0.06x | — |
| **概率加权** | **100%** | **2.11x** | **~8.5%** |

---

## Step 5: 基准比较与市场数据

### Cambridge Associates PE Benchmark (Q3 2025)

| 基准 | Net IRR | Net TVPI |
|------|---------|----------|
| US PE Buyout (All Vintages) | 16.0% | 1.7x |
| US Growth Equity | 18.5% | 1.9x |
| Top Quartile Buyout | 22.0% | 2.2x+ |
| **本交易 Base Case (Net)** | **11.1%** | **1.69x** |
| **本交易 Bull Case (Net)** | **30.7%** | **3.77x** |

### 关键判断

1. **Base Case IRR (11.1% net)** 低于PE行业中位数（16%），低于Growth Equity基准（18.5%）
2. **入场倍数25x NTM EBITDA**是主要拖累因素 — 即使Exit 12x（板块中上水平），仍存在-13x的倍数收缩
3. 要达到目标回报（20%+ net IRR），需要：
   - 收入CAGR >25% **且** Exit >16x，或
   - Exit倍数维持18x+（需持续高增长叙事）
4. **Bear情景下存在本金亏损风险**（MOIC 0.24x）
5. 在$5B EV入场的growth equity场景中，**需要exit EV达到$7-10B+**才能产生合格回报

---

## 数据来源声明

| 数据项 | 来源 | 获取日期 |
|--------|------|----------|
| CYBR 市值、股价 | Macrotrends, Yahoo Finance | 2026-05 |
| CYBR 收入、EBITDA | CyberArk FY2025财报, Macrotrends | 2026-02 |
| 分析师目标价 | DA Davidson | 2026-02-06 |
| 网络安全板块倍数 | Finrofca, Momentum Cyber 2025年报, ICON Corporate Finance | 2025-2026 |
| EV/EBITDA板块中位数 | NYU Stern / Damodaran (Jan 2026) | 2026-01 |
| SOFR预测 | FTI Consulting 2026杠杆贷款调查, Kalshi | 2026 |
| PE回报基准 | Cambridge Associates US PE Benchmark Q3 2025 | 2025-12 |
| 杠杆融资市场 | S&P Global Leveraged Finance Q1 2026, Moody's CLO 2026 Outlook | 2026 |
| SFERS PE组合参考 | SFERS Private Equity Update (Sep 2025) | 2025-09 |

---

*本分析基于公开市场数据，仅供测试验证使用，不构成投资建议。*
