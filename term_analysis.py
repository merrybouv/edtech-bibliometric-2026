# term_analysis.py
# Calculates term frequency for optimization vs governance vocabulary across all abstracts.
# Also produces year-by-year trend analysis.
# Input: edtech_corpus_clean.csv
# Output: term_frequency_analysis.csv, year_trend_analysis.csv
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd

df = pd.read_csv('edtech_corpus_clean.csv')
df['abstract'] = df['abstract'].fillna('').astype(str).str.lower()
df = df[df['abstract'].str.len() > 50]
total = len(df)
print(f"Analyzing {total} abstracts...")

# Terms selected a priori based on relevance to each analytical category
optimization_terms = ['skills', 'impact', 'integration', 'engagement', 'effectiveness']
governance_terms = ['surveillance', 'consent', 'governance', 'data rights', 'monetization',
                    'platform capitalism', 'surveillance capitalism', 'data harvesting',
                    'digital rights', 'third party', 'procurement', 'exploitation', 'data privacy']

# ── FINDING 1: Term frequency across full corpus ────────────────────────────
rows = []
for term in optimization_terms + governance_terms:
    count = df['abstract'].str.contains(term, regex=False).sum()
    pct = round(count / total * 100, 1)
    category = 'optimization' if term in optimization_terms else 'governance'
    rows.append({'term': term, 'count': count, 'pct': pct, 'category': category})
    print(f"  {term}: {count} ({pct}%)")

freq_df = pd.DataFrame(rows)
freq_df.to_csv('term_frequency_analysis.csv', index=False)
print(f"\nSaved term_frequency_analysis.csv")

# ── FINDING 3: Year trend analysis ─────────────────────────────────────────
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df[df['year'].between(2014, 2025)]

year_rows = []
for year, group in df.groupby('year'):
    n = len(group)
    abstracts = group['abstract']
    
    crit_count = abstracts.apply(
        lambda a: any(t in a for t in governance_terms)
    ).sum()
    opt_count = abstracts.apply(
        lambda a: any(t in a for t in optimization_terms)
    ).sum()
    
    year_rows.append({
        'year': int(year),
        'n_papers': n,
        'critical_pct': round(crit_count / n * 100, 1),
        'optimization_pct': round(opt_count / n * 100, 1)
    })

year_df = pd.DataFrame(year_rows).sort_values('year')
print("\nYear trend:")
print(year_df.to_string(index=False))
year_df.to_csv('year_trend_analysis.csv', index=False)
print("\nSaved year_trend_analysis.csv")