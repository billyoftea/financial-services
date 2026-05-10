import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

output_dir = "C:/Users/Lenovo/Desktop/financial-services-fork/financial-services/test-validation/charts_earnings"
os.makedirs(output_dir, exist_ok=True)

# Style settings
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.facecolor'] = '#FAFAFA'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

TESLA_BLUE = '#1A3A5C'
TESLA_RED = '#CC0000'
GREEN = '#2E8B57'
LIGHT_BLUE = '#4A90D9'
GRAY = '#888888'
GOLD = '#DAA520'

quarters = ["Q1'24", "Q2'24", "Q3'24", "Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26"]
x = np.arange(len(quarters))
width = 0.35

# ============ Chart 1: Quarterly Revenue Progression ============
revenue_actual = [21.30, 25.50, 25.18, 25.71, 19.34, 24.93, 25.18, 25.71, 22.39]
revenue_estimate = [21.50, 24.80, 25.40, 27.30, 21.70, 24.20, 25.40, 27.10, 22.64]

fig, ax = plt.subplots(figsize=(10, 5))
bars1 = ax.bar(x - width/2, revenue_actual, width, label='Actual', color=TESLA_BLUE, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, revenue_estimate, width, label='Consensus', color=LIGHT_BLUE, alpha=0.6, edgecolor='white', linewidth=0.5)
bars1[-1].set_color(GREEN)

for i, (a, e) in enumerate(zip(revenue_actual, revenue_estimate)):
    diff_pct = (a - e) / e * 100
    color = GREEN if diff_pct >= 0 else TESLA_RED
    symbol = '+' if diff_pct >= 0 else ''
    if i == len(quarters) - 1:
        ax.annotate(f'{symbol}{diff_pct:.1f}%', xy=(i, max(a, e) + 0.3), fontsize=9, ha='center',
                    fontweight='bold', color=color,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9))

ax.set_ylabel('Revenue ($B)', fontsize=11)
ax.set_title('Figure 1: Tesla Quarterly Revenue - Actual vs Consensus', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(quarters, fontsize=9)
ax.legend(loc='upper left', fontsize=9)
ax.set_ylim(0, 32)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart1_revenue_progression.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 2: Quarterly EPS Progression ============
eps_actual = [0.45, 0.52, 0.72, 0.73, 0.27, 0.52, 0.72, 0.73, 0.41]
eps_consensus = [0.43, 0.50, 0.60, 0.75, 0.39, 0.50, 0.60, 0.75, 0.37]

fig, ax = plt.subplots(figsize=(10, 5))
bars_a = ax.bar(x - width/2, eps_actual, width, label='Actual EPS (Non-GAAP)', color=TESLA_BLUE, edgecolor='white', linewidth=0.5)
bars_c = ax.bar(x + width/2, eps_consensus, width, label='Consensus EPS', color=LIGHT_BLUE, alpha=0.6, edgecolor='white', linewidth=0.5)
bars_a[-1].set_color(GREEN)

for i, (a, c) in enumerate(zip(eps_actual, eps_consensus)):
    marker = 'Beat' if a >= c else 'Miss'
    color = GREEN if a >= c else TESLA_RED
    ax.annotate(marker, xy=(i, max(a, c) + 0.015), fontsize=7, ha='center', color=color, fontweight='bold')

ax.set_ylabel('EPS ($)', fontsize=11)
ax.set_title('Figure 2: Tesla Quarterly EPS - Actual vs Consensus', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(quarters, fontsize=9)
ax.legend(loc='upper left', fontsize=9)
ax.set_ylim(0, 1.0)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart2_eps_progression.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 3: Margin Trends ============
gross_margin = [17.4, 18.0, 19.8, 20.6, 16.2, 18.5, 19.8, 20.3, 21.1]
op_margin = [5.5, 6.3, 8.1, 7.9, 2.1, 6.0, 8.1, 7.6, 4.2]
auto_gm_excl = [15.6, 16.1, 17.4, 18.2, 13.5, 16.2, 17.5, 18.0, 19.2]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(quarters, gross_margin, 'o-', color=TESLA_BLUE, linewidth=2, markersize=6, label='Gross Margin (%)')
ax.plot(quarters, op_margin, 's-', color=TESLA_RED, linewidth=2, markersize=6, label='Operating Margin (%)')
ax.plot(quarters, auto_gm_excl, '^-', color=GREEN, linewidth=2, markersize=6, label='Auto GM excl. Credits (%)')

ax.plot(quarters[-1], gross_margin[-1], 'o', color=TESLA_BLUE, markersize=12, markerfacecolor='none', markeredgewidth=2.5)
ax.annotate(f'{gross_margin[-1]}%', xy=(quarters[-1], gross_margin[-1]), xytext=(10, 10),
            textcoords='offset points', fontsize=9, fontweight='bold', color=TESLA_BLUE)

ax.set_ylabel('Margin (%)', fontsize=11)
ax.set_title('Figure 3: Tesla Quarterly Margin Trends', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='lower left', fontsize=9)
ax.set_ylim(0, 25)
plt.xticks(rotation=30, fontsize=9)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart3_margin_trends.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 4: Revenue by Segment ============
segments = ['Automotive', 'Energy Gen.\n& Storage', 'Services\n& Other']
q1_26_seg = [16.23, 2.46, 3.70]
q1_25_seg = [13.97, 2.79, 2.58]

fig, ax = plt.subplots(figsize=(8, 5))
x_seg = np.arange(len(segments))
width_seg = 0.35
bars1 = ax.bar(x_seg - width_seg/2, q1_25_seg, width_seg, label="Q1'25", color=LIGHT_BLUE, edgecolor='white')
bars2 = ax.bar(x_seg + width_seg/2, q1_26_seg, width_seg, label="Q1'26", color=TESLA_BLUE, edgecolor='white')

for bar, val in zip(bars2, q1_26_seg):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
            f'${val:.1f}B', ha='center', va='bottom', fontsize=10, fontweight='bold', color=TESLA_BLUE)

yoy_changes = ['+16.2%', '-11.8%', '+43.4%']
for i, yc in enumerate(yoy_changes):
    clr = GREEN if '+' in yc else TESLA_RED
    ax.text(x_seg[i] + width_seg/2, q1_26_seg[i] + 0.8, yc, ha='center', fontsize=9, color=clr, fontweight='bold')

ax.set_ylabel('Revenue ($B)', fontsize=11)
ax.set_title('Figure 4: Tesla Q1 2026 Revenue by Segment', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x_seg)
ax.set_xticklabels(segments, fontsize=10)
ax.legend(fontsize=10)
ax.set_ylim(0, 20)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart4_segment_revenue.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 5: Deliveries & Production ============
deliveries = [387, 444, 463, 496, 337, 444, 463, 496, 358]
production = [433, 411, 470, 457, 363, 411, 470, 457, 408]

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width/2, deliveries, width, label='Deliveries', color=TESLA_BLUE, edgecolor='white')
ax.bar(x + width/2, production, width, label='Production', color=LIGHT_BLUE, alpha=0.7, edgecolor='white')

ax.annotate(f'358K\n(Est: 370K)', xy=(8, 358), xytext=(6.8, 430),
            fontsize=9, fontweight='bold', color=TESLA_RED,
            arrowprops=dict(arrowstyle='->', color=TESLA_RED, lw=1.5))

ax.set_ylabel('Units (thousands)', fontsize=11)
ax.set_title('Figure 5: Tesla Quarterly Vehicle Deliveries & Production', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(quarters, fontsize=9)
ax.legend(fontsize=10)
ax.set_ylim(0, 550)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart5_deliveries_production.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 6: Beat/Miss Summary ============
fig, ax = plt.subplots(figsize=(10, 5))

metrics_bm = ['Total Revenue', 'EPS (Non-GAAP)', 'Auto Revenue', 'Energy Revenue', 'Deliveries', 'Gross Margin']
values_bm = [-1.1, +10.8, -3.0, -15.2, -3.2, +490]
colors_bm = [GREEN if v >= 0 else TESLA_RED for v in values_bm]

bars = ax.barh(metrics_bm, values_bm, color=colors_bm, edgecolor='white', height=0.6)
ax.axvline(x=0, color='black', linewidth=0.8)

labels_bm = ['-1.1%', '+10.8%', '-3.0%', '-15.2%', '-3.2%', '+490bps']
for bar, lbl in zip(bars, labels_bm):
    x_pos = bar.get_width() + (1 if bar.get_width() >= 0 else -1)
    ha = 'left' if bar.get_width() >= 0 else 'right'
    ax.text(x_pos, bar.get_y() + bar.get_height()/2., lbl,
            va='center', ha=ha, fontsize=9, fontweight='bold', color=bar.get_facecolor())

ax.set_xlabel('Variance vs Consensus (%)', fontsize=11)
ax.set_title('Figure 6: Tesla Q1 2026 Beat/Miss vs Consensus', fontsize=13, fontweight='bold', pad=15)
ax.set_xlim(-20, 12)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart6_beat_miss.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 7: Estimate Revisions ============
categories = ['FY2026E\nRevenue', 'FY2026E\nEPS', 'FY2026E\nEBITDA', 'FY2027E\nRevenue', 'FY2027E\nEPS']
old_est = [96.5, 2.50, 14.2, 108.0, 3.20]
new_est = [98.2, 2.65, 14.8, 112.0, 3.45]

fig, ax = plt.subplots(figsize=(10, 5))
x_est = np.arange(len(categories))
ax.bar(x_est - width/2, old_est, width, label='Pre-Q1 (Old)', color=GRAY, edgecolor='white', alpha=0.7)
ax.bar(x_est + width/2, new_est, width, label='Post-Q1 (New)', color=TESLA_BLUE, edgecolor='white')

for i in range(len(categories)):
    change = (new_est[i] - old_est[i]) / old_est[i] * 100
    clr = GREEN if change >= 0 else TESLA_RED
    ax.text(x_est[i] + width/2, new_est[i] + 0.3, f'{change:+.1f}%', ha='center', fontsize=9, fontweight='bold', color=clr)

ax.set_ylabel('Estimate Value', fontsize=11)
ax.set_title('Figure 7: Tesla Forward Estimate Revisions Post Q1 2026', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x_est)
ax.set_xticklabels(categories, fontsize=9)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart7_estimate_revisions.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 8: Valuation P/E Bands ============
pe_ratio = [42, 55, 68, 75, 62, 58, 50, 45, 48]
pe_avg = [55] * 9

fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(range(len(quarters)), [35]*9, [75]*9, alpha=0.1, color=LIGHT_BLUE, label='5Y Range (35x-75x)')
ax.plot(quarters, pe_ratio, 'o-', color=TESLA_BLUE, linewidth=2.5, markersize=7, label='Forward P/E')
ax.plot(quarters, pe_avg, '--', color=GOLD, linewidth=1.5, alpha=0.7, label='5Y Average (55x)')
ax.plot(quarters[-1], pe_ratio[-1], 'o', color=TESLA_RED, markersize=14, markerfacecolor='none', markeredgewidth=2.5)
ax.annotate(f'Current: {pe_ratio[-1]}x', xy=(quarters[-1], pe_ratio[-1]), xytext=(-60, 15),
            textcoords='offset points', fontsize=10, fontweight='bold', color=TESLA_RED)

ax.set_ylabel('Forward P/E Multiple', fontsize=11)
ax.set_title('Figure 8: Tesla Historical Valuation - Forward P/E', fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=9)
ax.set_ylim(20, 90)
plt.xticks(rotation=30, fontsize=9)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart8_valuation_pe.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 9: Energy Storage Deployments ============
gwh_deployed = [4.1, 9.4, 6.9, 11.0, 10.4, 9.4, 6.9, 11.0, 8.8]
energy_rev = [1.64, 3.01, 2.38, 3.06, 2.79, 3.01, 2.38, 3.06, 2.46]

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(quarters, gwh_deployed, color=TESLA_BLUE, alpha=0.6, edgecolor='white', label='Deployments (GWh)')
ax1.set_ylabel('Deployments (GWh)', color=TESLA_BLUE, fontsize=11)
ax1.tick_params(axis='y', labelcolor=TESLA_BLUE)

ax2 = ax1.twinx()
ax2.plot(quarters, energy_rev, 'o-', color=GREEN, linewidth=2.5, markersize=7, label='Energy Revenue ($B)')
ax2.set_ylabel('Energy Revenue ($B)', color=GREEN, fontsize=11)
ax2.tick_params(axis='y', labelcolor=GREEN)

ax1.set_title('Figure 9: Tesla Energy Storage Quarterly Deployments & Revenue', fontsize=13, fontweight='bold', pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
plt.xticks(rotation=30, fontsize=9)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart9_energy_storage.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ Chart 10: Price Target Walk ============
fig, ax = plt.subplots(figsize=(10, 5))
steps = ['Current Price\n$258', 'Pre-Q1 PT\n$300', 'Q1 Impact\n+$15', 'New PT\n$315']
vals = [258, 300, 315, 315]
clrs = [GRAY, LIGHT_BLUE, GREEN, TESLA_BLUE]

ax.bar(steps, vals, color=clrs, edgecolor='white', width=0.5, alpha=0.8)

for i in range(len(steps) - 1):
    ax.annotate('', xy=(i+0.15, vals[i+1] * 0.95), xytext=(i+0.15, vals[i] + 2),
                arrowprops=dict(arrowstyle='->', color=TESLA_BLUE, lw=2))

for i, v in enumerate(vals):
    ax.text(i, v + 3, f'${v}', ha='center', fontsize=11, fontweight='bold')

# Upside annotation
ax.annotate(f'Upside: +22.1%', xy=(3, 315), xytext=(3, 335),
            fontsize=10, fontweight='bold', color=GREEN, ha='center')

ax.set_ylabel('Price / Target ($)', fontsize=11)
ax.set_title('Figure 10: Tesla Price Target Walk', fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(200, 360)
plt.tight_layout()
plt.savefig(f'{output_dir}/chart10_price_target_walk.png', dpi=150, bbox_inches='tight')
plt.close()

print("All 10 charts generated successfully!")
for f in sorted(os.listdir(output_dir)):
    print(f"  {f}")
