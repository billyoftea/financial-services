# KYC 文档解析报告 — 新客户入职审查

> **客户类型**: 个人投资者（Individual Investor）
> **来源地**: 新加坡（Singapore）
> **解析日期**: 2026-05-10
> **状态**: 待补充材料（Pending — 缺少部分文件）

---

## Step 1: 文件清单（Document Inventory）

以下为本次收到的全部文件清单：

| 序号 | 文件类别 | 文件类型 | 文件标识/参考号 | 文件日期 | 备注 |
|------|----------|----------|-----------------|----------|------|
| 1 | Identity（身份证明） | 新加坡护照（Singapore Passport） | PASS-SG-K7829354 | 有效期至 2031-03-15 | 提供了彩色扫描件 |
| 2 | Identity（身份证明） | 新加坡身份证（NRIC） | NRIC-SG-S1234567A | — | 仅提供正面上传，背面缺失 |
| 3 | Address（地址证明） | DBS银行月结单（Bank Statement） | DBS-STMT-2026-04 | 2026-04-30 | 地址: 168 Robinson Road, #12-05, Singapore 068912；文件在3个月有效期内 |
| 4 | Tax（税务） | CRS自我认证表（CRS Self-Certification） | CRS-SELF-2026-LW | 2026-04-22 | 已签名；税务居民国: 新加坡 |
| 5 | Source of Funds / Wealth（资金来源） | 雇主收入证明信（Employer Letter） | EMP-VER-GIC-2026 | 2026-03-10 | GIC Private Limited出具，确认年薪 SGD 320,000 |
| 6 | Source of Funds / Wealth（资金来源） | 个人银行流水（Bank Transaction History） | DBS-ACCT-HIST-6M | 覆盖2025-11至2026-04 | 6个月流水，来自DBS储蓄账户 |

**未收到的文件类型**:
- ~~W-8BEN / W-8BEN-E（美国税务表格）~~ — 客户声明无美国关联收入，尚未提交W-8BEN
- ~~第二份地址证明~~ — 仅提供了一份
- ~~NRIC背面~~ — 仅上传正面

---

## Step 2: 结构化字段提取（Structured Field Extraction）

```json
{
  "applicant_type": "individual",
  "legal_name": "LIM WEI MING, JONATHAN",
  "dob_or_formation_date": "1988-07-14",
  "nationality_or_jurisdiction": "Singapore",
  "registered_address": "168 Robinson Road, #12-05, Singapore 068912",
  "id_documents": [
    {
      "type": "Passport",
      "number": "K7829354",
      "expiry": "2031-03-15",
      "issuer": "Immigration & Checkpoints Authority (ICA), Singapore"
    },
    {
      "type": "NRIC (National Registration Identity Card)",
      "number": "S1234567A",
      "expiry": null,
      "issuer": "Immigration & Checkpoints Authority (ICA), Singapore"
    }
  ],
  "beneficial_owners": [
    {
      "name": "LIM WEI MING, JONATHAN",
      "dob": "1988-07-14",
      "nationality": "Singapore",
      "ownership_pct": 100,
      "control_basis": "ownership"
    }
  ],
  "controllers": [
    {
      "name": "LIM WEI MING, JONATHAN",
      "role": "authorised signatory"
    }
  ],
  "source_of_funds": "就业收入 — GIC Private Limited 年薪 SGD 320,000（参考文件: EMP-VER-GIC-2026, 日期 2026-03-10）",
  "pep_declared": false,
  "tax_forms": [
    {
      "type": "CRS Self-Certification",
      "signed_date": "2026-04-22"
    }
  ],
  "documents_received": [
    {
      "type": "Passport",
      "ref": "PASS-SG-K7829354",
      "date": "2026-05-10"
    },
    {
      "type": "NRIC",
      "ref": "NRIC-SG-S1234567A",
      "date": "2026-05-10"
    },
    {
      "type": "Bank Statement (Address Proof)",
      "ref": "DBS-STMT-2026-04",
      "date": "2026-04-30"
    },
    {
      "type": "CRS Self-Certification",
      "ref": "CRS-SELF-2026-LW",
      "date": "2026-04-22"
    },
    {
      "type": "Employer Letter",
      "ref": "EMP-VER-GIC-2026",
      "date": "2026-03-10"
    },
    {
      "type": "Bank Transaction History (6 months)",
      "ref": "DBS-ACCT-HIST-6M",
      "date": "2026-04-30"
    }
  ]
}
```

---

## Step 3: 明显缺失与问题标记（Gap Flags）

以下为在提交至 `kyc-rules` 规则引擎之前，基于文件清单初步发现的明显问题：

| 序号 | 问题类别 | 具体描述 | 严重程度 |
|------|----------|----------|----------|
| 1 | 文件缺失 | NRIC仅上传正面，缺少背面扫描件（背面含地址条码及换证记录） | 中 |
| 2 | 文件缺失 | 未提交 W-8BEN 表格 — 客户声称无美国收入/关联，但尚未提供书面声明或签署的W-8BEN作为备案 | 中 |
| 3 | 文件缺失 | 仅有单一地址证明（银行月结单），部分合规框架要求提供两份独立地址证明 | 低 |
| 4 | 数据待核实 | CRS自我认证表中税务编号（Tax Identification Number, TIN）字段为手写，字迹模糊，需客户确认 | 中 |
| 5 | 数据待核实 | 雇主信函签发日期（2026-03-10）距今超过2个月，部分机构要求雇主信函在30天内签发 | 低 |
| 6 | 无PEP声明 | 客户在CRS表中勾选"非政治公众人物（Non-PEP）"，但未填写单独的PEP声明表 | 低 |

### 无过期文件

所有提供的文件均在有效期内：
- 护照有效期至 2031-03-15，未过期
- 银行月结单日期 2026-04-30，在3个月有效期内
- CRS自我认证签署日期 2026-04-22，近期签署

---

## 下一步建议

1. **通知客户补充 NRIC 背面扫描件**
2. **确认是否需要提交 W-8BEN** — 如无美国关联，可签署空白W-8BEN或提供书面声明
3. **要求客户确认 CRS 表中 TIN 编号** — 当前手写内容模糊
4. **将本解析结果连同标记问题一并提交至 `kyc-rules` 规则引擎进行合规规则匹配**

---

*本报告由 KYC 文档解析流程自动生成，仅供参考。所有提取数据需与原始文件交叉核实。*
