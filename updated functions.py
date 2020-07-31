#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:57:39 2020

@author: vasudhamanikandan
"""
import pandas as pd


stats = pd.read_csv("nba_years_dataset_summer.csv")

avg_age = stats.groupby('Year')['Age'].mean()
avg_pts = stats['PTS'].mean()
avg_mins = stats['MP'].mean()
avg_ast = stats['AST'].mean()

def PlayerLookup():
     playername = input("Look up a player by player name:")
     year = input("What year do you want?")
     player = stats.loc[(stats['Player'] == playername) & (stats['Year'] == int(year)),:]
     return player
    
    
def PlayerComp():
    chosen_year = stats.loc[stats["Year"] == int(year)]
    mean_for_age = chosen_year["Age"].mean()
    avg_pts = round(chosen_year["PTS"].mean(),2)
    player = PlayerLookup()
    avg_nba = pd.DataFrame().reindex_like(player)
    avg_nba['Age'] = mean_for_age
    avg_nba['PTS']= avg_pts
    avg_nba['Player'] = 'Avg Player'
    comp = pd.concat([player, avg_nba])
    comp_plot = comp.plot.bar(x="Age", y="PTS", rot=70, title =  playername + " vs Avg Nba")
    return comp_plot


def yearAvg(year, stat_cat, topnum):
    yeardata = stats.loc[stats["Year"] == year]
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

print(YearlyComparisonTrend(1995, 2008, "PTS", 10))


    