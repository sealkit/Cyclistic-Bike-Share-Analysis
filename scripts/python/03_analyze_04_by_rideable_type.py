# scripts/python/03_analyze_04_by_rideable_type.py
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
output_file = os.path.join(output_path, 'descriptive_stats_by_rideable_type.csv')

print("Starting analysis by rideable_type...")

# Load the final dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Loaded {len(df):,} rows for analysis")

# Group by rideable_type and member_casual
grouped = df.groupby(['rideable_type', 'member_casual']).agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()

# Calculate percentage within each member_casual group
grouped['percentage'] = grouped.groupby('member_casual')['ride_count'].transform(lambda x: x / x.sum() * 100).round(2)

# Overall (without member_casual)
overall = df.groupby('rideable_type').agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()
overall['member_casual'] = 'Overall'
overall['percentage'] = overall['ride_count'] / overall['ride_count'].sum() * 100
overall['percentage'] = overall['percentage'].round(2)

# Combine Overall + Casual + Member
combined = pd.concat([overall, grouped], ignore_index=True)

# Reorder columns for better readability
combined = combined[['rideable_type', 'member_casual', 'ride_count', 
                     'percentage', 'mean_ride_length', 'median_ride_length']]

# Sort by rideable_type then member_casual
combined = combined.sort_values(by=['rideable_type', 'member_casual'])

print("\n=== Rideable Type Statistics (Overall vs Casual vs Member) ===")
print(combined)

# Save to CSV
combined.to_csv(output_file, index=False)
print(f"\nStatistics saved to: {output_file}")

print("\nAnalyze step 04 completed.")