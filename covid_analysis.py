#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Step 1: Load data
url = './data/time_series_covid_19_confirmed.csv'
df = pd.read_csv(url)

# Step 2: Understand the data
df.shape
# checking the top 10 rows，
df.head(10) 
# getting a summary of the columns
df.describe()
# getting a summary of the numeric columns
df.info()
# Note: The Province/State column contains numerous missing values (NaNs). As the analysis aggregates data by Country/Region, these missing values are not considered.

# Step 3: Check for anomaly
# Check for duplicate rows
print("\nChecking for duplicate rows:")
duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"Found {duplicates} duplicate rows. Removing duplicates.")
    df = df.drop_duplicates()
else:
    print("No duplicate rows found.")

# Check for zero values in lat/long 
date_cols = df.columns[:4]  # From the 5th column (index 4) onward are dates
zero_lat_long = (df[date_cols] == 0).any(axis=1)
print(df[zero_lat_long])  # Show records with zeros in lat/long
# The records with zeros in lat/long are all about cruise ship, in this analysis they will simplely be ignored

# Note： In this file, some numbers on certain dates are lower than those on the previous day, likely because some cases were false positives and were ignored.
# Codes for checking decreases in cumulative cases will be added later.

# Step 3: Preprocessing
# Unify China data
df['Country/Region'] = df['Country/Region'].replace(['Mainland China', 'Hong Kong', 'Macau', 'Taiwan*'], 'China')

# Aggregate to country level
df_country = df.groupby('Country/Region').sum(numeric_only=True).reset_index()

# Process date columns: Skip Lat, Long
date_cols = df_country.columns[4:]  # From the 5th column (index 4) onward are dates
df_melt = pd.melt(df_country, id_vars=['Country/Region'], value_vars=date_cols,
                  var_name='Date', value_name='Confirmed')
df_melt['Date'] = pd.to_datetime(df_melt['Date'], format='%m/%d/%y')

# Calculate daily new cases
df_melt = df_melt.sort_values(['Country/Region', 'Date'])
df_melt['Daily_New'] = df_melt.groupby('Country/Region')['Confirmed'].diff().fillna(0)

# Global totals
global_df = df_melt.groupby('Date').agg({'Confirmed': 'sum', 'Daily_New': 'sum'}).reset_index()

# Step 4: Dynamic trend plot - Global cumulative & daily new cases
fig = make_subplots(rows=2, cols=1, subplot_titles=('Global Cumulative Confirmed Trend (up to 2021-05-29)', 'Global Daily New Confirmed Trend'))

# Cumulative confirmed line plot
fig.add_trace(
    go.Scatter(x=global_df['Date'], y=global_df['Confirmed'], mode='lines', name='Cumulative Confirmed', line=dict(color='blue')),
    row=1, col=1
)

# Daily new cases bar plot
fig.add_trace(
    go.Bar(x=global_df['Date'], y=global_df['Daily_New'], name='Daily New Cases', marker_color='red'),
    row=2, col=1
)

fig.update_layout(height=600, showlegend=True, title_text="Global COVID-19 Confirmed Trend (Interactive)")
fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Cumulative Confirmed Cases", row=1, col=1)
fig.update_yaxes(title_text="Daily New Cases", row=2, col=1)
fig.show()

# Step 5: Dynamic country comparison - Animated bar chart
# Define periods (monthly)
periods = [
    ('2020-01', '2020-01-22', '2020-01-31'),
    ('2020-02', '2020-02-01', '2020-02-29'),
    ('2020-03', '2020-03-01', '2020-03-31'),
    ('2020-04', '2020-04-01', '2020-04-30'),
    ('2020-05', '2020-05-01', '2020-05-31'),
    ('2020-06', '2020-06-01', '2020-06-30'),
    ('2020-07', '2020-07-01', '2020-07-31'),
    ('2020-08', '2020-08-01', '2020-08-31'),
    ('2020-09', '2020-09-01', '2020-09-30'),
    ('2020-10', '2020-10-01', '2020-10-31'),
    ('2020-11', '2020-11-01', '2020-11-30'),
    ('2020-12', '2020-12-01', '2020-12-31'),
    ('2021-01', '2021-01-01', '2021-01-31'),
    ('2021-02', '2021-02-01', '2021-02-28'),
    ('2021-03', '2021-03-01', '2021-03-31'),
    ('2021-04', '2021-04-01', '2021-04-30'),
    ('2021-05', '2021-05-01', '2021-05-29')
]

# Prepare period data: Top 10 countries for each period
period_data = []
for label, start, end in periods:
    period_df = df_melt[(df_melt['Date'] >= start) & (df_melt['Date'] <= end)]
    period_summary = period_df.groupby('Country/Region')['Confirmed'].last().nlargest(10).reset_index()
    period_summary['Period'] = label
    period_data.append(period_summary)
period_df_all = pd.concat(period_data)

# Animated bar chart
fig2 = px.bar(period_df_all, x='Country/Region', y='Confirmed', color='Country/Region',
              animation_frame='Period', title='Monthly Top 10 Countries by Cumulative Confirmed Cases (Animated)',
              labels={'Confirmed': 'Cumulative Confirmed Cases', 'Country/Region': 'Country'},
              height=600)

# Dynamically update x-axis and y-axis
for frame in fig2.frames:
    period = frame.name
    period_data = period_df_all[period_df_all['Period'] == period]
    period_countries = period_data['Country/Region'].tolist()
    max_confirmed = period_data['Confirmed'].max() * 1.1  # Add 10% margin
    frame.layout.update(
        xaxis=dict(categoryorder='array', categoryarray=period_countries),
        yaxis=dict(range=[0, max_confirmed])
    )

# Set single play button
fig2.update_layout(
    showlegend=True,
    xaxis_title="Country",
    yaxis_title="Cumulative Confirmed Cases",
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=1.0,
        x=1.0,
        xanchor="right",
        yanchor="top",
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[None, dict(frame=dict(duration=3000, redraw=True),
                                fromcurrent=True,  # Continue from current frame
                                transition=dict(duration=500))]
            ),
            dict(
                label="Pause",
                method="animate",
                args=[[None], dict(frame=dict(duration=0, redraw=False),
                                  mode="immediate",
                                  transition=dict(duration=0))]
            )
        ]
    )]
)
fig2.show()

# Step 6: Output table of top 10 countries for each period
print("Monthly Top 10 Countries by Cumulative Confirmed Cases (End-of-Month Values):")
for label, start, end in periods:
    period_df = df_melt[(df_melt['Date'] >= start) & (df_melt['Date'] <= end)]
    period_summary = period_df.groupby('Country/Region')['Confirmed'].last().nlargest(10)
    print(f"\n{label}:")
    print(period_summary)

# Step 7: Choropleth map
fig_map = px.choropleth(
    df_melt,
    locations="Country/Region",
    locationmode="country names",  # Keep original mode, ignore warnings
    color="Confirmed",
    hover_name="Country/Region",
    animation_frame=df_melt['Date'].dt.strftime('%Y-%m-%d'),
    title="Global COVID-19 Confirmed Cases Distribution (Animated)",
    color_continuous_scale=px.colors.sequential.Plasma,
    height=800,  # Increase map height
    width=1200  # Increase map width
)
fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
    margin=dict(l=10, r=10, t=50, b=10)  # Reduce margins
)
fig_map.show()

# Get top 10 countries for the entire period (based on 2021-05-29 cumulative confirmed cases)
top_countries = df_melt[df_melt['Date'] == '2021-05-29'].groupby('Country/Region')['Confirmed'].sum().nlargest(10).index.tolist()

# Prepare heatmap data: Cumulative confirmed cases for top 10 countries by month
heatmap_data = []
for label, start, end in periods:
    period_df = df_melt[(df_melt['Date'] >= start) & (df_melt['Date'] <= end) & (df_melt['Country/Region'].isin(top_countries))]
    period_summary = period_df.groupby('Country/Region')['Confirmed'].last().reindex(top_countries, fill_value=0).reset_index()
    period_summary['Period'] = label
    heatmap_data.append(period_summary)
heatmap_df = pd.concat(heatmap_data)

# Convert to pivot table (x: months, y: countries, values: confirmed cases)
pivot_df = heatmap_df.pivot(index='Country/Region', columns='Period', values='Confirmed')

# Use logarithmic scale (to avoid large values compressing differences)
pivot_df_log = np.log10(pivot_df + 1)  # Add 1 to avoid log(0)

# Step 8: Heatmap
fig_heatmap = px.imshow(
    pivot_df_log,
    labels=dict(x="Month", y="Country", color="Cumulative Confirmed Cases (log10)"),
    x=pivot_df_log.columns,
    y=pivot_df_log.index,
    title="Monthly Top 10 Countries Cumulative Confirmed Cases Heatmap (Log Scale)",
    color_continuous_scale='Viridis'  # Color from blue (low) to yellow (high)
)
fig_heatmap.update_layout(height=600, width=800)
fig_heatmap.show()

