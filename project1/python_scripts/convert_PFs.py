# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:12:25 2019

@author: matcc
function to convert Person Factor data into format required for RUMM input 
"""

import numpy as np
import pandas as pd

def convert_PFs (PFs_old,PFs_new):    
    PF_names = PFs_old.columns
    n = len(PF_names)
    for j in range(n):
        PF_item = PFs_old.loc[:,PF_names[j]]
        PF_list = np.unique(PF_item)   
        PF_list = PF_list[~pd.isnull(PF_list)]
        PF_dict = {}
        for i in range(len(PF_list)):
            PF_dict[i] = {PF_list[i]: i}
            PFs_new.loc[:,PF_names[j]].replace(PF_dict[i], inplace=True)

def convert_facets (facets_old,facets_new)
    facet_list = np.unique(facets_old) #count number of distinct facets
    facet_dict = {}
    for i in range(len(facet_list)):
        facets_dict[i] = {facet_list[i]: i}
        facets_new.replace(facet_dict[i], inplace=True)    