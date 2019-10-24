# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:32:55 2019
Script to analyse individual person fit within the Rasch model.
Input is the inidividual person fit table from RUMM2030.
@author: matcc
"""

import pandas as pd
import numpy as np

data = pd.read_excel('../data/Data1_saudi/usual15_persons.xlsx') #individual person fit data

#column indicating extreme people
extremes = data.loc[:,'Extm']

#ID of extreme persons
extreme_index = extremes[extremes=='extm'].index #index of extreme persons
extreme_ID = data.loc[extreme_index,'Unnamed: 10'] 
n_extremes = len(extreme_ID)