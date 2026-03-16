# topic_model.py
# Runs BERTopic unsupervised topic modeling on the ERIC corpus.
# Input: edtech_corpus_clean.csv (collected and date-filtered by collect_papers.py)
# Output: edtech_corpus_with_topics.csv, topic_summary.csv, bertopic_model/
# Note: date filtering (2014–2026) is applied upstream at the API level in collect_papers.py
# Part of: Optimization Without Accountability (Bouvier, 2026)

import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN

# Load corpus (already filtered to 2014–2026 at collection stage)
df = pd.read_csv('edtech_corpus_clean.csv')
df['abstract'] = df['abstract'].fillna('').astype(str)

# Remove records with no meaningful abstract text
df = df[df['abstract'].str.len() > 50]
print(f"Running topic model on {len(df)} abstracts...")

# Configure UMAP for dimensionality reduction
# random_state=42 ensures reproducible results
umap_model = UMAP(
    n_neighbors=15,
    n_components=5,
    min_dist=0.0,
    metric='cosine',
    random_state=42
)

# Configure HDBSCAN — min_topic_size=75 forces broader, more coherent clusters
# Higher value = fewer topics; adjust down if too few topics result
hdbscan_model = HDBSCAN(
    min_cluster_size=40,
    metric='euclidean',
    cluster_selection_method='eom',
    prediction_data=True
)

# Configure vectorizer to capture single words and two-word phrases
# min_df=2 means a term must appear in at least 2 documents to be included
vectorizer = CountVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
)

# Run BERTopic — unsupervised topic modeling using transformer-based embeddings
topic_model = BERTopic(
    language="english",
    calculate_probabilities=True,
    verbose=True,
    vectorizer_model=vectorizer,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model
)

topics, probs = topic_model.fit_transform(df['abstract'].tolist())

# Save model for reproducibility
topic_model.save("bertopic_model")

# Display top topics
print("\nTOP TOPICS:")
topic_info = topic_model.get_topic_info()
print(topic_info.to_string())

# Save corpus with topic assignments and topic summary
df['topic'] = topics
df.to_csv('edtech_corpus_with_topics.csv', index=False)
topic_info.to_csv('topic_summary.csv', index=False)
print("\nSaved edtech_corpus_with_topics.csv and topic_summary.csv")

# Print top keywords for all topics
print("\nDETAILED TOPIC KEYWORDS:")
for i in range(len(topic_info) - 1):  # -1 excludes the -1 noise topic
    words = topic_model.get_topic(i)
    if words:
        keywords = [w[0] for w in words[:8]]
        print(f"Topic {i}: {keywords}")