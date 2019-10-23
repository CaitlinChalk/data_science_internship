# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:47:22 2019

@author: matcc
"""

import pandas as pd
import numpy as np

data = pd.read_excel('../data/Data1_saudi/residuals_analysis_usual_brands.xlsx') #read raw data

n_items = 6
n_facets = 10

res_facet1 = data.iloc[0:n_items,1:n_items+1]
res_facet1 = res_facet1.astype(float)
av_res = np.nanmean(res_facet1)
dep_items = res_facet1[res_facet1[:] > 0.2*av_res]
dep_items.replace(np.diagonal(dep_items),np.nan, inplace=True) #replace matrix diagonals (which correspond to items residual with itself) to NaN

#%%

#dependencies = dep_items.copy()
for i in range(n_items):
    item = dep_items.iloc[:,i][np.isnan(dep_items.iloc[:,i]) == False] # non-NaN elements (corresponding to correlated items)
    deps = item.index #index of non-NaN elements
    n_deps = len(deps)
    #dep_items.iloc[:,i].replace(pd.Series(item).values,pd.Series(deps).values+1, inplace=True)
    Series1 = pd.DataFrame(data = deps+1,columns=[i])    #dependencies.iloc[i,deps[j]] = i+1
    if i == 0:
        dependencies = Series1
    else:
        dependencies = pd.concat([dependencies,Series1],axis=1) 
 #%%   
dependencies2 = dependencies.copy()
for i in range(len(dependencies2.columns)): #each column = number of items
    col1 = dependencies2.loc[:,i]
    x = col1.notna().sum() #number of non-NaN values in column
    k=0
    #item = dep_items.iloc[:,i][np.isnan(dep_items.iloc[:,i]) == False] 
    if x > 0:
        for j in range (x):
            val = col1.iloc[j]
            col2 = dependencies2.loc[:,int(val-1)]
            next_row = col2.notna().idxmin() #next non-NaN location in row
            if next_row + 1 == len(col2):
                dependencies2 = dependencies2.append(pd.DataFrame([np.nan]), ignore_index=True)
                next_row = next_row+1
            dependencies2.iloc[int(next_row),int(val-1)] = i+1
     
        #%%
        
for i in range(n_items):
    dependencies2.rename(columns={i: i+1}, inplace=True)
           # if k == 0:
           #     dep_items2 = dep_col
           # else:
           #     dep_items2 = pd.concat([dep_items2,dep_col],axis=1)
           # k=k+1
#ADD LINE TO CHECK IF NUMBER ISN'T ALREADY IN!!

#j = SERIES.notna().idxmin()


    #pd.concat([output_key,Series0], axis=1)
    #dependencies.iloc[:,i] = 
    




#res_facet1.replace(np.nan,-1,inplace=True) 