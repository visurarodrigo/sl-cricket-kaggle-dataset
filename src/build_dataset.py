"""
Sri Lanka International Cricket Performance Dataset Builder

This module downloads Cricsheet data (Tests, ODIs, T20s) and generates
a clean CSV dataset of Sri Lanka's international cricket matches from 2000 onwards.
"""

import json
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

import pandas as pd
import requests
from tqdm import tqdm


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Cricsheet data URLs
CRICSHEET_URLS = {
    'tests': 'https://cricsheet.org/downloads/tests_json.zip',
    'odis': 'https://cricsheet.org/downloads/odis_json.zip',
    't20s': 'https://cricsheet.org/downloads/t20s_json.zip'
}

# Output configuration
OUTPUT_CSV = 'sri_lanka_international_cricket_matches_2000_present.csv'
TEMP_DIR = Path('temp')
START_YEAR = 2000


def download_file(url: str, destination: Path) -> bool:
    """
    Download a file from URL with progress bar.
    
    Args:
        url: URL to download from
        destination: Path where file will be saved
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Downloading {url}")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as f, tqdm(
            desc=destination.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                progress_bar.update(size)
        
        logger.info(f"Successfully downloaded {destination.name}")
        return True
        
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error downloading {url}: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """
    Extract a zip file to destination.
    
    Args:
        zip_path: Path to zip file
        extract_to: Directory to extract to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Extracting {zip_path.name}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Successfully extracted {zip_path.name}")
        return True
        
    except zipfile.BadZipFile as e:
        logger.error(f"Invalid zip file {zip_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error extracting {zip_path}: {e}")
        return False


def parse_match_date(match_data: Dict) -> Optional[str]:
    """
    Parse match date from Cricsheet JSON.
    
    Args:
        match_data: Match JSON data
        
    Returns:
        Date string in YYYY-MM-DD format or None
    """
    try:
        dates = match_data.get('info', {}).get('dates', [])
        if not dates:
            return None
        
        date_str = dates[0]  # Use first date
        
        # Parse various date formats
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y']:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If parsing fails, try to handle YYYY-MM-DD directly
        if isinstance(date_str, str) and len(date_str) >= 10:
            return date_str[:10]
        
        return None
        
    except Exception as e:
        logger.debug(f"Error parsing date: {e}")
        return None


def get_teams(match_data: Dict) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract team names from match data.
    
    Args:
        match_data: Match JSON data
        
    Returns:
        Tuple of (team1, team2)
    """
    try:
        teams = match_data.get('info', {}).get('teams', [])
        if len(teams) >= 2:
            return teams[0], teams[1]
        return None, None
    except Exception:
        return None, None


def determine_winner(match_data: Dict, sri_lanka_team: str, opponent_team: str) -> str:
    """
    Determine the winner from match outcome.
    
    Args:
        match_data: Match JSON data
        sri_lanka_team: Name of Sri Lanka's team in this match
        opponent_team: Name of opponent team
        
    Returns:
        Winner as: "Sri Lanka", "Opponent", "Draw", "Tie", "No Result", or ""
    """
    try:
        info = match_data.get('info', {})
        outcome = info.get('outcome', {})
        
        # Check for no result
        result = outcome.get('result')
        if result:
            if result.lower() in ['no result', 'abandoned', 'cancelled']:
                return 'No Result'
            elif result.lower() in ['tie', 'tied']:
                return 'Tie'
            elif result.lower() in ['draw']:
                return 'Draw'
        
        # Check for winner
        winner = outcome.get('winner')
        if winner:
            if winner == sri_lanka_team or winner.lower() == 'sri lanka':
                return 'Sri Lanka'
            else:
                return 'Opponent'
        
        # Check if it's a draw (common in Tests)
        if not winner and not result:
            # For completed matches without a winner, likely a draw
            match_type = info.get('match_type', '')
            if match_type.lower() == 'test':
                return 'Draw'
        
        return ''
        
    except Exception as e:
        logger.debug(f"Error determining winner: {e}")
        return ''


def get_margin(match_data: Dict) -> str:
    """
    Extract match margin from outcome.
    
    Args:
        match_data: Match JSON data
        
    Returns:
        Margin string (e.g., "5 wickets", "123 runs") or ""
    """
    try:
        outcome = match_data.get('info', {}).get('outcome', {})
        
        if 'by' in outcome:
            by = outcome['by']
            if 'runs' in by:
                return f"{by['runs']} runs"
            elif 'wickets' in by:
                return f"{by['wickets']} wickets"
        
        return ''
        
    except Exception as e:
        logger.debug(f"Error getting margin: {e}")
        return ''


def parse_match_json(json_path: Path, match_format: str) -> Optional[Dict]:
    """
    Parse a single match JSON file.
    
    Args:
        json_path: Path to JSON file
        match_format: Match format (Test, ODI, T20)
        
    Returns:
        Dictionary with parsed match data or None
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            match_data = json.load(f)
        
        # Get basic info
        info = match_data.get('info', {})
        teams = info.get('teams', [])
        
        # Check if Sri Lanka is involved
        sri_lanka_variations = ['Sri Lanka', 'SL', 'sri lanka']
        sri_lanka_team = None
        opponent_team = None
        
        for team in teams:
            if any(sl in team for sl in sri_lanka_variations):
                sri_lanka_team = team
            else:
                opponent_team = team
        
        if not sri_lanka_team:
            return None  # Sri Lanka not in this match
        
        # Parse date and check year
        match_date = parse_match_date(match_data)
        if not match_date:
            return None
        
        try:
            year = int(match_date[:4])
            if year < START_YEAR:
                return None
        except (ValueError, TypeError):
            return None
        
        # Get venue
        ground = info.get('venue', '')
        
        # Determine winner
        winner = determine_winner(match_data, sri_lanka_team, opponent_team)
        
        # Get margin
        margin = get_margin(match_data)
        
        return {
            'Match_Date': match_date,
            'Match_Format': match_format,
            'Opponent': opponent_team if opponent_team else '',
            'Winner': winner,
            'Margin': margin,
            'Ground': ground,
            'Year': year
        }
        
    except json.JSONDecodeError as e:
        logger.debug(f"Invalid JSON in {json_path}: {e}")
        return None
    except Exception as e:
        logger.debug(f"Error parsing {json_path}: {e}")
        return None


def process_format(format_name: str, format_dir: Path) -> List[Dict]:
    """
    Process all matches for a specific format.
    
    Args:
        format_name: Format name (Test, ODI, T20)
        format_dir: Directory containing JSON files
        
    Returns:
        List of parsed match dictionaries
    """
    matches = []
    json_files = list(format_dir.glob('*.json'))
    
    logger.info(f"Processing {len(json_files)} {format_name} matches")
    
    for json_file in tqdm(json_files, desc=f"Parsing {format_name}"):
        match_data = parse_match_json(json_file, format_name)
        if match_data:
            matches.append(match_data)
    
    logger.info(f"Found {len(matches)} Sri Lanka {format_name} matches from {START_YEAR} onwards")
    return matches


def build_dataset():
    """
    Main function to build the Sri Lanka cricket dataset.
    """
    logger.info("=" * 80)
    logger.info("Sri Lanka International Cricket Dataset Builder")
    logger.info("=" * 80)
    
    # Create temp directory
    TEMP_DIR.mkdir(exist_ok=True)
    
    all_matches = []
    
    # Process each format
    for format_key, url in CRICSHEET_URLS.items():
        logger.info(f"\n{'=' * 80}")
        logger.info(f"Processing {format_key.upper()}")
        logger.info(f"{'=' * 80}")
        
        # Download
        zip_path = TEMP_DIR / f"{format_key}_json.zip"
        if not download_file(url, zip_path):
            logger.warning(f"Skipping {format_key} due to download failure")
            continue
        
        # Extract
        extract_dir = TEMP_DIR / format_key
        extract_dir.mkdir(exist_ok=True)
        
        if not extract_zip(zip_path, extract_dir):
            logger.warning(f"Skipping {format_key} due to extraction failure")
            continue
        
        # Determine format name
        format_name = {
            'tests': 'Test',
            'odis': 'ODI',
            't20s': 'T20'
        }[format_key]
        
        # Process matches
        matches = process_format(format_name, extract_dir)
        all_matches.extend(matches)
    
    # Create DataFrame
    if not all_matches:
        logger.error("No matches found! Dataset not created.")
        return
    
    logger.info(f"\n{'=' * 80}")
    logger.info(f"Creating CSV with {len(all_matches)} total matches")
    logger.info(f"{'=' * 80}")
    
    df = pd.DataFrame(all_matches)
    
    # Sort by date
    df = df.sort_values('Match_Date')
    
    # Ensure column order
    df = df[['Match_Date', 'Match_Format', 'Opponent', 'Winner', 'Margin', 'Ground', 'Year']]
    
    # Save CSV
    df.to_csv(OUTPUT_CSV, index=False)
    
    logger.info(f"\n{'=' * 80}")
    logger.info(f"SUCCESS!")
    logger.info(f"{'=' * 80}")
    logger.info(f"Dataset saved to: {OUTPUT_CSV}")
    logger.info(f"Total matches: {len(df)}")
    logger.info(f"Date range: {df['Match_Date'].min()} to {df['Match_Date'].max()}")
    logger.info(f"\nBreakdown by format:")
    logger.info(df['Match_Format'].value_counts().to_string())
    logger.info(f"\nBreakdown by winner:")
    logger.info(df['Winner'].value_counts().to_string())
    
    # Clean up temp directory (optional)
    logger.info(f"\nNote: Temporary files are in '{TEMP_DIR}' (you can delete this folder)")


def main():
    """Entry point for CLI."""
    try:
        build_dataset()
    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
    except Exception as e:
        logger.error(f"\n\nFatal error: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
