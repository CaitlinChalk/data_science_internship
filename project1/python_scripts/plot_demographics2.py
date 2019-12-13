# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:51:27 2019

@author: matcc
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

data1 = pd.read_excel('../Rasch_analysis/Data1_Saudi/ratings_PFs2.xlsx') #read raw data
data2 = pd.read_excel('../Rasch_analysis/Data1_Saudi/agreements_PFs2.xlsx') #read raw data

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
#%% products
        
data1 = pd.read_excel('../Rasch_analysis/Data1_Saudi/ratings_products.xlsx') #read raw data
data2 = pd.read_excel('../Rasch_analysis/Data1_Saudi/agreements_products.xlsx') #read raw data    

location1 = data1.Location
location2 = data2.Location

rating_data = []
agreement_data = []
#for i in range(10):
#    rating_data.append(location1[data1.iloc[:,-1]==i])
#    agreement_data.append(location2[data2.iloc[:,-1]==i])

rating_data.append(location1[data1.iloc[:,-1].isin([0,1])])
agreement_data.append(location1[data2.iloc[:,-1].isin([0,1])])
rating_data.append(location1[data1.iloc[:,-1].isin([7])])
agreement_data.append(location1[data2.iloc[:,-1].isin([7])])
rating_data.append(location1[data1.iloc[:,-1].isin([8])])
agreement_data.append(location1[data2.iloc[:,-1].isin([8])])
    
fig1,ax = plt.subplots(1,2,figsize=cm2inch(19,12))
ax[0].boxplot(rating_data)
ax[1].boxplot(agreement_data)

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Person location')
ax[0].set_xlabel('Product')
ax[1].set_xlabel('Product')

ax[0].set_xticklabels(['1 and 2', '8', '9'])
ax[1].set_xticklabels(['1 and 2', '8', '9'])
ax[1].set_yticks([])

figname = 'product_box2'
matplotlib.rc('font', **font)

#plt.savefig('Figures/'+figname+'.pdf')
#plt.savefig('Figures/'+figname+'.jpg')
    


#%% nationality
#ratings
location = data1.Location
PF = 'PF_noChildren'

data_rating = []

data_rating.append(location[data1.loc[:,PF].isin([1])]) #none 
data_rating.append(location[data1.loc[:,PF].isin([2])]) #one 
data_rating.append(location[data1.loc[:,PF].isin([3])]) #two 
data_rating.append(location[data1.loc[:,PF].isin([0])]) #3 plus 

#agreements
location = data2.Location
data_agreement = []

data_agreement.append(location[data2.loc[:,PF].isin([1])]) #none 
data_agreement.append(location[data2.loc[:,PF].isin([2])]) #one 
data_agreement.append(location[data2.loc[:,PF].isin([3])]) #two 
data_agreement.append(location[data2.loc[:,PF].isin([0])]) #3 plus
#box plot

fig1,ax = plt.subplots(1,2,figsize=cm2inch(19,12))
ax[0].boxplot(data_rating)
ax[1].boxplot(data_agreement)

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Person location')

labels = ['None\n(128)', 'One\n(176)', 'Two\n(246)', 'Three plus\n(162)']
labels2 = ['None\n(133)', 'One\n(168)', 'Two\n(248)', 'Three plus\n(180)']
ax[1].set_yticks([])
ax[0].set_xticklabels(labels)
ax[1].set_xticklabels(labels2)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}

figname = 'nochildren_box'
matplotlib.rc('font', **font)

#plt.savefig('Figures/'+figname+'.pdf')
#plt.savefig('Figures/'+figname+'.jpg')

#%% employment
#ratings
location = data1.Location
PF = 'PF_emplymnt'

data_rating = []

data_rating.append(location[data1.loc[:,PF].isin([0])]) #full time
data_rating.append(location[data1.loc[:,PF].isin([2])]) #parent
data_rating.append(location[data1.loc[:,PF].isin([4])]) #unemployed

#agreements
location = data2.Location
data_agreement = []

data_agreement.append(location[data2.loc[:,PF].isin([0])]) #none 
data_agreement.append(location[data2.loc[:,PF].isin([2])]) #one 
data_agreement.append(location[data2.loc[:,PF].isin([4])]) #two 

#box plot

fig1,ax = plt.subplots(1,2,figsize=cm2inch(19,12))
ax[0].boxplot(data_rating)
ax[1].boxplot(data_agreement)

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Person location')

labels = ['Full time \n(214)', 'Unemployed\n(131)', 'Parent\n(194)']
labels2 = ['Full time \n(235)', 'Unemployed\n(125)', 'Parent\n(185)']
ax[1].set_yticks([])
ax[0].set_xticklabels(labels)
ax[1].set_xticklabels(labels2)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}

figname = 'employment_box'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')




