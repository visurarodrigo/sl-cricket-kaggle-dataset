# Sri Lanka International Cricket Performance Dataset (2000–Present)

A clean, well-structured Python project to generate a comprehensive Kaggle dataset of Sri Lanka's international cricket matches from 2000 to the present, using official [Cricsheet](https://cricsheet.org/) data.

## 📊 Dataset Overview

The generated CSV contains Sri Lanka's performance in all three international formats:
- **Test Matches**
- **One Day Internationals (ODIs)**
- **Twenty20 Internationals (T20s)**

### Output File
`sri_lanka_international_cricket_matches_2000_present.csv`

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

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Script

Simply run:
```bash
python -m src.build_dataset
```

The script will:
1. Download Cricsheet data (tests, ODIs, T20s)
2. Extract and parse JSON files
3. Filter for Sri Lanka matches from 2000 onwards
4. Generate the final CSV dataset

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
│   └── build_dataset.py          # Main script
├── tests/
│   ├── __init__.py
│   └── test_build_dataset.py     # Unit tests
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔧 Technical Details

### Data Source
- **Cricsheet**: Official cricket match data in JSON format
- Downloads from:
  - `https://cricsheet.org/downloads/tests_json.zip`
  - `https://cricsheet.org/downloads/odis_json.zip`
  - `https://cricsheet.org/downloads/t20s_json.zip`

### Libraries Used
- **pandas** (2.1.4): Data manipulation and CSV generation
- **requests** (2.31.0): HTTP requests for downloading data
- **tqdm** (4.66.1): Progress bars for better UX
- **pytest** (7.4.3): Testing framework

### Key Features
- ✅ Robust error handling for network and file operations
- ✅ Progress bars for downloads and processing
- ✅ Detailed logging with timestamps
- ✅ Comprehensive unit tests
- ✅ Filters for Sri Lanka matches only (2000+)
- ✅ Handles various date formats
- ✅ Proper winner categorization
- ✅ Clean, maintainable code structure

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

This project is provided as-is for educational and research purposes. The cricket data is sourced from [Cricsheet](https://cricsheet.org/), which is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

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
