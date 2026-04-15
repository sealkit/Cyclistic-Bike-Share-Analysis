# scripts/python/02_process_01_clean.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')

# Input and output files
input_file = os.path.join(processed_path, 'cyclistic_trips_12months.csv')
output_file = os.path.join(processed_path, 'cyclistic_trips_cleaned.csv')

print("Starting data cleaning process...")

# Load the merged dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Original rows: {len(df):,}")

# Step 1: Remove duplicate ride_id (should be unique)
initial_rows = len(df)
df = df.drop_duplicates(subset=['ride_id'])
print(f"Rows after removing duplicates: {len(df):,} (removed {initial_rows - len(df):,} duplicates)")

# Step 2: Convert timestamp columns to datetime
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])
print("Converted started_at and ended_at to datetime")

# Step 3: Create ride_length in minutes
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
print("Created ride_length column (minutes)")

# Step 4: Create day_of_week (1 = Sunday, 7 = Saturday)
# pandas.dt.weekday: 0=Mon ... 6=Sun , convert to 1=Sun, 7=Sat
df['day_of_week'] = ((df['started_at'].dt.weekday + 1) % 7) + 1
print("Created day_of_week column (1=Sunday)")

# Step 5: Fill missing station values with "Unknown"
station_cols = ['start_station_name', 'start_station_id', 
                'end_station_name', 'end_station_id']
missing_before = df[station_cols].isnull().sum().sum()
df[station_cols] = df[station_cols].fillna("Unknown")
missing_after = df[station_cols].isnull().sum().sum()
print(f"Filled station missing values with 'Unknown' (before: {missing_before:,}, after: {missing_after:,})")

# Final info
print(f"\nCleaned dataset rows: {len(df):,}")
print(f"Total columns: {df.shape[1]}")
memory_usage_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"Approximate memory usage: {memory_usage_mb:.2f} MB")

# Save cleaned file
df.to_csv(output_file, index=False)
print(f"\nCleaned file saved to: {output_file}")
print("Process cleaning step 01 completed.")