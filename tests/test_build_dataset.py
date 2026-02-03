"""
Unit tests for Sri Lanka Cricket Dataset Builder
"""

import json
from pathlib import Path
from datetime import datetime
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.build_dataset import (
    parse_match_date,
    get_teams,
    determine_winner,
    get_margin,
    parse_match_json
)


class TestParseMatchDate:
    """Tests for date parsing function."""
    
    def test_parse_standard_date(self):
        """Test parsing standard YYYY-MM-DD format."""
        match_data = {
            'info': {
                'dates': ['2020-01-15']
            }
        }
        result = parse_match_date(match_data)
        assert result == '2020-01-15'
    
    def test_parse_slash_date(self):
        """Test parsing date with slashes."""
        match_data = {
            'info': {
                'dates': ['2020/01/15']
            }
        }
        result = parse_match_date(match_data)
        assert result == '2020-01-15'
    
    def test_parse_missing_dates(self):
        """Test handling missing dates."""
        match_data = {
            'info': {}
        }
        result = parse_match_date(match_data)
        assert result is None
    
    def test_parse_empty_dates_list(self):
        """Test handling empty dates list."""
        match_data = {
            'info': {
                'dates': []
            }
        }
        result = parse_match_date(match_data)
        assert result is None
    
    def test_parse_multiple_dates(self):
        """Test that first date is used when multiple dates exist."""
        match_data = {
            'info': {
                'dates': ['2020-01-15', '2020-01-16', '2020-01-17']
            }
        }
        result = parse_match_date(match_data)
        assert result == '2020-01-15'


class TestGetTeams:
    """Tests for team extraction function."""
    
    def test_get_two_teams(self):
        """Test extracting two teams."""
        match_data = {
            'info': {
                'teams': ['Sri Lanka', 'India']
            }
        }
        team1, team2 = get_teams(match_data)
        assert team1 == 'Sri Lanka'
        assert team2 == 'India'
    
    def test_get_teams_missing(self):
        """Test handling missing teams."""
        match_data = {
            'info': {}
        }
        team1, team2 = get_teams(match_data)
        assert team1 is None
        assert team2 is None
    
    def test_get_teams_insufficient(self):
        """Test handling insufficient teams."""
        match_data = {
            'info': {
                'teams': ['Sri Lanka']
            }
        }
        team1, team2 = get_teams(match_data)
        assert team1 is None
        assert team2 is None


class TestDetermineWinner:
    """Tests for winner determination function."""
    
    def test_sri_lanka_wins(self):
        """Test Sri Lanka winning."""
        match_data = {
            'info': {
                'outcome': {
                    'winner': 'Sri Lanka'
                }
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'Sri Lanka'
    
    def test_opponent_wins(self):
        """Test opponent winning."""
        match_data = {
            'info': {
                'outcome': {
                    'winner': 'India'
                }
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'Opponent'
    
    def test_tie(self):
        """Test tied match."""
        match_data = {
            'info': {
                'outcome': {
                    'result': 'tie'
                }
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'Tie'
    
    def test_draw(self):
        """Test drawn match."""
        match_data = {
            'info': {
                'outcome': {
                    'result': 'draw'
                }
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'Draw'
    
    def test_no_result(self):
        """Test no result match."""
        match_data = {
            'info': {
                'outcome': {
                    'result': 'no result'
                }
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'No Result'
    
    def test_draw_test_match_no_winner(self):
        """Test test match without winner (draw)."""
        match_data = {
            'info': {
                'outcome': {},
                'match_type': 'Test'
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        assert result == 'Draw'
    
    def test_unknown_outcome(self):
        """Test unknown outcome."""
        match_data = {
            'info': {
                'outcome': {}
            }
        }
        result = determine_winner(match_data, 'Sri Lanka', 'India')
        # Should return empty string for unknown
        assert result == ''


class TestGetMargin:
    """Tests for margin extraction function."""
    
    def test_margin_by_runs(self):
        """Test margin by runs."""
        match_data = {
            'info': {
                'outcome': {
                    'by': {
                        'runs': 123
                    }
                }
            }
        }
        result = get_margin(match_data)
        assert result == '123 runs'
    
    def test_margin_by_wickets(self):
        """Test margin by wickets."""
        match_data = {
            'info': {
                'outcome': {
                    'by': {
                        'wickets': 5
                    }
                }
            }
        }
        result = get_margin(match_data)
        assert result == '5 wickets'
    
    def test_no_margin(self):
        """Test no margin (tie/no result)."""
        match_data = {
            'info': {
                'outcome': {}
            }
        }
        result = get_margin(match_data)
        assert result == ''
    
    def test_missing_outcome(self):
        """Test missing outcome."""
        match_data = {
            'info': {}
        }
        result = get_margin(match_data)
        assert result == ''


class TestParseMatchJson:
    """Tests for complete match JSON parsing."""
    
    def test_parse_complete_match(self, tmp_path):
        """Test parsing a complete match."""
        match_data = {
            'info': {
                'teams': ['Sri Lanka', 'India'],
                'dates': ['2020-01-15'],
                'venue': 'Galle International Stadium',
                'outcome': {
                    'winner': 'Sri Lanka',
                    'by': {
                        'wickets': 5
                    }
                }
            }
        }
        
        # Create temporary JSON file
        json_file = tmp_path / "test_match.json"
        with open(json_file, 'w') as f:
            json.dump(match_data, f)
        
        result = parse_match_json(json_file, 'Test')
        
        assert result is not None
        assert result['Match_Date'] == '2020-01-15'
        assert result['Match_Format'] == 'Test'
        assert result['Opponent'] == 'India'
        assert result['Winner'] == 'Sri Lanka'
        assert result['Margin'] == '5 wickets'
        assert result['Ground'] == 'Galle International Stadium'
        assert result['Year'] == 2020
    
    def test_parse_non_sri_lanka_match(self, tmp_path):
        """Test that non-Sri Lanka matches are filtered out."""
        match_data = {
            'info': {
                'teams': ['India', 'Australia'],
                'dates': ['2020-01-15'],
                'venue': 'MCG'
            }
        }
        
        json_file = tmp_path / "test_match.json"
        with open(json_file, 'w') as f:
            json.dump(match_data, f)
        
        result = parse_match_json(json_file, 'Test')
        assert result is None
    
    def test_parse_pre_2000_match(self, tmp_path):
        """Test that pre-2000 matches are filtered out."""
        match_data = {
            'info': {
                'teams': ['Sri Lanka', 'India'],
                'dates': ['1999-12-31'],
                'venue': 'Test Ground'
            }
        }
        
        json_file = tmp_path / "test_match.json"
        with open(json_file, 'w') as f:
            json.dump(match_data, f)
        
        result = parse_match_json(json_file, 'Test')
        assert result is None
    
    def test_parse_invalid_json(self, tmp_path):
        """Test handling of invalid JSON."""
        json_file = tmp_path / "invalid.json"
        with open(json_file, 'w') as f:
            f.write("{ invalid json }")
        
        result = parse_match_json(json_file, 'Test')
        assert result is None
    
    def test_parse_missing_date(self, tmp_path):
        """Test handling of match with missing date."""
        match_data = {
            'info': {
                'teams': ['Sri Lanka', 'India'],
                'venue': 'Test Ground'
            }
        }
        
        json_file = tmp_path / "test_match.json"
        with open(json_file, 'w') as f:
            json.dump(match_data, f)
        
        result = parse_match_json(json_file, 'Test')
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
