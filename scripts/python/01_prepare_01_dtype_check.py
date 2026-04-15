# scripts/python/01_prepare_01_dtype_check.py
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

print("Starting dtype and missing value check before concatenation...")

# Get all 2025*.csv files and sort by filename to keep chronological order
csv_files = sorted(glob.glob(os.path.join(raw_data_path, '2025*.csv')))

if not csv_files:
    raise FileNotFoundError("No 2025*.csv files found in data/raw/")

print(f"Found {len(csv_files)} CSV files (202501 to 202512)")

# Prepare lists to collect results
dtype_dict = {}
missing_dict = {}
row_count_dict = {}

# Process each file independently
for file in csv_files:
    month = os.path.basename(file).split('-')[0]  # e.g., 202501
    print(f"Processing {month} ...")
    
    df = pd.read_csv(file, low_memory=False)
    
    # Record row count
    row_count_dict[month] = len(df)
    
    # Get dtypes
    dtype_dict[month] = df.dtypes
    
    # Get missing percentage
    missing_pct = df.isnull().mean() * 100
    missing_dict[month] = missing_pct

# Create DataFrames
dtype_df = pd.DataFrame(dtype_dict)
missing_df = pd.DataFrame(missing_dict)

# Reorder columns to ensure 202501 to 202512
month_order = [f"2025{str(i).zfill(2)}" for i in range(1, 13)]
dtype_df = dtype_df.reindex(columns=month_order)
missing_df = missing_df.reindex(columns=month_order)

# Print results
print("\n=== DTYPE COMPARISON TABLE ===")
print(dtype_df)

print("\n=== MISSING PERCENTAGE COMPARISON TABLE (%) ===")
print(missing_df.round(2))

print("\n=== ROW COUNT PER MONTH ===")
for month, count in row_count_dict.items():
    print(f"{month}: {count:,} rows")

# Save to processed folder
dtype_df.to_csv(os.path.join(processed_path, 'dtype_comparison.csv'))
missing_df.to_csv(os.path.join(processed_path, 'missing_percentage_comparison.csv'))

print("\nCheck completed.")
print(f"dtype_comparison.csv and missing_percentage_comparison.csv saved to {processed_path}")