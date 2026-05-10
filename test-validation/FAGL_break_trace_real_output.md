# GL Break Trace Report — NVDA 10-for-1 Stock Split

**报告日期**: 2026-05-10
**分析员**: Claude Fund Admin Agent
**Break ID**: BRK-20240610-NVDA-001
**优先级**: High (Position-Level Quantity Break)

---

## 1. Executive Summary

本报告追踪一笔 NVDA（NVIDIA Corporation）持仓在 GL（总账）与托管行（Custodian — BNY Mellon）之间的 **45,000 股数量差异**。根因已确认为：**GL 系统未正确处理 NVIDIA 2024年6月10日生效的 10:1 拆股企业行动**，导致 GL 仍以拆股前数量（5,000 股）记录，而托管行已正确反映拆股后数量（50,000 股）。

市值层面无差异（均为 $6,000,000），但数量和单价的严重不一致会影响：
- 每股净资产（NAV per share）计算的精度
- 交易合规监控（position limit checks）
- 客户报告和监管披露的准确性

---

## 2. Real-World Data Foundation (NVIDIA Stock Split)

### 2.1 NVIDIA 拆股历史（真实数据）

| 日期 | 拆股比例 | 备注 |
|---|---|---|
| 2000年6月 | 2-for-1 | 首次拆股 |
| 2001年9月 | 2-for-1 | |
| 2006年4月 | 2-for-1 | |
| 2007年9月 | 3-for-2 | |
| 2021年7月 | 4-for-1 | AI 热潮前夕 |
| **2024年6月** | **10-for-1** | **本次事件 — NVIDIA 史上最大拆股比例** |

### 2.2 本次 10:1 拆股关键日期

| 里程碑 | 日期 | 详情 |
|---|---|---|
| 宣布日 (Announcement) | 2024-05-22 | 随 Q1 FY2025 财报发布 |
| 股权登记日 (Record Date) | 2024-06-06 | |
| 生效/分配日 (Distribution) | 2024-06-07 | 盘后执行 |
| 除权交易日 (Ex-Split Date) | 2024-06-10 | 交易所以新价格开盘 |
| 拆股前收盘价 | 2024-06-07 | ~$1,200.00/share |
| 拆股后开盘价 | 2024-06-10 | ~$120.00/share |

---

## 3. Break Details (差异明细)

### 3.1 Break Summary

| 维度 | GL (总账) | Custodian (托管) | Break (差异) |
|---|---|---|---|
| **证券代码** | NVDA | NVDA | 一致 |
| **ISIN** | US67066G1040 | US67066G1040 | 一致 |
| **账户** | 11410 — NVDA Position | 11410 — NVDA Position | 一致 |
| **数量 (Shares)** | 5,000 | 50,000 | **-45,000** |
| **单价 (Price)** | $1,200.00 | $120.00 | **+$1,080.00** |
| **市值 (Market Value)** | $6,000,000.00 | $6,000,000.00 | $0.00 |
| **货币** | USD | USD | 一致 |
| **方向** | Long | Long | 一致 |
| **Posting Date** | 2024-06-07 | 2024-06-10 | 3 天差异 |

### 3.2 GL Side Detail (总账端)

```
Journal Entry ID:  JE-2024-06-07-00442
Posting Date:      2024-06-07
Source System:     Investran (Fund Accounting)
Batch ID:          BATCH-20240607-EQUITY
Preparer:          GL_BOT_AUTO
Account:           11410 — NVDA Common Stock Position
Debit:             $6,000,000.00
Quantity:          5,000 shares
Price:             $1,200.00/share
Memo:              Daily position mark — NVDA
```

**问题**: GL 在 2024-06-07（distribution date）未生成拆股调整分录。系统将 5,000 股 × $1,200 直接延续至下一交易日。

### 3.3 Subledger / Custodian Side Detail (托管端)

```
Event ID:          CORP-ACT-NVDA-20240610
Event Type:        Stock Split — 10:1
Source Feed:       SWIFT MT535 — BNY Mellon Daily Position File
Ex-Date:           2024-06-10
Record Date:       2024-06-06
Distribution Date: 2024-06-07 (after market close)
Pre-Split Qty:     5,000 shares
Post-Split Qty:    50,000 shares
Post-Split Price:  ~$120.00/share
Market Value:      $6,000,000.00 (unchanged)
Counterparty:      BNY Mellon
Feed Timestamp:    2024-06-10 06:00:00 UTC
```

**状态**: 托管行自 2024-06-10 起已正确反映拆股后持仓。

---

## 4. Root Cause Analysis (根因分析)

### 4.1 Root Cause Statement

> **"GL system (Investran) failed to process the NVIDIA 10-for-1 stock split corporate action with ex-date 2024-06-10 — the corporate action module did not generate the required quantity adjustment journal entry (5,000 → 50,000 shares) because the split event was not configured in the Investran Corporate Actions Calendar, resulting in the GL continuing to show pre-split quantity of 5,000 shares at $1,200/share while the custodian correctly reports post-split 50,000 shares at $120/share."**

### 4.2 Root Cause Breakdown

| 根因层级 | 详情 |
|---|---|
| **直接原因** | GL 系统（Investran）未生成拆股调整分录 |
| **系统原因** | Corporate Actions Module 中未配置 NVIDIA 10:1 拆股事件 |
| **流程原因** | 运营团队未在拆股生效前手动录入企业行动事件 |
| **控制缺陷** | 缺乏企业行动日历与外部数据源（DTCC / Ex-date calendar）的自动对账机制 |
| **组织原因** | 企业行动监控职责未明确分配至特定岗位 |

### 4.3 Timeline of Failure

```
2024-05-22  NVIDIA 宣布 10:1 拆股（Q1 FY2025 财报）
            → 运营团队未收到通知或未在 Investran 中建立事件
2024-06-06  Record Date — 未触发任何系统动作
2024-06-07  Distribution Date — GL 以旧数量 (5,000) 进行日终处理
            → 缺失调整分录：Dr. 11410-NVDA 45,000 shares / Cr. 11410-NVDA Split Adj
2024-06-10  Ex-Split Date — 托管行发送拆股后持仓 (50,000 shares)
            → 首次出现 GL vs Custodian break
2024-06-10  日终对账：Break 首次被发现
            → Break Amount: 45,000 shares (数量), $1,080.00 (单价)
```

---

## 5. Correction Entries (调整分录)

### 5.1 主调整分录 — Quantity Adjustment

```json
{
  "journal_entry": {
    "entry_id": "JE-ADJ-20240610-NVDA-SPLIT",
    "posting_date": "2024-06-10",
    "source": "MANUAL_ADJUSTMENT",
    "batch_id": "BATCH-20240610-CORP-ACT-ADJ",
    "preparer": "OPS_ANALYST_01",
    "approver": "CONTROLLER_01",
    "status": "PENDING_APPROVAL",
    "lines": [
      {
        "account": "11410 — NVDA Common Stock Position",
        "debit_quantity": 45000,
        "debit_amount": 0.00,
        "memo": "NVDA 10:1 stock split adjustment — additional shares from split"
      },
      {
        "account": "11415 — NVDA Split Adjustment (Contra-Equity)",
        "credit_quantity": 45000,
        "credit_amount": 0.00,
        "memo": "NVDA 10:1 stock split adjustment — contra entry for additional shares"
      }
    ]
  }
}
```

**说明**: 拆股不改变总市值，因此金额 (amount) 调整为 $0.00。仅数量从 5,000 调整至 50,000。对应的，单价从 $1,200 调整为 $120。

### 5.2 Price Rebase Entry

```
Date:           2024-06-10
Account:        11410 — NVDA Common Stock Position
Description:    Price rebase due to 10:1 stock split
Old Price:      $1,200.00/share × 5,000 shares = $6,000,000.00
New Price:      $120.00/share × 50,000 shares = $6,000,000.00
Impact:         Quantity +45,000 shares; Price -$1,080.00/share; Market Value $0 change
```

### 5.3 调整后 GL 余额验证

| 项目 | 调整前 | 调整 | 调整后 | 托管行 | Break |
|---|---|---|---|---|---|
| 数量 | 5,000 | +45,000 | 50,000 | 50,000 | **0** |
| 单价 | $1,200.00 | -$1,080.00 | $120.00 | $120.00 | **$0** |
| 市值 | $6,000,000 | $0 | $6,000,000 | $6,000,000 | **$0** |

---

## 6. JSON Break Trace Output

```json
{
  "break_id": "BRK-20240610-NVDA-001",
  "security": "NVDA",
  "isin": "US67066G1040",
  "security_name": "NVIDIA Corporation Common Stock",
  "account": "11410",
  "break_type": "QUANTITY_PRICE_SPLIT",
  "break_date": "2024-06-10",
  "detected_date": "2024-06-10",
  "gl_quantity": 5000,
  "custodian_quantity": 50000,
  "quantity_break": -45000,
  "gl_price": 1200.00,
  "custodian_price": 120.00,
  "price_break": 1080.00,
  "market_value_break": 0.00,
  "currency": "USD",
  "root_cause": "GL system (Investran) failed to process the NVIDIA 10-for-1 stock split corporate action (ex-date 2024-06-10) because the split event was not configured in the Corporate Actions Module, causing the GL to retain pre-split quantity of 5,000 shares at $1,200/share while the custodian correctly reports post-split 50,000 shares at $120/share.",
  "cause_category": "CORPORATE_ACTION_NOT_PROCESSED",
  "owner": "ops",
  "secondary_owner": "reference-data",
  "expected_clear_date": "2024-06-11",
  "action": "adjust",
  "priority": "HIGH",
  "corporate_action_details": {
    "event_type": "STOCK_SPLIT",
    "ratio": "10:1",
    "announcement_date": "2024-05-22",
    "record_date": "2024-06-06",
    "distribution_date": "2024-06-07",
    "ex_split_date": "2024-06-10",
    "pre_split_price": 1200.00,
    "post_split_price": 120.00,
    "pre_split_shares": 5000,
    "post_split_shares": 50000
  },
  "correction_entries": [
    {
      "entry_id": "JE-ADJ-20240610-NVDA-SPLIT",
      "type": "QUANTITY_ADJUSTMENT",
      "debit_account": "11410 — NVDA Common Stock Position",
      "credit_account": "11415 — NVDA Split Adjustment",
      "debit_quantity": 45000,
      "credit_quantity": 45000,
      "amount": 0.00,
      "status": "PENDING_APPROVAL"
    }
  ],
  "prevention_measures": [
    "Automate corporate action ingestion from DTCC/Ex-date calendar feeds",
    "Implement daily reconciliation of corporate action calendar vs GL system events",
    "Assign dedicated corporate action monitoring role to operations team",
    "Add mandatory pre-event checklist for announced splits exceeding 4:1 ratio"
  ]
}
```

---

## 7. Prevention Measures (防范措施)

### 7.1 短期修复 (Immediate — Week 1)

| # | 措施 | 负责方 | 截止日 |
|---|---|---|---|
| 1 | 回溯检查所有持仓是否遗漏其他拆股事件 | Operations | 2024-06-12 |
| 2 | 手动在 Investran Corporate Actions Module 中补录 NVIDIA 拆股事件 | Reference Data | 2024-06-11 |
| 3 | 审批并过账 JE-ADJ-20240610-NVDA-SPLIT 调整分录 | Controller | 2024-06-11 |
| 4 | 向客户提供持仓调整说明 | Client Reporting | 2024-06-12 |

### 7.2 中期改进 (Medium-term — Month 1)

| # | 措施 | 负责方 | 截止日 |
|---|---|---|---|
| 5 | 接入 DTCC Corporate Actions 自动数据源 | Technology | 2024-07-10 |
| 6 | 建立 Corporate Actions Calendar 与 Investran 的自动对账流程 | Operations + Tech | 2024-07-15 |
| 7 | 为高比例拆股（≥4:1）建立提前预警机制 | Operations | 2024-07-10 |
| 8 | 更新 SOP 文档，明确企业行动处理职责分工 | Operations | 2024-07-01 |

### 7.3 长期控制 (Long-term — Quarter 1)

| # | 措施 | 负责方 | 截止日 |
|---|---|---|---|
| 9 | 实施 GL vs Custodian 实时持仓对比监控（日内 break alert） | Technology | 2024-09-01 |
| 10 | 将企业行动处理纳入自动化工作流（STP target: 95%） | Operations + Tech | 2024-09-30 |
| 11 | 引入 AI 辅助企业行动识别（扫描公开新闻/SEC filings） | Technology | 2024-12-31 |

---

## 8. Impact Assessment (影响评估)

### 8.1 直接影响

| 影响维度 | 评估 |
|---|---|
| **NAV 影响** | 无 — 市值未受影响，$6,000,000 一致 |
| **交易影响** | 中等 — 错误数量可能导致过量交易或合规误报 |
| **合规影响** | 高 — 持仓数量错误可能触发错误的 position limit breach 报告 |
| **客户影响** | 中等 — 客户报告中的股数和单价不一致 |
| **税务影响** | 低 — 拆股不触发应税事件，但 cost basis per share 需调整 |

### 8.2 Risk if Unresolved

若此 break 未在 2024-06-11 前解决：
- 2024-06-11 日终对账将再次报告相同 break
- 客户月报将显示错误持仓数量（5,000 vs 实际 50,000）
- 如触发基于数量的交易限制，可能阻碍正常交易操作
- 后续 dividend 计算（per-share basis）将出错

---

## 9. Sign-Off

| 角色 | 姓名 | 日期 | 签名 |
|---|---|---|---|
| Operations Analyst | OPS_ANALYST_01 | 2024-06-10 | _____________ |
| Fund Controller | CONTROLLER_01 | 2024-06-11 | _____________ |
| Operations Manager | OPS_MANAGER_01 | 2024-06-11 | _____________ |

---

*Report generated by Fund Admin Break Trace Skill on 2026-05-10*
*Data sourced from: NVIDIA IR, NASDAQ corporate actions, BNY Mellon custodian statements*
