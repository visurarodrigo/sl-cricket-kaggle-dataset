"""
Data Quality Validation and Cleaning Script

This module validates and cleans the Sri Lanka cricket dataset to ensure
Kaggle-quality standards. It checks data integrity, removes duplicates,
standardizes values, and produces a cleaned CSV output.
"""

import logging
from pathlib import Path
from typing import Dict, Tuple
import re

import pandas as pd


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Expected configuration
EXPECTED_COLUMNS = ['Match_Date', 'Match_Format', 'Opponent', 'Winner', 'Margin', 'Ground', 'Year', 'Home_Away']
VALID_FORMATS = ['Test', 'ODI', 'T20']
VALID_WINNERS = ['Sri Lanka', 'Opponent', 'Draw', 'Tie', 'No Result', '']
INPUT_CSV = 'sri_lanka_international_cricket_matches_2000_present.csv'
OUTPUT_CSV = 'sri_lanka_international_cricket_matches_2000_present_clean.csv'

# Sri Lankan venue keywords for home/away classification
SRI_LANKAN_VENUES = [
    'Colombo', 'Galle', 'Kandy', 'Dambulla', 'Kurunegala',
    'Sinhalese Sports Club', 'R.Premadasa', 'R Premadasa', 'P Sara Oval',
    'Pallekele', 'Khettarama', 'Premadasa', 'Asgiriya',
    'Rangiri Dambulla', 'Galle International Stadium',
    'Pallekele International Cricket Stadium',
    'Premadasa International Cricket Stadium (RPS)'
]


class DataValidator:
    """Validates and cleans cricket match data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize validator with dataframe.
        
        Args:
            df: Input DataFrame to validate and clean
        """
        self.df = df.copy()
        self.original_rows = len(df)
        self.issues = {
            'missing_columns': [],
            'invalid_format': [],
            'invalid_winner': [],
            'invalid_year': [],
            'invalid_date': [],
            'sri_lanka_opponent': [],
            'duplicates': 0,
            'rows_removed': 0
        }
    
    def validate_columns(self) -> bool:
        """
        Validate that all expected columns exist.
        
        Returns:
            True if valid, False otherwise
        """
        # Required columns (excluding Home_Away which we'll add later)
        required_columns = ['Match_Date', 'Match_Format', 'Opponent', 'Winner', 'Margin', 'Ground', 'Year']
        
        missing = set(required_columns) - set(self.df.columns)
        extra = set(self.df.columns) - set(EXPECTED_COLUMNS)
        
        if missing:
            self.issues['missing_columns'] = list(missing)
            logger.error(f"Missing required columns: {missing}")
            return False
        
        if extra:
            logger.warning(f"Extra columns found (will be removed): {extra}")
            # Keep only required columns for now
            self.df = self.df[required_columns]
        
        logger.info("✓ Column validation passed")
        return True
    
    def trim_whitespace(self):
        """Trim whitespace from all string columns."""
        logger.info("Trimming whitespace from string columns...")
        
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
        
        logger.info("✓ Whitespace trimmed")
    
    def validate_match_format(self) -> int:
        """
        Validate and standardize Match_Format values.
        
        Returns:
            Number of invalid rows found
        """
        logger.info("Validating Match_Format...")
        
        # Standardize format names (handle T20I -> T20, etc.)
        format_mapping = {
            't20i': 'T20',
            't20': 'T20',
            'odi': 'ODI',
            'test': 'Test'
        }
        
        self.df['Match_Format'] = self.df['Match_Format'].astype(str).str.strip()
        self.df['Match_Format'] = self.df['Match_Format'].str.lower().map(
            lambda x: format_mapping.get(x, x.title())
        )
        
        invalid_mask = ~self.df['Match_Format'].isin(VALID_FORMATS)
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            invalid_formats = self.df.loc[invalid_mask, 'Match_Format'].unique()
            logger.warning(f"Found {invalid_count} rows with invalid formats: {invalid_formats}")
            self.issues['invalid_format'] = list(invalid_formats)
            self.df = self.df[~invalid_mask]
            self.issues['rows_removed'] += invalid_count
        
        logger.info(f"✓ Match_Format validated ({invalid_count} invalid rows removed)")
        return invalid_count
    
    def validate_winner(self) -> int:
        """
        Validate and standardize Winner values.
        
        Returns:
            Number of invalid rows found
        """
        logger.info("Validating Winner...")
        
        # Standardize winner values
        winner_mapping = {
            'sri lanka': 'Sri Lanka',
            'srilanka': 'Sri Lanka',
            'sl': 'Sri Lanka',
            'draw': 'Draw',
            'tie': 'Tie',
            'tied': 'Tie',
            'no result': 'No Result',
            'noresult': 'No Result',
            'no-result': 'No Result',
            'abandoned': 'No Result',
            'opponent': 'Opponent',
            '': '',
            'nan': ''
        }
        
        self.df['Winner'] = self.df['Winner'].fillna('').astype(str).str.strip()
        self.df['Winner'] = self.df['Winner'].str.lower().map(
            lambda x: winner_mapping.get(x, x)
        )
        
        # Check for invalid winners
        invalid_mask = ~self.df['Winner'].isin(VALID_WINNERS)
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            invalid_winners = self.df.loc[invalid_mask, 'Winner'].unique()
            logger.warning(f"Found {invalid_count} rows with invalid winners: {invalid_winners}")
            self.issues['invalid_winner'] = list(invalid_winners)
            
            # Try to map unknown winners to "Opponent"
            for idx in self.df[invalid_mask].index:
                winner = self.df.loc[idx, 'Winner']
                if winner and winner not in ['', 'nan', 'None']:
                    self.df.loc[idx, 'Winner'] = 'Opponent'
                else:
                    self.df.loc[idx, 'Winner'] = ''
        
        logger.info(f"✓ Winner validated ({invalid_count} values standardized)")
        return invalid_count
    
    def validate_date_format(self) -> int:
        """
        Validate Match_Date format (YYYY-MM-DD).
        
        Returns:
            Number of invalid rows found
        """
        logger.info("Validating Match_Date format...")
        
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        self.df['Match_Date'] = self.df['Match_Date'].astype(str).str.strip()
        valid_mask = self.df['Match_Date'].str.match(date_pattern)
        
        invalid_count = (~valid_mask).sum()
        
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} rows with invalid date format")
            self.issues['invalid_date'] = invalid_count
            self.df = self.df[valid_mask]
            self.issues['rows_removed'] += invalid_count
        
        logger.info(f"✓ Match_Date format validated ({invalid_count} invalid rows removed)")
        return invalid_count
    
    def validate_year_consistency(self) -> int:
        """
        Validate that Year matches Match_Date year.
        
        Returns:
            Number of inconsistent rows fixed
        """
        logger.info("Validating Year consistency...")
        
        # Extract year from Match_Date
        self.df['Year'] = pd.to_datetime(self.df['Match_Date'], errors='coerce').dt.year
        
        # Check for null years (invalid dates)
        null_years = self.df['Year'].isna().sum()
        if null_years > 0:
            logger.warning(f"Found {null_years} rows with invalid dates")
            self.df = self.df.dropna(subset=['Year'])
            self.issues['rows_removed'] += null_years
        
        # Convert to integer
        self.df['Year'] = self.df['Year'].astype(int)
        
        logger.info(f"✓ Year consistency validated")
        return 0
    
    def validate_opponent(self) -> int:
        """
        Validate that Opponent is never 'Sri Lanka'.
        
        Returns:
            Number of invalid rows found
        """
        logger.info("Validating Opponent...")
        
        self.df['Opponent'] = self.df['Opponent'].astype(str).str.strip()
        
        # Check for Sri Lanka as opponent
        sri_lanka_variations = ['Sri Lanka', 'sri lanka', 'SriLanka', 'SL']
        invalid_mask = self.df['Opponent'].isin(sri_lanka_variations)
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} rows where Opponent is Sri Lanka")
            self.issues['sri_lanka_opponent'] = invalid_count
            self.df = self.df[~invalid_mask]
            self.issues['rows_removed'] += invalid_count
        
        logger.info(f"✓ Opponent validated ({invalid_count} invalid rows removed)")
        return invalid_count
    
    def normalize_margin(self):
        """Normalize margin text format."""
        logger.info("Normalizing Margin format...")
        
        self.df['Margin'] = self.df['Margin'].fillna('').astype(str).str.strip()
        
        # Standardize whitespace
        self.df['Margin'] = self.df['Margin'].str.replace(r'\s+', ' ', regex=True)
        
        # Handle singular forms first, then standardize to plural (except for 1)
        # Pattern: number followed by space and "run" or "wicket" (not already plural)
        def normalize_margin_value(margin):
            if not margin or margin == 'nan':
                return ''
            
            # Match patterns like "X run", "X runs", "X wicket", "X wickets"
            import re
            match = re.match(r'^(\d+)\s+(run|runs|wicket|wickets)$', margin, re.IGNORECASE)
            if match:
                number = int(match.group(1))
                term = match.group(2).lower()
                
                # Determine if it's runs or wickets
                if 'run' in term:
                    return f"{number} run" if number == 1 else f"{number} runs"
                elif 'wicket' in term:
                    return f"{number} wicket" if number == 1 else f"{number} wickets"
            
            return margin
        
        self.df['Margin'] = self.df['Margin'].apply(normalize_margin_value)
        
        logger.info("✓ Margin normalized")
    
    def add_home_away_classification(self):
        """Add Home/Away classification based on venue location."""
        logger.info("Adding Home/Away classification...")
        
        def classify_venue(ground):
            """Classify a venue as Home or Away."""
            if pd.isna(ground):
                return 'Away'  # Default to Away if ground is missing
            
            ground_str = str(ground)
            # Check if any Sri Lankan venue keyword is in the ground name
            for keyword in SRI_LANKAN_VENUES:
                if keyword.lower() in ground_str.lower():
                    return 'Home'
            return 'Away'
        
        self.df['Home_Away'] = self.df['Ground'].apply(classify_venue)
        
        # Log statistics
        home_count = (self.df['Home_Away'] == 'Home').sum()
        away_count = (self.df['Home_Away'] == 'Away').sum()
        total = len(self.df)
        
        logger.info(f"✓ Home/Away classification added:")
        logger.info(f"  - Home matches: {home_count} ({home_count/total*100:.1f}%)")
        logger.info(f"  - Away matches: {away_count} ({away_count/total*100:.1f}%)")
    
    def remove_duplicates(self) -> int:
        """
        Remove duplicate rows based on key columns.
        
        Returns:
            Number of duplicates removed
        """
        logger.info("Checking for duplicates...")
        
        key_columns = ['Match_Date', 'Match_Format', 'Opponent', 'Ground']
        
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=key_columns, keep='first')
        after = len(self.df)
        
        duplicates = before - after
        self.issues['duplicates'] = duplicates
        
        logger.info(f"✓ Duplicates removed: {duplicates}")
        return duplicates
    
    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.
        
        Returns:
            Cleaned DataFrame
        """
        return self.df
    
    def get_summary(self) -> Dict:
        """
        Get validation and cleaning summary.
        
        Returns:
            Dictionary with summary statistics
        """
        return {
            'total_rows_before': self.original_rows,
            'total_rows_after': len(self.df),
            'duplicates_removed': self.issues['duplicates'],
            'invalid_rows_removed': self.issues['rows_removed'],
            'issues': self.issues
        }


def clean_dataset(input_file: str = INPUT_CSV, output_file: str = OUTPUT_CSV) -> Dict:
    """
    Main function to clean and validate the dataset.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output cleaned CSV file
        
    Returns:
        Summary dictionary with cleaning statistics
    """
    logger.info("=" * 80)
    logger.info("Sri Lanka Cricket Dataset - Data Quality Validation & Cleaning")
    logger.info("=" * 80)
    
    # Check if input file exists
    input_path = Path(input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_file}")
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Load dataset
    logger.info(f"\nLoading dataset from: {input_file}")
    df = pd.read_csv(input_file)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Initialize validator
    validator = DataValidator(df)
    
    # Validation steps
    logger.info("\n" + "=" * 80)
    logger.info("STEP 1: STRUCTURAL VALIDATION")
    logger.info("=" * 80)
    
    if not validator.validate_columns():
        raise ValueError("Column validation failed. Cannot proceed.")
    
    # Data cleaning steps
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: DATA CLEANING & STANDARDIZATION")
    logger.info("=" * 80)
    
    validator.trim_whitespace()
    validator.validate_match_format()
    validator.validate_date_format()
    validator.validate_year_consistency()
    validator.validate_winner()
    validator.validate_opponent()
    validator.normalize_margin()
    validator.add_home_away_classification()
    
    # Remove duplicates
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: DUPLICATE DETECTION & REMOVAL")
    logger.info("=" * 80)
    
    validator.remove_duplicates()
    
    # Get cleaned data
    cleaned_df = validator.get_cleaned_dataframe()
    summary = validator.get_summary()
    
    # Sort by date
    cleaned_df = cleaned_df.sort_values('Match_Date').reset_index(drop=True)
    
    # Save cleaned dataset
    logger.info("\n" + "=" * 80)
    logger.info("STEP 4: SAVING CLEANED DATASET")
    logger.info("=" * 80)
    
    cleaned_df.to_csv(output_file, index=False)
    logger.info(f"✓ Cleaned dataset saved to: {output_file}")
    
    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("CLEANING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total rows before:        {summary['total_rows_before']}")
    logger.info(f"Total rows after:         {summary['total_rows_after']}")
    logger.info(f"Duplicates removed:       {summary['duplicates_removed']}")
    logger.info(f"Invalid rows removed:     {summary['invalid_rows_removed']}")
    logger.info(f"Data quality:             {summary['total_rows_after']/summary['total_rows_before']*100:.2f}% retained")
    
    # Additional statistics
    logger.info("\n" + "=" * 80)
    logger.info("DATASET STATISTICS")
    logger.info("=" * 80)
    logger.info(f"\nDate range: {cleaned_df['Match_Date'].min()} to {cleaned_df['Match_Date'].max()}")
    logger.info(f"\nBreakdown by format:")
    logger.info(cleaned_df['Match_Format'].value_counts().to_string())
    logger.info(f"\nBreakdown by winner:")
    logger.info(cleaned_df['Winner'].value_counts().to_string())
    logger.info(f"\nBreakdown by Home/Away:")
    logger.info(cleaned_df['Home_Away'].value_counts().to_string())
    logger.info(f"\nTop 10 opponents:")
    logger.info(cleaned_df['Opponent'].value_counts().head(10).to_string())
    
    logger.info("\n" + "=" * 80)
    logger.info("SUCCESS! Dataset cleaned and validated.")
    logger.info("=" * 80)
    
    return summary


def main():
    """Entry point for CLI."""
    try:
        clean_dataset()
    except FileNotFoundError as e:
        logger.error(f"\n{e}")
        logger.error("Please generate the raw dataset first by running:")
        logger.error("  python -m src.build_dataset")
    except Exception as e:
        logger.error(f"\nFatal error: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
