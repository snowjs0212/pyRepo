# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:37:55 2024

@author: Joonsoo
"""
#### Packages
import streamlit as st
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

#### Get data
fred = Fred(api_key = fred_api_key)

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
df.index = pd.to_datetime(df.index, format = '%m/%d/%Y').strftime('%Y-%m-%d')
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