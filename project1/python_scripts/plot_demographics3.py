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

data1 = pd.read_excel('../Rasch_analysis/Data1_Saudi/extra_PFs/ratings_results_purchase_history.xlsx') #read raw data
data2 = pd.read_excel('../Rasch_analysis/Data1_Saudi/extra_PFs/agreements_results_purchase_history.xlsx') #read raw data

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
factor = 'Purchase history'
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
if factor == 'Purchase history':
    factor_keyR = 'Unnamed: 6'
    factor_keyA = 'Unnamed: 6'
    labels = ['Many times before','A few times before','Once before','Never before']
    labels_i = [2,1,3,0]
    save_name = 'history'

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

#agreements
save_fig = True
rating = False
performance = False
distinctiveness = False
value = False
history = False
wash = False
detergent = False
scents = False
bleach = False
 
    
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
    ax.plot(loc3,score3,'-*',linewidth=3)
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
    ax.plot(loc3,score3,'-*',linewidth=3)
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
    ax.plot(loc3,score3,'-*',linewidth=3)
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
    

    loc1 = [-0.62, 0.27,	0.62,	0.88,	1.19,	1.64,	2.16,	2.75,	3.8]
    loc2 = [-0.38, 0.27,	0.64,	0.88,	1.18,	1.64,	2.19,	2.73,	3.73]
    loc3 = [-0.86, 0.3, 	0.65,	0.88,	1.15,	1.59,	2.08,	2.66,	3.7]
    loc4 = [-0.38, 0.25,	0.53,	0.88,	1.25,	1.66,	2.3,	2.69,	3.4]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-*',linewidth=3)
    ax.plot(loc4,score4,'-v',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.0003)',FontSize=12)
    ax.legend(['Purchased: Many times','Purchased: Few times','Purchased: Once','Purchased: Never'],prop={"size":10},loc='upper left')

    figname = 'history_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
#type of wash
if wash:
    
    score1 = [1.45,	2.25,	2.45,	2.38,	2.78,	2.92,	3,	3.28,	3.7]
    score2 = [1.6,	1.63,	2.23,	2.44,	2.79,	2.93,	3.33,	3.64,	3.83]

    loc1 = [-0.57,	0.28,	0.62,	0.88,	1.19,	1.65,	2.18,	2.73,	3.73]
    loc2 = [-0.44,	0.26,	0.63,	0.88,	1.18,	1.63,	2.16,	2.73,	3.74]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.0012)',FontSize=12)
    ax.legend(['Usual wash: Hand and machine wash','Usual wash: Machine wash only'],prop={"size":10},loc='lower right')

    figname = 'wash_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
if detergent:
    
    score1 = [1.38,	2.65,	2.68,	3,	3,	3.26,	3.68,	3.75,	3.71]
    score2 = [2,	2.76,	2.93,	2.95,	3.05,	3.45,	3.54,	3.64,	3.94]

    loc1 = [-0.45,	0.27,	0.6,	0.88,	1.2,	1.66,	2.19,	2.69,	3.79]
    loc2 = [-0.53,	0.28,	0.64,	0.88,	1.18,	1.63,	2.16,	2.74,	3.71]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 9',FontSize=12)
    ax.set_title('This product is excellent at completely removing bad odours (p = 0.0028)',FontSize=12)
    ax.legend(['Type of detergent: Mainly powder','Type of detergent: Powder and liquid'],prop={"size":10},loc='lower right')

    figname = 'det_DIF_item9'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
        
if scents:
    
    score1 = [1.49,	2,	2.18,	2.4,	2.8,	2.88,	3.02,	3.38,	3.71]
    score2 = [1.45,	2.03,	2.43,	2.39,	2.73,	2.92,	3.34,	3.43,	3.84]
    score3 = [2.5,	2.33,	2.75,	3,	3,	3.67,	3.4,	3.67,	3.8]
    

    loc1 = [-0.43,	0.28,	0.62,	0.88,	1.2,	1.63,	2.18,	2.7,	3.73]
    loc2 = [-0.63,	0.27,	0.63,	0.88,	1.18,	1.65,	2.15,	2.76,	3.72]
    loc3 = [-0.32,	0.29,	0.7,	0.88,	1.2,	1.61,	2.24,	2.79,	3.97]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-*',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.004)',FontSize=12)
    ax.legend(['Preferred scent: A large amount','Preferred scent: A little amount','Preferred scent: None'],prop={"size":10},loc='lower right')

    figname = 'scent_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
#bleach
if bleach:
    
    score2 = [1.44,	1.97,	2.14,	2.62,	2.75,	2.81,	3.12,	3.22,	3.7]
    score1 = [1.57,	2.05,	2.44,	2.27,	2.82,	3,	3.18,	3.49,	3.79]

    loc2 = [-0.36,	0.29,	0.63,	0.88,	1.18,	1.68,	2.15,	2.72,	3.66]
    loc1 = [-0.57,	0.27,	0.63,	0.88,	1.19,	1.61,	2.18,	2.73,	3.77]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 3',FontSize=12)
    ax.set_title('This product is excellent at removing tough stains (p = 0.036)',FontSize=12)
    ax.legend(['Use liquid bleach: yes','Use liquid bleach: no'],prop={"size":12})

    figname = 'bleach_DIF_item3'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
#ratings
rating_ra = False
distinctiveness_ra = False
history_ra = False
intent_ra = False
wash_ra = False
machine_ra = False
scents_ra = False
bleach_ra = True

#overall rating
if rating_ra:
    
    score1 = [1.76,	2.24,	2.56,	2.79,	2.79,	3.18,	3.49,	3.53,	3.71,	3.87]
    score2 = [1.46,	2.02,	2.21,	2.73,	2.93,	3.23,	3.17,	3.44,	3.63]

    loc1 = [-0.63, 0.24,	0.57,	0.9,	1.3,	1.64,	2.05,	2.5,	3.11,	4.06]
    loc2 = [-0.55, 0.21,	0.56,	0.89,	1.27,	1.63,	2.02,	2.52,	3.12]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 10',FontSize=12)
    ax.set_title('Rating for keeping colours vivid and bright (p = 0.0098)',FontSize=12)
    ax.legend(['Overall score: Excellent','Overall score: Very good'],prop={"size":12})

    figname = 'rating_DIF_item10_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')

if distinctiveness_ra:
    
    score1 = [1.6,	1.4,	2,	2.39,	3,	3.05,	3.16,	3.31,	3.65,	3.86]
    score2 = [1.58,	2.03,	2.29,	2.22,	2.64,	2.77,	2.74,	3.5,	3.41,	3.77]
    score3 = [0.95,	1.84,	1.9,	2.36,	2.71,	2.63,	3.44,	3,	4,	4]
    

    loc1 = [-0.76,	0.05,	0.47,	0.79,	1.16,	1.52,	1.93,	2.39,	2.9,	3.9]
    loc2 = [-0.6,	0.04,	0.45,	0.75,	1.13,	1.54,	1.91,	2.37,	2.91,	3.66]
    loc3 = [-1.16,	0.05,	0.43,	0.79,	1.18,	1.57,	1.94,	2.21,	3.11,	4.05]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-*',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 4',FontSize=12)
    ax.set_title('Rating for keeping clothes looking their best over time (p = 0.0086)',FontSize=12)
    ax.legend(['Distinctiveness: Very new','Distinctiveness: Fairly new','Distinctiveness: About the same'],prop={"size":10},loc='lower right')

    figname = 'distinctiveness_DIF_item4_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
if history_ra:
    
    score1 = [1.08,	1.83,	1.96,	2.03,	2.54,	2.72,	2.95,	3.32,	3.43,	3.88]
    score2 = [1.25,	1.9,	2.13,	2.5,	2.83,	3,	3.09,	3.43,	3.71,	3.79]
    score3 = [1,	2.33,	2.33,	2.88,	3,	2.8,	2.89,	3.6,	3,	3.88]
    score4 = [1.5,	1.5,	2.67,	2.5,	2.67,	2.67,	3.33,	3,	4,	4]
    

    loc1 = [-1.1,	-0.01,	0.46,	0.77,	1.13,	1.49,	1.93,	2.41,	2.9,	3.87]
    loc2 = [-0.93,	0.01,	0.42,	0.75,	1.14,	1.54,	1.91,	2.34,	2.9	,3.78]
    loc3 = [-1.09,	0.07,	0.45,	0.74,	1.12,	1.58,	1.86,	2.28,	2.73,	3.93]
    loc4 = [-0.75,	0.02,	0.41,	0.77,	1.18,	1.55,	1.91,	2.43,	2.99,	4.31]
    
    loc1 = [-1.1,	0.01,	0.49,	0.8,	1.16,	1.53,	1.97,	2.46,	2.96,	3.93]
    loc2 = [-0.93,	0.04,	0.45,	0.78,	1.18,	1.58,	1.95,	2.39,	2.95,	3.84]

    #option 2 - only 'many times' and 'few times' consumers were included in the analysis

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    #ax.plot(loc3,score3,'-*',linewidth=3) #comment if only considering the 'many times' and 'few times' analysis
    #ax.plot(loc4,score4,'-v',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 4',FontSize=12)
    ax.set_title('Rating for keeping clothes looking their best over time (p = 0.001)',FontSize=12) #p = 0.0067 when all categories are included
    ax.legend(['Purchased: Many times','Purchased: Few times','Purchased: Once','Purchased: Never'],prop={"size":10},loc='upper left')

    figname = 'history_DIF_item4_ra2'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')

#overall rating
if intent_ra:
    
    score1 = [2.15,	2.56,	2.79,	2.97,	3.17,	3.15,	3.53,	3.57,	3.74,	3.9]
    score2 = [1.71,	2.42,	2.57,	2.48,	3.12,	3.24,	3.44,	3.69,	3.67,	4]

    loc1 = [-0.61,	0.11,	0.47,	0.75,	1.11,	1.49,	1.9,	2.34,	2.87,	3.85]
    loc2 = [-0.89,	0.08,	0.46,	0.73,	1.14,	1.53,	1.85,	2.36,	2.91,	3.67]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 1',FontSize=12)
    ax.set_title('Rating for cleaning laundry overall (p = 0.006)',FontSize=12)
    ax.legend(['Purchase intent: Definitely buy again','Purchase intent: Probably buy again'],prop={"size":10},loc = 'lower right')

    figname = 'intent_DIF_item1_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')

#type of wash
if wash_ra:
    
    score1 = [1.38,	1.98,	2.13,	2.58,	2.67,	2.75,	3.09,	3.31,	3.48,	3.87]
    score2 = [1.22,	2.07,	2.35,	2.73,	2.67,	3,	3.06,	3.53,	3.79,	3.82]

    loc1 = [-1.01,	0.04,	0.44,	0.76,	1.15,	1.51,	1.93,	2.38,	2.89,	3.9]
    loc2 = [-0.98,	-0.03,	0.43,	0.76,	1.12,	1.53,	1.89,	2.35,	2.9,	3.8]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 15',FontSize=12)
    ax.set_title('Rating for being gentle and safe on clothes and sensitive skin (p = 0.027)',FontSize=12)
    ax.legend(['Usual wash: Hand and machine wash','Usual wash: Machine wash only'],prop={"size":10},loc='lower right')

    figname = 'wash_DIF_item15_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
if machine_ra:
    
    score1 = [1,	1.89,	2.29,	2.35,	2.42,	2.96,	3.2,	3.5,	3.78,	3.84]
    score2 = [1.21,	2,	2.26,	2.3,	2.52,	3,	2.97,	3.46,	3.64,	3.89]
    score3 = [0.94,	1.54,	2.33,	2.08,	2.35,	2.94,	3.13,	3.24,	3.15,	3.65]
    

    loc1 = [-1.07,	-0.01,	0.44,	0.74,	1.14,	1.53,	1.89,	2.4,	2.93,	3.87]
    loc2 = [-0.94,	0.01,	0.43,	0.77,	1.14,	1.51,	1.91,	2.34,	2.87,	3.82]
    loc3 = [-1.12,	0.03,	0.44,	0.78,	1.15,	1.54,	1.94,	2.36,	2.94,	3.92]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.plot(loc3,score3,'-*',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 8',FontSize=12)
    ax.set_title('Rating for providing long lasting freshness (p = 0.0086)',FontSize=12)
    ax.legend(['Machine type: Fully automatic, front loader','Machine type: Fully automatic, top loader','Machine type: Semi-automatic, top loader'],prop={"size":9.5},loc='lower right')

    figname = 'machine_DIF_item8_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
if scents_ra:
    
    score1 = [1.26,	1.88,	2.29,	2.89,	2.92,	3.08,	3.55,	3.59,	3.65,	3.79]
    score2 = [1.27,	1.81,	2.19,	2.65,	2.68,	2.93,	3.23,	3.34,	3.57,	3.88]
    

    loc1 = [-0.89,	0.01,	0.47,	0.78,	1.18,	1.55,	1.94,	2.43,	2.93,	3.78]
    loc2 = [-1.13,	0.04,	0.47,	0.79,	1.17,	1.55,	1.94,	2.37,	2.93,	3.96]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 10',FontSize=12)
    ax.set_title('Rating for keeping colours vivid and bright (p = 0.0097)',FontSize=12)
    ax.legend(['Preferred scent: A large amount','Preferred scent: A little amount'],prop={"size":10},loc='lower right')

    figname = 'scent_DIF_item10_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg') 
        
if bleach_ra:
    
    score1 = [1.29,	1.9,	2.2,	2.71,	2.51,	2.83,	3,	3.42,	3.57,	3.84]
    score2 = [1.32,	2.25,	2.31,	2.61,	2.93,	2.93,	3.21,	3.43,	3.82,	3.86]

    loc1 = [-1.08,	0.02,	0.44,	0.77,	1.14,	1.52,	1.91,	2.38,	2.89,	3.85]
    loc2 = [-0.89,	0,	0.44,	0.75,	1.13,	1.53,	1.91,	2.33,	2.91,	3.84]

    fig,ax = plt.subplots()

    ax.plot(loc1,score1,'-o',linewidth=3)
    ax.plot(loc2,score2,'-s',linewidth=3)
    ax.set_xlabel('Person location (logits)',FontSize=12)
    ax.set_ylabel('Expected score for Item 15',FontSize=12)
    ax.set_title('Rating for being gentle and safe on clothes and sensitive skin  (p = 0.021)',FontSize=12)
    ax.legend(['Use liquid bleach: yes','Use liquid bleach: no'],prop={"size":12})

    figname = 'bleach_DIF_item15_ra'

    if save_fig:
        plt.savefig('Figures3/'+figname+'.pdf')
        plt.savefig('Figures3/'+figname+'.jpg')
        
        
        
        
        