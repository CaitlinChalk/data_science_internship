# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:32:55 2019
Script to analyse individual person fit within the Rasch model.
Input is the inidividual person fit table from RUMM2030.
@author: matcc
"""

import pandas as pd
import numpy as np
from data_manipulation import ammend_facet_key

data = pd.read_excel('../data/Data1_saudi/facet7_extreme_persons.xlsx') #individual person fit data

#column indicating extreme people
extremes = data.loc[:,'Extm']

#ID of extreme persons
extreme_index = extremes[extremes=='extm'].index #index of extreme persons
extreme_persons = extreme_index.values+1

#extreme_ID = data.loc[extreme_index,'Unnamed: 10'] #extreme person IDs
#extreme_ID_index = extreme_ID.index #index of extreme person IDs
#extreme_ID.sort_values(inplace=True) #put in ascending order
#n_extremes = len(extreme_ID) #number of extreme persons

#facet_new, extreme_facets = ammend_facet_key(facets_RUMM,facets_key,extreme_ID)

#%%

facet = 7
facetID = facets_RUMM[facets_RUMM==facet-1] #.index
persons = facetID.index.values+1
#PID = pd.Series(data=facetID.index.values+1)
#persons = data.loc[extreme_index,'Unnamed: 10'] 

        

