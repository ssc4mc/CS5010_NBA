# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:10:26 2020

@author: ssc4mc
"""
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

#os.chdir("C:\\users\\student\\Desktop\\CS5010\\Natty_Champs")

# =============================================================================
# url1980 = "https://www.basketball-reference.com/leagues/NBA_1980_per_game.html"
# 
# url2020 = "https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
# =============================================================================

url = f"https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"

html = urlopen(url)

soup = BeautifulSoup(html, features= "lxml")

# use findALL() to get the column headers
soup.findAll('tr', limit=2)

# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]

# avoid the first header row
rows = soup.findAll('tr')[2:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

#Official Data set
stats = pd.DataFrame(player_stats, columns = headers)
stats = stats.astype(str)
stats = stats.mask(stats.eq('None')).dropna()
stats['Age'] = stats['Age'].astype(int)
stats['PTS'] = stats['PTS'].astype(float)
stats['MP'] = stats['MP'].astype(float)
stats['AST'] = stats['AST'].astype(float)
    
#Add Year column to dataset, populate with year
stats["Year"] = 2020

#Average Player:
avg_age = stats['Age'].mean()
avg_pts = stats['PTS'].mean()
avg_mins = stats['MP'].mean()
avg_ast = stats['AST'].mean()
    

#create csv
stats.to_csv('nba_data.csv', mode='w', index=False, header=True)
print('2020 csv created')

#1980 is the first year that all columns have stats recorded
#so we'll start our loop at the year 2019 since we already have 202 and go all the way back to 1980 

for year in range(2019,1979,-1):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"

    html = urlopen(url)

    soup = BeautifulSoup(html, features= "lxml")

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)

    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]


    # avoid the first header row
    rows = soup.findAll('tr')[2:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

    #Official Data set
    stats = pd.DataFrame(player_stats, columns = headers)
    stats = stats.astype(str)
    stats = stats.mask(stats.eq('None')).dropna()
    stats['Age'] = stats['Age'].astype(int)
    stats['PTS'] = stats['PTS'].astype(float)
    stats['MP'] = stats['MP'].astype(float)
    stats['AST'] = stats['AST'].astype(float)
    
    #Add Year column to dataset, populate with year
    #just realized I'm not sure if these years are integers
    stats["Year"] = year

    #Average Player:
    avg_age = stats['Age'].mean()
    avg_pts = stats['PTS'].mean()
    avg_mins = stats['MP'].mean()
    avg_ast = stats['AST'].mean()
    
    
    #append these stats to existing csv file, no headers needed
    stats.to_csv('nba_data.csv', mode='a', index=False, header=False)
    print(year, "done")


dataset = pd.read_csv('nba_data.csv')

def PlayerLookup():
     playername = input("Look up a player by player name:")
     year = input("What year do you want?")
     player = dataset.loc[(dataset['Player'] == playername) & (dataset['Year'] == int(year)),:]
     return player
    
    
def PlayerComp():
    chosen_year = dataset.loc[dataset["Year"] == int(year)]
    mean_for_age = chosen_year["Age"].mean()
    avg_pts = round(chosen_year["PTS"].mean(),2)
    player = PlayerLookup()
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

print(YearlyComparisonTrend(1995, 2008, "PTS", 10))

PlayerLookup()

PlayerComp()

yearAvg(2020,"PTS",10)
    

# Results
'''
Who’s the best player in NBA history in terms of statistics (not including wins, championships, and MVPS? 
Jordan (1984 - 2003) vs Lebron (2003-2020)
Player Statistics of Lebron vs Jordan (query 1 - via PlayerLookup)
Comparison of how well they did verse the league averages of the year(s) they played basketball (query 2 - via PlayerComp)
'''
PlayerLookup()

'''
How has basketball changed in terms of various statistics that define the sport?
Is it as physical? 
Trend of 3 point field goals and 2 point field goals and how they have changed over the years (via YearlyComparisonTrend)
Are players generally better
Trend of FG percentage and points and how that has changed over the years (via YearlyCompariosonTrend)
'''






'''
REFERENCES:
1) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pt3)
2) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pr4)
3) https://pythontic.com/pandas/dataframe-plotting/bar%20chart
4) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
'''
