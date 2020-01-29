# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:09:00 2019

@author: matcc
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

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
        
data1 = pd.read_excel('../Data2_Shaving/shave_numbers/shave1_results.xls',header=None)
data2 = pd.read_excel('../Data2_Shaving/shave_numbers/shave2_results.xls',header=None)
data3 = pd.read_excel('../Data2_Shaving/shave_numbers/shave3_results.xls',header=None)
data4 = pd.read_excel('../Data2_Shaving/shave_numbers/shave4_results.xls',header=None)
data5 = pd.read_excel('../Data2_Shaving/shave_numbers/shave5_results.xls',header=None)
data6 = pd.read_excel('../Data2_Shaving/shave_numbers/shave6_results.xls',header=None)
data7 = pd.read_excel('../Data2_Shaving/shave_numbers/shave7_results.xls',header=None)
data8 = pd.read_excel('../Data2_Shaving/shave_numbers/shave8_results.xls',header=None)
data10 = pd.read_excel('../Data2_Shaving/shave_numbers/shave10_results.xls',header=None)
data11 = pd.read_excel('../Data2_Shaving/chemistry_shaves_as_facets/10_shaves_chem_only_results.xls',header=None)

#data = [data1,data2,data3,data4,data5,data6,data7,data8,data10]
data = [data11]

no_shaves = len(data)

shaves = {name: pd.DataFrame for name in range(no_shaves)}
items = {name: pd.DataFrame for name in range(no_shaves)}

for i in range(no_shaves):
    shaves[i] = data[i].iloc[:,7]
    items[i] = data[i].iloc[:,2]
    index_dict = dict(zip(shaves[i].index,data[i].iloc[:,6]))
    shaves[i].rename(index_dict,inplace=True)

#%% three facet analysis
    
data =   pd.read_excel('../Data2_Shaving/shave_numbers/shave1_3_results.xls',header=None)  
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

if len(shaves) == 10:
    new_index = ['prod18','con18','prod19','con19','prod6','con6']
    index_dict = dict(zip(products.index,new_index))
    products.rename(index_dict,inplace=True)
    
#%% plot histograms of product and item locations for the different shave numbers
products_plot = False
item_plot = False
shave_plot = False
shave_item_plot = True
save = True

if products_plot:
    labels = ['Control 18','Product 2', 'Product 31', 'Control 32', 'Product 32', 'Control 2', 'Control 29',
          'Product 19', 'Control 31','Control 6', 'Product 18', 'Control 19', 'Product 29', 'Product 6']
    #labels = ['Shave 1','Shave 10']
    
    #fig = plt.figure()
    #ax = plt.axes()
    
    fig,ax = plt.subplots(3,3,figsize=cm2inch(25,18))
    
    x = np.arange(len(labels))
    width = 0.85
    
    xmin = -0.5
    xmax = 13.5
    
    l=0
    k=0
    for i in range(no_shaves):
        if i < 3:
            ax[k,l].bar([0,1],[shaves[i].loc['product2'],shaves[i].loc['control2']],width,label='Product 2',edgecolor=['black','none'],linewidth=[1,0],
              color='dodgerblue')
        if i < 5:
            ax[k,l].bar([2,3],[shaves[i].loc['product31'],shaves[i].loc['control31']],width,label='Product 31',edgecolor=['black','none'],linewidth=[1,0],
              color='orange')
            ax[k,l].bar([4,5],[shaves[i].loc['product32'],shaves[i].loc['control32']],width,label='Product 32',edgecolor=['black','none'],linewidth=[1,0],
              color='limegreen')
        ax[k,l].bar([6,7],[shaves[i].loc['product19'],shaves[i].loc['control19']],width,label='Product 19',edgecolor=['black','none'],linewidth=[1,0],
          color='red')
        ax[k,l].bar([8,9],[shaves[i].loc['product18'],shaves[i].loc['control18']],width,label='Product 18',edgecolor=['black','none'],linewidth=[1,0],
          color='mediumslateblue')
        if i < 5:
            ax[k,l].bar([10,11],[shaves[i].loc['product29'],shaves[i].loc['control29']],width,label='Product 29',edgecolor=['black','none'],linewidth=[1,0],
              color='saddlebrown')
        ax[k,l].bar([12,13],[shaves[i].loc['product6'],shaves[i].loc['control6']],width,label='Product 6',edgecolor=['black','none'],linewidth=[1,0],
          color='magenta')
        ax[k,l].set_xticks([])
        ax[k,l].set_yticks([])
        ax[k,l].tick_params(axis="y",labelsize=8)
        ax[k,l].set_xlim([xmin,xmax])
        ax[k,l].set_title('Shave ' + str(i+1))
        if i == 8:
            ax[k,l].set_title('Shave 10')
        l=l+1
        if l == 3:
            l=0
            k=k+1

    plt.tight_layout()
    fig.subplots_adjust(right=0.8)

    
    ax[1,0].set_ylabel('Mean location (logits)')
    
    legend_outside = True
    
    if legend_outside:    
        box = ax[0,2].get_position()
        #ax[2,2].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        lgd = ax[0,2].legend(loc='upper center', bbox_to_anchor=(1.45,0.65),
                      fancybox=True, shadow=True)
    else:
        ax[2,2].legend(loc='best', fancybox=True, shadow=True)

    font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 12}

    figname = 'shaves'
    matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')

if item_plot:
    
    labels = ('Item 1', 'Item 2' ,'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10')
    
    fig,ax = plt.subplots(3,3,figsize=cm2inch(25,18))
    
    x = np.arange(len(labels))+1
    width = 0.85
    
    xmin = 0.5
    xmax = 10.5
    
    l=0
    k=0
    for i in range(no_shaves):
        for j in range(len(x)):
            ax[k,l].bar(x[j],items[i].iloc[j],width,label=labels[j])
        ax[k,l].set_xticks(list(range(1,11)))
        ax[k,l].set_yticks([])
        ax[k,l].tick_params(axis="x",labelsize=8)
        ax[k,l].set_xlim([xmin,xmax])
        ax[k,l].set_title('Shave ' + str(i+1))
        if i == 8:
            ax[k,l].set_title('Shave 10')
        l=l+1
        if l == 3:
            l=0
            k=k+1

    plt.tight_layout()
    fig.subplots_adjust(right=0.8)

    
    ax[1,0].set_ylabel('Mean location (logits)')
    
    legend_outside = True
    
    if legend_outside:    
        box = ax[0,2].get_position()
        #ax[2,2].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        lgd = ax[0,2].legend(loc='upper center', bbox_to_anchor=(1.45,0.65),
                      fancybox=True, shadow=True)
    else:
        ax[2,2].legend(loc='best', fancybox=True, shadow=True)
    font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 12}

    figname = 'items'
    matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
        
if shave_plot:
    
    fig,ax = plt.subplots(1,3,figsize=cm2inch(25,6))
    
    width = 0.85
    
    xmax = max(items.max(),shaves.max(),products.max()) + 0.1
    xmin = min(items.min(),shaves.min(),products.min()) - 0.1
    
    #plot products
    if len(shaves)<10:
        ax[0].bar([0,1],[products.loc['prod32'],products.loc['con32']],width,label='Product 32',edgecolor=['black','none'],linewidth=[1,0],
              color='limegreen')
        ax[0].bar([2,3],[products.loc['prod31'],products.loc['con31']],width,label='Product 31',edgecolor=['black','none'],linewidth=[1,0],
              color='orange')
    if len(shaves)==3:
        ax[0].bar([4,5],[products.loc['prod2'],products.loc['con2']],width,label='Product 2',edgecolor=['black','none'],linewidth=[1,0],
              color='dodgerblue')
    ax[0].bar([6,7],[products.loc['prod19'],products.loc['con19']],width,label='Product 19',edgecolor=['black','none'],linewidth=[1,0],
          color='red')
    ax[0].bar([8,9],[products.loc['prod6'],products.loc['con6']],width,label='Product 6',edgecolor=['black','none'],linewidth=[1,0],
          color='magenta')
    if len(shaves)<10:
        ax[0].bar([10,11],[products.loc['prod29'],products.loc['con29']],width,label='Product 29',edgecolor=['black','none'],linewidth=[1,0],
              color='saddlebrown')
    ax[0].bar([12,13],[products.loc['prod18'],products.loc['con18']],width,label='Product 18',edgecolor=['black','none'],linewidth=[1,0],
          color='mediumslateblue')
    ax[0].set_title('Products')
    ax[0].set_yticks([])
    ax[0].set_xticks([])
    ax[0].set_ylim([xmin,xmax])
    #plot items
    labels = ('Item 1', 'Item 2' ,'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10')
    
    x = np.arange(len(labels))+1

    for j in range(len(x)):
        ax[1].bar(x[j],items[j+1],width,label=labels[j])
    ax[1].set_xticks(list(range(1,11)))
    ax[1].set_yticks([])
    ax[1].tick_params(axis="x",labelsize=8)
    ax[1].set_title('Items')
    ax[1].set_ylim([xmin,xmax])
    
    #plot shaves
    
    labels2 = ('Shave 1', 'Shave 2' ,'Shave 3')
    
    x2 = np.arange(len(labels2))+1

    for j in range(len(shaves)):
        ax[2].bar(j+1,shaves.iloc[j],width,label='Shave '+str(j+1))
    ax[2].set_xticks(list(range(1,len(shaves)+1)))
    ax[2].set_yticks([])
    ax[2].tick_params(axis="x",labelsize=8)
    ax[2].set_title('Shaves')
    ax[2].set_ylim([xmin,xmax])
    
    ax[0].set_ylabel('Mean location (logits)')
    
    plt.tight_layout()
    fig.subplots_adjust(left=0.2)
    
    legend_outside = True
    
    if legend_outside:    
        box = ax[0].get_position()
        #ax[2,2].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        lgd = ax[0].legend(loc='upper center', bbox_to_anchor=(-0.45,1.1),
                      fancybox=True, shadow=True)
    else:
        ax[2,2].legend(loc='best', fancybox=True, shadow=True)
    font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 12}

    figname = '3shaves'
    matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')


if shave_item_plot:
    
    fig,ax = plt.subplots(1,2,figsize=cm2inch(15,6))
    
    width = 0.85
    
    xmax = max(items[0].max(),shaves[0].max()) + 0.1
    xmin = min(items[0].min(),shaves[0].min()) - 0.1
    
    labels = ('Item 1', 'Item 2' ,'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10')
           
    labels2 = ('Shave 1', 'Shave 2' ,'Shave 3', 'Shave 4', 'Shave 5', 'Shave 6', 'Shave 7', 'Shave 8', 'Shave 9', 'Shave 10')
    
    x = np.arange(len(labels))+1

    for j in range(len(x)):
        ax[0].bar(x[j],items[0].iloc[j],width,label=labels[j])
    ax[0].set_xticks(list(range(1,11)))
    ax[0].set_yticks([])
    ax[0].tick_params(axis="x",labelsize=12)
    ax[0].set_title('Items')
    ax[0].set_ylim([xmin,xmax])
    
    x2 = np.arange(len(labels2))+1

    for j in range(len(shaves[0])):
        ax[1].bar(j+1,shaves[0].iloc[j],width,label='Shave '+str(j+1))
    ax[1].set_xticks(list(range(1,11)))
    ax[1].set_yticks([])
    ax[1].tick_params(axis="x",labelsize=12)
    ax[1].set_title('Shaves')
    ax[1].set_ylim([xmin,xmax])
    
    ax[0].set_ylabel('Mean location (logits)',fontsize=12)
    
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

        figname = 'approach4_chemistry'
        matplotlib.rc('font', **font)
    
    if save:    

        plt.savefig('Figures2/'+figname+'.pdf')
        plt.savefig('Figures2/'+figname+'.jpg')
    
