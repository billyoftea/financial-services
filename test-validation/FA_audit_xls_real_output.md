# 电子表格审计报告

**审计日期：** 2026年5月10日
**审计范围：** Sheet（Valuation 工作表）
**审计文件：** test_dirty_data.xlsx
**工作表数量：** 2（Financial Data, Valuation）

---

## 审计范围确认

用户指定：**sheet** 范围，目标工作表为 **Valuation**。
该工作表包含2个公式，均引用 Financial Data 工作表的数据。

---

## 审计结果总览

| 指标 | 数量 |
|---|---|
| Critical | 4 |
| Warning | 5 |
| Info | 3 |
| **合计** | **12** |

---

## 详细发现表

| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested Fix |
|---|---|---|---|---|---|---|
| 1 | Financial Data | B3 | **Critical** | 数值存储为文本 | Revenue 值 `'215900'` 以文本格式存储，`=SUM('Financial Data'!B2:B11)` 会自动忽略该单元格，导致总计少算 $215,900M | 将 B3 单元格转换为数值格式：清除内容后重新输入 215900，或使用 `=VALUE(B3)` |
| 2 | Financial Data | C3 | **Critical** | 数值存储为文本 | Growth 值 `'65%'` 以文本格式存储，`=AVERAGE('Financial Data'!C2:C11)` 会自动忽略该单元格，导致平均值计算错误 | 将 C3 转换为数值 0.65，或使用百分比格式存储 |
| 3 | Financial Data | C5 | **Critical** | 数值存储为文本 | Growth 值 `'0.25'` 以文本格式存储（ Broadcom ），AVERAGE 公式同样会忽略此值 | 将 C5 从文本 `'0.25'` 转换为数值 0.25 |
| 4 | Financial Data | B9 | **Critical** | 缺失数据 | Texas Instruments 的 Revenue 为空（ None ），SUM 公式跳过该行，但该公司应有收入数据 | 补充 Texas Instruments 的 Revenue 数据 |
| 5 | Financial Data | B2:B11 | **Warning** | 重复行 | NVIDIA 出现两次：Row 2（`'NVIDIA'`）和 Row 3（`'  NVIDIA  '`），收入均为 215,900，SUM 会重复计算 | 删除重复行 Row 3，或确认是否为不同实体的数据 |
| 6 | Financial Data | A6:A7 | **Warning** | 重复行 | Intel 出现两次：Row 6（`'intel'`）和 Row 7（`'Intel'`），数据完全相同 | 删除重复行 Row 6 或 Row 7 |
| 7 | Financial Data | A10 | **Warning** | 缺失标识 | Row 10 公司名为空（ A10=None ），但 B10=8900 有收入数据，该笔收入会被计入 SUM 但无法归属 | 补充 Row 10 的公司名称 |
| 8 | Financial Data | A3, E3, F3 | **Warning** | 空白字符污染 | 单元格内容前后含空白字符：`'  NVIDIA  '`、`'US '`、`'   AI leader   '`，可能导致 VLOOKUP/MATCH 等函数匹配失败 | 使用 `=TRIM()` 清除多余空白，或手动清理 |
| 9 | Financial Data | D列 | **Warning** | 日期格式不一致 | D2 为 datetime 对象，D3 为文本 `'2026-01-26'`，D5 为文本 `'03/29/2026'`，其他行为 datetime。混合格式会导致日期排序和比较失败 | 统一为 datetime 格式，使用 `=DATEVALUE()` 转换文本日期 |
| 10 | Financial Data | A6 vs A7 | **Info** | 大小写不一致 | `'intel'`（全小写）vs `'Intel'`（首字母大写），影响数据标准化和分组 | 统一公司名称格式为 Proper Case |
| 11 | Financial Data | E6 | **Info** | 大小写不一致 | Region 列 `'us'`（小写）vs 其他行 `'US'`（大写），影响筛选和分组 | 统一 Region 为大写 |
| 12 | Valuation | B2:B3 | **Info** | 跨工作表引用完整性 | 公式引用范围 `'Financial Data'!B2:B11` 和 `C2:C11` 包含所有 10 行数据，但由于源数据存在文本格式和缺失值，实际计算结果可能偏离预期 | 修复源数据后验证公式结果 |

---

## 关键发现详解

### 1. 公式计算影响量化

**`=SUM('Financial Data'!B2:B11)`**

| 项目 | 值 |
|---|---|
| 当前公式实际计算结果 | 309,060 |
| 期望结果（所有数值正确） | 524,960 |
| **差异** | **-215,900（少算 41.1%）** |

原因分析：
- B3 = `'215900'`（文本）被 SUM 忽略 → 少算 215,900
- B9 = None（缺失）被 SUM 忽略 → TI 收入缺失

**`=AVERAGE('Financial Data'!C2:C11)`**

| 项目 | 值 |
|---|---|
| 当前公式实际计算结果 | 17.75% |
| 期望结果（所有数值正确） | 23.20% |
| **差异** | **-5.45 个百分点** |

原因分析：
- C3 = `'65%'`（文本）被 AVERAGE 忽略
- C5 = `'0.25'`（文本）被 AVERAGE 忽略

### 2. 重复数据影响

- NVIDIA（Row 2 + Row 3）：如果 Row 3 的 Revenue 被修复为数值，SUM 会将 NVIDIA 收入计算两次（431,800 而非 215,900）
- Intel（Row 6 + Row 7）：收入已重复计入 24,600 而非 12,300

### 3. 公式结构评价

- Valuation 工作表的公式语法正确，跨工作表引用路径无误
- 未检测到循环引用
- 未检测到 `#REF!`、`#VALUE!`、`#N/A`、`#DIV/0!`、`#NAME?` 等公式错误
- 无隐藏行、隐藏列或合并单元格

---

## 修复优先级建议

1. **立即修复（Critical）：** 将 B3、C3、C5 从文本转换为数值格式；补充 B9 缺失数据
2. **尽快修复（Warning）：** 删除重复行（Row 3 NVIDIA、Row 6/7 Intel 之一）；补充 Row 10 公司名称
3. **建议改进（Info）：** 统一大小写格式、清理空白字符、统一日期格式

---

---

# 附录：FA_comps_semiconductor.xlsx Model级别审计

**审计日期：** 2026年5月10日
**审计范围：** Model（整个工作簿）
**审计文件：** FA_comps_semiconductor.xlsx
**模型类型：** Comps（可比公司分析）

---

## Model审计结果总览

> Model type: Comps — Overall: Minor Issues — 1 critical, 4 warnings, 3 info

| 指标 | 数量 |
|---|---|
| Critical | 1 |
| Warning | 4 |
| Info | 3 |
| **合计** | **8** |

---

## 详细发现表

| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested Fix |
|---|---|---|---|---|---|---|
| 1 | Comps Analysis | I28 | **Critical** | PEG计算错误 | INTC PEG = 14.51，但 PE(TTM) = -201.5, Growth = 7%，正确 PEG 应为 -28.79（或标记为 N/A）。当前值 14.51 使用了绝对值或 Forward PE，逻辑不透明 | 对于负 PE 公司，PEG 应标记为 N/A 或使用 Forward PE / Growth 并注明 |
| 2 | Comps Analysis | H24:I31 | **Warning** | 硬编码值 | EV/EBITDA vs 10Y Median（H列）和 PEG Ratio（I列）均为硬编码数值，而非公式计算。共 16 个硬编码单元格 | 建议将 PEG 改为公式 `=F24/(C7*100)`，或将 EV/EBITDA vs 10Y Median 标注为外部数据源引用 |
| 3 | Comps Analysis | I29, I30 | **Warning** | PEG计算不一致 | MRVL PEG = 0.73（存储值）vs 计算值 1.23（PE=51.8/Growth=42.1%）；ARM PEG = 6.32（存储值）vs 计算值 10.00（PE=250/Growth=25%）。差异来源不明 | 核实 PEG 数据来源是否使用了不同定义（如 Forward PEG），并在注释中说明 |
| 4 | Comps Analysis | B16:B20, B33:B37 | **Warning** | 统计公式缺失 | 统计行（Max/75th/Median/25th/Min）中，B 列（Revenue / Market Cap）无公式，与其他列不一致 | 补充 B 列统计公式，或在注释中说明为何不计算 Revenue/MC 统计 |
| 5 | Comps Analysis | K11 | **Warning** | 负PE值 | INTC PE(TTM) = -201.5，公司处于净亏损状态，负 PE 在统计计算（MAX/MEDIAN）中会扭曲结果 | 将 INTC PE 标记为 N/A 或使用 Forward PE 替代，统计公式中排除负值 |
| 6 | Comps Analysis | J13, K13 | **Info** | 极端估值倍数 | ARM EV/EBITDA = 200x, PE(TTM) = 250x，远超行业正常范围（半导体行业 EV/EBITDA 通常 15-50x） | 确认数据准确性，ARM 的高增长和高利润率可能支撑高估值，但需在报告中注明 |
| 7 | Comps Analysis | E列 | **Info** | 列含义不一致 | E 列在 Operating Statistics 区为 EBITDA($B)（Row 7-14），在 Valuation Multiples 区为 EV/EBITDA(x)（Row 24-31）。虽然分区有标题区分，但同列不同含义增加了误读风险 | 考虑在 Valuation 区调整列顺序，或在 E 列添加明确的列头区分 |
| 8 | Comps Analysis | F9 | **Info** | 浮点精度 | AVGO EBITDA Margin = 0.5870000000000001（应为 0.587），存在浮点精度误差 | 使用 `=ROUND(E9/B9, 3)` 替代直接除法 |

---

## 结构性评价

### 正面发现
- 工作表结构清晰，分为 Operating Statistics、Valuation Multiples、Notes 三个区域
- 公式模式一致（D24:D31 全部使用 `=Cxx/Jxx` 格式）
- 统计函数使用正确（MAX/MIN/MEDIAN/QUARTILE）
- 跨区域引用正确（Valuation 区 A24:A31 引用 Operating 区 A7:A14）
- 包含详细的方法论注释（Row 39-56）

### 待改进
- H 列和 I 列全部硬编码，降低了模型可审计性
- 缺少数据更新日期的动态引用
- 无输入/计算颜色编码区分

---

*审计报告由 audit-xls 技能生成 — 未经修改前，请勿修改原始文件。*
