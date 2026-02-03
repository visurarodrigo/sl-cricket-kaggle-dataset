# Sri Lanka International Cricket Matches (2000-2026) - Complete Performance Dataset

## 📊 Overview

This dataset provides a **complete and validated** record of Sri Lanka's international cricket performance across all three major formats from January 2000 to January 30, 2026. With over 1,000 meticulously compiled matches, this dataset is perfect for cricket analytics, predictive modeling, and sports data science projects.

The data has been sourced from **Cricsheet** (the world's most comprehensive cricket data repository), cleaned, validated, and formatted for immediate analysis. Every match includes detailed outcome information, venue details, opponent teams, and victory margins, making it ideal for both exploratory data analysis and machine learning applications.

## 🏏 Dataset Columns

- **Match_Date**: Date when the match was played (YYYY-MM-DD format)
- **Match_Format**: Type of international cricket (Test, ODI, T20)
- **Opponent**: Team that played against Sri Lanka
- **Winner**: Match outcome (Sri Lanka, Opponent, Draw, Tie, No Result)
- **Margin**: Victory margin (e.g., "5 wickets", "123 runs", or empty for draws/ties)
- **Ground**: Stadium or venue where the match was played
- **Year**: Match year (2000-2026) for easy filtering

## 📅 Time Coverage

**Date Range**: January 2000 - January 30, 2026 (26+ years of data)  
**Total Matches**: 1,082 international matches

**Breakdown by Year**:
- First match: June 27, 2002
- Last match: January 30, 2026
- Continuous coverage across all three formats

## 🎯 Cricket Formats Included

1. **Test Cricket** (174 matches) - The traditional 5-day format
2. **One Day Internationals (ODI)** (572 matches) - 50-over format
3. **Twenty20 (T20)** (336 matches) - Fast-paced 20-over format

## 💡 Suggested Use Cases

### Exploratory Data Analysis (EDA)
- **Performance Trends**: Analyze Sri Lanka's win rate over time
- **Home vs Away**: Compare performance at home grounds vs international venues
- **Format Analysis**: Identify which format Sri Lanka performs best in
- **Opponent Analysis**: Discover most challenging opponents and rivalry patterns
- **Venue Insights**: Find grounds where Sri Lanka has the best/worst record
- **Temporal Patterns**: Examine performance by year, season, or era
- **Margin Analysis**: Study typical victory margins and dominant wins

### Machine Learning Projects
- **Match Outcome Prediction**: Build classifiers to predict match winners
- **Win Probability Models**: Estimate win likelihood based on opponent and venue
- **Performance Forecasting**: Time series analysis of team performance trends
- **Clustering Analysis**: Group matches by similar characteristics
- **Feature Engineering**: Create new features like rolling averages, win streaks
- **Sentiment Analysis**: Combine with news data for performance correlation studies

### Visualization Projects
- **Interactive Dashboards**: Build web apps with Plotly Dash or Streamlit
- **Heat Maps**: Visualize performance across years and opponents
- **Geographic Analysis**: Map match locations and performance by country
- **Timeline Visualizations**: Create compelling stories of Sri Lanka's cricket journey

## 🔍 Data Quality & Processing

✅ **Validated Dataset**: All rows pass comprehensive quality checks  
✅ **No Missing Values**: Complete data for all critical fields  
✅ **Standardized Format**: Consistent naming and date formatting  
✅ **Duplicate-Free**: Automatic duplicate detection and removal  
✅ **Clean Categories**: Standardized match outcomes and formats  

**Processing Pipeline**:
1. Raw data extracted from Cricsheet JSON files
2. Filtered for Sri Lanka participation
3. Date validation (YYYY-MM-DD format)
4. Format standardization (Test/ODI/T20)
5. Winner categorization (5 standard outcomes)
6. Duplicate removal based on date + format + opponent + ground
7. Whitespace trimming and text normalization

## 📌 Data Source & Attribution

**Primary Source**: [Cricsheet](https://cricsheet.org/)  
**Creator**: Stephen Rushe  
**Data License**: Creative Commons Attribution 4.0 International License (CC BY 4.0)

Cricsheet provides comprehensive ball-by-ball cricket data in JSON format. This dataset aggregates match-level information specifically for Sri Lanka's international fixtures.

**Required Citation**:
```
Sri Lanka International Cricket Performance Dataset (2000-2026)
Data Source: Cricsheet (https://cricsheet.org/)
Created by: Stephen Rushe
Compiled and cleaned for Kaggle
License: CC BY 4.0
```

## ⚠️ Limitations & Notes

**Match Outcome Mapping**:
- Some historical matches may have incomplete outcome data
- "No Result" includes abandoned, cancelled, and rain-affected matches
- Draws primarily occur in Test cricket (multi-day format)

**Venue Naming**:
- Ground names follow Cricsheet's conventions
- Some venues may have undergone name changes over 26 years
- Spelling variations exist for international grounds

**Date Considerations**:
- Multi-day Test matches use the start date only
- Time zones are not included in the date field
- Some very early 2000s matches may have less detailed margin information

**Winner Field**:
- "Sri Lanka" = Sri Lanka won
- "Opponent" = The opposing team won (team name in Opponent column)
- "Draw" = Match ended without result (primarily Tests)
- "Tie" = Both teams scored exactly the same
- "No Result" = Match abandoned or no official result
- Empty = Unknown outcome (rare historical cases)

## 🏆 Dataset Highlights

- **Most Played Opponent**: India (179 matches)
- **Win Rate**: ~42% (452 wins out of 1,000 decided matches)
- **Format Distribution**: ODIs dominate (53%), followed by T20s (31%), then Tests (16%)
- **Most Common Outcome**: Opponent wins (548) vs Sri Lanka wins (452)
- **Special Matches**: 10 ties and 35 no-results across all formats

## 📊 Quick Statistics

| Metric | Value |
|--------|-------|
| Total Matches | 1,082 |
| Date Range | 2002-2026 |
| Sri Lanka Wins | 452 |
| Opponent Wins | 548 |
| Draws | 37 |
| Ties | 10 |
| No Results | 35 |
| Unique Opponents | 15+ teams |
| Unique Venues | 100+ grounds |

## 🚀 Getting Started

**Load the Data** (Python):
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('sri_lanka_international_cricket_matches_2000_present_clean.csv')

# Quick overview
print(df.head())
print(df.info())
print(df['Winner'].value_counts())
```

**Basic Analysis**:
```python
# Sri Lanka's win rate
sl_wins = len(df[df['Winner'] == 'Sri Lanka'])
total_matches = len(df[df['Winner'].isin(['Sri Lanka', 'Opponent'])])
win_rate = (sl_wins / total_matches) * 100
print(f"Win Rate: {win_rate:.2f}%")

# Performance by format
format_analysis = df.groupby(['Match_Format', 'Winner']).size().unstack(fill_value=0)
print(format_analysis)
```

## 📚 Additional Resources

- **Full Documentation**: See `data_dictionary.md` for detailed column descriptions
- **Source Code**: GitHub repository includes data processing scripts
- **Original Data**: Visit [Cricsheet.org](https://cricsheet.org/) for raw match data

## 🏅 Tags

`cricket` `sports` `time-series` `classification` `data-cleaning` `sri-lanka` `international-sports` `test-cricket` `odi` `t20` `sports-analytics` `machine-learning` `data-visualization`

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Maintainer**: Dataset compiled from Cricsheet data  
**Feedback**: Please report any data quality issues or suggestions for improvement!
