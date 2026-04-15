# scripts/python/02_process_03_ride_length_outlier_analysis.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')

# Input file
input_file = os.path.join(processed_path, 'cyclistic_trips_valid.csv')

print("Starting ride_length outlier analysis...")

# Load the cleaned dataset
df = pd.read_csv(input_file, low_memory=False)

# 1. Calculate 1% and 99% percentiles grouped by member_casual
percentiles = df.groupby('member_casual')['ride_length'].quantile([0.01, 0.99]).unstack()
percentiles.columns = ['1_percentile', '99_percentile']
print("\n=== RIDE LENGTH PERCENTILES BY MEMBER TYPE ===")
print(percentiles.round(2))

# 2. Mark outliers based on group-specific percentiles
df['is_outlier'] = False

for member_type in ['casual', 'member']:
    p1 = percentiles.loc[member_type, '1_percentile']
    p99 = percentiles.loc[member_type, '99_percentile']
    mask = (df['member_casual'] == member_type) & (
        (df['ride_length'] < p1) | (df['ride_length'] > p99)
    )
    df.loc[mask, 'is_outlier'] = True

# 3. Outlier count and percentage
total_rows = len(df)
outlier_rows = df['is_outlier'].sum()
print(f"\nTotal rows: {total_rows:,}")
print(f"Outlier rows: {outlier_rows:,} ({outlier_rows/total_rows*100:.2f}%)")

outlier_by_group = df.groupby('member_casual')['is_outlier'].agg(
    outlier_count='sum',
    outlier_pct=lambda x: x.mean()*100
).round(2)
print("\n=== OUTLIER COUNT BY MEMBER TYPE ===")
print(outlier_by_group)

# 4. Ride length statistics comparison (outlier vs non-outlier)
stats_comparison = df.groupby('is_outlier')['ride_length'].agg(
    count='count',
    mean='mean',
    median='median',
    max='max',
    min='min',
    std='std'
).round(2)
print("\n=== RIDE LENGTH STATS: OUTLIER vs NON-OUTLIER ===")
print(stats_comparison)

# 5. Impact if outliers are removed
mean_before = df['ride_length'].mean()
median_before = df['ride_length'].median()
mean_after = df.loc[~df['is_outlier'], 'ride_length'].mean()
median_after = df.loc[~df['is_outlier'], 'ride_length'].median()

impact = pd.DataFrame({
    'metric': ['mean', 'median'],
    'before_removal': [round(mean_before, 2), round(median_before, 2)],
    'after_removal': [round(mean_after, 2), round(median_after, 2)],
    'change': [round(mean_after - mean_before, 2), round(median_after - median_before, 2)]
})
print("\n=== IMPACT OF REMOVING OUTLIERS ===")
print(impact)

# Save all results to CSV
percentiles.to_csv(os.path.join(processed_path, 'ride_length_percentiles_by_group.csv'))
outlier_by_group.to_csv(os.path.join(processed_path, 'outlier_count_by_group.csv'))
stats_comparison.to_csv(os.path.join(processed_path, 'ride_length_outlier_stats.csv'))
impact.to_csv(os.path.join(processed_path, 'ride_length_outlier_impact.csv'))

print("\nAnalysis completed.")
print(f"Four comparison CSV files saved to {processed_path}")