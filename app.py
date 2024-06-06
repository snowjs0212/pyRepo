# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:37:55 2024

@author: Joonsoo
"""
#### Packages
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import os
import requests
from fredapi import Fred
import matplotlib.pyplot as plt

print(st.__version__)

#### Headers
st.set_page_config(page_title = "Joonsoo's playground with coffee", page_icon="☕")
st.title("Joonsoo's first test on streamlit")
st.text("This is a testing environment to build a better analytics tool in the future.")
st.markdown("**Gayun** is my wife, and she is cute(?).")

#### API Keys
#os.environ["ANTHROPIC_API_ID"] = st.secrets["ANTHROPIC_API_KEY"]

#### Imunika coffee data
#### File import
#uploaded_file = st.file_uploader("Upload your file here.")
#
#if uploaded_file:
#    df = pd.read_csv(uploaded_file)
#    st.write(df.describe())
st.header("LookUp - Imunika coffee research data")
df_1 = pd.read_csv("Imunika_Pilot_Stage1_Final.csv")
st.write(df_1.describe())

st.header("Data header summary")
st.write(df_1.head(10))

#### File import
st.header("User data analytics tool (csv file supported)")
uploaded_file = st.file_uploader("Upload your file here.")

if uploaded_file:
    df_2 = pd.read_csv(uploaded_file)
    st.write(df_2.describe())

#### API key
fred_api_key_input = st.secrets["fred_api_key"]
fred = Fred(api_key = fred_api_key_input)

### Global price of Coffee, Robustas
df_robus = fred.get_series('PCOFFROBUSDM')
df_robus.name = 'robustas'
df_robus.tail(50)

### Global price of Coffee, Other Mild Arabica
df_arabica = fred.get_series('PCOFFOTMUSDM')
df_arabica.name = 'arabica'
df_arabica.tail(50)

#### Data transformation
### Join data sources
df = pd.merge(
    df_robus, 
    df_arabica,
    left_index = True
    ,right_index = True)

### Data format changes
#df.index = pd.to_datetime(df.index, format = '%m/%d/%Y').strftime('%Y-%m-%d')
df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
df['close_date'] = df.index
df = df.round(2)

### Filter by rolling 4 years of data
df = df.tail(48)

#### Visualization
### Line chart
## Define figure and ax
df.plot.line(subplots = False)
fig, ax = plt.subplots()

## Plot the series on the axes
df.plot(ax = ax, linewidth = 2)

## Set the title and labels
ax.set_title('Coffee Bean Price Tracker - Rolling 4 Years')
ax.set_ylabel('USD($)')

## Display line chart in streamlit
st.header("Coffee Bean Price Tracker")
st.text("I want my coffee to be affordable!!!")
st.pyplot(fig)

## Sidebard
with st.sidebar:
    # Show the filtered DataFrame
    # Displaying a table
    st.subheader("Coffee Bean Price Summary Table - Rolling 12 Months")
    st.dataframe(df.tail(12), width = 400)

    # Source
    todays_date = str(df.tail(1).index[0])

    link1 = "https://fred.stlouisfed.org/series/PCOFFROBUSDM"
    link2 = "https://fred.stlouisfed.org/series/PCOFFROBUSDM"
    link3 = "https://fred.stlouisfed.org/series/PCOFFOTMUSDM"

    st.write(f"Data sources: International Monetary Fund, Global price of Coffee, Robustas [PCOFFROBUSDM], Global price of Coffee, Other Mild Arabica [PCOFFOTMUSDM] retrieved from FRED, [Federal Reserve Bank of St. Louis]({link1}) as of {todays_date}")
    st.write(
        f"Global price of Coffee, Robustas: [PCOFFROBUSDM]({link2}), Global price of Coffee, Arabica: [PCOFFOTMUSDM]({link3})"
    )


#### Altair practice
#### Data transformation
### Join data sources
df = pd.merge(
    df_robus, 
    df_arabica,
    left_index = True
    ,right_index = True)

### Data format changes
#df['Close Date'] = df.index.strftime("%Y-%m-%d")
df['Close Date'] = df.index
#df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
df = df.round(2)

### Rename column names
new_column_names = {
    "robustas": "Robusta",
    "arabica": "Arabica"
}
df = df.rename(columns = new_column_names)

### Filter by rolling 4 years of data
df_base = df.tail(48)

### Data transformation for altair package
## Melt the DataFrame to convert it to long format
melted_df = df_base.melt(id_vars = "Close Date", var_name = "Bean Type", value_name = "Price")

## Output columns
output_list = ["Robusta", "Arabica"]

### Define range:
## Determine the minimum and maximum values of 'Robusta' or 'Arabica'
min_y_value = melted_df["Price"].min()
max_y_value = melted_df["Price"].max()


## Calculate the starting and end points for the Y-axis range
y_start = np.floor(min_y_value * 1.8) / 2
y_end = np.ceil(max_y_value * 2.2) / 2

## Make radio button less cramped by adding a space after each label
labels = [option + " " for option in output_list]

input_dropdown = alt.binding_radio(
    # Add the empty selection which shows all when clicked
    options=output_list + [None],
    labels=labels + ["All"],
    name="Bean Type: ",
)
selection = alt.selection_point(
    fields=["Bean Type"],
    bind=input_dropdown,
)

## Basic line chart
base_chart = (
    alt.Chart(melted_df).mark_line()
    .encode(
        x = "Close Date:T",
        y = alt.Y(
            "Price:Q", 
            scale = alt.Scale(domain=[y_start, y_end])),
        color = alt.Color("Bean Type:N", sort=output_list),
        # tooltip=['Ticker:N', 'Yield:Q']
    )
    .add_params(selection)
    .transform_filter(selection)
)

## Add interactive vertical line
selector = alt.selection_single(
    encodings = ["x"],  # Selection based on x-axis (Close Date)
    on = "mouseover",  # Trigger on mouseover
    nearest = True,  # Select the value nearest to the mouse cursor
    empty = "none",  # Don't show anything when not mousing over the chart
)

rule = (
    alt.Chart(melted_df)
    .mark_rule()
    .encode(
        x = "Close Date:T",
        opacity = alt.condition(selector, alt.value(1), alt.value(0)),
        color = alt.value("gray"),
    )
    .add_selection(selector)
)

## Add text annotations for Ticker and Yield at intersection
## This step might require adjusting depending on your DataFrame's structure
text = (
    base_chart.mark_text(
        align = "left",
        dx = 5, 
        dy = -10, 
        fontWeight = "bold", 
        fontSize = 15)
    .encode(text=alt.condition(
        selector, 
        "Price:Q", 
        alt.value(" "), 
        format=".2f"))
    .transform_filter(selector)
)

## Assuming 'melted_df' has a 'Close Date' column in datetime format
start_date = melted_df["Close Date"].min()
end_date = melted_df["Close Date"].max()

## Generate quarter start dates within the range of your data
quarter_starts = pd.date_range(
    start = start_date, 
    end = end_date, 
    freq="QS").to_series()
quarter_starts_df = pd.DataFrame({"Close Date": quarter_starts})

## Chart for bold vertical lines at each quarter start
quarter_lines = (
    alt.Chart(quarter_starts_df).mark_rule(
        color="gray",
        strokeWidth=1
    )  # Bold vertical lines, adjust color/strokeWidth as needed
    .encode(x="Close Date:T")
)

## Combine the charts
final_chart = alt.layer(base_chart, rule, text, quarter_lines)

## Draw a chart
st.altair_chart(
    final_chart,
    theme = None,
    #theme = "streamlit",
    use_container_width = True,
)




#### M-over-M delta calculation
### Data transformation
## Add columns
df['Robusta Chg'] = df['Robusta']/df['Robusta'].shift(1) - 1
df['Arabica Chg'] = df['Arabica']/df['Arabica'].shift(1) - 1
df_chg_col_list = ['Close Date', 'Robusta Chg', 'Arabica Chg']

## Rename column names
df_chg = df[df_chg_col_list].tail(48)
new_column_names = {
    "Robusta Chg": "Robusta",
    "Arabica Chg": "Arabica"
}
df_chg = df_chg.rename(columns = new_column_names)

## Melt the DataFrame to convert it to long format
melted_df = df_chg.melt(id_vars = "Close Date", var_name = "Bean Type", value_name = "Change")

## Output columns
output_list = ["Robusta", "Arabica"]

### Define range:
## Determine the minimum and maximum values of 'Robusta' or 'Arabica'
min_y_value = melted_df["Change"].min()
max_y_value = melted_df["Change"].max()

## Calculate the starting and end points for the Y-axis range
y_start = (min_y_value * 2.2) / 2
y_end = (max_y_value * 2.2) / 2

## Make radio button less cramped by adding a space after each label
labels = [option + " " for option in output_list]

input_dropdown = alt.binding_radio(
    # Add the empty selection which shows all when clicked
    options=output_list + [None],
    labels=labels + ["All"],
    name="Bean Type: ",
)
selection = alt.selection_point(
    fields=["Bean Type"],
    bind=input_dropdown,
)

## Basic line chart
base_chart = (
    alt.Chart(melted_df).mark_line()
    .encode(
        x = "Close Date:T",
        y = alt.Y(
            "Change:Q", 
            scale = alt.Scale(domain=[y_start, y_end])).axis(format='.1%'),
        color = alt.Color("Bean Type:N", sort=output_list),
        # tooltip=['Ticker:N', 'Yield:Q']
    )
    .add_params(selection)
    .transform_filter(selection)
)

## Add interactive vertical line
selector = alt.selection_single(
    encodings = ["x"],  # Selection based on x-axis (Close Date)
    on = "mouseover",  # Trigger on mouseover
    nearest = True,  # Select the value nearest to the mouse cursor
    empty = "none",  # Don't show anything when not mousing over the chart
)

rule = (
    alt.Chart(melted_df)
    .mark_rule()
    .encode(
        x = "Close Date:T",
        opacity = alt.condition(selector, alt.value(1), alt.value(0)),
        color = alt.value("gray"),
    )
    .add_selection(selector)
)

## Add text annotations for Ticker and Yield at intersection
## This step might require adjusting depending on your DataFrame's structure
text = (
    base_chart.mark_text(
        align = "left",
        dx = 5, 
        dy = -10, 
        fontWeight = "bold", 
        fontSize = 15)
    .encode(text=alt.condition(
        selector, 
        "Change:Q", 
        alt.value(" "), 
        format = ".1%"))
    .transform_filter(selector)
)

## Assuming 'melted_df' has a 'Close Date' column in datetime format
start_date = melted_df["Close Date"].min()
end_date = melted_df["Close Date"].max()

## Generate quarter start dates within the range of your data
quarter_starts = pd.date_range(
    start = start_date, 
    end = end_date, 
    freq = "QS").to_series()
quarter_starts_df = pd.DataFrame({"Close Date": quarter_starts})

## Chart for bold vertical lines at each quarter start
quarter_lines = (
    alt.Chart(quarter_starts_df).mark_rule(
        color="gray",
        strokeWidth=1
    )  # Bold vertical lines, adjust color/strokeWidth as needed
    .encode(x = "Close Date:T")
)

## Chart for 0% horizontal line
y_zero = (
    alt.Chart(pd.DataFrame({'Change':[0]})).mark_rule(
        color = 'black',
        size = 3)
    .encode(y = "Change"))

## Combine the charts
final_chart = alt.layer(base_chart, rule, text, quarter_lines, y_zero)

## Draw a chart
st.altair_chart(
    final_chart,
    #theme = None,
    theme = "streamlit",
    use_container_width = True,
)

#### Summary statistics
### Data pre-proc
df_summary_stat = df.tail(48).describe().loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
df_summary_stat = df_summary_stat.round(2)
df_summary_stat['Robusta Chg'] = df_summary_stat['Robusta Chg'].map('{:.1%}'.format)
df_summary_stat['Arabica Chg'] = df_summary_stat['Arabica Chg'].map('{:.1%}'.format)

### Header
st.header("Coffee tracker summary statistics")
st.write(df_summary_stat[['Robusta', 'Arabica', 'Robusta Chg', 'Arabica Chg']])