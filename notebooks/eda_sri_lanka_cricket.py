"""
Exploratory Data Analysis: Sri Lanka International Cricket Dataset (2000-2026)

This script performs comprehensive EDA on Sri Lanka's international cricket matches.
Includes visualizations and insights across all formats (Test, ODI, T20).
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Use non-interactive backend for automated execution
import matplotlib
matplotlib.use('Agg')

# Set style for better-looking plots
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def load_data():
    """Load and perform initial data exploration."""
    print("=" * 80)
    print("Sri Lanka International Cricket Dataset - Exploratory Data Analysis")
    print("=" * 80)
    print()
    
    # Load the clean dataset
    df = pd.read_csv('../sri_lanka_international_cricket_matches_2000_present_clean.csv')
    
    print(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print()
    
    # Display column information
    print("Columns:")
    for col in df.columns:
        print(f"  - {col}")
    print()
    
    # Check for missing values
    print("Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  ✓ No missing values found!")
    else:
        print(missing[missing > 0])
    print()
    
    # Data types
    print("Data Types:")
    print(df.dtypes)
    print()
    
    # Date range
    print(f"Date Range: {df['Match_Date'].min()} to {df['Match_Date'].max()}")
    print()
    
    return df


def plot_matches_per_year(df):
    """Visualize number of matches played per year."""
    print("\n" + "=" * 80)
    print("1. MATCHES PER YEAR")
    print("=" * 80)
    
    matches_per_year = df.groupby('Year').size().sort_index()
    
    plt.figure(figsize=(14, 6))
    plt.plot(matches_per_year.index, matches_per_year.values, 
             marker='o', linewidth=2, markersize=6, color='#1f77b4')
    plt.fill_between(matches_per_year.index, matches_per_year.values, 
                     alpha=0.3, color='#1f77b4')
    
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Matches', fontsize=12, fontweight='bold')
    plt.title('Sri Lanka International Cricket Matches Per Year (2002-2026)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure
    plt.savefig('../eda_outputs/matches_per_year.png', dpi=300, bbox_inches='tight')
    print("✓ Chart saved: eda_outputs/matches_per_year.png")
    
    plt.close()  # Close figure instead of showing
    
    # Insights
    peak_year = matches_per_year.idxmax()
    peak_count = matches_per_year.max()
    print(f"\n📊 Insights:")
    print(f"  • Peak year: {peak_year} with {peak_count} matches")
    print(f"  • Average matches per year: {matches_per_year.mean():.1f}")
    print(f"  • Total years covered: {len(matches_per_year)}")


def plot_matches_by_format(df):
    """Visualize matches by cricket format."""
    print("\n" + "=" * 80)
    print("2. MATCHES BY FORMAT")
    print("=" * 80)
    
    format_counts = df['Match_Format'].value_counts()
    
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    bars = plt.bar(format_counts.index, format_counts.values, 
                   color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Match Format', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Matches', fontsize=12, fontweight='bold')
    plt.title('Distribution of Matches by Format', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Save figure
    plt.savefig('../eda_outputs/matches_by_format.png', dpi=300, bbox_inches='tight')
    print("✓ Chart saved: eda_outputs/matches_by_format.png")
    
    plt.close()
    
    # Insights
    print(f"\n📊 Insights:")
    for fmt, count in format_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  • {fmt}: {count} matches ({percentage:.1f}%)")


def plot_match_outcomes(df):
    """Visualize match outcome distribution."""
    print("\n" + "=" * 80)
    print("3. MATCH OUTCOMES")
    print("=" * 80)
    
    outcome_counts = df['Winner'].value_counts()
    
    plt.figure(figsize=(12, 6))
    colors = ['#3498db', '#e74c3c', '#95a5a6', '#f39c12', '#9b59b6']
    bars = plt.bar(outcome_counts.index, outcome_counts.values, 
                   color=colors[:len(outcome_counts)], 
                   edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.xlabel('Match Outcome', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Matches', fontsize=12, fontweight='bold')
    plt.title('Distribution of Match Outcomes', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    # Save figure
    plt.savefig('../eda_outputs/match_outcomes.png', dpi=300, bbox_inches='tight')
    print("✓ Chart saved: eda_outputs/match_outcomes.png")
    
    plt.close()
    
    # Calculate win rate
    decided_matches = df[df['Winner'].isin(['Sri Lanka', 'Opponent'])]
    sl_wins = len(df[df['Winner'] == 'Sri Lanka'])
    total_decided = len(decided_matches)
    win_rate = (sl_wins / total_decided) * 100 if total_decided > 0 else 0
    
    print(f"\n📊 Insights:")
    print(f"  • Sri Lanka wins: {sl_wins} ({win_rate:.1f}% of decided matches)")
    print(f"  • Opponent wins: {outcome_counts.get('Opponent', 0)}")
    print(f"  • Draws: {outcome_counts.get('Draw', 0)}")
    print(f"  • Ties: {outcome_counts.get('Tie', 0)}")
    print(f"  • No Results: {outcome_counts.get('No Result', 0)}")


def plot_top_opponents(df):
    """Visualize top 10 opponents by match count."""
    print("\n" + "=" * 80)
    print("4. TOP 10 OPPONENTS")
    print("=" * 80)
    
    top_opponents = df['Opponent'].value_counts().head(10)
    
    plt.figure(figsize=(12, 7))
    colors = plt.cm.viridis(range(len(top_opponents)))
    bars = plt.barh(top_opponents.index, top_opponents.values, 
                    color=colors, edgecolor='black', linewidth=1.2)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_opponents.values)):
        plt.text(value, bar.get_y() + bar.get_height()/2, 
                f' {int(value)}',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.xlabel('Number of Matches', fontsize=12, fontweight='bold')
    plt.ylabel('Opponent Team', fontsize=12, fontweight='bold')
    plt.title('Top 10 Opponents by Match Count', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='x')
    plt.gca().invert_yaxis()  # Highest at top
    plt.tight_layout()
    
    # Save figure
    plt.savefig('../eda_outputs/top_opponents.png', dpi=300, bbox_inches='tight')
    print("✓ Chart saved: eda_outputs/top_opponents.png")
    
    plt.close()
    
    # Insights
    print(f"\n📊 Insights:")
    print(f"  • Most played opponent: {top_opponents.index[0]} ({top_opponents.values[0]} matches)")
    print(f"  • Total unique opponents: {df['Opponent'].nunique()}")
    
    # Win rate against top opponent
    top_opp = top_opponents.index[0]
    top_opp_matches = df[df['Opponent'] == top_opp]
    top_opp_wins = len(top_opp_matches[top_opp_matches['Winner'] == 'Sri Lanka'])
    top_opp_total = len(top_opp_matches[top_opp_matches['Winner'].isin(['Sri Lanka', 'Opponent'])])
    if top_opp_total > 0:
        top_opp_win_rate = (top_opp_wins / top_opp_total) * 100
        print(f"  • Win rate vs {top_opp}: {top_opp_win_rate:.1f}%")


def plot_top_grounds(df):
    """Visualize top 10 grounds by match count."""
    print("\n" + "=" * 80)
    print("5. TOP 10 MATCH VENUES")
    print("=" * 80)
    
    top_grounds = df['Ground'].value_counts().head(10)
    
    plt.figure(figsize=(12, 7))
    colors = plt.cm.plasma(range(len(top_grounds)))
    bars = plt.barh(top_grounds.index, top_grounds.values, 
                    color=colors, edgecolor='black', linewidth=1.2)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_grounds.values)):
        plt.text(value, bar.get_y() + bar.get_height()/2, 
                f' {int(value)}',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.xlabel('Number of Matches', fontsize=12, fontweight='bold')
    plt.ylabel('Ground/Venue', fontsize=12, fontweight='bold')
    plt.title('Top 10 Match Venues by Match Count', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='x')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    # Save figure
    plt.savefig('../eda_outputs/top_grounds.png', dpi=300, bbox_inches='tight')
    print("✓ Chart saved: eda_outputs/top_grounds.png")
    
    plt.close()
    
    # Insights
    print(f"\n📊 Insights:")
    print(f"  • Most frequent venue: {top_grounds.index[0]} ({top_grounds.values[0]} matches)")
    print(f"  • Total unique venues: {df['Ground'].nunique()}")


def analyze_format_performance(df):
    """Analyze performance across different formats."""
    print("\n" + "=" * 80)
    print("6. PERFORMANCE BY FORMAT")
    print("=" * 80)
    
    for fmt in ['Test', 'ODI', 'T20']:
        fmt_df = df[df['Match_Format'] == fmt]
        decided = fmt_df[fmt_df['Winner'].isin(['Sri Lanka', 'Opponent'])]
        wins = len(fmt_df[fmt_df['Winner'] == 'Sri Lanka'])
        total = len(decided)
        
        if total > 0:
            win_rate = (wins / total) * 100
            print(f"\n{fmt} Cricket:")
            print(f"  • Total matches: {len(fmt_df)}")
            print(f"  • Wins: {wins}")
            print(f"  • Win rate: {win_rate:.1f}%")


def generate_summary_statistics(df):
    """Generate overall summary statistics."""
    print("\n" + "=" * 80)
    print("7. SUMMARY STATISTICS")
    print("=" * 80)
    
    print(f"\n📈 Overall Statistics:")
    print(f"  • Total matches: {len(df)}")
    print(f"  • Date range: {df['Match_Date'].min()} to {df['Match_Date'].max()}")
    print(f"  • Years covered: {df['Year'].nunique()}")
    print(f"  • Formats: {', '.join(df['Match_Format'].unique())}")
    print(f"  • Unique opponents: {df['Opponent'].nunique()}")
    print(f"  • Unique venues: {df['Ground'].nunique()}")
    
    # Margin analysis
    print(f"\n🎯 Victory Margins:")
    margins_with_data = df[df['Margin'] != '']
    print(f"  • Matches with margin data: {len(margins_with_data)}")
    
    wicket_margins = margins_with_data[margins_with_data['Margin'].str.contains('wicket', case=False, na=False)]
    run_margins = margins_with_data[margins_with_data['Margin'].str.contains('run', case=False, na=False)]
    
    print(f"  • Wins by wickets: {len(wicket_margins)}")
    print(f"  • Wins by runs: {len(run_margins)}")


def main():
    """Main EDA execution function."""
    # Load data
    df = load_data()
    
    # Generate all visualizations and analyses
    plot_matches_per_year(df)
    plot_matches_by_format(df)
    plot_match_outcomes(df)
    plot_top_opponents(df)
    plot_top_grounds(df)
    analyze_format_performance(df)
    generate_summary_statistics(df)
    
    print("\n" + "=" * 80)
    print("✓ EDA Complete! All visualizations saved.")
    print("=" * 80)


if __name__ == '__main__':
    main()
