# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 16:49:26 2020

@author: matcc
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

data = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves1_2.xlsx') #read raw data
dataA = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves12_1.xlsx')
dataB = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves12_2.xlsx')

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
#%%stacked data

shaves = 2        

#get IDs at time 1, and remove last digit from each value
data1 = dataA
personID1 = data1.loc[:,'personID'][data1.iloc[:,7]==1]
n = len(personID1)
index1 = personID1.index
personID1 = personID1.array
personID1 = [str(personID1[i])[0:-1] for i in range(n)]
personID1 = [int(personID1[i]) for i in range(n)]
personID1 = pd.Series(personID1,index=index1)
#person locations at time 1 
loc1 = data1.loc[:,'Location'][data1.iloc[:,7]==1]#.array
#track extreme people
ext1 = np.zeros(n)
ext1_index = data1.loc[:,'Extm'][(data1.loc[:,'Extm']=='extm') & (data1.iloc[:,7]==1)].index
ext1_index = ext1_index.array - n #minus the number of people at time 2 (which are stacked above time 1)
ext1[ext1_index] = 1

if shaves > 1:
    #get IDs at time 2, and remove last digit from each value
    data2 = dataB
    personID2 = data2.loc[:,'personID'][data2.iloc[:,7]==2]    
    index2 = personID2.index
    personID2 = [str(personID2[i])[0:-1] for i in range(n)]
    personID2 = [int(personID2[i]) for i in range(n)]
    personID2 = pd.Series(personID2,index=index2)    
    #person locations at time 2
    loc2 = data2.loc[:,'Location'][data2.iloc[:,7]==2]#.array
    #track extreme people
    ext2 = np.zeros(n)
    ext2_index = data2.loc[:,'Extm'][(data2.loc[:,'Extm']=='extm') & (data2.iloc[:,7]==2)].index
    ext2_index = ext2_index.array
    ext2[ext2_index] = 1



#create dictionary of the two index arrays
index_dict = dict(zip(index1,index2))
#reset the index values for loc1 to equal loc2
loc1.rename(index_dict,inplace=True)
personID1.rename(index_dict,inplace=True)

results12 = pd.concat([personID1,loc1,personID2,loc2], axis=1, ignore_index=True)


#%% plots

plot12 = True

if plot12:
#sort results by location values at time 1
    results12 = results12.sort_values(by=[1])

    fig = plt.figure()
    ax = plt.axes()
    ax.plot(index1,results12.loc[:,1],'o-',label='Shave 1')
    ax.plot(index1,results12.loc[:,3],'o-',label='Shave 2')


#visualise extreme locations
    for label,x,y in zip(ext1,index1,results12.loc[:,1]):
        if (label==1):
            #plt.annotate('*', xy = (x,y), color = 'red')
            ax.plot(x,y,'',color='black')

    for label1,label2,x,y in zip(ext1,ext2,index1,results12.loc[:,3]):
        if (label2==1) & (label1==0):
            #plt.annotate('*', xy = (x,y), color = 'red')
            ax.plot(x,y,'o',color='red')

#%
    ax.set_xticks([])
    ax.set_xlabel('Person')
    ax.set_ylabel('Location (logits)')
    ax.legend(loc='best',
              fancybox=True, shadow=True)

    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 11.5}

    figname = 'anchored_12'
    matplotlib.rc('font', **font)

    plt.savefig('Figures2/'+figname+'.pdf')
    plt.savefig('Figures2/'+figname+'.jpg')