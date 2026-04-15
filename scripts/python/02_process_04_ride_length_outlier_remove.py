# scripts/python/02_process_04_ride_length_outlier_remove.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')

# Input and output files
input_file = os.path.join(processed_path, 'cyclistic_trips_valid.csv')
output_file = os.path.join(processed_path, 'cyclistic_trips_final.csv')

print("Starting final ride_length outlier removal...")

# Load the cleaned dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Original rows before outlier removal: {len(df):,}")

# Calculate 1% and 99% percentiles grouped by member_casual
percentiles = df.groupby('member_casual')['ride_length'].quantile([0.01, 0.99]).unstack()
percentiles.columns = ['1_percentile', '99_percentile']

# Mark and remove outliers based on group-specific percentiles
df['is_outlier'] = False

for member_type in ['casual', 'member']:
    p1 = percentiles.loc[member_type, '1_percentile']
    p99 = percentiles.loc[member_type, '99_percentile']
    mask = (df['member_casual'] == member_type) & (
        (df['ride_length'] < p1) | (df['ride_length'] > p99)
    )
    df.loc[mask, 'is_outlier'] = True

# Remove outliers
initial_rows = len(df)
df_clean = df[~df['is_outlier']].copy().drop(columns=['is_outlier'])
final_rows = len(df_clean)

print(f"Rows removed as outliers: {initial_rows - final_rows:,} ({(initial_rows - final_rows)/initial_rows*100:.2f}%)")
print(f"Final rows after outlier removal: {final_rows:,}")

# Final ride_length statistics after removal
final_stats = df_clean['ride_length'].agg(
    mean='mean',
    median='median',
    max='max',
    min='min',
    std='std'
).round(2)
print("\n=== FINAL RIDE LENGTH STATISTICS AFTER REMOVAL ===")
print(final_stats)

# Save the final cleaned file
df_clean.to_csv(output_file, index=False)
print(f"\nFinal cleaned file saved to: {output_file}")
print("Process stage - outlier removal completed.")