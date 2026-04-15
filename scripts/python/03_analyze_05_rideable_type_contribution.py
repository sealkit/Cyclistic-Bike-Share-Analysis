# scripts/python/03_analyze_05_rideable_type_contribution.py
import pandas as pd
import os

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
processed_path = os.path.join(project_root, 'data', 'processed')
output_path = os.path.join(project_root, 'data', 'output')
os.makedirs(output_path, exist_ok=True)

input_file = os.path.join(processed_path, 'cyclistic_trips_final.csv')
output_file = os.path.join(output_path, 'rideable_type_contribution.csv')

print("Starting rideable_type contribution analysis for both casual and member...")

# Load data
df = pd.read_csv(input_file, low_memory=False)

def contribution_analysis(group_df, group_name):
    contrib = group_df.groupby('rideable_type').agg(
        ride_count=('ride_length', 'count'),
        total_ride_minutes=('ride_length', 'sum'),
        mean_ride_length=('ride_length', 'mean'),
        median_ride_length=('ride_length', 'median')
    ).round(2)
    
    total_rides = contrib['ride_count'].sum()
    total_minutes = contrib['total_ride_minutes'].sum()
    
    contrib['ride_percentage'] = (contrib['ride_count'] / total_rides * 100).round(2)
    contrib['minutes_percentage'] = (contrib['total_ride_minutes'] / total_minutes * 100).round(2)
    contrib['group'] = group_name
    
    # Important: reset_index to bring 'rideable_type' back as a column
    return contrib.reset_index()

# Analyze casual and member separately
casual = df[df['member_casual'] == 'casual'].copy()
member = df[df['member_casual'] == 'member'].copy()

casual_contrib = contribution_analysis(casual, 'casual')
member_contrib = contribution_analysis(member, 'member')

# Combine both
combined = pd.concat([casual_contrib, member_contrib], ignore_index=True)

# Reorder columns for better readability
combined = combined[['group', 'rideable_type', 'ride_count', 'ride_percentage', 
                     'mean_ride_length', 'median_ride_length', 
                     'total_ride_minutes', 'minutes_percentage']]

print("\n=== Rideable Type Contribution Analysis (Casual vs Member) ===")
print(combined)

# Counterfactual means
print(f"\nCasual overall mean ride length     : {casual['ride_length'].mean():.2f} minutes")
print(f"If all casual used only classic     : {casual_contrib.loc[casual_contrib['rideable_type']=='classic_bike', 'mean_ride_length'].values[0]:.2f} minutes")
print(f"If all casual used only electric    : {casual_contrib.loc[casual_contrib['rideable_type']=='electric_bike', 'mean_ride_length'].values[0]:.2f} minutes")
print(f"\nMember overall mean ride length     : {member['ride_length'].mean():.2f} minutes")
print(f"If all member used only classic     : {member_contrib.loc[member_contrib['rideable_type']=='classic_bike', 'mean_ride_length'].values[0]:.2f} minutes")
print(f"If all member used only electric    : {member_contrib.loc[member_contrib['rideable_type']=='electric_bike', 'mean_ride_length'].values[0]:.2f} minutes")

# Save
combined.to_csv(output_file, index=False)
print(f"\nContribution analysis saved to: {output_file}")
print("\nAnalyze step 05 completed.")