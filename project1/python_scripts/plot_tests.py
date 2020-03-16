# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:09:00 2019

@author: matcc
"""
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

os.chdir("C:\\Users\\matcc\\LIDA_internship\\project1\\python_scripts")

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
    
    #function to put label at the top of each bar
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

#%% two facet analysis
#read data
        
data1 = pd.read_excel('../Data2_Shaving/track_tests/shave1_results.xls',header=None)
data2 = pd.read_excel('../Data2_Shaving/track_tests/shave2_results_control2.xls',header=None)
data3 = pd.read_excel('../Data2_Shaving/track_tests/shave5_results.xls',header=None)


data = [data2]

no_shaves = len(data)

shaves = {name: pd.DataFrame for name in range(no_shaves)}
controls = {name: pd.DataFrame for name in range(no_shaves)}
items = {name: pd.DataFrame for name in range(no_shaves)}

for i in range(no_shaves):
    shaves[i] = data[i].iloc[:,7]
    items[i] = data[i].iloc[:,2]
    index_dict = dict(zip(shaves[i].index,data[i].iloc[:,6]))
    shaves[i].rename(index_dict,inplace=True)
    
separate_controls = True

if separate_controls:
    control_index = {name: [] for name in range(no_shaves)}
    for i in range(no_shaves):
        index2 = shaves[i].dropna().index.copy()
        for j in range(len(index2)):            
            if 'control' in index2[j]:
                idb = index2.get_loc(index2[j])
                control_index[i].append(idb)
        
        controls[i] = shaves[i][control_index[i]]
        shaves[i].drop(shaves[i][control_index[i]].index,inplace=True)
        
#%% three facet analysis
    
data =   pd.read_excel('../Data2_Shaving/track_tests/3facet_results.xls',header=None)  
products = data.iloc[:,7]
items = data.iloc[:,2]
shaves = data.iloc[:,12]
index_dict = dict(zip(products.index,data.iloc[:,6]))
products.rename(index_dict,inplace=True)
index_dict2 = dict(zip(items.index,data.iloc[:,0]))
items.rename(index_dict2,inplace=True)
index_dict3 = dict(zip(shaves.index,data.iloc[:,11]))
shaves.rename(index_dict3,inplace=True)

shaves = shaves.dropna()
products = products.dropna()
items = items.dropna()

    
    
#%% plot histograms of product and item locations for the different test numbers
        
shave_item_plot = False
test_item_product_plot = True
save = True


if shave_item_plot:
    
    k=0
    
    fig,ax = plt.subplots(1,2,figsize=cm2inch(15,6))
    
    width = 0.85
    
    xmax = max(items[k].max(),shaves[k].max()) + 0.1
    xmin = min(items[k].min(),shaves[k].min()) - 0.1
    
    labels = ('Item 1', 'Item 2' ,'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10')
           
    labels2 = ('Test 1', 'Test 2' ,'Test 3', 'Test 4', 'Test 5', 'Test 6', 'Test 7', 'Test 8', 'Test 9')
    
    x = np.arange(len(labels))+1

    for j in range(len(x)):
        ax[0].bar(x[j],items[k].iloc[j],width,label=labels[j])
    ax[0].set_xticks(list(range(1,11)))
   # ax[0].set_yticks([])
    ax[0].tick_params(axis="x",labelsize=12)
    ax[0].tick_params(axis="y",labelsize=10)
    ax[0].set_title('Items')
    ax[0].set_ylim([xmin,xmax])
    
    x2 = np.arange(len(labels2))+1

    for j in range(len(shaves[k].dropna())):
        ax[1].bar(j+1,shaves[k].iloc[j],width,label='Shave '+str(j+1))
    ax[1].set_xticks(list(range(1,7)))
    ax[1].set_yticks([])
    ax[1].tick_params(axis="x",labelsize=12)
    #ax[1].tick_params(axis="y",labelsize=12)
    ax[1].set_title('Tests')
    ax[1].set_ylim([xmin,xmax])
    
    ax[0].set_ylabel('Location (logits)',fontsize=12)
    
    plt.tight_layout()
    fig.subplots_adjust(left=0.2)
     
    legend = False
    if legend:
        legend_outside = True
    
        if legend_outside:    
            box = ax[0].get_position()
            #ax[2,2].set_position([box.x0, box.y0, box.width * 0.8, box.height])
            lgd = ax[0].legend(loc='upper center', bbox_to_anchor=(-0.45,1.1),
                      fancybox=True, shadow=True)
        else:
            ax[0].legend(loc='best', fancybox=True, shadow=True)
    font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 12}

    figname = 'shave2_tests2'
    matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
        
if test_item_product_plot:
    
    fig,ax = plt.subplots(1,3,figsize=cm2inch(15,6))
    
    width = 0.85
    
    xmax = max(items.max(),shaves.max(),products.max()) + 0.1
    xmin = min(items.min(),shaves.min(),products.min()) - 0.1
    
    #plot products

    ax[0].bar(0,products.loc['control1'],width,label='Control 1')
    ax[0].bar(1,products.loc['control2'],width,label='Control 2')

    labels = ['1','2']
    ax[0].set_title('Controls')
    ax[0].set_xticks([0,1])
    ax[0].set_xticklabels(labels)
    ax[0].tick_params(axis="y",labelsize=12)
    ax[0].set_ylim([xmin,xmax])
    #plot items
    labels = ('Item 1', 'Item 2' ,'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10')
    
    x = np.arange(len(labels))+1

    for j in range(len(x)):
        ax[1].bar(x[j],items[j+1],width,label=labels[j])
    ax[1].set_xticks(list(range(1,11)))
    ax[1].set_yticks([])
    ax[1].tick_params(axis="x",labelsize=10)
    ax[1].set_title('Items')
    ax[1].set_ylim([xmin,xmax])
    
    #plot shaves
    
    labels2 = ('Test 1', 'Test 2' ,'Test 3')
    
    x2 = np.arange(len(labels2))+1

    for j in range(len(shaves)):
        ax[2].bar(j+1,shaves.iloc[j],width,label='Shave '+str(j+1))
    ax[2].set_xticks(list(range(1,len(shaves)+1)))
    ax[2].set_yticks([])
    ax[2].tick_params(axis="x",labelsize=12)
    ax[2].set_title('Tests')
    ax[2].set_ylim([xmin,xmax])
    
    ax[0].set_ylabel('Location (logits)')
    
    plt.tight_layout()
    #fig.subplots_adjust(left=0.2)
       
    figname = '3tests_3facets'
    matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
    
