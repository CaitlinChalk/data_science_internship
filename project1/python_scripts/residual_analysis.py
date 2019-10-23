# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:47:22 2019
script to read in item residuals, output from RUMM as an excel or csv file
outputs matrix listing dependent items 
for multi-facet analysis, specify the facet of interest 
@author: matcc
"""

import pandas as pd
import numpy as np

data = pd.read_excel('../data/Data1_saudi/residuals_analysis_usual_brands.xlsx') #read raw data (use read_csv or read_excel accordingly)

n_items = 6 #number of items
n_facets = 10 #number of facets

facet = 2 #facet of interest

res_facet1 = data.iloc[(facet-1)*n_items:facet*n_items,1+(facet-1)*n_items:1+facet*n_items] #matrix of item correlation resididuals
res_facet1 = res_facet1.astype(float) #convert to float
res_facet1.replace(np.diagonal(res_facet1),np.nan, inplace=True) #replace matrix diagonals (which correspond to items residual with itself) to NaN
av_res = np.nanmean(res_facet1) #average residual value excluding NaNs
extrm_correlations = res_facet1[res_facet1[:] > 0.2 + av_res] #dependent items approximated as having residual correlations > 0.2 + average residual
#extrm_correlations = dataframe displaying correlation residuals of dependent items only 

#%% display list of dependent items in dataframe, where each column corresponds to each item

for i in range(n_items): #loop through each item
    item = extrm_correlations.iloc[:,i][np.isnan(extrm_correlations.iloc[:,i]) == False] # non-NaN elements (corresponding to correlated items)
    deps = item.index #index of non-NaN elements
    Series1 = pd.DataFrame(data = deps+1,columns=[i]) #items that are dependent to item i (listen in column i-1)
    if i == 0:
        dependent_items = Series1
    else:
        dependent_items = pd.concat([dependent_items,Series1],axis=1) 
        
#%% add dependent items to both columns in dataframe (e.g. if item 1 (column 1) has dependence on item 2 (column 2), add item 1 to the column for item 2)  
for i in range(n_items): #each column = number of items
    col1 = dependent_items.loc[:,i]
    x = col1.notna().sum() #number of non-NaN values in column 1
    if x > 0: #if there are dependent items in column 1
        for j in range (x): #go through all dependent items in column 1, and add the item value of that column to the others
            val = col1.iloc[j] #corresponding dependent items
            col2 = dependent_items.iloc[:,int(val-1)] #corresponding column for that item
            if col2.isin([i+1]).sum() > 0: #if item 1 is already in item 2, don't add it twice
                break
            if col2.isna().sum() > 0: #if there are NaNs in column2
                next_row = col2.notna().idxmin() #find next non-NaN location in row
            else: #if column already has other dependent items listed
           # if next_row + 1 == len(col2): #if there is no non-NaN element after value
                dependent_items = dependent_items.append(pd.DataFrame([np.nan])) #add row of NaNs, so that existing values aren't written over
                next_row = next_row+1 #increase row index to avoid replacing existing items
            dependent_items.iloc[int(next_row),int(val-1)] = i+1 #add dependent item to correct column

#renumber columns to correspond with item number        
for i in range(n_items):
    dependent_items.columns.values[i] = str(i+1)

#dependent_items = dataframe where each column corresponds to each item, with the elements denoting the other items that share dependence with that one