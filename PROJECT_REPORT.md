# PROJECT_REPORT.md
**Cyclistic Bike-Share Analysis – Full Process Documentation**  
Google Data Analytics Professional Certificate Capstone Project

---

## Ask

### Business Task
As a junior data analyst on the Cyclistic marketing team, the goal is to analyze Cyclistic’s historical trip data to identify how annual members and casual riders use Cyclistic bikes differently. These insights will support the design of a new marketing strategy aimed at converting casual riders into annual members, which has been identified by the finance team as the most profitable customer segment and the key driver for future company growth.

### Key Stakeholders
- **Primary**: Lily Moreno (Director of Marketing)  
- **Secondary**: Cyclistic Executive Team  
- **Internal**: Cyclistic Marketing Analytics Team

---

## Prepare

### Data Sources
The data used for this analysis is Cyclistic’s historical bike trip data, made publicly available by Motivate International Inc. under a license that permits exploration of customer usage patterns.

- **Source**: Divvy trip data (Cyclistic is a fictional brand name used in the case study; the actual data comes from Divvy Bikes in Chicago)  
- **Location**: https://divvy-tripdata.s3.amazonaws.com/index.html  
- **Time period**: January 2025 to December 2025 (12 monthly CSV files)  
- **File format**: CSV (zipped)  
- **Key variables**: `ride_id`, `rideable_type`, `started_at`, `ended_at`, `start_station_name`, `start_station_id`, `end_station_name`, `end_station_id`, `start_lat`, `start_lng`, `end_lat`, `end_lng`, `member_casual`  
- **Note**: Rider personally identifiable information is not included due to data privacy regulations.

**Special Note on Data Period**  
Due to an upload error in the official Divvy S3 bucket (the January 2026 file contained duplicated January 2025 data), the analysis uses the complete and verified 12-month period from January 2025 to December 2025 (5,552,092 total records before cleaning).

### Data Quality Check (Before Merging)
The 12 monthly CSV files (202501–202512) were individually inspected prior to merging.  

- All files share **identical column data types**.  
- Missing values are concentrated in `start_station_name`, `start_station_id`, `end_station_name`, and `end_station_id` columns (approximately 17–20%).  
- These missing values do not affect the core analysis variables (`ride_id`, `started_at`, `ended_at`, `member_casual`, coordinates).  

**ROCCC Assessment**  
- **Reliable** – Official data collected by the bike-share system  
- **Original** – First-party trip records  
- **Comprehensive** – Covers all trips in the service area for the selected period  
- **Current** – Uses the most recent 12 months available at the time of analysis  
- **Cited** – Properly attributed to Motivate International Inc.

**Output Files Generated**  
- `data/processed/dtype_comparison.csv` and `missing_percentage_comparison.csv` (quality check results)
---

## Process

### Documentation of Cleaning and Data Manipulation

The following cleaning and transformation steps were performed on the merged dataset (`cyclistic_trips_12months.csv`, 5,552,092 rows) to prepare the data for analysis.

#### 1. Initial Data Cleaning and Feature Engineering
- Removed duplicate `ride_id` records (0 duplicates found).
- Converted `started_at` and `ended_at` from object to `datetime64[ns]`.
- Created `ride_length` column (in minutes) using `(ended_at - started_at).dt.total_seconds() / 60`.
- Created `day_of_week` column (1 = Sunday, 7 = Saturday) using pandas `.dt.weekday` adjusted to match Excel WEEKDAY function.
- Filled missing values in `start_station_name`, `start_station_id`, `end_station_name`, and `end_station_id` with "Unknown".

**Result**: Cleaned file `cyclistic_trips_cleaned.csv` with 5,552,092 rows and 15 columns. No rows were deleted at this stage.

#### 2. Removal of Invalid Records
- Removed rows where `ride_length` ≤ 0 (clear data errors).  
  → 29 rows removed (0.001%).

**Result**: Dataset reduced to 5,552,063 rows.

#### 3. Missing Value Analysis (Station Information)
A comparison was conducted between records with missing station information (filled as "Unknown") and records with complete station data.

- Total records: 5,552,092  
- Records with missing station data: 1,862,960 (**33.55%**)

**Key Findings**:
- Missing station records are overwhelmingly electric bike rides (**99.69%**).
- Ride length, member_casual proportion, and day_of_week distribution show only minor differences between the two groups.

**Decision**: Retained all records with station = "Unknown". 
*Note*: Removing these records would disproportionately eliminate electric bike data (99.69% of missing records are electric, while electric bikes only represent 64.93% of the total dataset), creating severe bias in any analysis involving `rideable_type`.

#### 4. Outlier Analysis and Treatment (ride_length)
Outliers were examined using both Tableau visualizations (box plots and histograms) and Python group-specific percentile calculations (1% and 99% percentiles, calculated separately for casual and member riders).

**Key Findings**:
- Outlier records identified: 111,040 (**exactly 2.00%**)
- Perfectly balanced between groups: Casual (40,000 rows, 2.0%), Member (71,040 rows, 2.0%)
- Outliers have extremely high mean ride length (154.53 minutes) compared to non-outliers (13.27 minutes).
- Removing outliers reduces overall mean ride length from 16.10 to 13.27 minutes, while the median remains stable at 9.44 minutes.

**Decision**: Removed the 111,040 outliers using group-specific 1% and 99% percentiles. This is a data-driven decision that preserves the natural behavioral difference between casual and member riders while eliminating extreme errors.

#### Final Cleaned Dataset
- **File name**: `cyclistic_trips_final.csv`
- **Total rows**: 5,441,023
- **Total columns**: 15
- All original raw files remain untouched in the `data/raw/` folder.

**Output Files Generated**  
- `data/processed/missing_value_day_of_week_prop.csv`
- `data/processed/missing_value_member_casual_prop.csv`
- `data/processed/missing_value_ride_length_stats.csv`
- `data/processed/missing_value_rideable_type_prop.csv`
- `data/processed/outlier_count_by_group.csv`
- `data/processed/ride_length_outlier_impact.csv`
- `data/processed/ride_length_outlier_stats.csv`
- `data/processed/ride_length_percentiles_by_group.csv`

---
