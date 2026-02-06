"""
Automated Dataset Update Script

This script updates the entire dataset pipeline:
1. Downloads latest Cricsheet data
2. Builds raw dataset
3. Cleans and validates data
4. Regenerates EDA visualizations
5. Updates kaggle_release folder
6. Updates README with new statistics
7. Commits and pushes changes to GitHub

Usage:
    python update_dataset.py

Run this script monthly to keep the dataset current.
"""

import subprocess
import sys
import pandas as pd
import shutil
import re
from pathlib import Path
from datetime import datetime


def run_command(command, description):
    """Execute a command and handle errors."""
    print(f"\n{'=' * 80}")
    print(f"{description}")
    print(f"{'=' * 80}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stderr)
        return False


def update_readme_stats(csv_path):
    """Update README with latest dataset statistics."""
    print(f"\n{'=' * 80}")
    print("Updating README Statistics")
    print(f"{'=' * 80}")
    
    # Read the clean dataset
    df = pd.read_csv(csv_path)
    
    # Calculate statistics
    total_matches = len(df)
    min_date = df['Match_Date'].min()
    max_date = df['Match_Date'].max()
    
    print(f"📊 New Statistics:")
    print(f"  • Total matches: {total_matches}")
    print(f"  • Date range: {min_date} to {max_date}")
    
    # Read README
    readme_path = Path('README.md')
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Update badge with new match count
    readme_content = re.sub(
        r'\[!\[Dataset\]\(https://img\.shields\.io/badge/matches-\d+-orange\.svg\)\]',
        f'[![Dataset](https://img.shields.io/badge/matches-{total_matches}-orange.svg)]',
        readme_content
    )
    
    # Update Dataset Summary table
    readme_content = re.sub(
        r'\| \*\*Time Period\*\* \| January 2000 – .+ \|',
        f'| **Time Period** | January 2000 – {max_date} |',
        readme_content
    )
    
    readme_content = re.sub(
        r'\| \*\*Total Matches\*\* \| \d+,?\d* matches \|',
        f'| **Total Matches** | {total_matches:,} matches |',
        readme_content
    )
    
    # Update Last Updated in data dictionary overview
    current_month_year = datetime.now().strftime("%B %Y")
    readme_content = re.sub(
        r'\*\*Last Updated\*\*: .+ 20\d{2}',
        f'**Last Updated**: {current_month_year}',
        readme_content
    )
    
    # Update footer
    current_month = datetime.now().strftime("%B %Y")
    readme_content = re.sub(
        r'\*Last Updated: .+ \| Dataset Version: .+ \| Matches: \d+,?\d*\*',
        f'*Last Updated: {current_month} | Dataset Version: 1.0 | Matches: {total_matches:,}*',
        readme_content
    )
    
    # Write updated README
    readme_path.write_text(readme_content, encoding='utf-8')
    print("✅ README updated successfully")
    
    return total_matches, min_date, max_date


def main():
    """Main update pipeline."""
    print(f"\n{'=' * 80}")
    print("SRI LANKA CRICKET DATASET - AUTOMATED UPDATE")
    print(f"{'=' * 80}")
    print(f"Update started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Build raw dataset
    if not run_command(
        "python -m src.build_dataset",
        "STEP 1/7: Building Raw Dataset from Cricsheet"
    ):
        print("\n❌ Failed to build dataset. Exiting.")
        sys.exit(1)
    
    # Step 2: Clean and validate dataset
    if not run_command(
        "python -m src.clean_dataset",
        "STEP 2/7: Cleaning and Validating Dataset"
    ):
        print("\n❌ Failed to clean dataset. Exiting.")
        sys.exit(1)
    
    # Step 3: Regenerate EDA visualizations
    print(f"\n{'=' * 80}")
    print("STEP 3/7: Regenerating EDA Visualizations")
    print(f"{'=' * 80}")
    
    # Change to notebooks directory and run EDA
    original_dir = Path.cwd()
    notebooks_dir = Path('notebooks')
    
    try:
        import os
        os.chdir(notebooks_dir)
        
        if not run_command(
            "python eda_sri_lanka_cricket.py",
            "Generating charts..."
        ):
            print("⚠️  Warning: EDA generation failed, but continuing...")
        
        os.chdir(original_dir)
    except Exception as e:
        print(f"⚠️  Warning: Could not run EDA script: {e}")
        os.chdir(original_dir)
    
    # Step 4: Copy files to kaggle_release
    print(f"\n{'=' * 80}")
    print("STEP 4/7: Updating Kaggle Release Folder")
    print(f"{'=' * 80}")
    
    try:
        shutil.copy(
            'sri_lanka_international_cricket_matches_2000_present_clean.csv',
            'kaggle_release/sri_lanka_international_cricket_matches_2000_present_clean.csv'
        )
        print("✅ Copied clean CSV to kaggle_release/")
        
        shutil.copy(
            'data_dictionary.md',
            'kaggle_release/data_dictionary.md'
        )
        print("✅ Copied data dictionary to kaggle_release/")
    except Exception as e:
        print(f"⚠️  Warning: Could not copy files: {e}")
    
    # Step 5: Update README statistics
    try:
        total_matches, min_date, max_date = update_readme_stats(
            'sri_lanka_international_cricket_matches_2000_present_clean.csv'
        )
    except Exception as e:
        print(f"⚠️  Warning: Could not update README: {e}")
        total_matches = "unknown"
    
    # Step 6: Run tests (optional)
    print(f"\n{'=' * 80}")
    print("STEP 5/7: Running Tests (Optional)")
    print(f"{'=' * 80}")
    
    run_command(
        "pytest tests/ -v",
        "Validating with unit tests..."
    )
    
    # Step 7: Git commit and push
    print(f"\n{'=' * 80}")
    print("STEP 6/7: Committing Changes to Git")
    print(f"{'=' * 80}")
    
    commit_message = f"Auto-update dataset: {total_matches} matches as of {datetime.now().strftime('%Y-%m-%d')}"
    
    run_command("git add .", "Staging all changes...")
    run_command(f'git commit -m "{commit_message}"', "Committing changes...")
    
    print(f"\n{'=' * 80}")
    print("STEP 7/7: Pushing to GitHub")
    print(f"{'=' * 80}")
    
    if run_command("git push origin main", "Pushing to remote repository..."):
        print("\n✅ Successfully pushed to GitHub!")
    else:
        print("\n⚠️  Could not push to GitHub. Push manually with: git push origin main")
    
    # Summary
    print(f"\n{'=' * 80}")
    print("✅ UPDATE COMPLETE!")
    print(f"{'=' * 80}")
    print(f"📊 Dataset Statistics:")
    print(f"  • Total matches: {total_matches}")
    print(f"  • Updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📦 Updated Files:")
    print(f"  • sri_lanka_international_cricket_matches_2000_present.csv (raw)")
    print(f"  • sri_lanka_international_cricket_matches_2000_present_clean.csv")
    print(f"  • kaggle_release/ folder")
    print(f"  • eda_outputs/ visualizations")
    print(f"  • README.md statistics")
    print(f"\n🚀 Next Steps:")
    print(f"  1. Check GitHub for committed changes")
    print(f"  2. Update Kaggle dataset manually or via API")
    print(f"  3. Announce update on social media (optional)")
    print(f"{'=' * 80}\n")


if __name__ == '__main__':
    main()
