# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:51:27 2019

@author: matcc
"""
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

os.chdir('M:/LIDA_internship/project1/python_scripts')

data1 = pd.read_excel('../Rasch_analysis/Data1_Saudi/extra_PFs/ratings_results.xlsx') #read raw data
data2 = pd.read_excel('../Rasch_analysis/Data1_Saudi/extra_PFs/agreements_results.xlsx') #read raw data

#convert figsize from cm to inches
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)
#%% products
        

location1 = data1.Location
location2 = data2.Location

rating_data = []
agreement_data = []
#for i in range(10):
#    rating_data.append(location1[data1.iloc[:,-1]==i])
#    agreement_data.append(location2[data2.iloc[:,-1]==i])

save_fig = True
factor = 'Overall rating'
if factor == 'Overall rating':
    factor_keyR = 'PF_overall'
    factor_keyA = 'PF_overall'
    labels = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
    labels_i = [0,4,2,1,3]
    save_name = 'overall_rating'
if factor == 'Relative category':
    factor_keyR = 'PF_relCat'
    factor_keyA = 'PF_relCat'
    labels = ['The best','Slightly better','The same','Slightly worse','The worst']
    labels_i = [2,0,3,1,4]
    save_name = 'rel_cat'
if factor == 'Purchase intent':
    factor_keyR = 'PF_intent'
    factor_keyA = 'PF_intent'
    labels = ['Def. buy again','Prob. buy again','Might buy again','Prob. not buy again','Def. not buy again']
    labels_i = [0,3,2,4,1]
    save_name = 'purch_intent'
if factor == 'Performance vs. expectations':
    factor_keyR = 'PF_perfrmnce'
    factor_keyA = 'PF_prfrmnce'
    labels = ['Much better','A little better', 'About the same', 'A little worse']
    labels_i = [3,0,2,1]
    save_name = 'performance'
if factor == 'Distinctiveness vs other products':
    factor_keyR = 'PF_dstnvess'
    factor_keyA = 'PF_dstncvnes'
    labels = ['Very new','Somewhat new','About the same','Not very new','Not at all new']
    labels_i = [4,3,0,2,1]
    save_name = 'distinctiveness'
if factor == 'Value for Money':
    factor_keyR = 'PF_value'
    factor_keyA = 'PF_value'
    labels = ['Very good','Fairly good','Average','Somewhat poor','Very poor']
    labels_i = [3,1,0,2,4]
    save_name = 'value'

labels_r = labels.copy()
labels_a = labels.copy()
for i in range(len(labels_i)):
    rating_data.append(location1[data1[factor_keyR].isin([labels_i[i]])]) #ratings
    agreement_data.append(location2[data2[factor_keyA].isin([labels_i[i]])]) #agreements
    ss_r = len(location1[data1[factor_keyR].isin([labels_i[i]])]) #sample size for ratings
    ss_a = len(location2[data2[factor_keyA].isin([labels_i[i]])]) #sample size for agreements
    labels_r[i] = labels_r[i] + ' (' + str(ss_r) + ')' #add sample size to labels
    labels_a[i] = labels_a[i] + ' (' + str(ss_a) + ')'

fig1,ax = plt.subplots(1,2,figsize=cm2inch(19,12))
ax[0].boxplot(rating_data)
ax[1].boxplot(agreement_data)

ax[0].set_title('Ratings',FontSize=12)
ax[1].set_title('Agreements',FontSize=12)

ax[0].set_ylabel('Person location (logits)',FontSize=12)
#ax[0].set_xlabel(factor,FontSize=12)
#ax[1].set_xlabel(factor,FontSize=12)

ax[0].set_xticklabels(labels_r,rotation=45,FontSize=12)
ax[1].set_xticklabels(labels_a,rotation=45,FontSize=12)
ax[1].set_yticks([])

plt.tight_layout()

figname = save_name

if save_fig:
    plt.savefig('Figures3/'+figname+'.pdf')
    plt.savefig('Figures3/'+figname+'.jpg')
    
#%% DIF

save_fig = True
rating = False
performance = False
distinctiveness = False
value = False
history = True
 
#agreements
    
#overall rating
if rating:
    
    score1 = [1.95,	2.17,	2.49,	2.59,	2.76,	3.03,	2.94,	3.19,	3.39,	3.77]
    score2 = [1.49,	2.18,	2.14,	2.24,	2.65,	2.53,	2.9,	3.15,	3.46,	3.67]

    loc1 = [-0.36,	0.35,	0.67,	0.93,	1.13,	1.34,	1.69,	2.23,	2.79,	3.8]
    loc2 = [-0.33,	0.36,	0.66,	0.93,	1.13,	1.34,	1.68,	2.21,	2.78,	3.81]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.0095)',FontSize=12)
    ax.legend(['Overall score: Excellent','Overall score: Very good'],prop={"size":12})

    figname = 'rating_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')

if performance:
    
    score1 = [1.63,	2.33,	2.35,	2.94,	3,	3.09,	3.45,	3.52,	3.75]
    score2 = [1.95,	2.5,	2.53,	2.95,	2.91,	3.23,	3.06,	3.67,	3.88]
    score3 = [2.15,	2.72,	2.76,	3.17,	3.04,	3.38,	3.54,	3.86,	3.67]
    

    loc1 = [-0.48,	0.29,	0.67,	0.91,	1.22,	1.66,	2.21,	2.75,	3.76]
    loc2 = [-0.49,	0.28,	0.64,	0.91,	1.21,	1.65,	2.13,	2.74,	3.78]
    loc3 = [-0.4,	0.31,	0.65,	0.91,	1.21,	1.7,	2.24,	2.79,	3.78]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 8',FontSize=12)
    ax.set_title('This product gives the right level of suds throughout the wash (p = 0.0037)',FontSize=12)
    ax.legend(['Perf. vs expec.: Much better','Perf. vs expec.: A little better','Perf. vs expec.: About the same'],prop={"size":12},loc='lower right')

    figname = 'performance_DIF_item8'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
if distinctiveness:
    
    score1 = [2.3,	2.11,	2.44,	2.42,	3.04,	3,	3.16,	3.57,	3.81]
    score2 = [1.41,	2.03,	2.33,	2.47,	2.69,	2.93,	3.14,	3.19,	3.63]
    score3 = [1.47,	2,	2.25,	2.18,	2.69,	2.63,	3.25,	3.5,	4]
    

    loc1 = [-0.35,	0.27,	0.61,	0.91,	1.22,	1.69,	2.17,	2.79,	3.75]
    loc2 = [-0.58,	0.3,	0.66,	0.91,	1.22,	1.66,	2.22,	2.77,	3.67]
    loc3 = [-0.65,	0.33,	0.66,	0.91,	1.22,	1.7,	2.22,	2.78,	3.83]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.007)',FontSize=12)
    ax.legend(['Distinctiveness: Very new','Distinctiveness: Fairly new','Distinctiveness: About the same'],prop={"size":10},loc='upper left')

    figname = 'distinctiveness_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')

if value:
    
    score1 = [2.15,	2.75,	2.82,	3.07,	2.97,	3.24,	3.22,	3.64,	3.77]
    score2 = [1.96,	2.32,	2.82,	2.7,	2.88,	3.13,	3.16,	3.61,	3.63]
    score3 = [1.85,	2.35,	2.5,	2.82,	2.76,	2.92,	3.55,	3.09,	3.5]
    

    loc1 = [-0.51,	0.27,	0.67,	0.9,	1.21,	1.68,	2.21,	2.8	,3.78]
    loc2 = [-0.57,	0.3,	0.64,	0.9,	1.22,	1.66,	2.21,	2.75,	3.72]
    loc3 = [-0.44,	0.28,	0.63,	0.9,	1.21,	1.7,	2.19,	2.71,	4.05]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 1',FontSize=12)
    ax.set_title('This product provides excellent value (p = 0.001)',FontSize=12)
    ax.legend(['Value: Very good','Value: Fairly good','Value: Average'],prop={"size":10},loc='upper left')

    figname = 'value_DIF_item1'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
        
if history:
    
    score1 = [1.17,	1.96,	2.19,	2.53,	2.74,	3,	    3.03,	3.48,	3.74]
    score2 = [1.64,	1.95,	2.37,	2.39,	2.86,	2.92,	3.26,	3.51,	3.76]
    score3 = [1.73,	2.69,	2.67,	2.33,	2.78,	2.75,	3.2,	3,  	3.89]
    score4 = [1.25,	1.56,	2,  	2,  	2.4,	2.71,	3,  	2.33,	3.67]
    

    loc1 = [0.27,	0.62,	0.88,	1.19,	1.64,	2.16,	2.75,	3.8]
    loc2 = [0.27,	0.64,	0.88,	1.18,	1.64,	2.19,	2.73,	3.73]
    loc3 = [0.3,	0.65,	0.88,	1.15,	1.59,	2.08,	2.66,	3.7]
    loc4 = [0.25,	0.53,	0.88,	1.25,	1.66,	2.3,	2.69,	3.4]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.0003)',FontSize=12)
    ax.legend(['Purchased: Many times','Purchased: Few times','Purchased: Once','Purchased: Never'],prop={"size":10},loc='upper left')

    figname = 'history_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
