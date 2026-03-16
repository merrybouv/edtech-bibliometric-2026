# critical_papers.py
# Identifies papers in the corpus that engage critically with the political economy
# of classroom technology — examining governance, privacy, data extraction, or
# commercial interests rather than purely optimizing for learning outcomes.
# Input: edtech_corpus_clean.csv
# Output: critical_papers_final.csv
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd

df = pd.read_csv('edtech_corpus_clean.csv')
df['abstract'] = df['abstract'].fillna('').astype(str)
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df[df['abstract'].str.len() > 50]
df = df[df['year'].between(2014, 2025)]
total = len(df)
print(f"Scanning {total} abstracts for critical papers...")

# Terms indicating genuine critical/political economy engagement
# A paper must contain at least one of these to be flagged for review
critical_indicators = [
    'surveillance capitalism',
    'platform capitalism',
    'data harvesting',
    'data extraction',
    'digital rights',
    'student data privacy',
    'commercial interests',
    'data brokers',
    'third party data',
    'monetization',
    'exploitation',
    'surveillance',
    'consent',
    'governance',
    'privacy',
    'data protection',
]

# Flag papers containing at least one critical indicator
df['critical_flag'] = df['abstract'].str.lower().apply(
    lambda a: any(term in a for term in critical_indicators)
)

flagged = df[df['critical_flag']].copy()
print(f"Flagged for review: {len(flagged)} papers")

# Save for manual review — not all flagged papers will be genuinely critical
# Manual review required to confirm each paper engages substantively with
# political economy rather than merely mentioning a term in passing
# Preserve manual critical? column if it already exists
output = flagged[['title', 'year', 'journal', 'abstract']].sort_values('year').copy()
try:
    existing = pd.read_csv('critical_papers_flagged.csv')
    if 'critical?' in existing.columns:
        lookup = existing.set_index('title')['critical?']
        output['critical?'] = output['title'].map(lookup).fillna('No')
except FileNotFoundError:
    pass
output.to_csv('critical_papers_flagged.csv', index=False)

print(f"Saved critical_papers_flagged.csv for manual review")
print(f"\nTop titles flagged:")
for _, row in flagged[['title', 'year']].sort_values('year').head(20).iterrows():
    print(f"  {int(row['year'])}: {row['title'][:80]}")