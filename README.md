# Covid Data Analysis

A data analysis practice with the help of Grok. 

## Overview

This project analyzes and visualizes the COVID-19 confirmed cases time series data from Johns Hopkins University (`time_series_covid_19_confirmed.csv`). The analysis includes data cleaning, preprocessing, anomaly detection, country-level aggregation, global trend visualization, dynamic country comparisons, a global distribution map, and a heatmap of top countries. The goal is to explore global and country-specific pandemic trends and generate interactive visualizations.

## Dataset

### Source
Johns Hopkins University COVID-19 Dataset

### File
`time_series_covid_19_confirmed.csv`

### Content
- **Columns**: `Province/State`, `Country/Region`, `Lat`, `Long`, followed by daily confirmed cases from 2020-01-22 to 2021-05-29
- **Notes**:
  - The `Province/State` column contains many missing values (NaNs), which are ignored as the analysis aggregates data by `Country/Region`.
  - Some dates show cumulative cases lower than the previous day, likely due to false positives being removed.
  - Records with zero latitude/longitude ( records of cruise ships) are ignored in this analysis.

## Features

### Data Preprocessing
- Unifies China-related data (merges `Mainland China`, `Hong Kong`, `Macau`, `Taiwan*` into `China`).
- Aggregates data to the country level using `Country/Region`.
- Calculates daily new confirmed cases.

### Anomaly Detection
- Checks for duplicate rows and removes them if found.
- Identifies records with zero latitude/longitude (cruise ship data), which are ignored.
- *Note*: Code to detect decreases in cumulative cases (e.g., due to false positives) will be added later.

### Visualizations
- **Global Trend Plot**: Displays global cumulative confirmed cases (line plot) and daily new cases (bar plot).
- **Dynamic Country Comparison**: Animated bar chart showing the top 10 countries by cumulative confirmed cases for each month.
- **Global Distribution Map**: Animated choropleth map showing the global distribution of confirmed cases by date.
- **Heatmap**: Log-scale heatmap of cumulative confirmed cases for the top 10 countries by month.

## Dependencies

The following Python libraries are required:
- `pandas`
- `plotly`
- `numpy`

Install dependencies:
```bash
pip install pandas plotly numpy
```

## File Structure
```text
covid_analysis/
├── data/
│   └── time_series_covid_19_confirmed.csv  # Dataset file
├── covid_analysis.ipynb                    # Jupyter Notebook source code
├── covid_analysis.py                       # Converted Python script
└── README.md                               # Project documentation
```

## Usage
## Run the Code
### Jupyter Notebook
```bash
jupyter notebook covid_analysis.ipynb
```
Execute all cells to view interactive visualizations.
### Python Script
1. Convert the .ipynb file to .py (if not already done):
```bash
jupyter nbconvert --to python covid_analysis.ipynb
```
2. Run the Python script:
```bash
python covid_analysis.py
```
Ensure the dataset file is in the correct path and all dependencies are installed.

## Visualizations
- **Global Trend Plot**: Cumulative and daily new cases over time. A significant spike in global daily new confirmed cases occurred on December 10, 2020, reflecting a peak in the pandemic’s winter wave.
<img width="992" height="370" alt="image" src="https://github.com/user-attachments/assets/8a897e61-1709-44bf-ab7c-49317a36abf4" />
<img width="1070" height="386" alt="image" src="https://github.com/user-attachments/assets/2437b568-a2e1-42be-a8da-a3341c281ca9" />

- **Animated Bar Chart**: Top 10 countries by cumulative cases each month.
<img width="1364" height="602" alt="image" src="https://github.com/user-attachments/assets/ca047a53-f08c-45fd-91e5-bccf20ed6213" />

- **Choropleth Map**: Daily global distribution of confirmed cases.
<img width="1052" height="686" alt="image" src="https://github.com/user-attachments/assets/4da7398f-7505-4a04-ae4c-a68a075044c0" />

- **Heatmap**: Log-scale representation of monthly cases for top 10 countries.
<img width="1001" height="681" alt="image" src="https://github.com/user-attachments/assets/bb56f6b3-2d2f-49f3-ba2a-79383a574d36" />

## Future Work
- Add code to correct decreases in cumulative cases (e.g., due to false positives).
- Incorporate additional datasets (e.g., deaths, recoveries).
- Enhance map and heatmap visualizations (e.g., adjust colors or add interactivity).

## License
This project is licensed under the MIT License.
