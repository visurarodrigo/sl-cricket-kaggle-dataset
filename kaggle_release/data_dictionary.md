# Data Dictionary

## Sri Lanka International Cricket Matches Dataset (2000-2026)

This document provides detailed descriptions of each column in the dataset.

---

### Dataset Overview

**Filename**: `sri_lanka_international_cricket_matches_2000_present_clean.csv`

**Description**: A comprehensive dataset of Sri Lanka's international cricket matches across all formats (Test, ODI, T20) from January 2000 to January 30, 2026. The dataset includes match outcomes, venues, opponents, and victory margins.

**Source**: [Cricsheet](https://cricsheet.org/) - Official cricket match data in JSON format

**License**: Creative Commons Attribution 4.0 International License (CC BY 4.0)

**Last Updated**: February 2026

---

### Column Descriptions

| Column | Data Type | Description | Example Values | Notes |
|--------|-----------|-------------|----------------|-------|
| **Match_Date** | Date (YYYY-MM-DD) | The date when the match was played | `2020-01-15` | Format: ISO 8601 standard. For multi-day matches, this is the start date. |
| **Match_Format** | Categorical | The format/type of the cricket match | `Test`, `ODI`, `T20` | Three possible values: Test (5-day cricket), ODI (One Day International, 50 overs), T20 (Twenty20, 20 overs) |
| **Opponent** | String | The team that played against Sri Lanka | `India`, `Australia`, `England` | Full team names. Never contains "Sri Lanka". |
| **Winner** | Categorical | The outcome of the match | `Sri Lanka`, `Opponent`, `Draw`, `Tie`, `No Result` | **Sri Lanka**: Sri Lanka won; **Opponent**: The opposing team won; **Draw**: Match ended without a winner (common in Tests); **Tie**: Both teams scored the same runs; **No Result**: Match abandoned/cancelled. Empty values indicate unknown outcomes. |
| **Margin** | String | The victory margin | `5 wickets`, `123 runs`, `` | Format: "X runs" for batting first wins, "X wickets" for chasing wins. Empty for draws, ties, or no results. Singular form used for "1 run" or "1 wicket". |
| **Ground** | String | The venue/stadium where the match was played | `Galle International Stadium`, `R Premadasa Stadium` | Full venue names as provided by Cricsheet. |
| **Year** | Integer | The year when the match was played | `2020`, `2015`, `2003` | Extracted from Match_Date for easy filtering and analysis. Range: 2000 to 2026. |

---

### Data Quality Notes

✅ **Validated**: All rows have been validated for data integrity and consistency  
✅ **Cleaned**: Whitespace trimmed, standardized labels, duplicates removed  
✅ **Complete**: No missing values in key columns (Match_Date, Match_Format, Opponent, Year)  
✅ **Standardized**: All categorical values follow consistent naming conventions  

---

### Usage Examples

**Filter by format:**
```python
import pandas as pd

df = pd.read_csv('sri_lanka_international_cricket_matches_2000_present_clean.csv')

# Get all Test matches
test_matches = df[df['Match_Format'] == 'Test']

# Get all T20 matches
t20_matches = df[df['Match_Format'] == 'T20']
```

**Analyze win rate:**
```python
# Calculate Sri Lanka's win percentage
total_matches = len(df[df['Winner'].isin(['Sri Lanka', 'Opponent'])])
sl_wins = len(df[df['Winner'] == 'Sri Lanka'])
win_rate = (sl_wins / total_matches) * 100
print(f"Sri Lanka win rate: {win_rate:.2f}%")
```

**Get matches by year:**
```python
# Get all matches in 2015
matches_2015 = df[df['Year'] == 2015]
```

**Find most played opponents:**
```python
# Top 10 opponents
top_opponents = df['Opponent'].value_counts().head(10)
print(top_opponents)
```

---

### Citation

If you use this dataset in your research or analysis, please cite:

```
Sri Lanka International Cricket Performance Dataset (2000-Present)
Data Source: Cricsheet (https://cricsheet.org/)
Creator: Stephen Rushe
License: CC BY 4.0
Accessed: February 2026
```

---

### Contact & Contributions

For issues, questions, or suggestions:
- Open an issue on the GitHub repository
- Contribute improvements via pull requests

---

**Version**: 1.0  
**Generated**: February 2026  
**Rows**: ~600-800 matches (varies with updates)  
**Formats**: Test, ODI, T20
