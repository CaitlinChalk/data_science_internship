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

data = pd.read_excel('../data/Data1_saudi/residuals_analysis_usual_brands.xlsx') #read raw data (use read_csv if necessary)

n_items = 6 #number of items
n_facets = 10 #number of facets

res_facet1 = data.iloc[0:n_items,1:n_items+1] #matrix of item correlation resididuals
res_facet1 = res_facet1.astype(float) #convert to float
res_facet1.replace(np.diagonal(res_facet1),np.nan, inplace=True) #replace matrix diagonals (which correspond to items residual with itself) to NaN
av_res = np.nanmean(res_facet1) #average residual value excluding NaNs
dep_items = res_facet1[res_facet1[:] > 0.2 + av_res] #dependent items approximated as having residual correlations > 0.2 + average residual
#dep_items = dataframe displaying correlation residuals of dependent items only 

#%% display list of dependent items in dataframe, where each column corresponds to each item

for i in range(n_items): #loop through each item
    item = dep_items.iloc[:,i][np.isnan(dep_items.iloc[:,i]) == False] # non-NaN elements (corresponding to correlated items)
    deps = item.index #index of non-NaN elements
    Series1 = pd.DataFrame(data = deps+1,columns=[i]) #items that are dependent to item i (listen in column i-1)
    if i == 0:
        dependencies = Series1
    else:
        dependencies = pd.concat([dependencies,Series1],axis=1) 
        
# add dependent items to both columns in dataframe (e.g. if item 1 has dependence on item 2, add item 1 to the column for item 2)  
for i in range(len(dependencies.columns)): #each column = number of items
    col1 = dependencies.loc[:,i]
    x = col1.notna().sum() #number of non-NaN values in column
    if x > 0: #if there are dependent items in column
        for j in range (x):
            val = col1.iloc[j] #dependent item
            col2 = dependencies.loc[:,int(val-1)] #corresponding column for that item
            next_row = col2.notna().idxmin() #next non-NaN location in row
            if next_row + 1 == len(col2): #if there is no non-NaN element after value
                dependencies = dependencies.append(pd.DataFrame([np.nan])) #add row of NaNs, so that existing values aren't written over
                next_row = next_row+1 #increase row index to avoid replacing existing items
            dependencies.iloc[int(next_row),int(val-1)] = i+1 #add dependent item to correct column

#rename columns to correspond with item number        
for i in range(n_items):
    dependencies.columns.values[i] = str(i+1)

#dependencies = dataframe where each column corresponds to each item, with the elements denoting the other items that share dependence with that one