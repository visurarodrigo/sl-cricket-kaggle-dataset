import pandas as pd

# Define the stadiums that should be marked as Home
home_stadiums = [
    "Mahinda Rajapaksa International Cricket Stadium, Sooriyawewa",
    "Mahinda Rajapaksa International Cricket Stadium, Sooriyawewa, Hambantota",
    "Welagedara Stadium",
    "P Saravanamuttu Stadium",
    "Colts Cricket Club Ground"
]

# File paths to update
file_paths = [
    r"c:\Users\a12u\OneDrive\Desktop\Courses\Own Projects\Sri lanka cricket dataset\sri_lanka_international_cricket_matches_2000_present_clean.csv",
    r"c:\Users\a12u\OneDrive\Desktop\Courses\Own Projects\Sri lanka cricket dataset\kaggle_release\sri_lanka_international_cricket_matches_2000_present_clean.csv"
]

for file_path in file_paths:
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Count how many rows will be updated
    mask = df['Ground'].isin(home_stadiums) & (df['Home_Away'] == 'Away')
    count = mask.sum()
    
    print(f"\nFile: {file_path}")
    print(f"Found {count} matches to update")
    
    # Update Home_Away to Home for these stadiums
    df.loc[mask, 'Home_Away'] = 'Home'
    
    # Save the updated CSV
    df.to_csv(file_path, index=False)
    print(f"Updated {count} matches from Away to Home")

print("\n✓ All files have been updated successfully!")
