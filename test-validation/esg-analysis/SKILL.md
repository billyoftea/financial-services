---
name: esg-analysis
description: ESG（环境、社会、治理）评分分析与报告生成。支持多评级机构数据整合（MSCI、Sustainalytics、S&P Global）、公司ESG表现对比、E/S/G三维度细分分析、ESG风险识别与机会发现。当用户需要分析ESG评分、生成ESG报告、对比ESG表现、评估ESG风险、或讨论可持续性投资议题时使用此技能。触发场景包括：(1) 分析某公司的ESG评分，(2) 对比多家公司的ESG表现，(3) 生成ESG综合分析报告，(4) 评估ESG相关投资风险与机会，(5) 解读MSCI/Sustainalytics/S&P Global ESG评级。
---

# ESG 评分分析

## 工作流程

1. 确定分析范围：单公司分析 or 多公司对比
2. 获取 ESG 数据：运行 `scripts/esg_data_fetcher.py` 或使用用户提供的数据
3. 分析 E/S/G 维度：对照行业基准评估各维度表现
4. 识别风险与机会：应用红绿灯标准评估
5. 生成报告：运行 `scripts/esg_report_generator.py` 输出 Markdown 或 Excel

## 数据获取

### 从 Yahoo Finance 获取（默认）

```bash
python scripts/esg_data_fetcher.py --ticker AAPL --source yahoo --output json
```

### 多公司对比

```bash
python scripts/esg_data_fetcher.py --tickers AAPL MSFT GOOGL --output json
```

### 从本地文件导入

```bash
python scripts/esg_data_fetcher.py --file esg_data.csv --source csv
python scripts/esg_data_fetcher.py --file esg_data.xlsx --source excel
```

将输出重定向到 JSON 文件保存，供报告生成器使用。

## 维度分析方法

获取数据后，按以下框架分析每个维度：

**环境 (E)**: 碳排放强度、能源效率、资源利用、环境管理
**社会 (S)**: 劳动实践、数据隐私、供应链管理、社区影响
**治理 (G)**: 董事会独立性、高管薪酬、商业伦理、股东权益

对照 `references/esg_metrics.md` 中的行业基准表，判定每个指标处于领先/平均/滞后水平。

## 风险评估标准

应用以下快速判断标准：

| 信号 | MSCI | Sustainalytics | 说明 |
|------|------|---------------|------|
| 红灯 | CCC-BB | >40 | 重大ESG风险 |
| 黄灯 | BBB | 20-30 | 需要关注 |
| 绿灯 | A-AAA | <10 | 表现良好 |

完整评估框架参见 `references/esg_metrics.md` 的"ESG 风险红绿灯标准"章节。

## 报告生成

### Markdown 报告

```bash
python scripts/esg_report_generator.py --input esg_data.json --output esg_report.md
```

### Excel 报告

```bash
python scripts/esg_report_generator.py --input esg_data.json --output esg_report.xlsx
```

### 对比模式

```bash
python scripts/esg_report_generator.py --input comparison.json --output esg_compare.md --compare
```

## 报告结构模板

```markdown
# ESG 分析报告: [公司名称]

## 一、ESG 综合评分
[总评分及各机构评级汇总]

## 二、环境维度 (E) 分析
[碳排放、能源、资源等关键指标与行业基准对比]

## 三、社会维度 (S) 分析
[劳动力、隐私、供应链等关键指标与行业基准对比]

## 四、治理维度 (G) 分析
[董事会、薪酬、伦理等关键指标与行业基准对比]

## 五、风险识别与机会发现
[红/黄/绿灯标注的关键风险点和改善机会]

## 六、投资建议与行动要点
[基于ESG分析的具体建议]
```

## 参考资源

- **评级框架详解**: 需要了解 MSCI/Sustainalytics/S&P Global 评分方法论时，读取 `references/esg_frameworks.md`
- **指标与行业基准**: 需要行业基准数据或指标定义时，读取 `references/esg_metrics.md`
