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

os.chdir("M:\LIDA_internship\project1\python_scripts")

data = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves1_2.xlsx') #read raw data
dataA = pd.read_excel('../Data2_Shaving/racked/results_1_2.xls',header=None)
dataB = pd.read_excel('../Data2_Shaving/racked/results_2_3.xls',header=None)
dataC = pd.read_excel('../Data2_Shaving/racked/results_3_4.xls',header=None)
dataD = pd.read_excel('../Data2_Shaving/racked/results_4_5.xls',header=None)
dataE = pd.read_excel('../Data2_Shaving/racked/results_5_6.xls',header=None)
dataF = pd.read_excel('../Data2_Shaving/racked/results_6_7.xls',header=None)
dataG = pd.read_excel('../Data2_Shaving/racked/results_7_8.xls',header=None)
dataH = pd.read_excel('../Data2_Shaving/racked/results_8_9.xls',header=None)
dataI = pd.read_excel('../Data2_Shaving/racked/results_9_10.xls',header=None)
dataJ = pd.read_excel('../Data2_Shaving/racked/results_2_10.xls',header=None)

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
#%%stacked or anchored data
        
#list data files
#data = [dataA,dataB,dataC,dataD,dataE,dataF,dataG,dataH,dataI]     
data = [dataJ]

no_shaves = len(data)

products = {name: pd.DataFrame for name in range(no_shaves)}
items = {name: pd.DataFrame for name in range(no_shaves)}

for i in range(no_shaves): 
    items[i] = data[i].iloc[:,2]
    products[i] = data[i].iloc[:,6:7]
    items[i] = items[i].sort_values()
 
#%%

#plot item locations between shaves (for multiple shaves)
fig,ax = plt.subplots(3,3,figsize=cm2inch(25,18))
xitems = np.array(range(10))
yitems = np.array(range(10,20))
l=0
k=0
for i in range(no_shaves):     
    X = items[i][xitems]
    Y = items[i][yitems]
    ax[k,l].plot(X,Y,'.',MarkerSize=2,color='black')      
    xmin = items[i].min()-0.2
    xmax = items[i].max()+0.2
    xy = np.linspace(xmin,xmax,100) 
    ax[k,l].plot(xy,xy,'--',color='red',linewidth=1)
    ax[k,l].set_xticks([])
    ax[k,l].set_yticks([])
    ax[k,l].tick_params(axis="y",labelsize=8)
   # ax[k,l].set_xlim([xmin,xmax])
   # ax[k,l].set_ylim([xmin,xmax])
    ax[k,l].set_title('Shaves ' + str(i+1) +' and ' + str(i+2),FontSize=16)
    for j, label in enumerate(xitems+1):
        ax[k,l].annotate(label, (X.iloc[j],Y.iloc[j]),FontSize=16)
    
    l=l+1
    if l == 3:
        l=0
        k=k+1
        
    ax[2,0].set_xlabel('Shave n',FontSize=16)
    ax[2,0].set_ylabel('Shave n+1',FontSize=16)
    
    plt.tight_layout()
    figname = 'racked_chemistry_1_10'
    plt.savefig('Figures2/'+figname+'.pdf')
    #plt.savefig('Figures2/'+figname+'.jpg')


#%%
    
    #plot item locations between shaves (for 2 shaves)
fig = plt.figure(figsize=cm2inch(15,15))
ax = plt.axes()
xitems = np.array(range(10))
yitems = np.array(range(10,20))
  
X = items[0][xitems]
Y = items[0][yitems]
ax.plot(X,Y,'.',MarkerSize=3,color='red')      
xmin = items[i].min()-0.2
xmax = items[i].max()+0.2
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
    
ax.set_xlabel('Item difficulty at Shave 2 (logits)',FontSize=12)
ax.set_ylabel('Item difficulty at Shave 10 (logits)',FontSize=12)
    
#plt.tight_layout()
figname = 'racked_chemistry_2_10'
#plt.savefig('Figures2/'+figname+'.pdf')
#plt.savefig('Figures2/'+figname+'.jpg')

#%%
#plot the difference in item difficulty
item_list = xitems+1
diff = abs(X.array - Y.array)

item_sort = [x for _,x in sorted(zip(diff,item_list))]

diff = np.sort(diff)
fig = plt.figure(figsize=cm2inch(15,15))
ax = plt.axes()

ax.bar(item_list,diff,0.2)
ax.set_xticks(item_list)
ax.set_xticklabels(item_sort,fontsize=12)
ax.tick_params(axis="y",labelsize=12)
ax.set_xlabel('Item',fontsize=12)
ax.set_ylabel('Increase in difficulty (logits)',fontsize=12)

figname = 'racked_chemistry_2_10b'
plt.savefig('Figures2/'+figname+'.pdf')
plt.savefig('Figures2/'+figname+'.jpg')









