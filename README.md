# Cyclistic Bike-Share Analysis  
**Google Data Analytics Professional Certificate Capstone Project**

## Overview
This project analyzes Cyclistic's 2025 trip data to understand how **casual riders** and **annual members** use bike-share services differently. The goal is to provide data-driven recommendations to convert casual riders into annual members — the more profitable customer segment.

**Business Task**  
How do annual members and casual riders use Cyclistic bikes differently?

---

## Project Structure

```
Cyclistic-Bike-Share-Analysis/
├── README.md
├── PROJECT_REPORT.md
├── requirements.txt
├── data/
│   ├── processed/          ← Final cleaned dataset
│   └── output/             ← All analysis results (CSV)
├── scripts/
│   ├── python/             ← All Python analysis scripts
│   └── sql/                ← SQL queries
├── visualizations/
│   ├── tableau/            ← Tableau workbook (.twbx)
│   └── images/             ← Dashboard screenshots
└── report/                 ← Final report

```
---

## Key Findings

- Casual riders take **significantly longer trips** than members (17.19 min vs 11.07 min).
- Casual riders show strong **weekend and midday** usage patterns, preferring longer leisure rides.
- Classic bikes, although only 33.35% of casual rides, contribute **45.65%** of total ride minutes — dramatically increasing the overall average ride length.
- Members exhibit typical **commuting behavior**: high frequency on weekdays with clear morning and evening peaks.

## Visualizations

**Interactive Tableau Dashboard**  
[View Full Interactive Dashboard](https://public.tableau.com/views/CyclisticCaseStudy_17762667207600/Casualriderstakesignificantlylongertripsthanmembers?:language=zh-TW&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

**Main Dashboard Highlights:**
- Ride length comparison (Box plot + Histogram)
- Weekly and hourly usage patterns
- Rideable type contribution analysis
![Dashboard](visualizations/images/dashboard.png)
---

## Technologies Used
- **Python**: pandas, numpy, matplotlib, seaborn
- **Tableau**: Dashboard creation and visualization
- **Data Cleaning**: Outlier removal, missing value handling, datetime transformation

---

## Top 3 Recommendations
1. Target weekend and midday leisure riders with classic bike-focused membership offers.
2. Create a "Longer Ride" membership incentive program emphasizing classic bike usage.
3. Use time- and day-based messaging to highlight cost savings for casual riders.

---

Personal ReflectionThe analysis focused on ride length, temporal patterns (day of week and start hour), and rideable type. Additional dimensions such as monthly/seasonal trends and station-level analysis could be explored in future work to further strengthen marketing recommendations.

---

## Detailed Project Report
For the complete step-by-step process (Ask → Prepare → Process → Analyze → Share → Act), please see **[PROJECT_REPORT.md](PROJECT_REPORT.md)**

---

**License**  
MIT License
