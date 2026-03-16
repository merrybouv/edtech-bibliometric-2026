# collect_papers.py
# Collects EdTech papers from the ERIC API (2014–2026) across a set of search queries.
# Deduplicates by ERIC ID and saves raw corpus to CSV.

import requests
import pandas as pd
import time
from tqdm import tqdm

# ERIC API endpoint
API_URL = "https://api.ies.ed.gov/eric/"

# Search queries targeting specific platforms and general EdTech terms
# Queries selected to capture the dominant tools embedded in K-12 classrooms since 2014
SEARCH_QUERIES = [
    "YouTube classroom",
    "iPad school",
    "Chromebook school",
    "Google Classroom",
    "artificial intelligence classroom",
    "ChatGPT students",
    "educational technology elementary",
    "educational technology secondary",
    "instructional technology school",
    "Microsoft Teams school",
    "ClassDojo",
    "Seesaw app classroom",
    "Canvas LMS school",
    "smartboard classroom",
]

def search_eric(query, limit=100):
    """
    Query the ERIC API for a single search term.
    Results are filtered at the API level to 2014–2026 using Solr's fq parameter.
    Paginates automatically up to the specified limit.
    Includes a 3-second delay between requests to respect API rate limits.
    """
    all_papers = []
    start = 0
    
    while start < limit:
        params = {
            "search": query,
            "format": "json",
            "rows": min(100, limit - start),
            "start": start,
            "fq": "publicationdateyear:[2014 TO 2026]",  # Date filter applied at API level
            "fields": "title,author,publicationdateyear,description,id,subject,source,publicationtype"
        }
        
        response = requests.get(API_URL, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"  Error {response.status_code} for query: {query}")
            break
        
        data = response.json()
        docs = data.get("response", {}).get("docs", [])
        
        if not docs:
            break
        
        all_papers.extend(docs)
        start += len(docs)
        time.sleep(3)  # Rate limiting
    
    return all_papers

# Iterate over all queries and collect results
all_results = []

for query in tqdm(SEARCH_QUERIES):
    print(f"\nSearching: {query}")
    papers = search_eric(query, limit=200)
    
    for p in papers:
        all_results.append({
            "query": query,
            "title": p.get("title", ""),
            "year": p.get("publicationdateyear", ""),
            "abstract": p.get("description", ""),
            "subject": "; ".join(p.get("subject", [])) if isinstance(p.get("subject"), list) else p.get("subject", ""),
            "id": p.get("id", ""),
            "journal": p.get("source", ""),
            "pubtype": p.get("publicationtype", "")
        })
    
    print(f"  Got {len(papers)} papers")

# Deduplicate by ERIC ID (same paper may appear across multiple queries)
df = pd.DataFrame(all_results)
df.drop_duplicates(subset="id", inplace=True)
df.reset_index(drop=True, inplace=True)

# Save raw corpus before filtering
df.to_csv("edtech_corpus_raw.csv", index=False)
print(f"Raw corpus (before filtering): {len(df)}")

# Post-hoc filter: enforce date range, exclude incomplete year, require abstract
# Note: API-level date filter (fq parameter) does not reliably exclude all out-of-range records
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df_clean = df[
    (df["year"] >= 2014) &
    (df["year"] <= 2025) &
    (df["abstract"].notna()) &
    (df["abstract"].str.strip() != "")
].copy()

# Save clean analytical corpus
df_clean.to_csv("edtech_corpus_clean.csv", index=False)
print(f"Clean corpus (2014-2025, abstracts present): {len(df_clean)}")