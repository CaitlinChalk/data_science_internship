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
        #PFs_new.loc[:,PF_names[j]] = PFs_new.loc[:,PF_names[j]].astype(int)

    #return PFs_new
    