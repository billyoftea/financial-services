# GL Reconcile Skill 验证报告

**技能名称:** fund-admin:gl-recon
**测试参数:** "Reconcile GL vs subledger for month-end April 2026, CloudPeak Technologies fund"
**测试日期:** 2026-05-10
**验证人:** 自动化测试

---

## 1. Skill 触发验证

| 检查项 | 结果 | 说明 |
|---|---|---|
| Skill 工具调用 | 通过 | `fund-admin:gl-recon` 通过 Skill 工具成功调用 |
| SKILL.md 加载 | 通过 | SKILL.md 内容完整加载，4步工作流定义清晰 |
| 参数传递 | 通过 | 基金名称 (CloudPeak Technologies) 和期间 (April 2026) 均正确传入并在输出中体现 |
| 语言要求 | 通过 | 输出全程使用中文，技术术语保留英文 |

**结论: Skill 触发正确。**

---

## 2. 输出结构验证 — 是否符合 SKILL.md 定义的4步流程

### Step 1: Normalize（标准化）

| SKILL.md 要求 | 输出是否满足 | 说明 |
|---|---|---|
| 定义统一键值 (common key) | 通过 | 明确指定 `security_id + account + trade_date` |
| 定义比较列 (comparison columns) | 通过 | 列出 quantity, local_amount, base_amount, fx_rate, posting_date |
| 类型强制转换说明 | 通过 | 说明了日期转 ISO、金额转两位小数、标识符大写去空格 |
| 展示标准化后的双方数据 | 通过 | GL 25行 + Subledger 23行，以表格形式展示 |

### Step 2: Match（匹配）

| SKILL.md 要求 | 输出是否满足 | 说明 |
|---|---|---|
| Full outer join 逻辑 | 通过 | 明确说明执行 Full Outer Join |
| 六种 Bucket 分类 | 通过 | Matched / Amount break / Quantity break / Timing break / GL only / Subledger only 全部覆盖 |
| 容差设定 | 通过 | 金额 0.01，数量 0，符合 SKILL.md 默认值 |
| 每行匹配结果清晰标注 | 通过 | 25行逐行标注匹配分类 |

### Step 3: Classify（分类）

| SKILL.md 要求 | 输出是否满足 | 说明 |
|---|---|---|
| 六种原因标签 | 部分通过 | 使用了 Fee/accrual 和 Timing 两种标签；其他四种（FX、Mapping、Duplicate/missing、Data quality）因无对应 break 而未使用，合理 |
| 每条 Break 有原因和说明 | 通过 | B-001 和 B-002 均标注了原因分类和详细说明 |
| 强调为假设而非结论 | 通过 | 说明中使用了"可能原因"和"预计"等措辞 |

### Step 4: Output（输出交付物）

| SKILL.md 要求 | 输出是否满足 | 说明 |
|---|---|---|
| **Break report**（差异明细报告） | 通过 | 包含 key、双方金额、bucket、可能原因、备注，按金额差异绝对值降序排列 |
| **Summary**（汇总报告） | 通过 | 包含按 bucket 和按原因的笔数/金额汇总，以及匹配率 |
| 后续步骤建议 | 通过 | 明确指引提交 `break-trace` 进行根因追踪 |

**结论: 4步流程完整覆盖，结构符合 SKILL.md 定义。**

---

## 3. 交付物完整性检查

| SKILL.md 要求的交付物 | 是否交付 | 位置 |
|---|---|---|
| Break report（差异明细报告） | 是 | "交付物 1: Break Report" 章节 |
| Summary（汇总报告） | 是 | "交付物 2: Summary" 章节 |
| 按 bucket 汇总表 | 是 | Summary 中"按 Bucket 汇总"表 |
| 按原因汇总表 | 是 | Summary 中"按可能原因汇总"表 |
| 匹配率统计 | 是 | 包含按行数 (92.00%) 和按金额 (99.77%) 两种匹配率 |
| 按金额差异降序排列 | 是 | B-001 (87,500) 排在 B-002 (23,400) 之前 |

**结论: SKILL.md 要求的两项交付物（break report + summary）均已产出，无遗漏。**

---

## 4. 数据来源真实性评估

| 评估维度 | 结果 | 说明 |
|---|---|---|
| 是否从真实数据源获取 | 否 | 无真实 GL/Subledger 数据文件或 MCP 数据源可用 |
| 数据是否为模拟构造 | 是 | 基于合理的基金会计场景构造了 25 行 GL 和 23 行 Subledger 数据 |
| 模拟数据是否合理 | 是 | 包含股票交易、债券交易、现金、应计利息、应计费用、应收股利等典型基金会计科目 |
| ISIN 代码是否真实 | 是 | US0378331005 (Apple)、US5949181045 (Microsoft)、US0231351067 (Amazon)、US17275R1023 (Cisco)、US4592005065 (Intel)、US912810SD06 (US Treasury) 均为真实 ISIN |
| 差异场景是否合理 | 是 | 利息应计延迟和股利确认时差是基金会计中常见的月终对账差异 |

**结论: 数据为模拟构造，但场景设置合理、ISIN 真实、差异类型符合实务。如需正式使用，需接入真实 GL/Subledger 数据源。**

---

## 5. 质量评估

| 评估维度 | 评分 (1-5) | 说明 |
|---|---|---|
| **SKILL.md 规范遵循度** | 5 | 完整执行了4步工作流，每个步骤的输出要素齐全 |
| **输出结构与格式** | 4 | Markdown 表格清晰、排版规范；缺少 Excel 格式输出（SKILL.md 未强制要求） |
| **数据合理性** | 4 | 模拟数据专业且自洽，但非真实数据 |
| **差异分析深度** | 4 | 每条 Break 有分类和详细说明，但缺乏对 break-trace 的实际调用 |
| **可操作性** | 4 | 提供了明确的后续步骤建议 |
| **整体质量** | **4** | 输出完整、专业、符合 SKILL.md 规范，主要扣分项为数据非真实来源 |

---

## 6. 发现的问题与改进建议

1. **数据依赖:** Skill 在无真实 GL/Subledger 数据源时需依赖模拟数据。建议在 SKILL.md 中增加数据源获取指引（如 MCP 调用示例或数据文件格式说明）。
2. **Break trace 集成:** 输出中建议了提交 `break-trace`，但未实际调用。可考虑 Skill 之间自动衔接。
3. **Excel 输出:** 对账报告在实务中通常以 Excel 交付，建议增加可选的 xlsx-author 集成。
4. **容差参数化:** SKILL.md 提到"Use the firm's policy if provided"，但未提供参数传递机制。

---

## 7. 总结

| 项目 | 结论 |
|---|---|
| Skill 触发 | 正确 |
| 4步流程 (Normalize-Match-Classify-Output) | 完整覆盖 |
| Break report 交付物 | 已交付 |
| Summary 交付物 | 已交付 |
| 数据来源 | 模拟数据（无真实数据源） |
| 整体质量评分 | **4 / 5** |

Skill 输出完整遵循了 SKILL.md 定义的4步工作流，交付了 break report 和 summary 两个核心交付物。主要局限在于无真实数据源时的模拟数据场景。
