# scripts/python/02_process_02_ride_length_validation.py
import pandas as pd
import os

# Define paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')

# Input and output files
input_file = os.path.join(processed_path, 'cyclistic_trips_cleaned.csv')
output_file = os.path.join(processed_path, 'cyclistic_trips_final.csv')

print("Starting ride_length validation and final cleaning...")

# Load the cleaned dataset
df = pd.read_csv(input_file, low_memory=False)
print(f"Rows before validation: {len(df):,}")

# Step 1: Define mask for valid ride_length (only remove clear errors)
valid_mask = df['ride_length'] > 0

# Step 2: Apply the mask and create final dataframe
df_final = df[valid_mask].copy()

# Step 3: Calculate statistics
removed_rows = len(df) - len(df_final)
removed_pct = (removed_rows / len(df)) * 100 if len(df) > 0 else 0

print(f"Invalid rides removed (ride_length <= 0): {removed_rows:,} ({removed_pct:.3f}%)")
print(f"Final rows after cleaning: {len(df_final):,}")

# Step 4: Show ride_length statistics after cleaning
print("\nRide length statistics after removing invalid rides:")
print(df_final['ride_length'].describe().round(2))

# Save the final cleaned dataset
df_final.to_csv(output_file, index=False)
print(f"\nFinal cleaned file saved to: {output_file}")
print("Process ride_length validation step completed.")