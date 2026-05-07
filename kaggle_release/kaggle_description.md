
# Sri Lanka International Cricket Matches (2000–2026)

## Overview

This release provides a cleaned, validated, match-level dataset of Sri Lanka's international fixtures (Tests, ODIs, T20s), built from Cricsheet JSONs and prepared for analysis and Kaggle publication. The repository contains the raw downloads, a repeatable build pipeline, a cleaning/validation pass, EDA outputs, and the Kaggle-ready CSV.

## Key Columns

- `Match_Date` — Match start date (YYYY-MM-DD)
- `Match_Format` — Test, ODI, or T20
- `Opponent` — Opposing team
- `Winner` — `Sri Lanka`, opponent name, `Draw`, `Tie`, or `No Result`
- `Margin` — Victory margin when available
- `Ground` — Venue or stadium
- `Year` — Match year
- `Home_Away` — `Home` or `Away` classification
- `Gender`, `Toss_Winner`, `Toss_Decision`, `Player_of_Match`, `Event_Name` — additional match metadata

## Coverage & Totals

- Date range: 2000–2026 (dataset uses match start dates)
- Primary cleaned output: `sri_lanka_international_cricket_matches_2000_present_clean.csv`
- Total matches (approx.): 1,082 across Test, ODI, and T20 formats

## Data Quality & Processing

- Source: Cricsheet (https://cricsheet.org/) — licensed CC BY 4.0
- Pipeline: `src/build_dataset.py` (download + parse) → `src/clean_dataset.py` (normalize, validate, deduplicate, tag home/away)
- Checks: date normalization, required-column validation, duplicate removal, standardized outcome categories
- Notes: Test matches use the start date; time zones are not included. Some early matches may lack margin details.

## Suggested Uses

- Exploratory analysis (win rates, format trends, home/away comparison)
- Predictive models (match outcome classifiers, win-probability estimators)
- Visualizations and dashboards (time-series, heatmaps, geographic maps)

## Quick Start

Install and build the dataset locally:

```bash
pip install -r requirements.txt
python -m src.build_dataset
python -m src.clean_dataset
```

Then open the cleaned CSV:

```python
import pandas as pd
df = pd.read_csv('sri_lanka_international_cricket_matches_2000_present_clean.csv')
print(df.head())
```

Run the EDA notebooks:

```bash
cd notebooks
python eda_sri_lanka_cricket.py
```

## Attribution & License

Compiled from Cricsheet by Visura Rodrigo. This release is distributed under CC BY 4.0 — please cite the original source when reusing the data.

Citation:

> Sri Lanka International Cricket Dataset (2000–2026)
> Data source: Cricsheet
> Compiled by: Visura Rodrigo

---

**Version**: 2.0  
**Last updated**: 2026-05-07

