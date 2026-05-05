# Sri Lanka International Cricket Dataset (2000-2026)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Kaggle](https://img.shields.io/badge/kaggle-dataset-20BEFF.svg)](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)

An end-to-end dataset of Sri Lanka's international cricket matches from 2000 onward. The repository includes the raw Cricsheet downloads, a repeatable build step, a cleaning and validation pass, EDA outputs, and Kaggle-ready release files.

[View on Kaggle](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre) | [Data Dictionary](data_dictionary.md)

## Overview

| Feature | Details |
|---|---|
| Time coverage | 2000-2026 |
| Source | Cricsheet match JSON files |
| Formats | Test, ODI, T20 |
| Output | Clean CSV plus release assets |
| Validation | Column checks, normalization, duplicate removal, home/away tagging |

## What is included

The main cleaned dataset contains match-level records with these fields:

| Column | Description |
|---|---|
| Match_Date | Match date in YYYY-MM-DD format |
| Match_Format | Test, ODI, or T20 |
| Opponent | Opposing team |
| Winner | Sri Lanka, Opponent, Draw, Tie, or No Result |
| Margin | Victory margin when available |
| Ground | Venue or stadium |
| Year | Match year |
| Gender | Match gender |
| Toss_Winner | Team that won the toss |
| Toss_Decision | Toss choice, usually bat or field |
| Player_of_Match | Player of the match |
| Event_Name | Tournament or series name |
| Home_Away | Home or away classification |

## Quick Start

```bash
pip install -r requirements.txt
python -m src.build_dataset
python -m src.clean_dataset
cd notebooks && python eda_sri_lanka_cricket.py
```

The primary output is `sri_lanka_international_cricket_matches_2000_present_clean.csv`.

## Project Structure

```text
.
├── src/
│   ├── build_dataset.py
│   └── clean_dataset.py
├── notebooks/
│   ├── 01_eda_sri_lanka_cricket.ipynb
│   └── eda_sri_lanka_cricket.py
├── kaggle_release/
├── tests/
├── update_dataset.py
└── README.md
```

## Pipeline

### Build

`src/build_dataset.py` downloads the Cricsheet archives, parses the match JSON files, filters for Sri Lanka fixtures, and writes the raw combined CSV.

### Clean and Validate

`src/clean_dataset.py` standardizes formats and dates, validates required columns, removes duplicates, normalizes match outcomes, and adds the home/away classification.

### Explore

`notebooks/eda_sri_lanka_cricket.py` generates summary charts for match volume, format split, outcomes, opponents, venues, and home/away performance.

## Outputs

The repository produces the following main artifacts:

- `sri_lanka_international_cricket_matches_2000_present.csv`
- `sri_lanka_international_cricket_matches_2000_present_clean.csv`
- `eda_outputs/` charts from the EDA workflow
- `kaggle_release/` files prepared for Kaggle publishing

## Automated Updates

Run the refresh script manually with:

```bash
python update_dataset.py
```

The update flow downloads the latest Cricsheet data, rebuilds the dataset, reruns cleaning, refreshes the visualizations, and updates the release materials.

## Testing

```bash
pytest tests/ -v
```

The test suite covers dataset construction and cleaning behavior.

## Data Source and License

The data is sourced from [Cricsheet](https://cricsheet.org/) and distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The code in this repository is provided for educational and research use.

## Citation

```text
Sri Lanka International Cricket Dataset (2000-2026)
Data source: Cricsheet
Compiled by: Visura Rodrigo
License: CC BY 4.0
```

## Author

Visura Rodrigo

## Resources

- [Data Dictionary](data_dictionary.md)
- [Kaggle Dataset](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)
- [Cricsheet Documentation](https://cricsheet.org/)
