# scripts/python/03_analyze_01_descriptive_stats.py
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
output_file = os.path.join(output_path, 'descriptive_stats_member_casual.csv')

print("Starting descriptive statistics analysis...")

# Load the final dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Loaded {len(df):,} rows for analysis")

# Step 1: Overall statistics
overall_stats = df['ride_length'].describe().round(2)

# Step 2: Statistics grouped by member_casual
grouped_stats = df.groupby('member_casual')['ride_length'].describe().round(2)

# Step 3: Combine Overall + Member + Casual into one table
combined = pd.DataFrame({
    'count': overall_stats['count'],
    'mean': overall_stats['mean'],
    'std': overall_stats['std'],
    'min': overall_stats['min'],
    '25%': overall_stats['25%'],
    '50%': overall_stats['50%'],
    '75%': overall_stats['75%'],
    'max': overall_stats['max']
}, index=['Overall'])

combined = pd.concat([combined, grouped_stats])

# Rename index for clarity
combined.index.name = 'Member Type'
combined = combined.rename(index={'casual': 'Casual', 'member': 'Member'})

print("\n=== Ride Length Statistics - Overall vs Member vs Casual ===")
print(combined)

# Step 4: Save to CSV
combined.to_csv(output_file)
print(f"\nCombined descriptive statistics saved to: {output_file}")

print("\nAnalyze step 01 completed.")