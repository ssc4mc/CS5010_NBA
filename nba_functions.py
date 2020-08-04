# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 22:04:37 2020

@author: prabh
"""

import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot


dataset = pd.read_csv('nba_data.csv')


def PlayerLookup(playername, year):
      player = dataset.loc[(dataset['Player'] == playername) & (dataset['Year'] == int(year)),:]
      return player
PlayerLookup("LeBron James", 2012)
    
def PlayerCompLookup(playername, year): #playercomp cant write, just check if age is actually in the dataframe 
    chosen_year = dataset.loc[dataset["Year"] == int(year)]
    mean_for_age = chosen_year["Age"].mean()
    avg_pts = round(chosen_year["PTS"].mean(),2)
    player = PlayerLookup(playername, year)
    avg_nba = pd.DataFrame().reindex_like(player)
    avg_nba['Age'] = mean_for_age
    avg_nba['PTS']= avg_pts
    avg_nba['Player'] = 'Avg Player'
    comp = pd.concat([player, avg_nba])
    comp_plot = comp.plot.bar(x="Age", y="PTS", rot=70, title =  "Chosen player (left)  vs Avg Nba(right)")
    return comp_plot


def yearAvg(year, stat_cat, topnum):
    yeardata = dataset.loc[dataset["Year"] == year]
    yearstat_highest = yeardata.nlargest(topnum, stat_cat)
    yearstat_mean = yearstat_highest[stat_cat].mean()
    return yearstat_mean



# return a dict of stats for any given range of years
def YearlyComparisonTrend(startyear,endyear,statistic, howmany): #get the average of the statistic (column) of interest for every year   #top however many players 
    year_dict={}
    for year in range(startyear,endyear): # loop through every year finding the statistic of every player 
        year_dict[year] = yearAvg(year,statistic,howmany)
    new = pd.DataFrame(year_dict.items(), columns=["Year", statistic])
    plot1= new.plot.line(x="Year", y = statistic, title = statistic + " between " + str(startyear) + "-" + str(endyear))
    # plot1 = plt.plot(new["Year"], new[statistic], color = "blue", marker = "o")
    return plot1



#  #the specific year then the method will be called
# player1=PlayerLookup("LeBron James" , 2010)
# player1.iloc[1]


# BELOW ARE USER INPUT VARIATION OF PLAYER LOOKUP
##################################################
# =============================================================================
# def PlayerLookup():
#       playername = input("Look up a player by player name:")
#       year = int(input("What year do you want?"))
#       player = dataset.loc[(dataset['Player'] == playername) & (dataset['Year'] == int(year)),:]
#       print (player)
#       return player
#   #did the name input get stored in the playername, same for year as a 2020, 
#    
# 
# #PlayerLookup()
#     
# def PlayerCompLookup(): #playercomp cant write, just check if age is actually in the dataframe 
#     chosen_year = dataset.loc[dataset["Year"] == int(year)]
#     mean_for_age = chosen_year["Age"].mean()
#     avg_pts = round(chosen_year["PTS"].mean(),2)
#     player = PlayerLookup()
#     avg_nba = pd.DataFrame().reindex_like(player)
#     avg_nba['Age'] = mean_for_age
#     avg_nba['PTS']= avg_pts
#     avg_nba['Player'] = 'Avg Player'
#     comp = pd.concat([player, avg_nba])
#     comp_plot = comp.plot.bar(x="Age", y="PTS", rot=70, title =  "Chosen player (left)  vs Avg Nba(right)")
#     return comp_plot
# =============================================================================
