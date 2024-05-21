# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:37:55 2024

@author: Joonsoo
"""
#### Packages
import streamlit as st
import pandas as pd
import os

print(st.__version__)

#### Headers
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