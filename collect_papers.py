import requests
import pandas as pd
import time
from tqdm import tqdm

API_URL = "https://api.ies.ed.gov/eric/"

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
    all_papers = []
    start = 0
    
    while start < limit:
        params = {
            "search": query,
            "format": "json",
            "rows": min(100, limit - start),
            "start": start,
            "fields": "title,author,publicationdateyear,description,id,subject,source,publicationtype"}
        
        response = requests.get(API_URL, params=params)
        
        if response.status_code != 200:
            print(f"  Error {response.status_code} for query: {query}")
            break
        
        data = response.json()
        docs = data.get("response", {}).get("docs", [])
        
        if not docs:
            break
        
        all_papers.extend(docs)
        start += len(docs)
        time.sleep(3)
    
    return all_papers

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
    "subject": p.get("subject", ""),
    "id": p.get("id", ""),
    "journal": p.get("source", ""),
    "pubtype": p.get("publicationtype", "")
})
    
    print(f"  Got {len(papers)} papers")

df = pd.DataFrame(all_results)
df.drop_duplicates(subset="id", inplace=True)
df.to_csv("edtech_corpus_raw.csv", index=False)

print(f"\nDone. Total unique papers: {len(df)}")