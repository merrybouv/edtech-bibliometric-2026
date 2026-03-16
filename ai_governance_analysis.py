# ai_governance_analysis.py
# Examines whether governance vocabulary is growing within AI/ChatGPT papers specifically.
# Tests the "selective awakening" argument — whether critical discourse is emerging
# in the AI literature even as legacy platforms (iPads, Chromebooks) remain unscrutinized.
# Input: edtech_corpus_clean.csv
# Output: printed year-by-year breakdown (no CSV needed — used for in-paper reporting)
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd

df = pd.read_csv('edtech_corpus_clean.csv')
df['abstract'] = df['abstract'].fillna('').astype(str).str.lower()
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df[df['abstract'].str.len() > 50]

# Filter to 2014-2025 (2026 excluded — partial year, insufficient sample)
df = df[df['year'].between(2014, 2025)]

# AI/ChatGPT subset
ai_terms = ['chatgpt', 'artificial intelligence', 'machine learning', 'large language model']
ai_df = df[df['abstract'].apply(lambda a: any(t in a for t in ai_terms))]
print(f"AI/ChatGPT papers: {len(ai_df)} of {len(df)} total ({round(len(ai_df)/len(df)*100,1)}%)")

# Governance terms — slightly expanded to include privacy for AI context
governance_terms = ['surveillance', 'consent', 'governance', 'data rights', 'monetization',
                    'privacy', 'data harvesting', 'digital rights', 'third party']

print("\nGovernance term presence in AI/ChatGPT papers by year:")
print(f"{'Year':<8}{'Papers':<10}{'Gov %':<10}")
print("-" * 28)

for year, group in ai_df.groupby('year'):
    n = len(group)
    crit = group['abstract'].apply(lambda a: any(t in a for t in governance_terms)).sum()
    print(f"{int(year):<8}{n:<10}{round(crit/n*100,1):<10}")

# Break down which governance terms are driving presence in AI papers
print("\nGovernance term frequency in AI/ChatGPT papers (all years):")
print(f"{'Term':<25}{'Count':<10}{'%':<10}")
print("-" * 45)
for term in governance_terms:
    count = ai_df['abstract'].apply(lambda a: term in a).sum()
    pct = round(count / len(ai_df) * 100, 1)
    print(f"{term:<25}{count:<10}{pct:<10}")