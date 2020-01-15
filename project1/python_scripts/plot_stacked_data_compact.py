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
dataA = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves14_1.xlsx')
dataB = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves14_2.xlsx')
dataC = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves14_3.xlsx')
dataD = pd.read_excel('../Data2_Shaving/stacked/stacked_shaves14_4.xlsx')


#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
#%%stacked or anchored data
        
#list data files
data = [dataA,dataB,dataC,dataD]      

stacked = False

if not stacked:
    n = len(data[0])
    
#number of shaves
shave_list = [1,2,3,4]
shaves = len(shave_list)

personID = {name: pd.DataFrame for name in range(shaves)}
loc = {name: pd.DataFrame for name in range(shaves)}
ext = {name: np.zeros(n) for name in range(shaves)}
index = {name: [] for name in range(shaves)}

k=0
for i in range(shaves):
    if stacked:
        data1 = data
    else:
        data1 = data[i]
    personID[i] = data1.loc[:,'personID'][data1.iloc[:,7]==shave_list[i]]
    index1 = personID[i].index
    index[i] = personID[i].index
    personID1 = personID[i].array
    n = len(personID1)
    if shave_list[i] < 10:
        k = -1
    else:
        k = -2
    personID1 = [int(str(personID1[j])[0:k]) for j in range(n)]
    personID[i] = pd.Series(personID1,index=index1,name='ID')
    loc[i] = data1.loc[:,'Location'][data1.iloc[:,7]==shave_list[i]]
    loc[i].name = i+1
    ext_index = data1.loc[:,'Extm'][(data1.loc[:,'Extm']=='extm') & (data1.iloc[:,7]==shave_list[i])].index
    if stacked:
        ext_index = ext_index.array - (shaves-(i+1))*n #minus the number of people which are stacked above the current time (for stacked data only)
    ext[i][ext_index] = 1
    k=k+1
    if i == 0:
        index0 = index1
        results = pd.concat([personID[i],loc[i]], axis=1)
    else:
        index_dict = dict(zip(index1,index0))
        personID[i].rename(index_dict,inplace=True)
        loc[i].rename(index_dict,inplace=True)
        results = pd.concat([results,personID[i],loc[i]], axis=1)

#sort in ascending order, according to the results at time 1
results = results.sort_values(by=[1])
#%% plots

person_loc = False
loc_loc = False
pers_time = True
save = False

if person_loc:

    labels = ['Shave 1','Shave 2','Shave 3','Shave 4']
    #labels = ['Shave 1','Shave 10']
    fig = plt.figure()
    ax = plt.axes()
    for i in range(shaves):
        ax.plot(index1,results.loc[:,i+1],'o-',label=labels[i])
        #visualise extreme locations
        #if i > 0:
        for label,x,y in zip(ext[i],index[i],results.loc[:,i+1]):
            if (label==1): #& (label0==0):
                ax.plot(x,y,'',color='black')

    ax.set_xticks([])
    ax.set_xlabel('Person')
    ax.set_ylabel('Location (logits)')
    
    legend_outside = True
    
    if legend_outside:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.17,0.75),
                  fancybox=True, shadow=True)
    else:
        ax.legend(loc='best', fancybox=True, shadow=True)
    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 11.5}

    figname = 'anchored_1_10'
    matplotlib.rc('font', **font)
    
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
        
if loc_loc:
    
    labels = ['Shaves 1-2','Shaves 2-3','Shaves 3-4']
    fig = plt.figure()
    ax = plt.axes()
    for i in range(shaves-1):
        ax.plot(results.loc[:,i+1],results.loc[:,i+2],'o',label=labels[i])
        if i == 0:
            ax.plot(results.loc[:,i+1],results.loc[:,i+1],'-',color='red')
            
        for label,x,y in zip(ext[i+1],results.loc[:,i+1],results.loc[:,i+2]):
            if (label==1): #& (label0==0):
                ax.plot(x,y,'*',color='black')
    
    
    ax.set_xlabel('Location at time n')
    ax.set_ylabel('Location at time n+1')
    ax.set_title('Shave 1 vs Shave 2')
    
    legend = False
    
    if legend:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.2,0.75),
                  fancybox=True, shadow=True)
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 11.5}
    
    figname = 'anchored_1_2b'
    matplotlib.rc('font', **font)
        
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
    
if pers_time:

    #labels = ['Shave 1','Shave 2','Shave 3','Shave 4']
    #labels = ['Shave 1','Shave 10']
    #change to subplot!
    n_people = 10
           
    people = results.sample(n=n_people)    
    #people = {name: [] for name in range(shaves)} 
    
    fig = plt.figure()
    ax = plt.axes()
    for i in range(n_people):
        person = people.iloc[i,:]
        ax.plot(shave_list,person.loc[shave_list],'o-',label=person.iloc[0])
    
        
   # for i in range(shaves):
   #     ax.plot(index1,results.loc[:,i+1],'o-',label=labels[i])
        #visualise extreme locations
        #if i > 0:
  #      for label,x,y in zip(ext[i],index[i],results.loc[:,i+1]):
  #          if (label==1): #& (label0==0):
  #              ax.plot(x,y,'',color='black')

    ax.set_xlabel('Shave number')
    ax.set_ylabel('Location (logits)')
    
    
    legend = False
    if legend:
        legend_outside = False
    
        if legend_outside:    
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(loc='upper center', bbox_to_anchor=(1.17,0.75),
                  fancybox=True, shadow=True)
        else:
            ax.legend(loc='best', fancybox=True, shadow=True)
            font = {'family' : 'normal',
                        'weight' : 'normal',
                        'size'   : 11.5}

    figname = 'anchored_1_10'
    matplotlib.rc('font', **font)
    
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')    
    