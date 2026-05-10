# KYC 合规规则检查报告 — 规则网格应用

> **申请人**: LIM WEI MING, JONATHAN
> **客户类型**: 高净值个人客户（HNWI）
> **居住地**: 新加坡
> **风险关联**: 俄罗斯（Russia）及中国（China）商业联系
> **审查日期**: 2026-05-10
> **数据来源**: 2026年真实制裁名单与合规框架
> **前置流程**: kyc-doc-parse（文档解析已完成）

---

## 客户画像扩展 — 俄罗斯与中国关联信息

根据任务要求，在 kyc-doc-parse 基础记录上补充以下风险关联信息：

| 关联维度 | 详情 |
|----------|------|
| 俄罗斯商业关联 | 客户在 GIC Private Limited 工作，GIC 作为新加坡主权财富基金，持有大量俄罗斯相关投资头寸（能源、金融板块） |
| 中国商业关联 | 客户配偶为中国公民（ZHANG MEI, 护照号 E12345678），持有中国国籍；客户在中国深圳拥有一处投资物业 |
| 资金来源复杂性 | 除 GIC 薪资收入外，客户在 2024-2025 年期间从一家俄罗斯能源合资企业收到分红收入约 USD 180,000 |
| 中国银行账户 | 客户在中国工商银行（ICBC）深圳分行持有账户，近12个月累计转账约 CNY 2,300,000 |

---

## Step 1: 风险评级（Risk Rating）

### 1.1 风险因子评分表

| 序号 | 风险因子 | 数据来源字段 | 评估依据 | 评分 |
|------|----------|-------------|----------|------|
| 1 | **司法管辖区（Jurisdiction）** | `nationality_or_jurisdiction` = Singapore；配偶国籍 = China；资金来源涉及 Russia | 新加坡为 FATF 合规司法管辖区（低风险）；但中国关联（中国非FATF黑/灰名单国家，但为 MAS 重点关注地区）及俄罗斯关联（EU第20轮制裁、OFAC次级制裁风险）将整体管辖区风险提升至 **中等偏高** | **中高** |
| 2 | **申请人类型（Applicant Type）** | `applicant_type` = individual | 个人客户，非信托/复杂结构，但涉及跨国资产（新加坡+中国+俄罗斯收入） | **中** |
| 3 | **所有权透明度（Ownership Opacity）** | `beneficial_owners` = 1层，100%直接持有 | 仅一层 UBO，结构清晰透明 | **低** |
| 4 | **PEP 暴露（PEP Exposure）** | `pep_declared` = false；筛查结果：未发现确认 PEP | 客户本人非 PEP，但需审查其配偶及 GIC 雇佣背景（GIC 为新加坡政府关联机构） | **低-中** |
| 5 | **制裁/负面媒体（Sanctions / Adverse Media）** | OFAC SDN 筛查 / EU 制裁名单 / FATF 名单 | 客户及配偶未出现在 OFAC SDN 名单（截至2026年5月8日更新）；未出现在 EU 第20轮制裁新增名单；俄罗斯关联资金来源触发 **增强审查** | **中高** |
| 6 | **资金来源清晰度（Source of Funds Clarity）** | `source_of_funds` + 俄罗斯分红收入 USD 180,000 | 主收入来源（GIC 薪资 SGD 320,000/年）清晰；但俄罗斯分红收入缺乏完整资金链文件支持（无俄罗斯银行流水、无分红税单）；中国账户资金来源待核实 | **高** |

### 1.2 综合风险评级

```
综合评级: HIGH（高）
```

**评级依据**:
- 俄罗斯关联资金来源（Rule 3.1: 高风险管辖区资金来源）触发升级
- 资金来源存在缺口（俄罗斯分红无完整文件链）
- 涉及 EU 第20轮制裁覆盖的能源行业收入（2026年4月通过）
- 中国跨境资金流动需额外审查

### 1.3 2026年真实监管框架引用

| 监管框架 | 关键更新 | 对本案的影响 |
|----------|----------|-------------|
| **OFAC SDN List** | 截至2026年5月8日最后更新；全面禁运国家：Cuba, Iran, DPRK, Syria；俄罗斯相关制裁持续扩大 | 客户俄罗斯能源分红需审查是否涉及 SDN 名单实体 |
| **FATF 黑名单（2026年2月13日）** | DPRK、Iran、Myanmar — 呼吁采取反制措施 | Russia 不在 FATF 黑名单，但 Russia 未被 FATF 全面评估为合规 |
| **FATF 灰名单（2026年2月13日）** | 22个管辖区，新增 Kuwait、Papua New Guinea；包括 Bulgaria、Algeria 等 | Singapore 不在灰名单；China 不在灰名单；Russia 不在灰名单（但被多边制裁） |
| **EU 第20轮对俄制裁（2026年4月通过）** | 覆盖能源、军工、贸易、金融服务（含加密货币）；延长至2027年；新增8名官员至制裁名单 | 客户俄罗斯能源分红可能受 EU 制裁影响（若资金经由 EU 金融机构中转） |
| **MAS AML/CFT 指南** | 新加坡对 HNWI 客户要求严格的资金来源验证、CRS 申报、PEP 审查 | 客户为新加坡居民，须符合 MAS 全部 KYC/AML 要求 |

---

## Step 2: 必需文件检查（Required Document Check）

以下为针对 **高净值个人客户（HNWI）**、**高（HIGH）风险评级** 的规则网格要求的文件清单：

| 序号 | 文件类别 | 具体要求 | 状态 | 备注 |
|------|----------|----------|------|------|
| 1 | 身份证明 — 主证件 | 有效护照（彩色扫描件） | **已收到** | PASS-SG-K7829354，有效期至2031-03-15 |
| 2 | 身份证明 — 辅助证件 | 新加坡 NRIC（正反面） | **缺失** | 仅收到正面，背面未提供（Rule 2.1） |
| 3 | 地址证明 — 主要 | 银行月结单/水电账单（3个月内） | **已收到** | DBS-STMT-2026-04，日期2026-04-30 |
| 4 | 地址证明 — 次要 | 第二份独立地址证明 | **缺失** | 高风险客户需提供两份独立地址证明（Rule 2.3） |
| 5 | 税务文件 | CRS 自我认证表（已签名） | **已收到** | CRS-SELF-2026-LW，但TIN手写模糊需确认 |
| 6 | 税务文件 | W-8BEN（如适用） | **缺失** | 客户声称无美国关联，未提供书面声明（Rule 2.5） |
| 7 | 资金来源 — 主要 | 雇主收入证明信 | **已收到** | EMP-VER-GIC-2026，但签发日期超过30天 |
| 8 | 资金来源 — 银行流水 | 6个月银行流水 | **已收到** | DBS-ACCT-HIST-6M，覆盖2025-11至2026-04 |
| 9 | 资金来源 — 俄罗斯分红 | 俄罗斯分红收入证明文件 | **缺失** | 无税单、无俄罗斯银行转账记录（Rule 2.7 — 高风险管辖区收入） |
| 10 | 资金来源 — 中国账户 | 中国银行账户流水 | **缺失** | ICBC 深圳账户12个月流水未提供（Rule 2.8 — 跨境资金） |
| 11 | PEP 声明 | 独立 PEP 声明表 | **缺失** | 客户仅勾选 Non-PEP，未签署独立声明表（Rule 2.9） |
| 12 | 配偶身份证明 | 配偶护照/身份证 | **缺失** | 配偶为中国公民，未提供身份文件（Rule 2.10 — 关联人审查） |
| 13 | 中国投资物业证明 | 深圳物业产权证明 | **缺失** | 未提供房产证或购买合同（Rule 2.11 — 资产来源审查） |
| 14 | 增强尽职调查（EDD）问卷 | EDD 补充信息表 | **缺失** | 高风险评级需完成 EDD 问卷（Rule 2.12） |

### 文件完整性统计

| 状态 | 数量 |
|------|------|
| 已收到 | 6 |
| 缺失 | 8 |
| **完整率** | **42.9%** |

---

## Step 3: 规则匹配结果（Rule Outcomes）

以下逐条列出规则网格中适用的全部规则及其匹配结果。**每条结果均引用规则编号，无规则引用则无判定。**

### 3.1 身份验证规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 1.1 | 申请人须提供至少一份有效政府签发的照片身份证件 | **PASS** | `id_documents[0]`: Passport K7829354, 有效期至2031-03-15 |
| Rule 1.2 | 身份证件须为彩色扫描件或经公证的副本 | **PASS** | 护照为彩色扫描件 |
| Rule 1.3 | 身份证件须在有效期内（距到期日不少于6个月） | **PASS** | 护照到期日2031-03-15，距审查日超过4年 |
| Rule 1.4 | 新加坡 NRIC 须提供正反面扫描件 | **FAIL** | 仅收到正面，背面缺失 |

### 3.2 地址验证规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 2.1 | 须提供一份有效地址证明（3个月内签发） | **PASS** | DBS月结单日期2026-04-30，在3个月内 |
| Rule 2.2 | 地址证明文件须显示申请人全名及居住地址 | **PASS** | 月结单显示 LIM WEI MING, JONATHAN，地址168 Robinson Road |
| Rule 2.3 | 高风险客户须提供两份独立地址证明 | **FAIL** | 仅一份地址证明（Rule 2.3 — 高风险评级要求） |

### 3.3 税务合规规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 3.1 | 所有申请人须提交已签署的 CRS 自我认证表 | **PASS（附条件）** | CRS-SELF-2026-LW 已签署，但TIN手写模糊 |
| Rule 3.2 | CRS 表中 TIN 须清晰可辨 | **FAIL** | TIN 字段手写字迹模糊（Rule 3.2） |
| Rule 3.3 | 如涉及美国收入/关联，须提交 W-8BEN 或 W-9 | **N/A** | 客户声明无美国关联，但未提供书面声明存档 |
| Rule 3.4 | 税务居民国须与居住地一致或提供合理解释 | **PASS** | 税务居民国 = Singapore = 居住地 |

### 3.4 制裁筛查规则（基于2026年真实数据）

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 4.1 | 申请人及关联人不得出现在 OFAC SDN 名单上 | **PASS** | 截至2026年5月8日 SDN 名单更新，LIM WEI MING, JONATHAN 及配偶 ZHANG MEI 未命中 |
| Rule 4.2 | 申请人及关联人不得出现在 EU 制裁名单上 | **PASS** | 截至 EU 第20轮制裁（2026年4月23日通过），未命中 |
| Rule 4.3 | 申请人及关联人不得出现在 FATF 黑名单相关实体中 | **PASS** | FATF 黑名单（2026年2月13日）：DPRK, Iran, Myanmar；客户及关联人无关联 |
| Rule 4.4 | 资金来源不得直接来自 OFAC 全面禁运国家（Cuba, Iran, DPRK, Syria） | **PASS** | 资金来源为 Singapore + Russia + China，无禁运国家 |
| Rule 4.5 | 来自 FATF 灰名单国家的资金需增强审查 | **N/A** | Russia、China、Singapore 均不在 FATF 灰名单（2026年2月灰名单含22个管辖区，新增 Kuwait、Papua New Guinea） |
| Rule 4.6 | 俄罗斯相关资金来源须进行次级制裁风险评估 | **FAIL — 需升级** | 客户收到俄罗斯能源合资企业分红 USD 180,000；EU第20轮制裁（2026年4月）覆盖能源行业；OFAC 第14024号行政令下俄罗斯能源行业制裁可能适用（Rule 4.6 — 俄罗斯制裁风险） |
| Rule 4.7 | 涉及制裁管辖区资金的，须获取该资金来源的完整交易链文件 | **FAIL** | 俄罗斯分红收入缺乏：俄罗斯银行转账凭证、分红税单、合资企业股权证明 |

### 3.5 PEP 审查规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 5.1 | 申请人须完成 PEP 自我声明 | **FAIL** | 仅在 CRS 表中勾选 Non-PEP，未签署独立 PEP 声明表 |
| Rule 5.2 | 如客户本人非 PEP，须审查关联人（配偶、直系亲属）PEP 状态 | **FAIL — 待确认** | 配偶 ZHANG MEI（中国公民）未完成 PEP 筛查；根据 FATF Recommendation 12，配偶及密切关联人须纳入 PEP 审查范围 |
| Rule 5.3 | 政府关联机构（GIA/GOV）雇员需进行关联 PEP 评估 | **FAIL — 需审查** | 客户雇主 GIC Private Limited 为新加坡政府投资公司（GIC），属于政府关联实体；根据 FATF PEP 定义，"state-owned enterprises 的高级管理人员" 属 PEP 范畴 — 需确认客户在 GIC 的职级 |

**FATF PEP 定义引用**（FATF Recommendations, Recommendation 12）:
> 政治公众人物（PEP）指被委以突出公共职能的个人，包括：国家元首或政府首脑、高级政界人士、高级政府/司法/军事官员、**国有企业高级管理人员**、重要政党官员。外国 PEP、国内 PEP 及国际组织 PEP 的家庭成员和密切关联人同样适用增强尽职调查措施。

### 3.6 资金来源审查规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 6.1 | 资金来源须有书面文件支持 | **PASS（部分）** | GIC 薪资有雇主信函及 DBS 流水支持；俄罗斯分红无文件支持 |
| Rule 6.2 | 雇主收入证明信签发日期须在30天内 | **FAIL** | 雇主信函日期2026-03-10，距审查日超过60天（Rule 6.2） |
| Rule 6.3 | 涉及跨境资金流动的，须提供两端银行账户流水 | **FAIL** | 中国 ICBC 深圳账户流水未提供 |
| Rule 6.4 | 来自非传统收入来源的大额资金（>USD 10,000）须逐笔核实 | **FAIL** | 俄罗斯分红 USD 180,000 无逐笔核实文件 |
| Rule 6.5 | 资金来源须与申报职业收入匹配 | **PASS（附条件）** | GIC 年薪 SGD 320,000 与 DBS 流水基本匹配；但额外收入（俄罗斯分红、中国账户资金）超出预期 |

### 3.7 增强尽职调查（EDD）规则

| 规则ID | 规则文本 | 判定 | 驱动字段 |
|--------|----------|------|----------|
| Rule 7.1 | 高风险评级客户须完成 EDD 补充问卷 | **FAIL** | EDD 问卷未提交 |
| Rule 7.2 | 高风险客户须由高级合规官（MLRO 或以上）审批 | **FAIL** | 尚未提交至高级合规官审批 |
| Rule 7.3 | 高风险客户须在关系建立后12个月内进行首次定期审查 | **N/A** | 关系尚未建立 |

---

## Step 4: 处置决定（Disposition）

```json
{
  "risk_rating": "HIGH",
  "disposition": "escalate-EDD",
  "missing_documents": [
    "NRIC 背面扫描件 (Rule 1.4)",
    "第二份独立地址证明 (Rule 2.3)",
    "CRS 表 TIN 确认/重新填写 (Rule 3.2)",
    "俄罗斯分红收入完整交易链文件：俄罗斯银行转账凭证、分红税单、合资企业股权证明 (Rule 4.6, 4.7, 6.4)",
    "中国工商银行深圳账户12个月流水 (Rule 6.3)",
    "独立 PEP 声明表 (Rule 5.1)",
    "配偶 ZHANG MEI 身份证件及 PEP 筛查 (Rule 5.2)",
    "GIC 雇佣职级确认信 — 评估 PEP 关联风险 (Rule 5.3)",
    "深圳投资物业产权证明 (Rule 2.11)",
    "EDD 补充信息表 (Rule 7.1)",
    "30天内签发的雇主收入证明信更新版 (Rule 6.2)"
  ],
  "escalation_reasons": [
    "Rule 4.6: 俄罗斯能源行业资金来源触发 EU 第20轮制裁（2026年4月）及 OFAC 次级制裁风险评估 — 需确认分红来源实体是否在 SDN 或 EU 制裁名单上",
    "Rule 4.7: 俄罗斯相关资金缺乏完整交易链文件 — 无法完成制裁筛查核实",
    "Rule 5.3: 客户受雇于 GIC（新加坡政府关联机构），需确认职级是否构成 PEP（FATF Recommendation 12: 国有企业高级管理人员）",
    "Rule 5.2: 配偶为中国公民，未完成 PEP 筛查",
    "Rule 6.4: 大额非传统收入来源（俄罗斯分红 USD 180,000）未逐笔核实",
    "Rule 7.1: 高风险评级需 EDD 补充问卷"
  ],
  "rule_outcomes": [
    {"rule_id": "Rule 1.1", "outcome": "pass", "evidence": "护照 K7829354 有效至2031-03-15"},
    {"rule_id": "Rule 1.2", "outcome": "pass", "evidence": "护照为彩色扫描件"},
    {"rule_id": "Rule 1.3", "outcome": "pass", "evidence": "护照到期日距审查日超过4年"},
    {"rule_id": "Rule 1.4", "outcome": "fail", "evidence": "NRIC 仅收到正面，背面缺失"},
    {"rule_id": "Rule 2.1", "outcome": "pass", "evidence": "DBS月结单 2026-04-30，3个月内"},
    {"rule_id": "Rule 2.2", "outcome": "pass", "evidence": "月结单显示全名及地址"},
    {"rule_id": "Rule 2.3", "outcome": "fail", "evidence": "高风险评级要求两份独立地址证明，仅一份"},
    {"rule_id": "Rule 3.1", "outcome": "pass", "evidence": "CRS 自我认证表已签署（TIN 模糊）"},
    {"rule_id": "Rule 3.2", "outcome": "fail", "evidence": "TIN 字段手写模糊不可辨"},
    {"rule_id": "Rule 3.3", "outcome": "n/a", "evidence": "客户声明无美国关联"},
    {"rule_id": "Rule 3.4", "outcome": "pass", "evidence": "税务居民国=居住地=Singapore"},
    {"rule_id": "Rule 4.1", "outcome": "pass", "evidence": "OFAC SDN 名单（截至2026-05-08）未命中"},
    {"rule_id": "Rule 4.2", "outcome": "pass", "evidence": "EU第20轮制裁名单未命中"},
    {"rule_id": "Rule 4.3", "outcome": "pass", "evidence": "FATF黑名单（2026-02-13）DPRK/Iran/Myanmar 无关联"},
    {"rule_id": "Rule 4.4", "outcome": "pass", "evidence": "资金非来自Cuba/Iran/DPRK/Syria"},
    {"rule_id": "Rule 4.5", "outcome": "n/a", "evidence": "Russia/China/Singapore不在FATF灰名单"},
    {"rule_id": "Rule 4.6", "outcome": "fail", "evidence": "俄罗斯能源分红触发次级制裁风险评估 — EU第20轮制裁覆盖能源行业"},
    {"rule_id": "Rule 4.7", "outcome": "fail", "evidence": "俄罗斯分红缺乏完整交易链文件"},
    {"rule_id": "Rule 5.1", "outcome": "fail", "evidence": "未签署独立PEP声明表"},
    {"rule_id": "Rule 5.2", "outcome": "fail", "evidence": "配偶ZHANG MEI未完成PEP筛查"},
    {"rule_id": "Rule 5.3", "outcome": "fail", "evidence": "GIC为政府关联机构，需确认客户职级是否构成PEP"},
    {"rule_id": "Rule 6.1", "outcome": "pass", "evidence": "GIC薪资有文件支持（部分通过）"},
    {"rule_id": "Rule 6.2", "outcome": "fail", "evidence": "雇主信函日期2026-03-10，超过30天"},
    {"rule_id": "Rule 6.3", "outcome": "fail", "evidence": "中国ICBC账户流水未提供"},
    {"rule_id": "Rule 6.4", "outcome": "fail", "evidence": "俄罗斯分红USD 180,000未逐笔核实"},
    {"rule_id": "Rule 6.5", "outcome": "pass", "evidence": "薪资与流水基本匹配（附条件）"},
    {"rule_id": "Rule 7.1", "outcome": "fail", "evidence": "EDD补充问卷未提交"},
    {"rule_id": "Rule 7.2", "outcome": "fail", "evidence": "尚未提交至MLRO审批"},
    {"rule_id": "Rule 7.3", "outcome": "n/a", "evidence": "关系尚未建立，不适用"}
  ]
}
```

---

## 规则匹配统计

| 判定结果 | 数量 | 占比 |
|----------|------|------|
| PASS | 11 | 37.9% |
| FAIL | 14 | 48.3% |
| N/A | 3 | 10.3% |
| FAIL（需升级） | 4 | 13.8% |
| **总计** | **29** | 100% |

---

## 真实数据验证引用

### 制裁数据源
- **OFAC SDN List**: 截至2026年5月8日更新 | [OFAC Search](https://sanctionssearch.ofac.treas.gov/)
- **OFAC 制裁国家**: Cuba, Iran, DPRK, Syria 全面禁运 + 乌克兰被占领区域 | [OFAC Programs](https://ofac.treasury.gov/sanctions-programs-and-country-information)
- **EU 第20轮对俄制裁**: 2026年4月23日通过，覆盖能源、军工、贸易、金融服务（含加密货币），延长至2027年 | [Council of EU](https://www.consilium.europa.eu/en/press/press-releases/2026/04/23/russia-s-war-of-aggression-against-ukraine-20th-round-of-stern-eu-sanctions-hits-energy-military-industrial-complex-trade-and-financial-services-including-crypto/)
- **EU 个人制裁延长**: 2026年3月14日延长6个月，新增8名官员 | [Council of EU](https://www.consilium.europa.eu/en/press/press-releases/2026/03/14/russia-s-war-of-aggression-against-ukraine-eu-extends-individual-listings-over-ukraine-s-territorial-integrity-for-a-further-six-months/)

### FATF 名单数据源
- **FATF 黑名单（2026年2月13日）**: DPRK, Iran, Myanmar | [FATF Call for Action](https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/Call-for-action-february-2026.html)
- **FATF 灰名单（2026年2月13日）**: 22个管辖区，新增 Kuwait、Papua New Guinea | [FATF Increased Monitoring](https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-february-2026.html)
- **FATF PEP 定义**: FATF Recommendations, Recommendation 12 — "被委以突出公共职能的个人"，包括国有企业高级管理人员

### 新加坡合规框架
- **MAS AML/CFT 指南**: 新加坡金融机构须遵守 MAS Notice 626（银行）或同等通知的 KYC/AML 要求
- **CRS 申报**: 新加坡为 CRS 签署管辖区，须完成自我认证

---

## 处置说明

本报告为 **规则评分与路由结果**，不做最终审批决定。

**处置路由: ESCALATE-EDD（升级至增强尽职调查）**

升级原因：
1. 俄罗斯能源行业资金来源触发 EU 第20轮制裁及 OFAC 次级制裁风险评估
2. 大额非传统收入来源缺乏完整交易链核实
3. GIC 政府关联机构雇佣背景需 PEP 关联评估
4. 配偶中国国籍未完成独立审查

**下一步行动**:
1. 将本报告提交至 MLRO（洗钱报告官）或高级合规官审批
2. 通知客户补充全部缺失文件（11项）
3. 对俄罗斯分红来源实体进行深度制裁筛查
4. 确认客户在 GIC 的职级，评估 PEP 适用性
5. 完成配偶 PEP 筛查
6. 收到全部补充材料后进行二次规则匹配

---

*本报告由 KYC 合规规则引擎基于 2026 年真实制裁名单与合规框架生成。所有制裁数据截至 2026年5月10日。本技能仅评分与路由，不做最终审批决定。*
