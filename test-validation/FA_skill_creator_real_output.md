# ESG评分分析技能生成输出

## 技能结构

```
esg-analysis/
├── SKILL.md                              # 核心技能定义文件
├── scripts/
│   ├── esg_data_fetcher.py               # ESG数据获取脚本
│   └── esg_report_generator.py           # ESG报告生成脚本
└── references/
    ├── esg_frameworks.md                 # ESG评级框架参考
    └── esg_metrics.md                    # ESG关键指标与行业基准
```

## SKILL.md 内容

```yaml
---
name: esg-analysis
description: ESG（环境、社会、治理）评分分析与报告生成。支持多评级机构数据整合（MSCI、Sustainalytics、S&P Global）、公司ESG表现对比、E/S/G三维度细分分析、ESG风险识别与机会发现。当用户需要分析ESG评分、生成ESG报告、对比ESG表现、评估ESG风险、或讨论可持续性投资议题时使用此技能。触发场景包括：(1) 分析某公司的ESG评分，(2) 对比多家公司的ESG表现，(3) 生成ESG综合分析报告，(4) 评估ESG相关投资风险与机会，(5) 解读MSCI/Sustainalytics/S&P Global ESG评级。
---
```

### SKILL.md 正文结构

1. **工作流程** - 5步清晰流程：确定范围 -> 获取数据 -> 维度分析 -> 风险识别 -> 生成报告
2. **数据获取** - 支持Yahoo Finance、CSV、Excel三种数据源
3. **维度分析方法** - E/S/G三维度分析框架
4. **风险评估标准** - 红黄绿灯快速判断表
5. **报告生成** - Markdown和Excel两种输出格式
6. **报告结构模板** - 标准化6章节报告模板
7. **参考资源** - 指向references目录的渐进式加载

## scripts/esg_data_fetcher.py

功能：
- 从Yahoo Finance获取ESG评分（基于yfinance）
- 从CSV文件导入ESG数据
- 从Excel文件导入ESG数据
- 支持多公司ESG对比
- 命令行接口，支持 --ticker/--tickers/--file/--source/--output 参数

## scripts/esg_report_generator.py

功能：
- 生成Markdown格式ESG分析报告
- 生成Excel格式ESG分析报告（含样式）
- 支持单公司和多公司对比模式
- 内置Sustainalytics风险等级判断和MSCI质量评级函数

## references/esg_frameworks.md

内容：
- MSCI ESG Ratings评分体系详解（评级范围、关键维度、行业实质性议题）
- Sustainalytics ESG Risk Rating评分体系详解（风险等级划分、关键指标）
- S&P Global CSA/DJSI评分体系详解（评估维度）
- 三家机构评级对比表（评分方向、核心视角、覆盖范围等）

## references/esg_metrics.md

内容：
- 环境维度(E)核心指标（碳排放、资源利用、生物多样性）
- 社会维度(S)核心指标（劳动力、社区与人权、数据隐私）
- 治理维度(G)核心指标（董事会治理、商业伦理、股东权益）
- 行业基准参考（科技、能源、金融三大行业）
- ESG风险红绿灯标准（红灯/黄灯/绿灯判定条件）

## 验证结果

- quick_validate.py: Skill is valid!
- package_skill.py: Successfully packaged to esg-analysis.skill
