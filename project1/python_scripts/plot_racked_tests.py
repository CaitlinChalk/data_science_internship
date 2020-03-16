# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 16:49:26 2020

@author: matcc
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

os.chdir("C:\\Users\\matcc\\LIDA_internship\\project1\\python_scripts")

data = pd.read_excel('../Data2_Shaving/racked_tests/tests1_3_2facet.xls')

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
#racked data
        
items = data['Tests1-3']
 

#%%
    
    #plot item locations between shaves (for 2 shaves)
fig = plt.figure(figsize=cm2inch(15,15))
ax = plt.axes()
xitems = np.array(range(10))
yitems = np.array(range(10,20))
  
X = items[xitems]
Y = items[yitems]
ax.plot(X,Y,'.',MarkerSize=3,color='red')      
xmin = items.min()-0.2
xmax = items.max()+0.2
xy = np.linspace(xmin,xmax,100) 
ax.plot(xy,xy,'--',color='red',linewidth=1)
#ax.set_xticks([])
#ax.set_yticks([])
#ax[k,l].tick_params(axis="y",labelsize=8)
ax.set_xlim([xmin,xmax])
ax.set_ylim([xmin,xmax])
#ax[k,l].set_title('Shaves ' + str(i+1) +' and ' + str(i+2),FontSize=16)
for j, label in enumerate(xitems+1):
    ax.annotate(label, (X.iloc[j],Y.iloc[j]+0.05),FontSize=16)
    
ax.set_xlabel('Item difficulty at Test 1 (logits)',FontSize=14)
ax.set_ylabel('Item difficulty at Test 3 (logits)',FontSize=14)
    
plt.tight_layout()
figname = 'racked_tests_1_3_2facet'
plt.savefig('Figures2/'+figname+'.pdf')
plt.savefig('Figures2/'+figname+'.jpg')











