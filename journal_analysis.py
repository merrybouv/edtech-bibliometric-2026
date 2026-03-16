# journal_analysis.py
# Analyzes journal distribution across the corpus to examine whether critical
# scholarship is segregated into specialist journals the mainstream field does not read.
# Input: edtech_corpus_clean.csv
# Output: journal_analysis.csv
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd

df = pd.read_csv('edtech_corpus_clean.csv')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df[df['year'].between(2014, 2025)]
df['journal'] = df['journal'].fillna('Unknown').astype(str)
total = len(df)
print(f"Analyzing journal distribution across {total} papers...")

# Count papers per journal
journal_counts = df['journal'].value_counts().reset_index()
journal_counts.columns = ['journal', 'count']
journal_counts['pct'] = (journal_counts['count'] / total * 100).round(1)

# Save full journal list
journal_counts.to_csv('journal_analysis.csv', index=False)
print(f"Saved journal_analysis.csv")

# Print top 20
print(f"\nTop 20 journals:")
print(journal_counts.head(20).to_string(index=False))

# Highlight critical journals specifically
critical_journals = [
    'Learning, Media and Technology',
    'Critical Studies in Education',
    'Postdigital Science and Education',
    'Journal of Education Policy',
]

print(f"\nCritical journals in corpus:")
for journal in critical_journals:
    match = journal_counts[journal_counts['journal'].str.contains(journal, case=False, na=False)]
    if not match.empty:
        print(f"  {journal}: {match.iloc[0]['count']} papers ({match.iloc[0]['pct']}%)")
    else:
        print(f"  {journal}: 0 papers")