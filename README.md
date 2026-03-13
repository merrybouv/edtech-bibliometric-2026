# Computational Bibliometric Analysis of K-12 Classroom Technology Research, 2014–2026

This repository contains the code used in the study "Optimization Without Accountability: 
A Computational Bibliometric Analysis of K-12 Classroom Technology Research, 2014–2026."

## Study Overview
Using the ERIC database, I collected 948 published studies and dissertations on classroom 
technology and applied term frequency analysis and topic modeling to map the conceptual 
terrain of the field. The central finding is that optimization terms dominate the literature while governance and accountability terms are nearly absent.

## Repository Contents
- `collect_papers.py` — collects papers from the ERIC API and saves to CSV
- `topic_model.py` — runs BERTopic topic modeling on the corpus
- `visualizations.py` — generates figures used in the paper

## Data
The full corpus and analysis outputs are available on OSF: [OSF link]

## Requirements
```
pip install requests pandas tqdm bertopic umap-learn scikit-learn matplotlib
```

## Usage
Run scripts in this order:
1. `collect_papers.py` — outputs `edtech_corpus_raw.csv`
2. Filter to 2014+ and save as `edtech_corpus_2014.csv`
3. `topic_model.py` — outputs topic assignments and model
4. `visualizations.py` — outputs figures

## Notes
- ERIC API requires no key but may experience intermittent downtime
- Topic model uses random_state=42 for reproducibility
- 2026 data is partial (collection conducted March 2026)

## Citation
[Citation to be added upon publication]

## License
MIT