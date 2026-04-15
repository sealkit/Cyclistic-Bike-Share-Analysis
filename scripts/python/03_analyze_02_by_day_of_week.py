# scripts/python/03_analyze_02_by_day_of_week.py
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
output_file = os.path.join(output_path, 'descriptive_stats_by_day_of_week.csv')

print("Starting analysis by day_of_week...")

# Load the final dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Loaded {len(df):,} rows for analysis")

# Add readable day name
day_map = {
    1: 'Sunday',
    2: 'Monday',
    3: 'Tuesday',
    4: 'Wednesday',
    5: 'Thursday',
    6: 'Friday',
    7: 'Saturday'
}
df['day_name'] = df['day_of_week'].map(day_map)

# Group by day_of_week and member_casual
grouped = df.groupby(['day_of_week', 'day_name', 'member_casual']).agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()

# Overall by day_of_week (without member_casual)
overall = df.groupby(['day_of_week', 'day_name']).agg(
    ride_count=('ride_length', 'count'),
    mean_ride_length=('ride_length', 'mean'),
    median_ride_length=('ride_length', 'median')
).round(2).reset_index()
overall['member_casual'] = 'Overall'

# Combine Overall + Casual + Member
combined = pd.concat([overall, grouped], ignore_index=True)

# Reorder columns for better readability
combined = combined[['day_of_week', 'day_name', 'member_casual', 
                     'ride_count', 'mean_ride_length', 'median_ride_length']]

# Sort by day_of_week then member_casual
combined = combined.sort_values(by=['day_of_week', 'member_casual'])

print("\n=== Ride Length Statistics by Day of Week (Overall vs Casual vs Member) ===")
print(combined)

# Save to CSV
combined.to_csv(output_file, index=False)
print(f"\nStatistics saved to: {output_file}")

print("\nAnalyze step 02 completed.")