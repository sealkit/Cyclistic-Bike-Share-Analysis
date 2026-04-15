# scripts/python/01_prepare_02_merge.py
import pandas as pd
import glob
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
raw_data_path = os.path.join(project_root, 'data', 'raw')
processed_path = os.path.join(project_root, 'data', 'processed')

# Ensure processed folder exists
os.makedirs(processed_path, exist_ok=True)

print("Starting merge of 12 monthly CSV files...")

# Get all 2025*.csv files and sort by filename to keep chronological order
csv_files = sorted(glob.glob(os.path.join(raw_data_path, '2025*.csv')))

if not csv_files:
    raise FileNotFoundError("No 2025*.csv files found in data/raw/")

print(f"Found {len(csv_files)} CSV files to merge")

# Read and concatenate all files
df_list = []
for file in csv_files:
    month = os.path.basename(file).split('-')[0]
    print(f"Reading {month} ...")
    temp_df = pd.read_csv(file, low_memory=False)
    df_list.append(temp_df)

# Concatenate all dataframes
df = pd.concat(df_list, ignore_index=True)

print("\nMerge completed successfully!")
print(f"Total rows: {len(df):,}")
print(f"Total columns: {df.shape[1]}")
print("\nColumn names:")
print(df.columns.tolist())

# Save the merged file
output_file = os.path.join(processed_path, 'cyclistic_trips_12months.csv')
df.to_csv(output_file, index=False)

print(f"\nMerged file saved to: {output_file}")
print("Prepare merge step completed.")