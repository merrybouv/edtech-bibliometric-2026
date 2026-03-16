# A Vocabulary of Optimization: Computational Bibliometric Analysis of K-12 Classroom Technology Research

This repository contains the analysis code for the study "A Vocabulary of Optimization: Computational Bibliometric Analysis of K-12 Classroom Technology Research," submitted to *Learning, Media and Technology* (2026).

## Study Overview

Using the ERIC database, I collected and filtered 1,404 published studies, dissertations, and conference papers on classroom technology published between 2014 and 2025, and applied term frequency analysis, BERTopic topic modeling, and manual abstract review to map the conceptual vocabulary of the field. The central finding is that optimization terms dominate the literature while governance and accountability terms are nearly absent — appearing in fewer than 0.4% of abstracts, with several registering zero occurrences.

## Repository Contents

- `collect_papers.py` — collects papers from the ERIC API, deduplicates, and saves raw and clean corpora
- `term_analysis.py` — term frequency analysis across all abstracts
- `topic_model.py` — BERTopic topic modeling on the clean corpus
- `ai_governance_analysis.py` — governance term presence within AI/ChatGPT papers by year
- `journal_analysis.py` — journal distribution analysis
- `critical_papers.py` — flags papers for manual review based on governance vocabulary
- `visualizations.py` — generates figures used in the paper
- `spot_check.py` — validation script for corpus integrity and analysis outputs

## Data

Full corpus and analysis outputs are deposited on OSF: https://osf.io/j74xv

## Requirements
```
pip install requests pandas tqdm bertopic umap-learn hdbscan scikit-learn matplotlib
```

## Usage

Run scripts in this order:

1. `collect_papers.py` — outputs `edtech_corpus_raw.csv` and `edtech_corpus_clean.csv`
2. `term_analysis.py` — outputs `term_frequency_analysis.csv` and `year_trend_analysis.csv`
3. `topic_model.py` — outputs `edtech_corpus_with_topics.csv`, `topic_summary.csv`, and `bertopic_model/`
4. `ai_governance_analysis.py` — printed output, no CSV
5. `journal_analysis.py` — outputs `journal_analysis.csv`
6. `critical_papers.py` — outputs `critical_papers_flagged.csv` for manual review
7. `visualizations.py` — outputs `figure1_term_frequency.png` and `figure2_year_trend.png`
8. `spot_check.py` — validates all outputs

## Notes

- ERIC API requires no key but may experience intermittent downtime
- API-level date filtering is unreliable; post-hoc filtering is applied in `collect_papers.py`
- Topic model uses `min_cluster_size=40` and `random_state=42` for reproducibility
- I manually coded the `critical?` column in `critical_papers_flagged.csv`

## Citation

Bouvier, M. (2026). A Vocabulary of Optimization: Computational Bibliometric Analysis of K-12 Classroom Technology Research. Submitted to *Learning, Media and Technology.*

## License

MIT License — Copyright (c) 2026 Meredith Bouvier, NET Lab, Inc.
