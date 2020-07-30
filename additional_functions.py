# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 22:07:14 2020

@author: prabh
"""
## Just a file I made to potentially store additional functions we want to do for 
## statistical analysis if we want


import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv('nba_years_dataset_summer.csv')



def yearAvg(year, stat_cat, topnum):
    yeardata = dataset.loc[dataset["Year"] == year]
    yearstat_highest = yeardata.nlargest(topnum, stat_cat)
    yearstat_mean = yearstat_highest[stat_cat].mean()
    return yearstat_mean
  

# return a dict of stats for any given range of years
def YearlyComparisonTrend(startyear,endyear,statistic, howmany): #get the average of the statistic (column) of interest for every year   
    year_dict={}
    for year in range(startyear,endyear): # loop through every year finding the statistic of every player 
        year_dict[year] = yearAvg(year,statistic,howmany)
    new = pd.DataFrame(year_dict.items(), columns=["Year", statistic])
    plot1= new.plot.line(x="Year", y = statistic)
    # plot1 = plt.plot(new["Year"], new[statistic], color = "blue", marker = "o")
    return plot1

print(YearlyComparisonTrend(1995, 2008, "PTS", 10))
