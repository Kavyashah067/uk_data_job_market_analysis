# UK Data Job Market Analysis (Python)

## Overview
Analysis of UK data-related job postings to identify hiring trends, salary patterns, and in-demand skills using a cleaned Kaggle dataset.

## Data Source
- Kaggle: UK Data Scientist Job Roles dataset  
- 750 job postings with company, role, location, salary, posting age, and skills

## Tools & Libraries
- Python
- pandas
- matplotlib

## Project Structure
uk_data_job_market_analysis/
│
├── data/
│   └── uk_data_jobs_raw.csv
│
├── src/
│   └── analysis.py
│
├── output/
│   └── cleaned_uk_data_jobs.csv
│
├── screenshots/
│   └── top_10_skills.png
│   └── top_paying_skills.png
│
└── README.md

## Methodology
- Data loading and validation
- String cleaning and normalization
- Feature engineering (days since posted, salary bands)
- Salary parsing (hourly vs yearly, ranges)
- Aggregation with minimum job-count filtering
- Skill extraction and frequency analysis
- Visualization of demand trends

## Key Insights
- Machine Learning roles dominate UK data hiring volume
- London is the primary hiring hub
- Cloud skills (AWS, Azure, GCP) correlate with higher salaries
- Statistical depth (Maths, SAS, Statistical Analysis) increases compensation
- Python alone is common and not a strong differentiator

## Visualization
### Top 10 Most In-Demand Skills
![Top 10 Most In-Demand Skills](screenshots/top_10_skills.png)

### Top 10 Highest Paying Skills (min 20 jobs)
![Top Paying Skills](screenshots/top_paying_skills.png)

### UK Data Job Salary Distribution
![UK Data Job Salary Distribution](screenshots/salary_distribution.png)

### UK Data Job Salary Boxplot
![UK Data Job Salary Boxplot](screenshots/salary_boxplot.png)

### Top 15 UK Locations by Average Salary
![Top 15 UK Locations by Average Salary](screenshots/salary_by_location.png)

### Remote vs Non-Remote Salary Comparison
![Remote vs Non-Remote Salary Comparison](screenshots/remote_vs_nonremote.png)

### Top Paying Data Skills in the UK (min 30 jobs)
![Top Paying Data Skills in the UK](screenshots/skills_vs_salary.png)


## Output
- Cleaned dataset with engineered features:
  - `days_since_posted`
  - `salary_min`
  - `salary_max`
  - `salary_avg`
  - `salary_type`
Saved to:
output/cleaned_uk_data_jobs.csv

