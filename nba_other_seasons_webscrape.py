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


#1980 is the first year that all columns have stats recorded
#so we'll start our loop at the year 1980 and finish at 2019 since we already have 2020

for year in range(2020,1980,-1):
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
    stats.to_csv('nba_years_dataset_summer.csv', mode='a', index=False, header=False)
    print(year, "done")


dataset = pd.read_csv('nba_years_dataset_summer.csv')

def PlayerLookup(playername):
    dataset.loc[dataset['Player'] == playername,:]
    player = (dataset.loc[dataset['Player'] == playername,:])
    return player

def user_input_lookup():
    x = input('Player Name?')
    dataset.loc[dataset['Player'] == x,:]
    player = (dataset.loc[dataset['Player'] == x,:])
    return player
    
    
def PlayerComp(playername):
    avg_age = dataset['Age'].mean()
    avg_pts = round(dataset['PTS'].mean(),2)
    player = PlayerLookup(playername)
    avg_nba = pd.DataFrame().reindex_like(player)
    avg_nba['Age'] = avg_age
    avg_nba['PTS']= avg_pts
    avg_nba['Player'] = 'Avg Player'
    comp = pd.concat([player, avg_nba])
    comp_plot = comp.plot.bar(x="Age", y="PTS", rot=70, title =  playername + " vs Avg Nba")
    return comp_plot


#Installed User Input
user_input_lookup()

#MVP'S
Lebron = PlayerLookup('LeBron James')
MJ  = PlayerLookup('Michael Jordan*')
Giannis = PlayerLookup('Giannis Antetokounmpo')




'''
REFERENCES:
1) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pt3)
2) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pr4)
3) https://pythontic.com/pandas/dataframe-plotting/bar%20chart
4) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
'''

