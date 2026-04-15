# scripts/python/02_process_03_missing_value_analysis.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')

# Input file
input_file = os.path.join(processed_path, 'cyclistic_trips_cleaned.csv')

print("Starting missing station value analysis...")

# Load the cleaned dataset
df = pd.read_csv(input_file, low_memory=False)

# Create flag for missing station
df['is_missing_station'] = (
    (df['start_station_name'] == 'Unknown') | 
    (df['start_station_id'] == 'Unknown') |
    (df['end_station_name'] == 'Unknown') | 
    (df['end_station_id'] == 'Unknown')
)

# Calculate group sizes
total_rows = len(df)
missing_rows = df['is_missing_station'].sum()
print(f"Total rows: {total_rows:,}")
print(f"Rows with missing station: {missing_rows:,} ({missing_rows/total_rows*100:.2f}%)")

# 1. ride_length statistics comparison
ride_stats = df.groupby('is_missing_station')['ride_length'].agg(
    count='count',
    mean='mean',
    median='median',
    max='max',
    min='min',
    std='std'
).round(2)
print("\n=== RIDE LENGTH STATISTICS COMPARISON ===")
print(ride_stats)

# 2. member_casual proportion
member_prop = pd.crosstab(
    df['is_missing_station'], 
    df['member_casual'], 
    normalize='index'
) * 100
member_prop = member_prop.round(2)
print("\n=== MEMBER_CASUAL PROPORTION (%) ===")
print(member_prop)

# 3. day_of_week proportion
day_prop = pd.crosstab(
    df['is_missing_station'], 
    df['day_of_week'], 
    normalize='index'
) * 100
day_prop = day_prop.round(2)
print("\n=== DAY_OF_WEEK PROPORTION (%) ===")
print(day_prop)

# 4. rideable_type proportion
rideable_prop = pd.crosstab(
    df['is_missing_station'], 
    df['rideable_type'], 
    normalize='index'
) * 100
rideable_prop = rideable_prop.round(2)
print("\n=== RIDEABLE_TYPE PROPORTION (%) ===")
print(rideable_prop)

# Save results to CSV
ride_stats.to_csv(os.path.join(processed_path, 'missing_value_ride_length_stats.csv'))
member_prop.to_csv(os.path.join(processed_path, 'missing_value_member_casual_prop.csv'))
day_prop.to_csv(os.path.join(processed_path, 'missing_value_day_of_week_prop.csv'))
rideable_prop.to_csv(os.path.join(processed_path, 'missing_value_rideable_type_prop.csv'))

print("\nAnalysis completed.")
print(f"Four comparison CSV files saved to {processed_path}")