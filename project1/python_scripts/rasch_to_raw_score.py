# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:15:50 2019

@author: matcc
"""

import pandas as pd
import numpy as np
from data_manipulation import remove_text
import matplotlib
import matplotlib.pyplot as plt

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

raw_data = pd.read_excel('../Rasch_analysis/Data1_Saudi/raw/Saudi_data.xlsx') 

RUMM_data = pd.read_csv('../Rasch_analysis/Data1_Saudi/rating_questions/all_persons_all_items.csv')

intent = raw_data.loc[:,'Purchase Intent For Usual Laundry Detergent'] 

overall = raw_data.loc[:,'Overall Rating For Usual Laundry Detergent']

#remove text from raw scores

remove_text(intent)
remove_text(overall)

#extract final people in RUMM analysis only
id1 = RUMM_data.loc[:,'personID']
intent = intent[raw_data.loc[:,'Respondent Serial'].isin(id1)]
overall = overall[raw_data.loc[:,'Respondent Serial'].isin(id1)]

#compare overall score with individual item score
items = ['01','02','03','04','05','06','08','09','10','12','13','14','15','16','17']
n = len(items)
fig1,ax = plt.subplots(5,3,figsize=cm2inch(20,25))


xmin=-5.00
xmax=5

i=0
k=-1
while i < n:
    j=0
    k=k+1
    while j < 3:
    #while j < 3:
        ax[k,j].scatter(RUMM_data.loc[:,'I00'+items[i]],overall)
        ax[k,j].set_title('Item '+items[i])
        ax[k,j].set_xlim([xmin,xmax])
        if i != n-1:
            ax[k,j].set_xticks([])
        i=i+1
        j=j+1
        
        
ax[k,1].set_xlabel('Logit score')
ax[2,0].set_ylabel('Purchase intent (raw score)')

