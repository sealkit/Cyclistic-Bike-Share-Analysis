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

