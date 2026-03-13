import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer

# Load corpus filtered to 2014-2026
df = pd.read_csv('edtech_corpus_2014.csv')
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

# Configure vectorizer to capture single words and two-word phrases
# min_df=3 means a term must appear in at least 3 documents to be included
vectorizer = CountVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=3
)

# Run BERTopic — unsupervised topic modeling using transformer-based embeddings
topic_model = BERTopic(
    language="english",
    calculate_probabilities=True,
    verbose=True,
    vectorizer_model=vectorizer,
    umap_model=umap_model
)

topics, probs = topic_model.fit_transform(df['abstract'].tolist())

# Save model for reproducibility
topic_model.save("bertopic_model")

# Display top topics
print("\nTOP TOPICS:")
topic_info = topic_model.get_topic_info()
print(topic_info.head(20).to_string())

# Save corpus with topic assignments and topic summary
df['topic'] = topics
df.to_csv('edtech_corpus_with_topics.csv', index=False)
topic_info.to_csv('topic_summary.csv', index=False)
print("\nSaved edtech_corpus_with_topics.csv and topic_summary.csv")

# Print top keywords for each topic for manual interpretation
print("\nDETAILED TOPIC KEYWORDS:")
for i in range(8):
    words = topic_model.get_topic(i)
    if words:
        keywords = [w[0] for w in words[:10]]
        print(f"\nTopic {i}: {', '.join(keywords)}")