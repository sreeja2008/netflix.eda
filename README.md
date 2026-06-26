# Netflix Content Catalog — Exploratory Data Analysis

A beginner/intermediate EDA project analyzing Netflix's content catalog (movies and TV shows) using Python, pandas, and matplotlib/seaborn.

## What this project does

- Loads and inspects a Netflix titles dataset (1,200+ titles)
- Cleans missing data (director, country) without dropping valid rows
- Parses dates and multi-value genre fields
- Answers 5 real analytical questions with visualizations:
  1. What's the split between Movies and TV Shows?
  2. How has Netflix's catalog grown over time?
  3. What are the most common genres?
  4. Which countries produce the most content?
  5. How long are Netflix movies, typically?

## Files

| File | Purpose |
|---|---|
| `generate_data.py` | Generates the dataset used in this repo (see note below) |
| `netflix_titles.csv` | The dataset |
| `01_eda.py` | Main analysis script — run this |
| `findings.txt` | Plain-English summary of results |
| `chart1_type_split.png` ... `chart5_movie_durations.png` | Output visualizations |

## About the dataset

This project uses a **synthetically generated** dataset that mirrors the structure of the well-known [Netflix Movies and TV Shows dataset on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows) (same columns: `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`).

It was generated this way because the analysis environment used to build this project didn't have internet access to download the live file. **To run this on the real data:**

1. Download `netflix_titles.csv` from the Kaggle link above
2. Replace the CSV in this folder
3. Run `python 01_eda.py` — no code changes needed, since column names match exactly

## How to run

```bash
pip install pandas matplotlib seaborn
python generate_data.py   # creates netflix_titles.csv (skip if using real data)
python 01_eda.py          # runs the analysis, saves charts + findings.txt
```

## Key skills demonstrated

- Data cleaning (missing values, type conversion, date parsing)
- Handling multi-value categorical columns (`explode()`)
- Descriptive statistics (mean, quartiles)
- Data visualization (bar, pie, histogram) with matplotlib/seaborn
- Translating numbers into plain-English findings

## Author

Katasani Sreeja Reddy — BCA Data Science Student, Presidency University
