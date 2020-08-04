# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:10:48 2020

@author: Latifa H
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest
from nba_functions import *
import math

# =============================================================================

# =============================================================================
class PlayerLookupTest(unittest.TestCase):
    
    def test_is_player_correct(self):
        #print statement that prints to the console, type in the name explicitly, only type 
        #the specific year then the method will be called
        player1=PlayerLookup("LeBron James" , 2010)
        self.assertEqual(player1["Player"].iloc[0], "LeBron James") 
        #should return the correct stats for specified player from specified year

    def test_is_age_correct(self):       
        player1=PlayerLookup("LeBron James" , 2012)
        self.assertEqual(player1["Age"].iloc[0], 27) # age changes on yearly basis
    
    def test_is_pos_correct(self):       
        player1=PlayerLookup("LeBron James" , 2012)
        self.assertEqual(player1["Pos"].iloc[0], "SF") #check if it returns the correct 
        #player position from any specified year for the given player

if __name__ == '__main__':
    unittest.main()


class yearAvgtests(unittest.TestCase):
    
    def test_correct_year_mean_oneplayer(self): 
        # check if the mean is calculated properly
        year1 = yearAvg(2005,"PTS", 1) # set by calling function
        self.assertEqual(year1, 30.7) 
        # leading scorer in 2005 was Allen Iverson who had an avg 30.7 points per game
    
    def test_correct_year_morethanone(self): 
        # check if the mean is calculated properly
        year1 = yearAvg(2005,"PTS", 2) # set by calling function
        self.assertEqual(year1, 29.15) # manually calculated mean of top 2 point scoreres in 2005, check if values are same

    
    def test_correct_year_morethanone(self): 
        # check if the mean is calculated properly when 0 players
        year1 = yearAvg(2005,"PTS", 0) # set by calling function
        self.assertTrue(math.isnan(year1)) # there should be nan returned - "not a number"


if __name__ == '__main__':
    unittest.main()

     
      