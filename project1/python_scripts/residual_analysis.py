# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:47:22 2019

@author: matcc
"""

import pandas as pd
import numpy as np

data = pd.read_csv('../data/Data1_saudi/residuals_analysis1.csv') #read raw data

n_items = 18
n_facets = 10

res_facet1 = data.iloc[0:n_items,1:n_items+1]
res_facet1 = res_facet1.astype(float)
av_res = np.nanmean(res_facet1)
dep_items = res_facet1[res_facet1[:] > 0.2*av_res]

dependencies = pd.DataFrame(np.nan, index=range(1,n_items), columns=range(1,n_items))
for i in range(n_items):
    item = dep_items.iloc[:,i][np.isnan(dep_items.iloc[:,i]) == False]
    deps = item.index 
    n_deps = len(deps)
    #for j in range(n_deps):
     #   dependencies.iloc[j,i] = deps[j]+1
    Series1 = pd.DataFrame(data = deps+1, columns = [i+1])    #dependencies.iloc[i,deps[j]] = i+1
    if i == 0:
        dependencies = Series1
    else:
        dependencies = pd.concat([dependencies,Series1],axis=1) 
    
for i in range(len(dependencies.columns)):
    col1 = dependencies.iloc[:,i]
    x = col1.notna().sum()
    if x > 0:
        for j in range (x):
            val = col1.iloc[j]
            col2 = dependencies.iloc[:,int(val-1)]
            next_row = col2.notna().idxmin()
            dependencies.iloc[int(next_row),int(val-1)] = i+1

#ADD LINE TO CHECK IF NUMBER ISN'T ALREADY IN!!

#j = SERIES.notna().idxmin()


    #pd.concat([output_key,Series0], axis=1)
    #dependencies.iloc[:,i] = 
    




#res_facet1.replace(np.nan,-1,inplace=True) 