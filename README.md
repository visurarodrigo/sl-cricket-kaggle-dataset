# 🏏 Sri Lanka International Cricket Performance Dataset (2000–Present)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Dataset](https://img.shields.io/badge/matches-1082-orange.svg)](https://github.com/visurarodrigo/sl-cricket-kaggle-dataset)
[![Kaggle Dataset](https://img.shields.io/badge/kaggle-dataset-20BEFF.svg)](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)
[![Data Engineering](https://img.shields.io/badge/type-data%20engineering-blueviolet.svg)](https://github.com/visurarodrigo/sl-cricket-kaggle-dataset)

## 📋 Overview

An end-to-end **data engineering pipeline** that extracts, cleans, validates, and publishes a comprehensive dataset of Sri Lanka's international cricket matches. Built with professional standards for data quality, reproducibility, and Kaggle publication readiness.

This project transforms raw cricket data from [Cricsheet](https://cricsheet.org/) into analysis-ready CSV files with comprehensive validation, automated testing, and exploratory data analysis.

🎯 **[View Dataset on Kaggle →](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)**

---

## 📊 Dataset Summary

| Attribute | Details |
|-----------|---------|
| **Time Period** | January 2000 – January 30, 2026 |
| **Match Formats** | Test, ODI (One Day International), T20 International |
| **Total Matches** | 1,082 matches |
| **Columns** | 8 (Match_Date, Match_Format, Opponent, Winner, Margin, Ground, Year, Home_Away) |
| **Data Quality** | 100% validated and cleaned |
| **Missing Values** | Margin column only (82 matches with no margin data) |
| **Coverage** | All Sri Lanka international matches from 2000 onwards |

### Dataset Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Match_Date` | String | Match date in YYYY-MM-DD format | `2020-01-15` |
| `Match_Format` | String | Cricket format (Test/ODI/T20) | `ODI` |
| `Opponent` | String | Opposing team name | `India` |
| `Winner` | String | Match outcome | `Sri Lanka`, `Opponent`, `Draw`, `Tie`, `No Result` |
| `Margin` | String | Victory margin (if applicable) | `5 wickets`, `123 runs` |
| `Ground` | String | Venue/stadium name | `Galle International Stadium` |
| `Year` | Integer | Match year | `2020` |
| `Home_Away` | String | Match location indicator | `Home`, `Away` |

---

## 🚀 Project Highlights

✨ **Key Features:**

- 🔄 **Automated Data Pipeline**: End-to-end extraction from Cricsheet to clean CSV
- ✅ **Comprehensive Validation**: 17 unit tests for data cleaning + 24 tests for parsing
- 🧹 **Data Quality Assurance**: Multi-stage validation (format, dates, consistency)
- 📦 **Kaggle-Ready Package**: Complete release folder with data dictionary and description
- 📊 **Reproducible EDA**: Python script + Jupyter notebook with 6 visualizations
- 🏗️ **Professional Structure**: Modular codebase following Python best practices
- 📈 **100% Test Coverage**: All parsing and validation functions tested
- 🔍 **Duplicate Detection**: Automatic identification and removal of duplicate matches
- 📝 **Complete Documentation**: README, data dictionary, and inline code comments

---

## 📁 Repository Structure

```
sri-lanka-cricket-dataset/
│
├── src/                                    # Source code
│   ├── build_dataset.py                   # Data extraction & parsing pipeline
│   └── clean_dataset.py                   # Data validation & cleaning pipeline
│
├── notebooks/                              # Analysis notebooks
│   ├── 01_eda_sri_lanka_cricket.ipynb     # Interactive Jupyter notebook
│   └── eda_sri_lanka_cricket.py           # Standalone Python EDA script
│
├── eda_outputs/                            # Generated visualizations
│   ├── matches_per_year.png               # Time series of matches
│   ├── matches_by_format.png              # Format distribution
│   ├── match_outcomes.png                 # Win/loss breakdown
│   ├── top_opponents.png                  # Most played opponents
│   └── top_grounds.png                    # Most frequent venues
│
├── kaggle_release/                         # 📦 Kaggle publication package
│   ├── sri_lanka_international_cricket_matches_2000_present_clean.csv
│   ├── data_dictionary.md                 # Detailed column descriptions
│   └── kaggle_description.md              # Kaggle dataset card (copy-paste ready)
│
├── tests/                                  # Unit tests
│   ├── test_build_dataset.py              # 24 tests for parsing functions
│   └── test_clean_dataset.py              # 17 tests for validation functions
│
├── sri_lanka_international_cricket_matches_2000_present.csv        # Raw output
├── sri_lanka_international_cricket_matches_2000_present_clean.csv  # Clean output ⭐
├── data_dictionary.md                      # Column documentation
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git ignore rules
└── README.md                               # This file
```

**What Each Component Does:**

- **`src/build_dataset.py`**: Downloads Cricsheet data, parses JSON, filters Sri Lanka matches
- **`src/clean_dataset.py`**: Validates data quality, removes duplicates, normalizes formats
- **`notebooks/`**: Exploratory data analysis with visualizations and statistics
- **`eda_outputs/`**: All generated charts (PNG format, 300 DPI)
- **`kaggle_release/`**: Complete package for Kaggle dataset upload
- **`tests/`**: Automated testing suite (pytest framework)

---

## 🛠️ How to Run the Project

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- Internet connection (for Cricsheet downloads)

### Step 1: Clone Repository

```bash
git clone https://github.com/visurarodrigo/sl-cricket-kaggle-dataset.git
cd sl-cricket-kaggle-dataset
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Generate Raw Dataset

```bash
python -m src.build_dataset
```

**What happens:**
1. Downloads Cricsheet data (tests_json.zip, odis_json.zip, t20s_json.zip)
2. Extracts and parses JSON match files
3. Filters for Sri Lanka matches from 2000 onwards
4. Outputs: `sri_lanka_international_cricket_matches_2000_present.csv`

**Expected runtime:** 3-10 minutes (depending on internet speed)

### Step 4: Clean & Validate Dataset

```bash
python -m src.clean_dataset
```

**What happens:**
1. Validates all columns and data formats
2. Removes duplicates (if any)
3. Normalizes margin text format
4. Outputs: `sri_lanka_international_cricket_matches_2000_present_clean.csv`

**Expected output:**
```
================================================================================
CLEANING SUMMARY
================================================================================
Total rows before:        1082
Total rows after:         1082
Duplicates removed:       0
Invalid rows removed:     0
Data quality:             100.00% retained
```

### Step 5: Run Exploratory Data Analysis (Optional)

**Option A: Python Script**
```bash
cd notebooks
python eda_sri_lanka_cricket.py
```

**Option B: Jupyter Notebook**
```bash
jupyter notebook notebooks/01_eda_sri_lanka_cricket.ipynb
```

**Generates:**
- 6 visualization charts in `eda_outputs/`
- Comprehensive statistics printed to console

### Step 6: Run Tests (Optional)

```bash
pytest tests/ -v
```

**Expected:** All 41 tests pass (24 build + 17 validation)

### 🔄 Automated Monthly Updates

**Manual Update (Run once per month):**
```bash
python update_dataset.py
```

This single script automatically:
- ✅ Downloads latest Cricsheet data
- ✅ Rebuilds and cleans dataset
- ✅ Regenerates all visualizations
- ✅ Updates README statistics
- ✅ Commits and pushes to GitHub

**Fully Automated (GitHub Actions):**

The repository includes a GitHub Actions workflow that runs automatically on the 1st of every month. No manual intervention needed!

- 📅 **Schedule:** Runs automatically monthly
- 🔧 **Manual Trigger:** Can also run from GitHub Actions tab
- 📊 **Updates:** Dataset, charts, README, and Kaggle release folder
- 🚀 **Auto-commit:** Changes are automatically committed and pushed

To enable: Just push the `.github/workflows/monthly_update.yml` file to your repository.

---

## 📦 Outputs

### 1. Raw Dataset

**File:** `sri_lanka_international_cricket_matches_2000_present.csv`

- Direct extraction from Cricsheet data
- Minimal processing applied
- Use for: Understanding raw data structure

### 2. Clean Dataset ⭐ (Recommended)

**File:** `sri_lanka_international_cricket_matches_2000_present_clean.csv`

- **Validated**: All columns pass format checks
- **Deduplicated**: No duplicate match records
- **Standardized**: Consistent naming and formatting
- **Kaggle-Ready**: No preprocessing needed
- Use for: Analysis, machine learning, Kaggle upload

**Quality Metrics:**
- ✅ 1,082 matches validated
- ✅ 100% data retention rate
- ✅ 0 duplicates found
- ✅ All dates in YYYY-MM-DD format
- ✅ All formats validated (Test/ODI/T20)

---

## 📊 Exploratory Data Analysis (EDA)

### Generated Visualizations

The EDA pipeline creates 6 comprehensive charts:

1. **`matches_per_year.png`** - Time series showing match frequency (2002-2026)
2. **`matches_by_format.png`** - Distribution across Test, ODI, and T20 formats
3. **`match_outcomes.png`** - Win/loss breakdown for Sri Lanka
4. **`top_opponents.png`** - Top 10 most played opponents
5. **`top_grounds.png`** - Top 10 most frequent match venues

### Key Insights

📈 **Match Statistics:**
- Peak year: **2024** (75 matches)
- Average: **43.3 matches/year**
- ODI most common format: **52.9%** (572 matches)

🏆 **Performance:**
- Overall win rate: **45.2%** (452 wins in 1,000 decided matches)
- Test win rate: **48.9%**
- ODI win rate: **46.0%**
- T20 win rate: **42.3%**

🌍 **Opponents:**
- Most played: **India** (179 matches)
- Total unique opponents: **23 countries**
- Total unique venues: **208 grounds**

---

## 📦 Kaggle Release

### 🌟 Live Dataset

**[View on Kaggle →](https://www.kaggle.com/datasets/visurarodrigo/sri-lanka-international-cricket-matches-2000pre)**

The dataset is now live and available for the community to use!

### What's in `kaggle_release/`?

This folder contains everything needed to publish on Kaggle:

1. **`sri_lanka_international_cricket_matches_2000_present_clean.csv`**
   - The validated, analysis-ready dataset
   
2. **`data_dictionary.md`**
   - Detailed column descriptions
   - Data types and examples
   - Usage guidelines

3. **`kaggle_description.md`**
   - Complete Kaggle dataset card
   - Copy-paste ready for Kaggle upload
   - Includes: overview, columns, use cases, attribution, limitations

---

## 🔬 Data Source & Attribution

### Primary Data Source

**Cricsheet** ([cricsheet.org](https://cricsheet.org/))

Cricsheet provides comprehensive ball-by-ball cricket data in JSON format for international and domestic matches.

**Downloads Used:**
- Test matches: `https://cricsheet.org/downloads/tests_json.zip`
- ODI matches: `https://cricsheet.org/downloads/odis_json.zip`
- T20 matches: `https://cricsheet.org/downloads/t20s_json.zip`

### Attribution Requirements

When using this dataset, please cite:

```
Sri Lanka International Cricket Performance Dataset (2000–Present)
Data Source: Cricsheet (https://cricsheet.org/)
Created by: Stephen Rushe
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
GitHub Repository: https://github.com/visurarodrigo/sl-cricket-kaggle-dataset
```

---

## 📜 License & Usage Notes

### Dataset License

The cricket data is sourced from [Cricsheet](https://cricsheet.org/) and is licensed under:
- **[Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**

**You are free to:**
- ✅ Share — copy and redistribute the material
- ✅ Adapt — remix, transform, and build upon the material
- ✅ Commercial use — use for commercial purposes

**Under these terms:**
- 📝 Attribution — Must give appropriate credit to Cricsheet

### Code License

The Python scripts and code in this repository are open source and free to use for educational and research purposes.

### Usage Guidelines

- Always credit Cricsheet when publishing analyses or papers
- Do not claim the data as your own creation
- Respect the CC BY 4.0 license terms
- Cite this repository if you use the cleaned dataset version

---

## 🔮 Future Improvements

Potential enhancements for this project:

### Data Enhancements
- 🏠 **Home/Away Classification**: Add home/away match indicator
- 👤 **Player-Level Statistics**: Include top scorers, bowlers for each match
- 🌤️ **Match Conditions**: Weather, pitch conditions, toss information
- 📍 **Geographic Data**: Latitude/longitude for all venues
- 🔢 **Team Rankings**: Historical ICC rankings at match time

### Analysis Extensions
- 🤖 **ML Models**: Predict match outcomes based on historical data
- 📊 **Power BI Dashboard**: Interactive dashboard for visualization
- 📈 **Time Series Forecasting**: Predict future performance trends
- 🔍 **Opponent Analysis**: Deep-dive into head-to-head records
- 🏆 **Tournament Segmentation**: World Cup, bilateral series breakdown

### Technical Improvements
- ⚡ **Real-time Updates**: GitHub Actions to auto-update dataset monthly
- 🐳 **Dockerization**: Container for reproducible execution
- 🌐 **Web API**: REST API to query dataset programmatically
- 📱 **Mobile Dashboard**: React Native app for dataset exploration

**Contributions welcome!** Open an issue or pull request to suggest improvements.

---

## 👨‍💻 Author

**Visura Rodrigo**

- 🔗 GitHub: [@visurarodrigo](https://github.com/visurarodrigo)
- 📧 Contact: Open an issue in this repository for questions
- 💼 Project: Data Engineering Portfolio Project

### About This Project

Built as a demonstration of:
- Data engineering best practices
- ETL pipeline development
- Data quality assurance
- Python software engineering
- Open-source dataset creation

Perfect for recruiters evaluating data engineering skills! 🎯

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Propose enhancements via issues
3. **Submit PRs**: Fork, create a branch, and submit pull requests
4. **Improve Docs**: Fix typos or add clarifications

---

## 🙏 Acknowledgments

- **Stephen Rushe** - Creator and maintainer of [Cricsheet](https://cricsheet.org/)
- **Cricsheet Community** - For providing comprehensive cricket data
- **Open Source Community** - For tools like pandas, pytest, and Python

---

## 📧 Support

Need help? Have questions?

- 📝 **Open an Issue**: [GitHub Issues](https://github.com/visurarodrigo/sl-cricket-kaggle-dataset/issues)
- 📖 **Read the Docs**: Check [data_dictionary.md](data_dictionary.md) for column details
- 🧪 **Run Tests**: `pytest tests/ -v` to verify setup

---

**Happy Data Science!** 🏏📊✨

---

*Last Updated: February 2026 | Dataset Version: 1.0 | Matches: 1,082*
