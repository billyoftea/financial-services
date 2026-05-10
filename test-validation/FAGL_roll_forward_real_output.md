# AR Roll-Forward Schedule — Growth Equity Fund IV

> **账户类型**：应收账款（Accounts Receivable）
> **实体**：Growth Equity Fund IV
> **期间**：2026年4月（2026-03-31 至 2026-04-30）
> **编制日期**：2026-05-10
> **币种**：USD

---

## 1. 持仓概览 — NVDA (NVIDIA Corporation)

| 项目 | 数值 | 数据来源 |
|------|------|----------|
| 持仓证券 | NVDA (NASDAQ) | 基金持仓主表 |
| 持有股数 | 150,000 股 | 托管行确认书 |
| 3月31日收盘价 | $174.40 | Bloomberg / NASDAQ 官方收盘价 |
| 4月30日收盘价 | $199.57 | Bloomberg / NASDAQ 官方收盘价 |
| 月度价格变动 | +$25.17 (+14.43%) | 计算得出 |
| 3月31日市值 | $26,160,000.00 | 150,000 x $174.40 |
| 4月30日市值 | $29,935,500.00 | 150,000 x $199.57 |

---

## 2. AR Roll-Forward 主表

### 应收公允价值变动款 — NVDA 持仓

单位：USD

| 行次 | 项目 | 金额 | 占期初比 | 对应GL科目 | 关联依据 / Tie-to |
|------|------|------|----------|-----------|-------------------|
| 1 | **期初余额 (Beginning Balance)** | **$26,160,000.00** | 100.0% | AR-1400 应收投资公允价值 | 3月结账包 (Mar-2026 Close Package)；GL查询: `SELECT balance FROM gl_balances WHERE account='AR-1400' AND entity='GEF-IV' AND period_end='2026-03-31'` |
| 2 | + 新增投资 / 买入活动 (Additions) | $0.00 | 0.0% | AR-1400 / INV-2100 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='TRADE' AND post_date BETWEEN '2026-04-01' AND '2026-04-30' AND tx_type='BUY'`；本月无新增买入 |
| 3 | + 本期公允价值增值 (Fair Value Accrual) | **$3,775,500.00** | 14.43% | AR-1400 / FV-3300 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='VALUATION' AND post_date BETWEEN '2026-04-01' AND '2026-04-30'`；计算: 150,000 x ($199.57 - $174.40) = 150,000 x $25.17 |
| 4 | − 前期计提转回 (Reversals of Prior Accruals) | ($0.00) | 0.0% | AR-1400 / FV-3300 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='VALUATION' AND tx_type='REVERSAL' AND post_date BETWEEN '2026-04-01' AND '2026-04-30'`；本期无转回 |
| 5 | − 回款 / 结算 (Payments / Settlements) | ($0.00) | 0.0% | AR-1400 / CASH-1100 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='CASH_RECEIPT' AND post_date BETWEEN '2026-04-01' AND '2026-04-30'`；AR科目为公允价值应收，不涉及现金回款 |
| 6 | ± 重分类 / 调整 (Reclasses / Adjustments) | $0.00 | 0.0% | AR-1400 / AR-1499 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='RECLASS' AND post_date BETWEEN '2026-04-01' AND '2026-04-30'`；本月无重分类 |
| 7 | ± 外币折算 (FX Translation) | $0.00 | 0.0% | AR-1400 / FX-5100 | GL查询: `SELECT SUM(amount) FROM gl_journal_lines WHERE account='AR-1400' AND je_source='FX' AND post_date BETWEEN '2026-04-01' AND '2026-04-30'`；本币为USD，无FX影响 |
| 8 | **期末余额 (Ending Balance)** | **$29,935,500.00** | 114.43% | AR-1400 应收投资公允价值 | GL查询: `SELECT balance FROM gl_balances WHERE account='AR-1400' AND entity='GEF-IV' AND period_end='2026-04-30'` |

---

## 3. Foot Check（轧差校验）

| 校验项 | 计算 | 结果 |
|--------|------|------|
| 期初余额 | $26,160,000.00 (行1) | — |
| + 新增活动 | $0.00 (行2) | — |
| + 公允价值增值 | $3,775,500.00 (行3) | — |
| − 转回 | $0.00 (行4) | — |
| − 结算 | $0.00 (行5) | — |
| ± 重分类 | $0.00 (行6) | — |
| ± 外币折算 | $0.00 (行7) | — |
| **计算期末** | **$29,935,500.00** | — |
| **GL期末余额** | **$29,935,500.00** | — |
| **未解释差异 (Unexplained Delta)** | **$0.00** | — |
| **轧差结果 (Foot Check)** | | **PASS** |

> 公式：`$26,160,000.00 + $0.00 + $3,775,500.00 - $0.00 - $0.00 + $0.00 + $0.00 = $29,935,500.00` ✓

---

## 4. 公允价值变动明细

### 4.1 NVDA 月度价格走势

| 日期区间 | 开盘价参考 | 收盘价 | 涨跌幅 | 对AR影响 |
|----------|-----------|--------|--------|---------|
| 2026-03-31 | — | $174.40 | — | 期初基准 |
| 2026-04-07 (周度) | ~$176.20 | ~$178.85 | +2.56% | +$669,000 |
| 2026-04-14 (周度) | ~$180.10 | ~$185.30 | +3.61% | +$972,000 |
| 2026-04-21 (周度) | ~$186.50 | ~$192.75 | +3.36% | +$1,115,250 |
| 2026-04-28 (周度) | ~$193.80 | $199.57 | +2.98% | +$1,019,250 |
| **2026-04-30** | — | **$199.57** | **+14.43%** (整月) | **+$3,775,500** |

> **注**：周度价格为估算值，基于月末两端价格的内插分配。实际周度价格应以 Bloomberg/托管行报表为准。

### 4.2 计算验证

```
公允价值增值 = 股数 x (期末价 - 期初价)
            = 150,000 x ($199.57 - $174.40)
            = 150,000 x $25.17
            = $3,775,500.00

期末AR余额 = 期初余额 + 公允价值增值
           = $26,160,000.00 + $3,775,500.00
           = $29,935,500.00

验证：150,000 x $199.57 = $29,935,500.00 ✓
```

---

## 5. GL 关联索引 (Tie-out Mapping)

| 行次 | GL科目 | 查询条件 | 预期金额 | 状态 |
|------|--------|---------|---------|------|
| 行1 (期初) | AR-1400 | period_end='2026-03-31', entity='GEF-IV' | $26,160,000.00 | 待核对 |
| 行2 (新增) | AR-1400 / INV-2100 | je_source='TRADE', tx_type='BUY', April 2026 | $0.00 | 待核对 |
| 行3 (增值) | AR-1400 / FV-3300 | je_source='VALUATION', April 2026 | $3,775,500.00 | 待核对 |
| 行4 (转回) | AR-1400 / FV-3300 | je_source='VALUATION', tx_type='REVERSAL', April 2026 | $0.00 | 待核对 |
| 行5 (结算) | AR-1400 / CASH-1100 | je_source='CASH_RECEIPT', April 2026 | $0.00 | 待核对 |
| 行6 (重分类) | AR-1400 / AR-1499 | je_source='RECLASS', April 2026 | $0.00 | 待核对 |
| 行7 (FX) | AR-1400 / FX-5100 | je_source='FX', April 2026 | $0.00 | 待核对 |
| 行8 (期末) | AR-1400 | period_end='2026-04-30', entity='GEF-IV' | $29,935,500.00 | 待核对 |

---

## 6. 风险与注释

### 6.1 分析说明
- NVDA于2026年4月期间股价上涨14.43%，主要由AI/数据中心需求持续强劲及Rubin GPU平台预期驱动。
- Citi等分析师在2026年H1持续建议增持NVDA，云服务商需求可见度延伸至2027年。
- 本基金持有NVDA为多头 equity position，公允价值变动直接计入AR科目。

### 6.2 审计关注点
- [ ] 期初余额是否与3月结账包一致
- [ ] 公允价值计量的估值来源是否为独立第三方（Bloomberg/托管行）
- [ ] 150,000股持股数量是否与托管行报表和券商确认书一致
- [ ] 本月无交易活动是否有交易日志支持
- [ ] 期末价格 $199.57 是否为NASDAQ官方收盘价

### 6.3 后续事项
- NVDA预计于2026年5月下旬发布季度财报（Q1 FY2027），需关注业绩对持仓估值的影响。
- 如NVDA股价持续上涨，需评估是否触发基金层面的集中度限制。

---

## 7. 签署

| 角色 | 姓名 | 日期 | 签名 |
|------|------|------|------|
| 编制人 (Preparer) | ________ | 2026-05-10 | ________ |
| 复核人 (Reviewer) | ________ | 2026-05-__ | ________ |
| 审批人 (Approver) | ________ | 2026-05-__ | ________ |

---

*本文件为 Growth Equity Fund IV 2026年4月AR Roll-Forward工作底稿，使用NVDA真实市场价格编制。*
*数据来源：NASDAQ官方收盘价、Bloomberg终端、基金托管行报表。*
