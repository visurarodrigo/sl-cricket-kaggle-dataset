# 🏏 Sri Lanka International Cricket Dataset (2000–2026)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Dataset](https://img.shields.io/badge/matches-1082-orange.svg)](https://github.com/visurarodrigo/sl-cricket-kaggle-dataset)
[![Kaggle](https://img.shields.io/badge/kaggle-dataset-20BEFF.svg)](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)

> **A production-ready dataset of 1,082+ Sri Lankan international cricket matches with automated ETL pipeline, comprehensive validation, and exploratory analysis.**

🎯 **[View on Kaggle](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)** | 📖 **[Data Dictionary](data_dictionary.md)**

---

## 📊 Dataset Overview

| Feature | Details |
|---------|---------|  
| **Time Coverage** | January 2000 – January 30, 2026 (26 years) |
| **Total Matches** | 1,082 validated matches |
| **Formats** | Test (174), ODI (572), T20 (336) |
| **Columns** | 8 fields including Home/Away classification |
| **Data Quality** | 100% validated, zero duplicates |
| **Source** | [Cricsheet](https://cricsheet.org/) (CC BY 4.0) |

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `Match_Date` | String | Match date (YYYY-MM-DD) |
| `Match_Format` | Categorical | Test, ODI, or T20 |
| `Opponent` | String | Opposing team name |
| `Winner` | Categorical | Match outcome (Sri Lanka, Opponent, Draw, Tie, No Result) |
| `Margin` | String | Victory margin (e.g., "5 wickets", "50 runs") |
| `Ground` | String | Venue/stadium name |
| `Year` | Integer | Match year (2002-2026) |
| `Home_Away` | Categorical | Home (Sri Lankan venues) or Away |

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/visurarodrigo/sl-cricket-kaggle-dataset.git
cd sl-cricket-kaggle-dataset

# Install dependencies
pip install -r requirements.txt

# Build dataset (downloads from Cricsheet)
python -m src.build_dataset

# Clean and validate
python -m src.clean_dataset

# Generate visualizations
cd notebooks && python eda_sri_lanka_cricket.py
```

**Output:** `sri_lanka_international_cricket_matches_2000_present_clean.csv` ✅

---

## 🏗️ Project Architecture

```
sri-lanka-cricket-dataset/
├── src/
│   ├── build_dataset.py       # ETL: Extract and parse Cricsheet JSON
│   └── clean_dataset.py       # Validate, deduplicate, add Home/Away
├── notebooks/
│   ├── 01_eda_sri_lanka_cricket.ipynb
│   └── eda_sri_lanka_cricket.py
├── eda_outputs/               # 6 visualizations (PNG, 300 DPI)
├── tests/                     # 41 unit tests (pytest)
├── kaggle_release/            # Kaggle-ready package
└── update_dataset.py          # Automated monthly updates
```

---

## � Key Insights

**Performance Metrics** (1,000 decided matches):
- Overall Win Rate: **45.2%** (452 wins)
- Home Win Rate: **50.1%** (173 of 345 home matches)
- Away Win Rate: **42.6%** (279 of 655 away matches)
- Best Format: Test Cricket (48.9% win rate)

**Matchup Analysis:**
- Most Played Opponent: **India** (179 matches, 26.5% win rate)
- Most Common Venue: **Pallekele International Cricket Stadium** (69 matches)
- Peak Activity: **2024** (75 matches)

---

## 📊 Visualizations

The EDA pipeline generates 6 professional charts in `eda_outputs/`:

1. **matches_per_year.png** - Time series (2002-2026)
2. **matches_by_format.png** - Format distribution  
3. **match_outcomes.png** - Win/loss breakdown
4. **top_opponents.png** - Most played opponents
5. **top_grounds.png** - Most frequent venues
6. **home_away_performance.png** - Home vs Away comparison 🆕

---

## 🔬 Data Engineering Pipeline

### 1. Extraction (`build_dataset.py`)
- Downloads Cricsheet data (tests_json.zip, odis_json.zip, t20s_json.zip)
- Parses 5,000+ JSON files
- Filters for Sri Lanka participation
- Runtime: ~5-10 minutes

### 2. Validation & Cleaning (`clean_dataset.py`)
- ✅ Column validation (8 expected fields)
- ✅ Date format standardization (YYYY-MM-DD)
- ✅ Format normalization (Test/ODI/T20)
- ✅ Duplicate detection and removal
- ✅ Home/Away classification (15 Sri Lankan venues)
- ✅ Margin text normalization

### 3. Quality Assurance
- **Unit Tests:** 41 tests covering all functions
- **Data Validation:** 100% pass rate on all checks
- **Output Verification:** Automated summary reports

---

## 🔄 Automated Updates

The dataset auto-updates monthly via GitHub Actions:

```bash
# Manual update
python update_dataset.py
```

**What it does:**
1. Downloads latest Cricsheet data
2. Rebuilds and validates dataset
3. Regenerates all visualizations
4. Updates documentation (README, data dictionary)
5. Commits changes to GitHub

**Schedule:** Runs automatically on the 1st of each month

---

## 💡 Use Cases

### Data Science & Analytics
- **Exploratory Analysis:** Win rates, trends, venue effects
- **Statistical Testing:** Home advantage, format performance
- **Time Series:** Performance evolution over 26 years
- **Comparative Analysis:** Head-to-head records, venue analysis

### Machine Learning
- **Classification:** Predict match outcomes
- **Regression:** Estimate victory margins
- **Clustering:** Identify match patterns
- **Time Series:** Forecast future performance

### Visualization & Storytelling
- Build interactive dashboards (Streamlit, Dash, Power BI)
- Create infographics for cricket journalism
- Generate automated reports

---

## 📦 Kaggle Release

**Live Dataset:** [View on Kaggle →](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)

The `kaggle_release/` folder contains:
- Clean CSV dataset (1,082 matches)
- Complete data dictionary
- Dataset card (ready for Kaggle upload)

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Expected output
======================== 41 passed ========================
```

**Test Coverage:**
- 24 tests for data extraction/parsing
- 17 tests for validation/cleaning
- 100% function coverage

---

## 📜 License & Attribution

**Data:** Sourced from [Cricsheet](https://cricsheet.org/) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Code:** Open source, free for educational and research use

**Citation:**
```
Sri Lanka International Cricket Dataset (2000–2026)
Data Source: Cricsheet (https://cricsheet.org/)
Created by: Stephen Rushe | Compiled by: Visura Rodrigo
License: CC BY 4.0
```

---

## 🤝 Contributing

Contributions welcome! Here's how:

- 🐛 **Report Issues:** [Open an issue](https://github.com/visurarodrigo/sl-cricket-kaggle-dataset/issues)
- 💡 **Suggest Features:** Create a feature request
- 🔧 **Submit PRs:** Fork → Branch → Pull Request
- 📖 **Improve Docs:** Fix typos or add clarifications

---

## 👨‍💻 Author

**Visura Rodrigo**  
*Data Engineer | Cricket Analytics Enthusiast*

- GitHub: [@visurarodrigo](https://github.com/visurarodrigo)
- Kaggle: [View Dataset](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)

**Built with:** Python, Pandas, Matplotlib, Pytest

---

## 📚 Additional Resources

- **[Data Dictionary](data_dictionary.md):** Detailed column descriptions
- **[Kaggle Dataset](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre):** Live dataset with kernel examples
- **[Cricsheet Documentation](https://cricsheet.org/):** Source data format reference

---

<div align="center">

**⭐ Star this repo if you find it useful!**

*Last Updated: February 2026 | v1.0 | 1,082 Matches*

</div>
