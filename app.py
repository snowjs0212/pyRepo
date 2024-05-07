# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:37:55 2024

@author: Joonsoo
"""
#### Packages
import streamlit as st
import pandas as pd

#### Headers
st.title("Joonsoo's first test on streamlit")
st.text("This is a testing environment to build a better analytics tool in the future.")
st.markdown("**Gayun** is my wife, and she is cute(?).")

#### File import
#uploaded_file = st.file_uploader("Upload your file here.")
#
#if uploaded_file:
#    df = pd.read_csv(uploaded_file)
#    st.write(df.describe())

st.header("LookUp - Imunika coffee research data")
df = pd.read_csv("Imunika_Pilot_Stage1_Final.csv")
st.write(df.describe())

st.header("Data header summary")
st.write(df.head(10))
