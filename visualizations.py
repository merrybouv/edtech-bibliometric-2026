import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ── FIGURE 1: Term Frequency Bar Chart ─────────────────────────────────────
# Hardcoded from term_frequency_analysis.csv results
# Optimization terms vs governance terms across 948 abstracts (2014-2026)

term_data = {
    'Optimization Terms': {
        'Skills': 21.2,
        'Impact': 20.0,
        'Integration': 16.5,
        'Engagement': 10.7,
        'Effectiveness': 8.8,
    },
    'Governance Terms': {
        'Surveillance': 0.4,
        'Consent': 0.3,
        'Governance': 0.1,
        'Data Rights': 0.0,
        'Monetization': 0.0,
    }
}

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Term Frequency in K-12 Classroom Technology Literature (2014–2026)',
             fontsize=13, fontweight='bold', y=1.02)

colors = ['#2c7bb6', '#d7191c']

for ax, (category, terms), color in zip(axes, term_data.items(), colors):
    bars = ax.barh(list(terms.keys()), list(terms.values()), color=color, alpha=0.85)
    ax.set_xlabel('Frequency (%)')
    ax.set_title(category, fontweight='bold')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlim(0, 25)
    # Add percentage labels to end of each bar
    for bar, val in zip(bars, terms.values()):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('figure1_term_frequency.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ── FIGURE 2: Year Trend Line Graph ────────────────────────────────────────
# Shows critical vs optimization term frequency by year
# Vertical line marks 2022 — when ChatGPT discourse begins to appear in literature

df = pd.read_csv('year_trend_analysis.csv')

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(df['year'], df['critical_pct'], color='#d7191c', linewidth=2.5,
        marker='o', markersize=5, label='Critical / Governance Terms')
ax.plot(df['year'], df['optimization_pct'], color='#2c7bb6', linewidth=2.5,
        marker='o', markersize=5, label='Optimization Terms')

# Mark ChatGPT launch as turning point in critical term frequency
ax.axvline(x=2022, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.text(2022.1, ax.get_ylim()[1] * 0.95, 'ChatGPT launch',
        fontsize=8, color='gray')

ax.set_xlabel('Year')
ax.set_ylabel('Frequency (%)')
ax.set_title('Critical vs. Optimization Terms Over Time (2014–2026)',
             fontweight='bold')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# Reverse legend order so optimization (top line) appears first
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
ax.set_xticks(df['year'])
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('figure2_year_trend.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")