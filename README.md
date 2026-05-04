# Predictive Analytics for Enterprise Streaming Acquisitions

**Course:** CMPS 451 -- Data Mining, Big Data & Analytics (Spring 2026)  
**Team:** 11

## Business Problem

How can a streaming enterprise estimate the likely audience reception of a title before acquiring it?

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Register Jupyter kernel
python -m ipykernel install --user --name=imdb_project --display-name="IMDb Project"

# 4. Download IMDb datasets (run once)
python download_data.py
```

## Project Structure

```
├── Dataset/                    # Raw data files
│   ├── Dataset.npy            # IEEE DataPort user ratings (4.67M)
│   ├── title.basics.tsv.gz    # IMDb title metadata
│   ├── title.ratings.tsv.gz   # IMDb aggregate ratings
│   ├── title.principals.tsv.gz
│   ├── title.crew.tsv.gz
│   ├── title.akas.tsv.gz
│   ├── title.episode.tsv.gz
│   └── name.basics.tsv.gz
├── notebooks/
│   ├── 01_preprocessing.ipynb       # Data loading, cleaning, joining
│   ├── 02_feature_engineering.ipynb # Feature creation & EDA
│   ├── 03_visualization.ipynb       # 10+ visualizations
│   ├── 04_modeling.ipynb            # ML model training
│   └── 05_evaluation.ipynb          # Results & business insights
├── outputs/
│   ├── plots/      # All generated visualizations
│   ├── models/     # Saved Spark ML models
│   └── results/    # Evaluation CSVs and JSONs
└── requirements.txt
```

## Pipeline

1. **Preprocessing** -- PySpark loads 7 IMDb TSV files + user ratings, filters/cleans/joins
2. **Feature Engineering** -- Genre one-hot, director/cast track records, language features, user stats
3. **Visualization** -- 10 publication-quality plots incl. language bias & numVotes analysis
4. **Modeling** -- 4 regressors + 3 classifiers + K-Means clustering via Spark MLlib
5. **Evaluation** -- Full metrics on train/validation/test, confusion matrix, feature importance

## Tech Stack

- **Apache PySpark** (pseudo-distributed mode, `local[*]`)
- **Spark MLlib** for model training
- **Matplotlib + Seaborn** for visualization
- **Python 3.12**
