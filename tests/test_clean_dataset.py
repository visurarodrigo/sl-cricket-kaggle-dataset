"""
Unit tests for data cleaning and validation
"""

import pandas as pd
import pytest
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.clean_dataset import DataValidator, EXPECTED_COLUMNS, VALID_FORMATS, VALID_WINNERS


class TestDataValidator:
    """Tests for DataValidator class."""
    
    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame for testing."""
        return pd.DataFrame({
            'Match_Date': ['2020-01-15', '2021-03-20', '2019-12-01'],
            'Match_Format': ['Test', 'ODI', 'T20'],
            'Opponent': ['India', 'Australia', 'England'],
            'Winner': ['Sri Lanka', 'Opponent', 'Draw'],
            'Margin': ['5 wickets', '50 runs', ''],
            'Ground': ['Galle Stadium', 'MCG', 'Lords'],
            'Year': [2020, 2021, 2019]
        })
    
    def test_validate_columns_success(self, sample_df):
        """Test successful column validation."""
        validator = DataValidator(sample_df)
        assert validator.validate_columns() is True
        assert len(validator.issues['missing_columns']) == 0
    
    def test_validate_columns_missing(self):
        """Test column validation with missing columns."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15'],
            'Match_Format': ['Test']
        })
        validator = DataValidator(df)
        assert validator.validate_columns() is False
        assert len(validator.issues['missing_columns']) > 0
    
    def test_validate_columns_extra(self, sample_df):
        """Test column validation with extra columns."""
        sample_df['Extra_Column'] = [1, 2, 3]
        validator = DataValidator(sample_df)
        assert validator.validate_columns() is True
        assert 'Extra_Column' not in validator.df.columns
    
    def test_trim_whitespace(self):
        """Test whitespace trimming."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15'],
            'Match_Format': ['  Test  '],
            'Opponent': ['India  '],
            'Winner': ['  Sri Lanka'],
            'Margin': ['5 wickets'],
            'Ground': ['  Galle  '],
            'Year': [2020]
        })
        validator = DataValidator(df)
        validator.trim_whitespace()
        
        assert validator.df['Match_Format'].iloc[0] == 'Test'
        assert validator.df['Opponent'].iloc[0] == 'India'
        assert validator.df['Winner'].iloc[0] == 'Sri Lanka'
        assert validator.df['Ground'].iloc[0] == 'Galle'
    
    def test_validate_match_format_valid(self, sample_df):
        """Test match format validation with valid data."""
        validator = DataValidator(sample_df)
        invalid_count = validator.validate_match_format()
        assert invalid_count == 0
        assert all(validator.df['Match_Format'].isin(VALID_FORMATS))
    
    def test_validate_match_format_standardization(self):
        """Test match format standardization."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-16', '2020-01-17'],
            'Match_Format': ['t20i', 'odi', 'test'],
            'Opponent': ['India', 'India', 'India'],
            'Winner': ['Sri Lanka', 'Sri Lanka', 'Sri Lanka'],
            'Margin': ['5 wickets', '5 wickets', '5 wickets'],
            'Ground': ['Galle', 'Galle', 'Galle'],
            'Year': [2020, 2020, 2020]
        })
        validator = DataValidator(df)
        validator.validate_match_format()
        
        assert validator.df['Match_Format'].iloc[0] == 'T20'
        assert validator.df['Match_Format'].iloc[1] == 'ODI'
        assert validator.df['Match_Format'].iloc[2] == 'Test'
    
    def test_validate_match_format_invalid(self):
        """Test match format validation with invalid data."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-16'],
            'Match_Format': ['Test', 'Invalid_Format'],
            'Opponent': ['India', 'India'],
            'Winner': ['Sri Lanka', 'Sri Lanka'],
            'Margin': ['5 wickets', '5 wickets'],
            'Ground': ['Galle', 'Galle'],
            'Year': [2020, 2020]
        })
        validator = DataValidator(df)
        invalid_count = validator.validate_match_format()
        
        assert invalid_count == 1
        assert len(validator.df) == 1
        assert validator.df['Match_Format'].iloc[0] == 'Test'
    
    def test_validate_winner_standardization(self):
        """Test winner value standardization."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18'],
            'Match_Format': ['Test', 'ODI', 'T20', 'ODI'],
            'Opponent': ['India', 'India', 'India', 'India'],
            'Winner': ['sri lanka', 'DRAW', 'tied', 'no result'],
            'Margin': ['', '', '', ''],
            'Ground': ['Galle', 'Galle', 'Galle', 'Galle'],
            'Year': [2020, 2020, 2020, 2020]
        })
        validator = DataValidator(df)
        validator.validate_winner()
        
        assert validator.df['Winner'].iloc[0] == 'Sri Lanka'
        assert validator.df['Winner'].iloc[1] == 'Draw'
        assert validator.df['Winner'].iloc[2] == 'Tie'
        assert validator.df['Winner'].iloc[3] == 'No Result'
    
    def test_validate_date_format_valid(self, sample_df):
        """Test date format validation with valid dates."""
        validator = DataValidator(sample_df)
        invalid_count = validator.validate_date_format()
        assert invalid_count == 0
    
    def test_validate_date_format_invalid(self):
        """Test date format validation with invalid dates."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '01/15/2020', 'invalid'],
            'Match_Format': ['Test', 'ODI', 'T20'],
            'Opponent': ['India', 'India', 'India'],
            'Winner': ['Sri Lanka', 'Sri Lanka', 'Sri Lanka'],
            'Margin': ['5 wickets', '5 wickets', '5 wickets'],
            'Ground': ['Galle', 'Galle', 'Galle'],
            'Year': [2020, 2020, 2020]
        })
        validator = DataValidator(df)
        invalid_count = validator.validate_date_format()
        
        assert invalid_count == 2
        assert len(validator.df) == 1
        assert validator.df['Match_Date'].iloc[0] == '2020-01-15'
    
    def test_validate_year_consistency(self, sample_df):
        """Test year consistency validation."""
        validator = DataValidator(sample_df)
        validator.validate_year_consistency()
        
        assert validator.df['Year'].iloc[0] == 2020
        assert validator.df['Year'].iloc[1] == 2021
        assert validator.df['Year'].iloc[2] == 2019
    
    def test_validate_opponent_valid(self, sample_df):
        """Test opponent validation with valid data."""
        validator = DataValidator(sample_df)
        invalid_count = validator.validate_opponent()
        assert invalid_count == 0
    
    def test_validate_opponent_invalid(self):
        """Test opponent validation with Sri Lanka as opponent."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-16'],
            'Match_Format': ['Test', 'ODI'],
            'Opponent': ['India', 'Sri Lanka'],
            'Winner': ['Sri Lanka', 'Opponent'],
            'Margin': ['5 wickets', '5 wickets'],
            'Ground': ['Galle', 'Galle'],
            'Year': [2020, 2020]
        })
        validator = DataValidator(df)
        invalid_count = validator.validate_opponent()
        
        assert invalid_count == 1
        assert len(validator.df) == 1
        assert validator.df['Opponent'].iloc[0] == 'India'
    
    def test_normalize_margin(self):
        """Test margin normalization."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-16', '2020-01-17'],
            'Match_Format': ['Test', 'ODI', 'T20'],
            'Opponent': ['India', 'India', 'India'],
            'Winner': ['Sri Lanka', 'Opponent', 'Sri Lanka'],
            'Margin': ['5 wicket', '100  run', '1 runs'],
            'Ground': ['Galle', 'Galle', 'Galle'],
            'Year': [2020, 2020, 2020]
        })
        validator = DataValidator(df)
        validator.normalize_margin()
        
        assert validator.df['Margin'].iloc[0] == '5 wickets'
        assert validator.df['Margin'].iloc[1] == '100 runs'
        assert validator.df['Margin'].iloc[2] == '1 run'
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-15', '2020-01-16'],
            'Match_Format': ['Test', 'Test', 'ODI'],
            'Opponent': ['India', 'India', 'India'],
            'Winner': ['Sri Lanka', 'Sri Lanka', 'Opponent'],
            'Margin': ['5 wickets', '5 wickets', '50 runs'],
            'Ground': ['Galle', 'Galle', 'Colombo'],
            'Year': [2020, 2020, 2020]
        })
        validator = DataValidator(df)
        duplicates = validator.remove_duplicates()
        
        assert duplicates == 1
        assert len(validator.df) == 2
    
    def test_get_summary(self, sample_df):
        """Test summary generation."""
        validator = DataValidator(sample_df)
        summary = validator.get_summary()
        
        assert 'total_rows_before' in summary
        assert 'total_rows_after' in summary
        assert 'duplicates_removed' in summary
        assert 'invalid_rows_removed' in summary
        assert summary['total_rows_before'] == 3
    
    def test_full_validation_pipeline(self):
        """Test complete validation pipeline."""
        df = pd.DataFrame({
            'Match_Date': ['2020-01-15', '2020-01-15', '2020-01-16', 'invalid'],
            'Match_Format': ['  test  ', 't20i', 'ODI', 'Test'],
            'Opponent': ['India', 'India', 'Australia', 'England'],
            'Winner': ['sri lanka', 'draw', 'opponent', 'Sri Lanka'],
            'Margin': ['5 wicket', '', '100 run', '1 runs'],
            'Ground': ['Galle', 'Galle', 'MCG', 'Lords'],
            'Year': [2020, 2020, 2020, 2020]
        })
        
        validator = DataValidator(df)
        validator.validate_columns()
        validator.trim_whitespace()
        validator.validate_match_format()
        validator.validate_date_format()
        validator.validate_year_consistency()
        validator.validate_winner()
        validator.validate_opponent()
        validator.normalize_margin()
        validator.remove_duplicates()
        
        cleaned_df = validator.get_cleaned_dataframe()
        
        # Should remove 1 invalid date, leaving 3 rows, then remove 1 duplicate, leaving 2
        # However, duplicates are based on [Match_Date, Match_Format, Opponent, Ground]
        # Row 0: 2020-01-15, Test, India, Galle
        # Row 1: 2020-01-15, T20, India, Galle - Different format, not a duplicate
        # Row 2: 2020-01-16, ODI, Australia, MCG
        # So actually 3 unique rows remain after removing invalid date
        assert len(cleaned_df) == 3
        assert all(cleaned_df['Match_Format'].isin(VALID_FORMATS))
        assert all(cleaned_df['Winner'].isin(VALID_WINNERS))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
