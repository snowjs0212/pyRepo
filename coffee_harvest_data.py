# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:55:30 2024

@author: Joonsoo
"""
from owid import catalog

# look for Covid-19 data, return a data frame of matches
catalog.find('covid')