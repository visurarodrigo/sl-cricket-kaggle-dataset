# Sri Lanka International Cricket Performance Dataset (2000–2026)

A clean, well-structured Python project to generate a comprehensive **Kaggle-ready** dataset of Sri Lanka's international cricket matches from January 2000 to January 30, 2026, using official [Cricsheet](https://cricsheet.org/) data.

## 📊 Dataset Overview

### About This Dataset

This dataset provides a comprehensive record of Sri Lanka's performance in international cricket across all three major formats from January 2000 to January 30, 2026. Perfect for cricket analytics, machine learning projects, sports data visualization, and statistical analysis.

**Key Features:**
- ✅ **Complete Coverage**: All Sri Lanka international matches (Tests, ODIs, T20s) from 2000 onwards
- ✅ **High Quality**: Validated and cleaned data with quality checks
- ✅ **Match Outcomes**: Detailed winner information and victory margins
- ✅ **Venue Information**: Stadium/ground names for location-based analysis
- ✅ **Ready to Use**: Clean CSV format, no preprocessing needed
- ✅ **Regularly Updated**: Based on latest Cricsheet data

### Output Files

**Raw Dataset (Generated):**  
`sri_lanka_international_cricket_matches_2000_present.csv` - Initial extracted data

**Clean Dataset (Validated & Ready for Analysis):**  
`sri_lanka_international_cricket_matches_2000_present_clean.csv` - Quality-checked, standardized dataset

### Columns
| Column | Description | Example |
|--------|-------------|---------|
| `Match_Date` | Match date in YYYY-MM-DD format | `2020-01-15` |
| `Match_Format` | Type of match | `Test`, `ODI`, `T20` |
| `Opponent` | Opposing team name | `India` |
| `Winner` | Match winner | `Sri Lanka`, `Opponent`, `Draw`, `Tie`, `No Result` |
| `Margin` | Victory margin | `5 wickets`, `123 runs` |
| `Ground` | Venue name | `Galle International Stadium` |
| `Year` | Match year | `2020` |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. **Clone this repository**
```bash
git clone https://github.com/visurarodrigo/sl-cricket-kaggle-dataset.git
cd sl-cricket-kaggle-dataset
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Option 1: Generate Both Raw and Clean Datasets (Recommended)

**Step 1: Generate raw dataset**
```bash
python -m src.build_dataset
```

**Step 2: Validate and clean the dataset**
```bash
python -m src.clean_dataset
```

This will create both:
- `sri_lanka_international_cricket_matches_2000_present.csv` (raw)
- `sri_lanka_international_cricket_matches_2000_present_clean.csv` (cleaned & validated)

### Option 2: Quick Start - Just Get the Raw Data

Simply run:
```bash
python -m src.build_dataset
```

The script will:
1. Download Cricsheet data (tests, ODIs, T20s)
2. Extract and parse JSON files
3. Filter for Sri Lanka matches from 2000 onwards
4. Generate the raw CSV dataset

### What the Cleaning Script Does

The data cleaning script (`clean_dataset.py`) performs comprehensive quality checks:

**Validation:**
- ✓ Verifies all required columns are present
- ✓ Validates Match_Format values (Test, ODI, T20)
- ✓ Checks date format (YYYY-MM-DD)
- ✓ Ensures Year matches Match_Date
- ✓ Validates Winner values
- ✓ Confirms Opponent is never "Sri Lanka"

**Cleaning:**
- ✓ Trims whitespace from all fields
- ✓ Standardizes categorical values
- ✓ Normalizes margin text format
- ✓ Removes duplicate matches
- ✓ Filters invalid rows

**Output:**
```
================================================================================
CLEANING SUMMARY
================================================================================
Total rows before:        657
Total rows after:         652
Duplicates removed:       3
Invalid rows removed:     2
Data quality:             99.24% retained
```

### Expected Output
```
================================================================================
Sri Lanka International Cricket Dataset Builder
================================================================================

================================================================================
Processing TESTS
================================================================================
Downloading https://cricsheet.org/downloads/tests_json.zip
...
Successfully downloaded tests_json.zip
Extracting tests_json.zip
Processing 2500 Test matches
Found 150 Sri Lanka Test matches from 2000 onwards

[Process repeats for ODIs and T20s]

================================================================================
SUCCESS!
================================================================================
Dataset saved to: sri_lanka_international_cricket_matches_2000_present.csv
Total matches: 650
Date range: 2000-01-15 to 2025-12-20

Breakdown by format:
Test    150
ODI     350
T20     150

Breakdown by winner:
Sri Lanka      280
Opponent       250
No Result       60
Draw            40
Tie             20
```

## 🧪 Testing

Run unit tests with:
```bash
pytest tests/ -v
```

Or:
```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── build_dataset.py          # Main dataset generation script
│   └── clean_dataset.py          # Data validation & cleaning script
├── tests/
│   ├── __init__.py
│   └── test_build_dataset.py     # Unit tests
├── data_dictionary.md             # Detailed column descriptions
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 📖 Data Dictionary

For detailed information about each column, see [data_dictionary.md](data_dictionary.md).

**Quick Reference:**
- **Match_Date**: Date in YYYY-MM-DD format
- **Match_Format**: Test, ODI, or T20
- **Opponent**: Team that played against Sri Lanka
- **Winner**: Match outcome (Sri Lanka, Opponent, Draw, Tie, No Result)
- **Margin**: Victory margin (e.g., "5 wickets", "123 runs")
- **Ground**: Venue/stadium name
- **Year**: Match year (2000-2026)

## 🔧 Technical Details

### Data Sources

**Primary Source: [Cricsheet](https://cricsheet.org/)**

Cricsheet provides comprehensive ball-by-ball cricket data in JSON format for international and domestic cricket. This project uses their match-level data.

**Downloads:**
- Test matches: `https://cricsheet.org/downloads/tests_json.zip`
- ODI matches: `https://cricsheet.org/downloads/odis_json.zip`
- T20 matches: `https://cricsheet.org/downloads/t20s_json.zip`

**Attribution:**  
Cricket data provided by Cricsheet (https://cricsheet.org/), created and maintained by Stephen Rushe. Licensed under [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

When using this dataset, please credit:
- **Data Source**: Cricsheet (https://cricsheet.org/)
- **Creator**: Stephen Rushe
- **License**: CC BY 4.0

### Libraries Used
- **pandas** (2.1.4): Data manipulation and CSV generation
- **requests** (2.31.0): HTTP requests for downloading data
- **tqdm** (4.66.1): Progress bars for better UX
- **pytest** (7.4.3): Testing framework

### Key Features
- ✅ **Data Quality**: Comprehensive validation and cleaning pipeline
- ✅ **Robust Error Handling**: Network and file operations with proper error handling
- ✅ **Progress Tracking**: Real-time progress bars for downloads and processing
- ✅ **Detailed Logging**: Timestamped logs for debugging and monitoring
- ✅ **Comprehensive Tests**: Unit tests for parsing and validation functions
- ✅ **Sri Lanka Filter**: Only matches where Sri Lanka participated (2000+)
- ✅ **Format Handling**: Automatic date parsing and format standardization
- ✅ **Winner Categorization**: Clear match outcome classification
- ✅ **Duplicate Detection**: Automatic removal of duplicate match records
- ✅ **Clean Code**: Well-structured, documented, maintainable codebase

### Kaggle-Ready Features
- 📊 **No Missing Values**: All critical fields populated
- 📊 **Standardized Format**: Consistent naming and formatting
- 📊 **Quality Validated**: All rows pass data integrity checks
- 📊 **Analysis Ready**: No preprocessing needed
- 📊 **Well Documented**: Comprehensive data dictionary included
- 📊 **Citation Info**: Proper attribution and licensing information

### Winner Logic
The `Winner` column follows this logic:
- **Sri Lanka**: Sri Lanka won the match
- **Opponent**: The opposing team won
- **Draw**: Match ended in a draw (common in Tests)
- **Tie**: Match ended in a tie (rare)
- **No Result**: Match abandoned/no result
- **Empty string**: Unknown outcome (rare edge cases)

## 🐛 Troubleshooting

### Download Issues
If downloads fail:
- Check your internet connection
- Verify Cricsheet URLs are accessible
- Try again (temporary network issues)

### Missing Matches
If some matches seem missing:
- Verify the match involved Sri Lanka as a team
- Check that the match date is 2000 or later
- Ensure the source JSON has valid date information

### Import Errors
If you get import errors:
```bash
# Ensure you're running from the project root
python -m src.build_dataset

# Not:
python src/build_dataset.py
```

## 📝 Notes

- **Temporary Files**: The script creates a `temp/` directory with downloaded files. You can delete this after the CSV is generated.
- **Processing Time**: Downloading and processing all formats takes 5-15 minutes depending on your connection.
- **Data Updates**: Cricsheet updates regularly. Re-run the script to get the latest data.

## 📜 License

This project is provided as-is for educational and research purposes.

**Dataset License:**  
The cricket data is sourced from [Cricsheet](https://cricsheet.org/) and is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Code License:**  
The Python scripts and code in this repository are open source and free to use.

**Citation:**  
When using this dataset in research, publications, or Kaggle competitions, please cite:
```
Sri Lanka International Cricket Performance Dataset (2000-2026)
Data Source: Cricsheet (https://cricsheet.org/)
Creator: Stephen Rushe  
License: CC BY 4.0
GitHub: https://github.com/visurarodrigo/sl-cricket-kaggle-dataset
Date Range: January 2000 - January 30, 2026
```

## 🎯 Use Cases

This dataset is perfect for:
- 🏏 **Cricket Analytics**: Analyze Sri Lanka's performance trends over time
- 📊 **Data Visualization**: Create interactive dashboards and charts
- 🤖 **Machine Learning**: Predict match outcomes, win probabilities
- 📈 **Statistical Analysis**: Study home/away performance, opponent analysis
- 🎓 **Educational Projects**: Learn data analysis with real-world sports data
- 🏆 **Kaggle Competitions**: Use as a foundation for cricket prediction models

## 🙏 Acknowledgments

- **Cricsheet**: For providing comprehensive cricket data
- **Stephen Rushe**: Creator and maintainer of Cricsheet

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest improvements
- Submit pull requests

## 📧 Contact

For questions or issues, please open an issue in the repository.

---

**Happy Data Science!** 🏏📊
