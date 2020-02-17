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

dataA = pd.read_excel('../Data2_Shaving/track_tests/results_1.xls')
dataB = pd.read_excel('../Data2_Shaving/track_tests/results_2.xls')
dataC = pd.read_excel('../Data2_Shaving/track_tests/results_3.xls')
dataD = pd.read_excel('../Data2_Shaving/track_tests/results_4.xls')
dataE = pd.read_excel('../Data2_Shaving/track_tests/results_5.xls')
dataF = pd.read_excel('../Data2_Shaving/track_tests/results_6.xls')
dataG = pd.read_excel('../Data2_Shaving/track_tests/results_7.xls')
dataH = pd.read_excel('../Data2_Shaving/track_tests/results_8.xls')
dataI = pd.read_excel('../Data2_Shaving/track_tests/results_9.xls')

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
#%%stacked or anchored data
        
#list data files
data = [dataA,dataB,dataC,dataD,dataE,dataF,dataG,dataH,dataI]      

stacked = False

if not stacked:
    n = len(data[0])
    
#number of shaves
shave_list = [1,2,3,4,5,6,7,8,9]
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

#%sort in ascending order, according to the results at time 1
results = results.sort_values(by=[1])

#%crop results to consider a selection of shaves only
selection = False
if selection:
    shave_select = [1,2,3]
    shaves = len(shave_select)
    index_select = []
    for i in range(len(shave_select)):
        index2 = shave_list.index(shave_select[i]) + 1
        index_select.append(results.columns.get_loc(index2)-1) #index corresponding to the personID (for that shave of interest)
        index_select.append(results.columns.get_loc(index2)) #index corresponding to the shave of interest
        
    shave_list = shave_select
    results = results.iloc[:,index_select]
        

#%reindex so index is in ascending order
new_index = list(range(len(results)))
index_dict2 = dict(zip(results.index,new_index))
results.rename(index_dict2,inplace=True)

#%reduce data set so that the same people are in each shave
people = np.unique(results.loc[:,'personID'])
people = people[~np.isnan(people)] #array of unique person IDs in results
people_keep = []
for i in range(len(people)):
    check1 = results.loc[:,'personID'].isin([people[i]])
    check2 = check1[check1]
    if check2.count().sum() == len(shave_list):
        people_keep.append(people[i])
        


#is_people = results.loc[:,'ID'].isin(people)
#people_keep = is_people[is_people].dropna() #peson IDs which are in all shaves
#reduced results with each person in every shave
#results_people = results.iloc[people_keep.index,:]
#% plots

loc_loc = False
pers_time = False
save = True
average = True

        
if loc_loc:
    
    labels = ['Shaves 2-5','Shaves 5-8','Shaves 8-10']
    #labels = ['Shaves 1-2','Shaves 2-3','Shaves 3-4']
    
    if selection:
        shave_list = shave_select
        shaves = len(shave_select)
    
    #resort according to person indices
  #  j=0
  #  for i in range(len(shave_list)):
   #     results_people.iloc[:,[j,j+1]] = results_people.iloc[:,[j,j+1]].sort_values(by=['ID'])
   #     j=j+2
    xmax = 3.5
    xmin = -3.5
    xy = np.linspace(xmin,xmax,100) 
   
    fig = plt.figure()
    ax = plt.axes()
    j=0
    for i in range(shaves-1):
        result_plot1 = results.iloc[:,[j,j+1]].sort_values(by=['personID'])
        result_plot2 = results.iloc[:,[j+2,j+3]].sort_values(by=['personID'])
        #remove people that aren't in both shaves
        keep1 = result_plot1.loc[:,'personID'].isin(people_keep)
        keep1_index = keep1[keep1].index
        result_plot1 = result_plot1.loc[keep1_index,:]
        keep2 = result_plot2.loc[:,'personID'].isin(people_keep)
        keep2_index = keep2[keep2].index
        result_plot2 = result_plot2.loc[keep2_index,:]
        ext2 = ext[i+1][keep2_index]
        if shaves == 2:
            label2 = ''
        else:
            label2 = labels[i]
        ax.plot(result_plot1.iloc[:,1],result_plot2.iloc[:,1],'o',label=label2)
        j=j+2
        if i == 0:
            ax.plot(xy,xy,'-',color='red')
            
      #  for label,x,y in zip(ext2,result_plot1.iloc[:,1],result_plot2.iloc[:,1]):
      #      if (label==1): #& (label0==0):
      #          ax.plot(x,y,'*',color='black')
    
   #% 
    
    if shaves == 2:  
        ax.set_xlabel('Location at test ' + str(shave_list[0]) + ' (logits)',FontSize=12)
        ax.set_ylabel('Location at test ' + str(shave_list[1]) + ' (logits)',FontSize=12)
    else:
        ax.set_xlabel('Location at test n (logits)')
        ax.set_ylabel('Location at test n + 1 (logits)')
   # ax.set_title('Shave ' + str(shave_list[0]) + ' vs Shave ' + str(shave_list[1]))
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(xmin,xmax)
    
    if shaves == 2:
        legend = False
    else:
        legend = True
    
    if legend:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.2,0.75),
                  fancybox=True, shadow=True)
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 11.5}
    
    figname = 'test_anchored_' + str(shave_list[0]) + '_' + str(shave_list[1]) + 'extb' 
        
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
        
    

    
if pers_time:
#plots the lcoation of every person over every shave

    #reduce data set to contain only the people who have completed all shaves
    j=0
    for i in range(shaves):
        result_plot1 = results.iloc[:,[j,j+1]].sort_values(by=['personID'])
        keep1 = result_plot1.loc[:,'personID'].isin(people_keep)
        keep1_index = keep1[keep1].index
        result_plot1 = result_plot1.loc[keep1_index,:]
        if i == 0:
            results2 = result_plot1
        else:
            results2 = results2.merge(result_plot1)
        j=j+2
           

    xmax = 6.5
    xmin = -3.5 
    fig, ax = plt.subplots(3,3,figsize=(10,10))
    k=0
    i=0
    j=0
    n = int(len(results2)/9) #number of plots in each subfigure
    while i < 3:
        k2 = k+n
        if i == 2 and j ==2:
            if len(results2) % 9 != 0: #plot remaining person in final subfig (if the number of people is not divisible by n)
                k2 = k+n+1
        for l in range(k,k2):
            ax[i,j].plot(shave_list,results2.iloc[l,1:shaves+1],'-o',label=int(results2.iloc[l,0]))
        ax[i,j].set_ylim(xmin,xmax)
        #ax[i,j].set_yticks([])
        ax[i,j].set_xticks(shave_list)
        ax[i,j].legend(loc='upper center', fancybox=True, shadow=True, ncol=3, prop={"size":8})
        
        k=k+5
        j=j+1
        if j == 3:
            i=i+1
            j=0
    
    ax[2,0].set_ylabel('Person location (logits)', fontsize=12)
    ax[2,0].set_xlabel('Test number', fontsize=12)
    
    
    legend = False
    if legend:
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

    figname = 'test_person_time_'+str(min(shave_list))+'_'+str(max(shave_list))
    #matplotlib.rc('font', **font)
    
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')  
        
if average:
#plots average results for each shave

    #average person location
    average_score = []
    for i in range(shaves):
        average_score.append(results.loc[:,i+1].mean())    
    
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(shave_list,average_score,'o-')
    ax.set_xticks(shave_list)
    ax.set_xlabel('Test number', fontsize=12)
    ax.set_ylabel('Average person location (logits)', fontsize=12)
    
    figname = 'average_score_tests'
    
    if save:
        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')  
    


        

    