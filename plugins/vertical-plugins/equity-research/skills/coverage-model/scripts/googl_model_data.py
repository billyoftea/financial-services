#!/usr/bin/env python3
"""
googl_model_data.py — Google (GOOGL) 估值模型数据准备
修正版：市占率持平，毛利率/费用率扩张更保守
"""

import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# 修正后的三情景假设
# ============================================================

# ============================================================
# TAM 定义：从GOOGL各分部收入反推对应市场规模
# ============================================================
#
# 分部收入(2025A) → 市占率 → 对应市场TAM:
#   Search & Other:   $224.5B / 91% (Statista) = $247B  (搜索广告市场)
#   YouTube Ads:      $40.4B  / 30% (视频广告份额估算) = $135B
#   Google Cloud:     $58.7B  / 13% (Synergy Q2'25) = $451B  (云基础设施)
#   Network(AdSense): $29.8B  / 20% (估算) = $150B  (第三方广告网络)
#   Subscriptions:    $48B    / 15% (估算) = $320B  (订阅+设备)
#   合计 TAM ≈ $1,300B
#
# 2025A GOOGL总收入 $402.8B / $1,300B ≈ 31.2% 起始市占率
# (这个31.2%是各分部加权市占率的综合体现)
#
# 注意：这里"TAM"不是GOOGL的总潜在市场，而是GOOGL目前参与的各市场之和
# 每个"分部×市占率"代表GOOGL在该分部的真实定位

ASSUMPTIONS = {
    'bear': {
        'tam_start': 1300.0,        # $B - 从分部收入反推的市场总和
        'tam_cagr_1_3': 0.09,
        'tam_cagr_4_6': 0.06,
        'tam_cagr_7_10': 0.04,
        'reachable_rate': 1.00,     # 100% - TAM已定义为GOOGL可触达市场之和
        'share_start': 0.312,       # $402.8B / $1,300B = 31.2%
        'share_end': 0.290,         # 市占率下降（搜索被蚕食 > Cloud增量）
        'gm_start': 0.597,
        'gm_end': 0.580,
        'expense_start': 0.277,
        'expense_end': 0.290,
        'tax_rate': 0.17,
        'pe_start': 22,
        'pe_end': 15,
        'shares_m': 5824,
    },
    'base': {
        'tam_start': 1300.0,
        'tam_cagr_1_3': 0.14,
        'tam_cagr_4_6': 0.10,
        'tam_cagr_7_10': 0.06,
        'reachable_rate': 1.00,
        'share_start': 0.312,
        'share_end': 0.320,         # 基本持平（+0.8pp）
        'gm_start': 0.597,
        'gm_end': 0.615,
        'expense_start': 0.277,
        'expense_end': 0.260,
        'tax_rate': 0.15,
        'pe_start': 27,
        'pe_end': 20,
        'shares_m': 5824,
    },
    'bull': {
        'tam_start': 1300.0,
        'tam_cagr_1_3': 0.20,
        'tam_cagr_4_6': 0.14,
        'tam_cagr_7_10': 0.09,
        'reachable_rate': 1.00,
        'share_start': 0.312,
        'share_end': 0.360,         # Cloud市占率突破+搜索维持
        'gm_start': 0.597,
        'gm_end': 0.640,
        'expense_start': 0.277,
        'expense_end': 0.245,
        'tax_rate': 0.14,
        'pe_start': 33,
        'pe_end': 25,
        'shares_m': 5824,
    },
}

# 历史财务数据 (单位: $M)
HIST_DATA = {
    '2021A': {'revenue': 257637},
    '2022A': {'revenue': 282836, 'cogs': 126203, 'gross_profit': 156633,
              'rd': 39500, 'sga': 26598, 'ebit': 74988, 'net_income': 59972,
              'gross_margin': 0.5538, 'ebit_margin': 0.2651, 'net_margin': 0.2120,
              'rd_ratio': 0.1397, 'sga_ratio': 0.0940},
    '2023A': {'revenue': 307394, 'cogs': 133452, 'gross_profit': 173942,
              'rd': 45364, 'sga': 24870, 'ebit': 84233, 'net_income': 73795,
              'gross_margin': 0.5658, 'ebit_margin': 0.2740, 'net_margin': 0.2401,
              'rd_ratio': 0.1476, 'sga_ratio': 0.0809, 'revenue_growth': 0.0868},
    '2024A': {'revenue': 350018, 'cogs': 146318, 'gross_profit': 203700,
              'rd': 45427, 'sga': 28400, 'ebit': 112230, 'net_income': 100118,
              'gross_margin': 0.5819, 'ebit_margin': 0.3206, 'net_margin': 0.2860,
              'rd_ratio': 0.1298, 'sga_ratio': 0.0811, 'revenue_growth': 0.1387},
    '2025A': {'revenue': 402779, 'cogs': 162322, 'gross_profit': 240457,
              'rd': 49600, 'sga': 29500, 'ebit': 128940, 'net_income': 132190,
              'gross_margin': 0.5969, 'ebit_margin': 0.3200, 'net_margin': 0.3282,
              'rd_ratio': 0.1231, 'sga_ratio': 0.0732, 'revenue_growth': 0.1507},
}

# 估值数据
VAL_DATA = {
    'current_market_cap': 4692900000000,
    'current_price': 387.35,
    'current_pe': 29.6,
    'forward_pe': 26.8,
    'shares_outstanding': 5824000000,
    'fifty_two_week_high': 402.00,
    'fifty_two_week_low': 159.61,
}


def project_scenario(name: str, params: dict, hist_data: dict, n_years: int = 10):
    """对单个情景做完整预测"""
    last_year = max(int(k.replace('A', '')) for k in hist_data)
    last_rev_M = hist_data[f'{last_year}A']['revenue']  # $M
    last_rev_B = last_rev_M / 1000  # $B

    rows = {y: {} for y in range(1, n_years + 1)}

    tam = params['tam_start']
    share_start = params['share_start']
    share_end = params['share_end']
    gm_start = params['gm_start']
    gm_end = params['gm_end']
    exp_start = params['expense_start']  # 起始费用率 (2025A)
    exp_end = params['expense_end']      # 终年费用率
    tax_rate = params['tax_rate']

    tam = params['tam_start']
    for t in range(1, n_years + 1):
        # TAM：每年都增长（包括第一年）
        if t <= 3:
            cagr = params['tam_cagr_1_3']
        elif t <= 6:
            cagr = params['tam_cagr_4_6']
        else:
            cagr = params['tam_cagr_7_10']
        tam = tam * (1 + cagr)

        sam = tam * params['reachable_rate']
        ms = share_start + (share_end - share_start) * (t - 1) / (n_years - 1)
        rev = sam * ms
        gm = gm_start + (gm_end - gm_start) * (t - 1) / (n_years - 1)
        gross_profit = rev * gm

        # 费用率：线性从起始到终年
        exp = exp_start + (exp_end - exp_start) * (t - 1) / (n_years - 1)
        opex = rev * exp
        ebit = gross_profit - opex
        net_income = ebit * (1 - tax_rate)

        # 增速
        if t == 1:
            rev_growth = (rev - last_rev_B) / last_rev_B
        else:
            prev_rev = rows[t - 1]['rev']
            rev_growth = (rev - prev_rev) / prev_rev if prev_rev else 0

        # PE: 线性插值从 pe_start 到 pe_end
        pe_start = params.get('pe_start', params.get('target_pe', 27))
        pe_end = params.get('pe_end', pe_start)  # 如果没有 pe_end，保持不变
        pe = pe_start + (pe_end - pe_start) * (t - 1) / (n_years - 1)

        rows[t] = {
            'tam': tam,
            'sam': sam,
            'ms': ms,
            'rev': rev,
            'rev_growth': rev_growth,
            'gm': gm,
            'gross_profit': gross_profit,
            'exp': exp,
            'opex': opex,
            'ebit': ebit,
            'tax_rate': tax_rate,
            'net_income': net_income,
            'ebit_margin': ebit / rev if rev else 0,
            'net_margin': net_income / rev if rev else 0,
            'pe': pe,
        }

    # 估值：用终年 PE
    terminal_ni = rows[n_years]['net_income']
    terminal_pe = rows[n_years]['pe']
    shares_m = params['shares_m']
    mkt_cap = terminal_ni * terminal_pe
    price = mkt_cap * 1000 / shares_m
    annual_return = (price / VAL_DATA['current_price']) ** (1 / n_years) - 1

    # CAGR
    cagr = (rev / last_rev_B) ** (1 / n_years) - 1

    return {
        'name': name,
        'rows': rows,
        'terminal': {
            'year': last_year + n_years,
            'rev_B': rev,
            'gm': gm,
            'ebit_margin': ebit / rev if rev else 0,
            'net_income_B': net_income,
            'mkt_cap_B': mkt_cap,
            'price': price,
            'cagr': cagr,
            'annual_return': annual_return,
        }
    }


def sanity_checks(scenarios: list, hist_data: dict):
    """三层合理性检验"""
    results = []
    n_years = 10

    # === 第一层：内部逻辑 ===
    for s in scenarios:
        name = s['name'].upper()
        rows = s['rows']

        # 收入增速衰减检查
        growths = [rows[t]['rev_growth'] for t in range(1, n_years + 1)]
        # 检查是否有连续2年增速上升（排除前2年，因为TAM CAGR切换可能有跳变）
        accel_count = 0
        for i in range(1, len(growths)):
            if growths[i] > growths[i-1]:
                accel_count += 1
            else:
                accel_count = 0
        growth_decay_ok = accel_count < 2

        # 增速绝对上限
        max_growth = max(growths)
        growth_abs_ok = max_growth < 0.60

        # 毛利率范围
        gms = [rows[t]['gm'] for t in range(1, n_years + 1)]
        gm_ok = all(0.30 < g < 0.80 for g in gms)

        # EBIT margin 范围
        ebm = [rows[t]['ebit_margin'] for t in range(1, n_years + 1)]
        ebit_ok = all(0 < e < 0.55 for e in ebm)

        results.append({
            'name': f'[{name}] 收入增速衰减',
            'bear': '✓' if name == 'BEAR' else '',
            'base': '✓' if name == 'BASE' else '',
            'bull': '✓' if name == 'BULL' else '',
            'status': '✓ 通过' if growth_decay_ok else '⚠ 注意',
        })
        results.append({
            'name': f'[{name}] 毛利率范围',
            'bear': '✓' if name == 'BEAR' else '',
            'base': '✓' if name == 'BASE' else '',
            'bull': '✓' if name == 'BULL' else '',
            'status': '✓ 通过' if gm_ok else '✗ 不通过',
        })
        results.append({
            'name': f'[{name}] EBIT margin 合理',
            'bear': '✓' if name == 'BEAR' else '',
            'base': '✓' if name == 'BASE' else '',
            'bull': '✓' if name == 'BULL' else '',
            'status': '✓ 通过' if ebit_ok else '✗ 不通过',
        })

    # === 第二层：跨情景排序 ===
    bear_t = scenarios[0]['terminal']
    base_t = scenarios[1]['terminal']
    bull_t = scenarios[2]['terminal']

    order_ok = bull_t['rev_B'] > base_t['rev_B'] > bear_t['rev_B']
    ni_order_ok = bull_t['net_income_B'] > base_t['net_income_B'] > bear_t['net_income_B']

    bull_base_gap = (bull_t['price'] - base_t['price']) / base_t['price']
    base_bear_gap = (base_t['price'] - bear_t['price']) / bear_t['price']
    gap_ok = 0.3 < bull_base_gap < 2.0 and 0.3 < base_bear_gap < 2.0

    results.append({
        'name': '终年收入排序 Bull>Base>Bear',
        'bear': f"${bear_t['rev_B']:.0f}B",
        'base': f"${base_t['rev_B']:.0f}B",
        'bull': f"${bull_t['rev_B']:.0f}B",
        'status': '✓ 通过' if order_ok else '✗ 不通过',
    })
    results.append({
        'name': '终年净利排序 Bull>Base>Bear',
        'bear': f"${bear_t['net_income_B']:.0f}B",
        'base': f"${base_t['net_income_B']:.0f}B",
        'bull': f"${bull_t['net_income_B']:.0f}B",
        'status': '✓ 通过' if ni_order_ok else '✗ 不通过',
    })
    results.append({
        'name': f'情景差距合理性 (B/B={base_bear_gap:.0%}, Bu/B={bull_base_gap:.0%})',
        'bear': '',
        'base': '',
        'bull': '',
        'status': '✓ 通过' if gap_ok else '⚠ 差距偏大',
    })

    # === 第三层：外部基准 ===
    base_cagr = base_t['cagr']
    results.append({
        'name': f'Base CAGR ({base_cagr:.1%}) vs MSFT历史 (~12%)',
        'bear': '',
        'base': f'{base_cagr:.1%}',
        'bull': '',
        'status': '✓ 合理' if 0.05 < base_cagr < 0.20 else '⚠ 偏离',
    })

    return results


def main():
    scenarios = []
    for name in ['bear', 'base', 'bull']:
        proj = project_scenario(name, ASSUMPTIONS[name], HIST_DATA)
        scenarios.append(proj)

        t = proj['terminal']
        print(f"\n{'='*60}")
        print(f"  {name.upper()} CASE — 终年 {t['year']}E")
        print(f"{'='*60}")
        print(f"  收入:       ${t['rev_B']:>10,.1f}B  (CAGR: {t['cagr']:.1%})")
        print(f"  毛利率:     {t['gm']:>10.1%}")
        print(f"  EBIT margin:{t['ebit_margin']:>10.1%}")
        print(f"  净利润:     ${t['net_income_B']:>10,.1f}B")
        print(f"  隐含市值:   ${t['mkt_cap_B']:>10,.1f}B")
        print(f"  隐含股价:   ${t['price']:>10,.1f}")
        print(f"  vs 当前:    {(t['price']/387.35 - 1):>10.1%}")
        print(f"  年化回报:   {t['annual_return']:>10.1%}")

    # 逐年明细（Base case）
    base_rows = scenarios[1]['rows']
    print(f"\n{'='*80}")
    print(f"  BASE CASE — 逐年明细")
    print(f"{'='*80}")
    header = f"{'Year':>6} {'TAM':>8} {'SAM':>8} {'MS':>6} {'Rev':>8} {'Gr':>6} {'GM':>6} {'EBIT':>8} {'NI':>8} {'PE':>5} {'Price':>8}"
    print(f"  {header}")
    print(f"  {'-'*82}")
    for t in range(1, 11):
        r = base_rows[t]
        year = 2025 + t
        implied_price = r['net_income'] * r['pe'] * 1000 / 5824
        print(f"  {year}E {r['tam']:>8,.0f} {r['sam']:>8,.0f} {r['ms']:>6.1%} "
              f"{r['rev']:>8,.1f} {r['rev_growth']:>6.1%} {r['gm']:>6.1%} "
              f"{r['ebit']:>8,.1f} {r['net_income']:>8,.1f} {r['pe']:>5.1f} "
              f"${implied_price:>8,.1f}")

    # 合理性检验
    checks = sanity_checks(scenarios, HIST_DATA)
    print(f"\n{'='*60}")
    print(f"  合理性检验")
    print(f"{'='*60}")
    for c in checks:
        vals = ' | '.join(filter(None, [c['bear'], c['base'], c['bull']]))
        print(f"  {c['name']:<40} {c['status']}")

    # 假设来源注释（说明每个数字是怎么推导出来的）
    sources = {
        'tam_start': (
            "$1,300B = GOOGL各分部对应市场之和（从分部收入反推）:\n"
            "分部收入(2025A) → 市占率 → 对应市场规模:\n"
            "(1) Search & Other: $224.5B / 91%市占率(Statista) = $247B 搜索广告市场\n"
            "(2) YouTube Ads: $40.4B / 30%市占率(视频广告份额估算) = $135B\n"
            "(3) Google Cloud: $58.7B / 13%市占率(Synergy Research Q2'25) = $451B 云基础设施\n"
            "(4) Network(AdSense): $29.8B / 20%市占率(估算) = $150B 第三方广告网络\n"
            "(5) Subscriptions/Devices: $48B / 15%市占率(估算) = $320B\n"
            "合计 $1,303B → 取整 $1,300B\n"
            "验证: GOOGL总收入$402.8B / $1,300B = 31.2% ✓"
        ),
        'tam_cagr_1_3': (
            "Base 14% = 各市场增速加权:\n"
            "(1) 搜索广告市场: 权重19% × 增速10% (eMarketer: 数字广告增速首次个位数)\n"
            "(2) 视频广告市场: 权重10% × 增速12% (视频广告增速>整体广告)\n"
            "(3) Cloud市场: 权重35% × 增速21% (Gartner: 2026公有云增速21.3%, AI驱动)\n"
            "(4) 广告网络市场: 权重12% × 增速5% (隐私政策压制,萎缩)\n"
            "(5) 订阅/设备市场: 权重24% × 增速13% (Grand View: streaming CAGR 13.2%)\n"
            "加权: 19%×10% + 10%×12% + 35%×21% + 12%×5% + 24%×13% = 14.3% ≈ 14%\n"
            "Bull 20%: AI爆发,Cloud增速超预期\n"
            "Bear 9%: 广告+Cloud双双放缓"
        ),
        'tam_cagr_4_6': (
            "Base 10%: S曲线衰减\n"
            "Cloud渗透率从当前~30%向50%过渡, 增速从21%降到15%\n"
            "参考: AWS增速轨迹 50%(2015)→30%(2020)→19%(2025), Synergy Research\n"
            "广告市场增速稳定在8-10% (成熟期)\n"
            "加权 ≈ 10%"
        ),
        'tam_cagr_7_10': (
            "Base 6%: 接近GDP+通胀的成熟期\n"
            "参考: Gartner全球IT支出长期CAGR 5-6%\n"
            "Cloud渗透率>50%后增速降到10-12%, 权重稀释后整体~6%"
        ),
        'reachable_rate': (
            "100% (三情景统一):\n"
            "此TAM已定义为GOOGL目前参与的市场之和\n"
            "不是'全球数字经济'这种宽泛概念\n"
            "GOOGL 2025A收入$402.8B全部来自这$1,300B市场, 可触达率=100%"
        ),
        'share_start': (
            "31.2% = 2025A实际\n"
            "= GOOGL总收入$402.8B / TAM$1,300B\n"
            "本质是各分部市占率的加权平均:\n"
            "  Search 91% × 搜索市场权重19%\n"
            "  + Cloud 13% × Cloud市场权重35%\n"
            "  + YouTube 30% × 视频权重10%\n"
            "  + Network 20% × 广告网络权重12%\n"
            "  + Subscriptions 15% × 订阅权重24%\n"
            "  = 31.2% ✓"
        ),
        'share_end': (
            "Base 32.0% (+0.8pp, 微升):\n"
            "分部拆解:\n"
            "  Search: 91%微降到88-89% (AI搜索蚕食, 参考: Intel CPU 90%→70%花8年)\n"
            "  Cloud: 13%涨到16-17% (Synergy: GCP从2022年10%→2025年13%, 每年+1pp)\n"
            "  YouTube: 30%维持 (短视频竞争激烈)\n"
            "  Network: 20%降到15% (AdSense萎缩,隐私政策)\n"
            "  Subscriptions: 15%涨到18% (YouTube Premium增长)\n"
            "加权后 ≈ 32%, 比31.2%微升(+0.8pp)\n"
            "Bull 36%: Cloud突破到20%+搜索维持\n"
            "Bear 29%: 搜索被AI颠覆+反垄断限制"
        ),
        'gm_start': (
            "59.7% = 2025A实际值\n"
            "历史轨迹: 55.4%(2022)→56.6%(2023)→58.2%(2024)→59.7%(2025)\n"
            "年均+1.1pp, 主因Cloud扭亏"
        ),
        'gm_end': (
            "Base 61.5% (+1.8pp / 10年, 年均+0.18pp):\n"
            "扩张支撑:\n"
            "  (1) Cloud扭亏: GCP 2023首次季度盈利, OPM从负→15-20%\n"
            "  (2) AI提升搜索变现: targeting精准→CPM↑\n"
            "压制因素:\n"
            "  (1) AI CapEx折旧: 2025 CapEx~$75B, 5-7年折旧进COGS, 年~$10-15B\n"
            "  (2) Cloud占比↑但利润率低: Cloud OPM 15-20% vs Search 40%+\n"
            "  (3) 硬件(Pixel)增长, 硬件GM 30-40%远低于搜索\n"
            "参考: MSFT毛利率65-70%(软件+Cloud), GOOGL硬件拖后腿"
        ),
        'expense_start': (
            "27.7% = 2025A实际\n"
            "= (收入 - COGS - EBIT) / 收入\n"
            "= ($402.8B - $162.3B - $128.9B) / $402.8B\n"
            "= R&D $49.6B(12.3%) + SGA $29.5B(7.3%) + 其他运营费用"
        ),
        'expense_end': (
            "Base 26.0% (-1.7pp / 10年):\n"
            "参考: META费用率从45%(2022)降到30%(2024), 裁员+效率年\n"
            "参考: MSFT费用率~30%(含更高R&D占比), GOOGL 27.7%已较低\n"
            "限制因素:\n"
            "  (1) AI人才成本高: ML researcher薪酬>$400K (Levels.fyi)\n"
            "  (2) Gemini需持续R&D: 2025A R&D $49.6B, YoY +9%\n"
            "历史: 2022→2025费用率仅降0.6pp, 取-1.7pp/10年保守"
        ),
        'tax_rate': (
            "Base 15%:\n"
            "GOOGL历史有效税率: ~16% (2024A 10-K)\n"
            "影响因素:\n"
            "  (1) 海外收入税率较低\n"
            "  (2) R&D税收抵免\n"
            "  (3) 股权投资收益/亏损波动"
        ),
        'pe_start': (
            "PE起始值:\n"
            "Base 27x: GOOGL 5年PE区间17-30, 中位27.4 (yfinance)\n"
            "  当前TTM 29.6x, Forward 26.8x\n"
            "Bull 33x: AI溢价维持, 参考 MSFT当前PE~35x\n"
            "Bear 22x: 已低于历史中位, 市场折价"
        ),
        'pe_end': (
            "PE终年值(增速衰减后):\n"
            "Base 20x: 增速降至~6%时合理PE\n"
            "  参考: MSFT PE从35x(高增长)→25x(增速~15%)→20x(成熟)\n"
            "  参考: AWS增速50%→19%, Amazon整体PE从80x压到30x\n"
            "  参考: Cisco极端 100x→15x\n"
            "Bull 25x: 即使Bull增速也放缓\n"
            "Bear 15x: 价值陷阱, 增长停滞"
        ),
        'shares_m': (
            "5,824M = yfinance sharesOutstanding\n"
            "假设10年不变(保守: GOOGL回购力度大, 实际可能降5-10%)"
        ),
    }

    # 输出 JSON 供 build_excel.py 使用
    output = {
        'hist_data': HIST_DATA,
        'val_data': VAL_DATA,
        'assumptions': ASSUMPTIONS,
        'checks': checks,
        'sources': sources,
        'language': 'zh-CN',  # 中文输出
        'currency_symbol': '$',
        'unit_suffix': 'M',
        'fiscal_year_analysis': {
            'fy_end_month': 12,
            'fiscal_year_end': '12-31',
            'is_calendar_year': True,
            'mapping_rule': 'FY ends in December, aligned with calendar year',
            'date_mappings': {},
            'fiscal_year_note': 'Google fiscal year ends December 31, aligned with calendar year. No mapping needed.',
        },
    }

    out_path = './out/googl_model_data.json'
    import os
    os.makedirs('./out', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存到 {out_path}")


if __name__ == '__main__':
    main()
