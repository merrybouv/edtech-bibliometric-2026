# spot_check.py
# Validation script for corpus integrity and analysis outputs.
# Run this after any changes to the corpus or analysis pipeline to confirm
# all outputs are consistent and based on the correct filtered dataset.
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd

print("=" * 60)
print("CORPUS SPOT CHECK")
print("=" * 60)

# ── 1. YEAR DISTRIBUTION ────────────────────────────────────
print("\n1. YEAR DISTRIBUTION")
df = pd.read_csv('edtech_corpus_clean.csv')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
print(f"   Total records: {len(df)}")
print(f"   Pre-2014 records (should be 0): {len(df[df['year'] < 2014])}")
print(f"   2026+ records (should be 0): {len(df[df['year'] >= 2026])}")
print(f"   Missing abstracts (should be 0): {df['abstract'].isna().sum()}")
print(f"   Year range: {int(df['year'].min())} – {int(df['year'].max())}")
print(f"\n   Papers per year:")
for year, count in df['year'].value_counts().sort_index().items():
    print(f"     {int(year)}: {count}")

# ── 2. TOPIC ASSIGNMENTS ────────────────────────────────────
print("\n2. TOPIC ASSIGNMENTS (3 sample titles per topic)")
topics = pd.read_csv('edtech_corpus_with_topics.csv')
topic_summary = pd.read_csv('topic_summary.csv')
print(f"\n   Topic counts:")
for _, row in topic_summary.iterrows():
    print(f"     Topic {row['Topic']}: {row['Count']} papers — {row['Name']}")
print()
for topic in sorted(topics['topic'].unique()):
    if topic == -1:
        continue
    print(f"\n   --- Topic {topic} samples ---")
    sample = topics[topics['topic'] == topic][['title', 'year']].head(3)
    for _, row in sample.iterrows():
        print(f"     [{int(row['year'])}] {str(row['title'])[:100]}")

# ── 3. CRITICAL PAPERS IN CORPUS ────────────────────────────
# 'critical?' column is added manually by the researcher after reviewing
# each flagged abstract. A paper is marked 'Yes' if critical or governance
# framing is central to its argument, not merely incidental.
print("\n3. CRITICAL PAPERS (manually confirmed)")
critical = pd.read_csv('critical_papers_flagged.csv')
if 'critical?' in critical.columns:
    confirmed = critical[critical['critical?'] == 'Yes'].sort_values('year')
    print(f"   Confirmed critical: {len(confirmed)} of {len(critical)} flagged\n")
    for _, row in confirmed.iterrows():
        print(f"     [{int(row['year'])}] {str(row['title'])[:90]}")
else:
    print("   No 'critical?' column found — add Yes/No to critical_papers_flagged.csv")

# ── 4. TERM FREQUENCY SANITY CHECK ──────────────────────────
print("\n4. TERM FREQUENCY CHECK")
terms = pd.read_csv('term_frequency_analysis.csv')
print(f"   Terms analyzed: {len(terms)}")
print(f"   Top optimization term: {terms.iloc[0]['term']} ({terms.iloc[0]['pct']:.1f}%)")
print(f"   Top governance term: ", end="")
gov_terms = ['surveillance', 'consent', 'governance', 'data rights', 'monetization']
gov = terms[terms['term'].isin(gov_terms)]
if len(gov) > 0:
    top_gov = gov.sort_values('pct', ascending=False).iloc[0]
    print(f"{top_gov['term']} ({top_gov['pct']:.1f}%)")
else:
    print("none found — check term_frequency_analysis.csv column names")

# ── 5. JOURNAL CHECK ────────────────────────────────────────
print("\n5. JOURNAL CHECK")
journals = pd.read_csv('journal_analysis.csv')
print(f"   Total unique journals: {len(journals)}")
print(f"   Top 5 journals:")
for _, row in journals.head(5).iterrows():
    print(f"     {row['journal'][:60]}: {row['count']} ({row['pct']:.1f}%)")
lmt = journals[journals['journal'].str.contains('Learning, Media', case=False, na=False)]
print(f"   Learning, Media and Technology: {lmt['count'].values[0] if len(lmt) > 0 else 0} papers")

print("\n" + "=" * 60)
print("SPOT CHECK COMPLETE")
print("=" * 60)