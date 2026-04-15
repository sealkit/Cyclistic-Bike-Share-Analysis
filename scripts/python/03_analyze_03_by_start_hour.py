# scripts/python/03_analyze_03_by_start_hour.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')
output_path = os.path.join(project_root, 'data', 'output')

# Ensure output folder exists
os.makedirs(output_path, exist_ok=True)

# Input file
input_file = os.path.join(processed_path, 'cyclistic_trips_final.csv')
output_file = os.path.join(output_path, 'descriptive_stats_by_start_hour.csv')

print("Starting analysis by start hour...")

# Load the final dataset
df = pd.read_csv(input_file, low_memory=False)

# Convert started_at to datetime (in case it was saved as string)
df['started_at'] = pd.to_datetime(df['started_at'])
df['start_hour'] = df['started_at'].dt.hour

print(f"Loaded {len(df):,} rows for analysis")

# Group by start_hour and member_casual
grouped = df.groupby(['start_hour', 'member_casual']).agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()

# Overall by start_hour (without member_casual)
overall = df.groupby('start_hour').agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()
overall['member_casual'] = 'Overall'

# Combine Overall + Casual + Member
combined = pd.concat([overall, grouped], ignore_index=True)

# Reorder columns
combined = combined[['start_hour', 'member_casual', 
                     'ride_count', 'mean_ride_length', 'median_ride_length']]

# Sort by start_hour then member_casual
combined = combined.sort_values(by=['start_hour', 'member_casual'])

print("\n=== Ride Length Statistics by Start Hour (Overall vs Casual vs Member) ===")
print(combined.to_string(index=False))

# Save to CSV
combined.to_csv(output_file, index=False)
print(f"\nStatistics saved to: {output_file}")

print("\nAnalyze step 03 completed.")