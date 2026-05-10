# FA_clean_data_xls 技能执行输出

## 基本信息

- **技能名称**: financial-analysis:clean-data-xls
- **输入文件**: test-validation/test_dirty_data.xlsx
- **输出文件**: test-validation/test_cleaned_data.xlsx
- **执行时间**: 2026-05-10
- **环境**: Python/openpyxl（独立 .xlsx 文件模式）

---

## Step 1: 确定范围 (Scope)

### 数据范围

- **工作表**: Financial Data（主数据表）、Valuation（汇总公式表）
- **范围**: A1:F11
- **数据行数**: 10 行（不含表头）
- **列数**: 6 列

### 列概要 (Column Profile)

| 列 | 表头 | 主导类型 | 非空值 | 类型分布 |
|----|------|----------|--------|----------|
| A | Company | text | 9/10 | str:9, None:1 |
| B | Revenue ($M) | number | 9/10 | int:8, str:1, None:1 |
| C | Growth % | number | 10/10 | float:8, str:2 |
| D | Date | date | 10/10 | datetime:8, str:2 |
| E | Region | text | 10/10 | str:10 |
| F | Notes | text | 9/10 | str:9, None:1 |

---

## Step 2: 检测问题 (Detect Issues)

共检测到 **15 个问题**，涵盖 8 种问题类型：

| # | 列 | 行 | 问题类型 | 原始值 | 说明 |
|---|-----|-----|----------|--------|------|
| 1 | Company | 3 | 空白字符 | `'  NVIDIA  '` | 前后空格 |
| 2 | Company | 10 | 空值缺失 | `None` | 公司名称缺失 |
| 3 | Company | 6 | 大小写不一致 | `'intel'` | 与行7的 `'Intel'` 不一致 |
| 4 | Revenue | 3 | 文本型数字 | `'215900'` | 数字存储为文本 |
| 5 | Revenue | 9 | 空值缺失 | `None` | 收入数据缺失 |
| 6 | Growth | 3 | 文本型数字(%) | `'65%'` | 百分比存储为文本带%符号 |
| 7 | Growth | 5 | 文本型数字 | `'0.25'` | 小数存储为文本 |
| 8 | Date | 3 | 混合日期格式 | `'2026-01-26'` | ISO格式文本日期 |
| 9 | Date | 5 | 混合日期格式 | `'03/29/2026'` | 美式格式文本日期 |
| 10 | Region | 3 | 空白字符 | `'US '` | 尾部空格 |
| 11 | Region | 6 | 大小写不一致 | `'us'` | 小写地区代码 |
| 12 | Notes | 3 | 空白字符 | `'   AI leader   '` | 前后空格 |
| 13 | Notes | 9 | 空值缺失 | `None` | 备注缺失 |
| 14 | Row | 6 vs 7 | 近似重复行 | intel/Intel | 仅大小写差异的重复行 |
| 15 | Company | 10 | 空值缺失 | `None` | 公司名称缺失 |

---

## Step 3: 修复建议 (Propose Fixes)

| 列 | 问题类型 | 数量 | 建议修复方式 |
|----|----------|------|-------------|
| Company | 空白字符 | 1 | TRIM 去除前后空格 |
| Company | 大小写不一致 | 1 | PROPER 标准化为首字母大写 |
| Company | 空值缺失 | 1 | 标记为 (missing) 待人工审核 |
| Revenue | 文本型数字 | 1 | VALUE 转换文本为数字 |
| Revenue | 空值缺失 | 1 | 标记为 (missing) 待人工审核 |
| Growth | 文本型数字(%) | 1 | VALUE(SUBSTITUTE(x,"%",""))/100 转换 |
| Growth | 文本型数字 | 1 | VALUE 转换文本为数字 |
| Date | 混合日期格式 | 2 | DATEVALUE 解析文本日期为datetime |
| Region | 空白字符 | 1 | TRIM 去除尾部空格 |
| Region | 大小写不一致 | 1 | UPPER 标准化为大写 |
| Notes | 空白字符 | 1 | TRIM 去除前后空格 |
| Notes | 空值缺失 | 1 | 标记为 (missing) 待人工审核 |
| Row | 近似重复 | 2组 | 删除重复行（行3=行2清洗后相同，行7=行6仅大小写差异） |

---

## Step 4: 执行修复 (Apply)

### Fix 1: 空白字符清理 (Whitespace)

| 行 | 列 | 修复前 | 修复后 |
|----|-----|--------|--------|
| 3 | A (Company) | `'  NVIDIA  '` | `'NVIDIA'` |
| 3 | E (Region) | `'US '` | `'US'` |
| 3 | F (Notes) | `'   AI leader   '` | `'AI leader'` |

### Fix 2: 大小写标准化 (Casing)

| 行 | 列 | 修复前 | 修复后 |
|----|-----|--------|--------|
| 6 | A (Company) | `'intel'` | `'Intel'` |
| 6 | E (Region) | `'us'` | `'US'` |

### Fix 3: 文本型数字转换 (Number-as-text)

| 行 | 列 | 修复前 | 修复后 |
|----|-----|--------|--------|
| 3 | B (Revenue) | `'215900'` | `215900` (int) |
| 3 | C (Growth) | `'65%'` | `0.65` (float) |
| 5 | C (Growth) | `'0.25'` | `0.25` (float) |

### Fix 4: 日期格式统一 (Date Standardization)

| 行 | 列 | 修复前 | 修复后 |
|----|-----|--------|--------|
| 3 | D (Date) | `'2026-01-26'` (str) | `2026-01-26` (datetime) |
| 5 | D (Date) | `'03/29/2026'` (str) | `2026-03-29` (datetime) |
| 所有 | D (Date) | 混合格式 | 统一 `yyyy-mm-dd` |

### Fix 5: 近似重复行删除 (Near-duplicate Removal)

| 操作 | 行 | 说明 |
|------|-----|------|
| 删除 | 原行7 | 与行6 (intel/Intel) 仅大小写差异，清洗后完全相同 |

### Fix 6: 清洗后重复检测 (Post-cleaning Dedup)

| 操作 | 行 | 说明 |
|------|-----|------|
| 删除 | 原行3 (清洗后) | 原始行3有空白/文本问题，清洗后与行2 (NVIDIA) 完全相同 |

### 空值标记 (Blank Flagging)

| 行 | 列 | 处理方式 |
|----|-----|----------|
| 8 (原9) | B (Revenue) | 标记为 `(missing)`，黄色高亮 |
| 8 (原9) | F (Notes) | 标记为 `(missing)`，黄色高亮 |
| 9 (原10) | A (Company) | 标记为 `(missing)`，黄色高亮 |

### 格式统一

- Revenue 列: `#,##0`
- Growth 列: `0.00%`
- Date 列: `yyyy-mm-dd`
- 表头: 加粗、白字、蓝色背景、居中

---

## 清洗前后对比

### 清洗前 (10 行数据)

| Company | Revenue ($M) | Growth % | Date | Region | Notes |
|---------|-------------|----------|------|--------|-------|
| NVIDIA | 215900 | 0.65 | 2026-01-26 | US | AI leader |
| `  NVIDIA  ` | `'215900'` | `'65%'` | `'2026-01-26'` | `US ` | `   AI leader   ` |
| AMD | 10250 | 0.38 | 2026-03-29 | US | Gaming+DC |
| Broadcom | 19310 | `'0.25'` | `'03/29/2026'` | US | Networking |
| `intel` | 12300 | -0.08 | 2026-03-29 | `us` | Turnaround |
| Intel | 12300 | -0.08 | 2026-03-29 | US | Turnaround |
| Qualcomm | 15800 | 0.15 | 2026-03-29 | US | Mobile+IoT |
| Texas Instruments | (空) | 0.12 | 2026-03-29 | US | (空) |
| (空) | 8900 | 0.1 | 2026-03-29 | US | Blank name |
| ASML | 14300 | 0.18 | 2026-03-29 | EU | EUV monopoly |

### 清洗后 (8 行数据，删除2行重复)

| Company | Revenue ($M) | Growth % | Date | Region | Notes |
|---------|-------------|----------|------|--------|-------|
| NVIDIA | 215,900 | 65% | 2026-01-26 | US | AI leader |
| AMD | 10,250 | 38% | 2026-03-29 | US | Gaming+DC |
| Broadcom | 19,310 | 25% | 2026-03-29 | US | Networking |
| Intel | 12,300 | -8% | 2026-03-29 | US | Turnaround |
| Qualcomm | 15,800 | 15% | 2026-03-29 | US | Mobile+IoT |
| Texas Instruments | (missing) | 12% | 2026-03-29 | US | (missing) |
| (missing) | 8,900 | 10% | 2026-03-29 | US | Blank name |
| ASML | 14,300 | 18% | 2026-03-29 | EU | EUV monopoly |

---

## 总计变更

- **总修复数**: 15 项
- **删除行数**: 2 行（1行近似重复 + 1行清洗后重复）
- **空白修复**: 3 处
- **大小写修复**: 2 处
- **文本型数字修复**: 3 处
- **日期格式修复**: 2 处
- **空值标记**: 3 处
- **格式统一**: 3 列
