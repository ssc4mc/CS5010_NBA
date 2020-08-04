# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:10:26 2020

@author: ssc4mc
"""
#import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plot

#Webscrape

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


#Defining Functions

dataset = pd.read_csv('nba_data.csv')

#See stats for a particular player
def PlayerLookup():
     playername = input("Look up a player by player name: ").strip()
     year = input("What year do you want? ").strip()
     player = dataset.loc[(dataset['Player'] == playername) & (dataset['Year'] == int(year)),:]
     return player

#Compare chosen player's average points with the average-aged player of that year
def PlayerComp():
    year = input('what year are you interested in the average nba player? ')
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

#Get average for a given stat in a given year for a given number of top players
def yearAvg(year, stat_cat, topnum):
    yeardata = dataset.loc[dataset["Year"] == year]
    yearstat_highest = yeardata.nlargest(topnum, stat_cat)
    yearstat_mean = yearstat_highest[stat_cat].mean()
    return yearstat_mean
  
# return a dict of stats for any given range of , a given statistic (column), and a given top number of players
def YearlyComparisonTrend(startyear,endyear,statistic, howmany):  
    year_dict={}
    for year in range(startyear,endyear): # loop through every year finding the statistic of every player 
        year_dict[year] = yearAvg(year,statistic,howmany)
    new = pd.DataFrame(year_dict.items(), columns=["Year", statistic])
    plot1= new.plot.line(x="Year", y = statistic, title = statistic + " between " + str(startyear) + "-" + str(endyear))
    return plot1

#access player without using user input
def return_player(player):
     player = dataset.loc[(dataset['Player'] == player)]
     player = pd.DataFrame(player)
     return player
 
#Testing some functions
# =============================================================================
# print(YearlyComparisonTrend(1995, 2008, "PTS", 10))
# 
# PlayerLookup()
# 
# PlayerComp()
# 
# yearAvg(2020,"PTS",10)
# =============================================================================


# Results
'''
Who’s the best player in NBA history in terms of statistics (not including wins, championships, and MVPS? 
Jordan (1984 - 2003) vs Lebron (2003-2020)
'''

MJ = return_player('Michael Jordan*')
MJ_avg = np.mean(MJ)
MJ_avg

LBJ = return_player('LeBron James')
LBJ_avg = np.mean(LBJ)
LBJ_avg

comparison_df = pd.DataFrame({"x":LBJ_avg, "y":MJ_avg})
comparisons_LBJ_MJ = comparison_df['x'] > comparison_df['y']
comparisons_LBJ_MJ = comparisons_LBJ_MJ.drop(labels=['Age', 'G', 'GS', 'FGA', '3PA', '2PA', 'FTA', 'TOV', 'PF', 'Year'])
comparisons_LBJ_MJ

i = 0 
a = 0 
for element in comparisons_LBJ_MJ:
    if element == True:
        i += 1
        print('LBJ advantage' )
    else:
        print('MJ advntage')
        a += 1
print()
print(f"LBJ advantages: {i}")
print(f"MJ advantages: {a}")


'''
Comparing each player's points to the average player in the median year of their career
'''
#1992 for MJ and 2002 for LBJ
PlayerComp()


'''
How has basketball changed in terms of various statistics that define the sport?
Is it as physical? 
Trend of 3 point field goals and 2 point field goals and how they have changed over the years
'''
YearlyComparisonTrend(1980, 2020, "3P", 100)
YearlyComparisonTrend(1980, 2020, "3P%", 100)

YearlyComparisonTrend(1980, 2020, "2P", 100)
YearlyComparisonTrend(1980, 2020, "2P%", 100)

YearlyComparisonTrend(1980, 2020, "PF", 100)


'''
Are players generally better?
Trend of FG percentage and points and how that has changed over the years
'''

YearlyComparisonTrend(1980, 2020, "FG%", 100)

YearlyComparisonTrend(1980, 2020, "PTS", 100)



#Legend
'''
Also view explanations by holding mouse over column headers
Rk -- Rank
Pos -- Position
Age -- Player's age on February 1 of the season
Tm -- Team
G -- Games
GS -- Games Started
MP -- Minutes Played Per Game
FG -- Field Goals Per Game
FGA -- Field Goal Attempts Per Game
FG% -- Field Goal Percentage
3P -- 3-Point Field Goals Per Game
3PA -- 3-Point Field Goal Attempts Per Game
3P% -- 3-Point Field Goal Percentage
2P -- 2-Point Field Goals Per Game
2PA -- 2-Point Field Goal Attempts Per Game
2P% -- 2-Point Field Goal Percentage
eFG% -- Effective Field Goal Percentage
This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal.
FT -- Free Throws Per Game
FTA -- Free Throw Attempts Per Game
FT% -- Free Throw Percentage
ORB -- Offensive Rebounds Per Game
DRB -- Defensive Rebounds Per Game
TRB -- Total Rebounds Per Game
AST -- Assists Per Game
STL -- Steals Per Game
BLK -- Blocks Per Game
TOV -- Turnovers Per Game
PF -- Personal Fouls Per Game
PTS -- Points Per Game

'''
    

'''
REFERENCES:
1) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pt3)
2) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/ (Pr4)
3) https://pythontic.com/pandas/dataframe-plotting/bar%20chart
4) https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
'''
