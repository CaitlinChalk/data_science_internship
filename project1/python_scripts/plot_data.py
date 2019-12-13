# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:09:00 2019

@author: matcc
"""
import numpy as np
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

#%% comparison of products (combo 2), with repeats
#labels = ['Tide Auto LS', 'Tide HS regular', 'Ariel Auto', 'Omo (LS and HS)', 'Persil (LS and HS)']
labels = ['Comb. 2','Rep. 1', 'Rep. 2', 'Rep. 3']
item8_means = [1.447, 1.447, 1.452, 1.372]
item8_error = [1.4,1.43,1.56,1.32]
item9_means = [1.417, 1.447, 1.425, 1.4]
item9_error = [1.4,1.41,1.4,1.4]
item1_means = [1.337, 1.366, 1.345, 1.363]
item1_error = [1.41,1.43,1.41,1.41]
item45_means = [1.316,1.346,1.324,1.342]
item45_error = [1.29,1.3,1.29,1.29]
item67_means = [1.072,1.098,1.079,1.098]
item67_error = [1.34,1.36,1.34,1.34]

item8_means_ag = [1.391,1.413,1.424,1.519]
item8_error_ag = [1.4,1.29,1.32,1.32]
item9_means_ag = [1.285, 1.288, 1.306, 1.278]
item9_error_ag = [1.21,1.21,1.2,1.19]
item1_means_ag = [1.728, 1.728, 1.746, 1.714]
item1_error_ag = [1.26,1.25,1.25,1.24]
item45_means_ag = [1.324,1.326,1.342,1.390]
item45_error_ag = [1.41,1.4,1.41,1.39]
item67_means_ag = [1.255,1.259,1.278,1.250]
item67_error_ag = [1.15,1.15,1.14,1.13]

x = [1,2,3,4]

fig1, ax1 = plt.subplots(1,2,figsize=cm2inch(21,12))
ax1[0].errorbar(x,item8_means, marker="o",yerr=item8_error,capsize=10, label='Tide LS')
ax1[0].errorbar(x,item9_means, marker="o",yerr=item9_error,capsize=10, label='Tide HS')
ax1[0].errorbar(x,item1_means, marker="o",yerr=item1_error,capsize=10, label='Ariel LS')
ax1[0].errorbar(x,item45_means, marker="o",yerr=item45_error,capsize=10, label='Omo (LS and HS)')
ax1[0].errorbar(x,item67_means, marker="o",yerr=item67_error,capsize=10, label='Persil (LS and HS)')

ax1[1].errorbar(x,item8_means_ag, marker="o",yerr=item8_error_ag,capsize=10, label='Tide LS')
ax1[1].errorbar(x,item9_means_ag, marker="o",yerr=item9_error_ag,capsize=10, label='Tide HS')
ax1[1].errorbar(x,item1_means_ag, marker="o",yerr=item1_error_ag,capsize=10, label='Ariel LS')
ax1[1].errorbar(x,item45_means_ag, marker="o",yerr=item45_error_ag,capsize=10, label='Omo (LS and HS)')
ax1[1].errorbar(x,item67_means_ag, marker="o",yerr=item67_error_ag,capsize=10, label='Persil (LS and HS)')

xmin=-0.5
xmax=3.2

ax1[0].set_ylim([xmin,xmax])
ax1[1].set_ylim([xmin,xmax])


ax1[0].set_title('Ratings')
ax1[1].set_title('Agreements')

ax1[0].set_ylabel('Mean person location')
ax1[0].set_xlabel('Test')
ax1[1].set_xlabel('Test')
ax1[1].set_yticks([])
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax1[1].get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height])
ax1[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig1.tight_layout()

figname = 'products_combo2'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% comparison of products (combo3)

labels = ['Combination 3']
#item8_means = [1.447, 1.447, 1.452, 1.372]
#item9_means = [1.417, 1.447, 1.425, 1.372]
#item1_means = [1.337, 1.366, 1.345, 1.363]
#item45_means = [1.316,1.346,1.324,1.342]
#item67_means = [1.072,1.098,1.079,1.098]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(19,12))
rects1 = ax[0].bar(x - 1.5*width, 1.457, width, label='Ariel (LS and HS)')
rects2 = ax[0].bar(x , 1.422, width, label='Tide HS')
rects3 = ax[0].bar(x + 1.5*width, 1.397, width, label='Tide LS') 

rects4 = ax[1].bar(x - 1.5*width, 1.652, width, label='Ariel (LS and HS)')
rects5 = ax[1].bar(x , 1.331, width, label='Tide HS')
rects6 = ax[1].bar(x + 1.5*width, 1.469, width, label='Tide LS') 

xmin=0.00
xmax=1.70

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean score')
ax[0].set_xticks([])
ax[0].set_xticklabels(labels)
ax[1].set_xticks([])
ax[1].set_yticks([])

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height])
ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products_combo3'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% comparison of products (combo 4), with repeats
labels = ['Comb. 4','Rep. 1', 'Rep. 2', 'Rep. 3']
item2_means = [1.849,1.952,1.848,1.766]
item2_means_e = [1.32,1.41,1.4,1.46]
item4_means = [1.431,1.475,1.442,1.377]
item4_means_e = [1.23,1.27,1.21,1.23] 
item1_means = [1.372,1.335,1.106,1.207]
item1_means_e = [1.21,1.65,1.19,1.42]
item8_means = [1.35,1.672,1.137,1.421]
item8_means_e = [1.51,1.7,1.43,1.59]
item5_means = [1.21,1.356,1.296,1.145]
item5_means_e = [1.33,1.45,1.34,1.43]
item9_means = [1.047,1.754,1.432,1.624]
item9_means_e = [1.16,1.41,1.49,1.4]
item7_means = [0.93,1.101,1.432,1.119]
item7_means_e = [1.29,1.28,1.49,1.3]

item2_means_ag = [1.25,1.273,1.303,1.272]
item2_means_e_ag = [1.21,1.2,1.19,1.23]
item4_means_ag = [1.476,1.388,1.425,1.421]
item4_means_e_ag = [1.38,1.38,1.36,1.42]
item1_means_ag = [1.713,1.697,2.016,1.963]
item1_means_e_ag = [1.24,1.24,1.18,1.36] 
item8_means_ag = [1.082,1.469,1.394,1.265]
item8_means_e_ag = [1.27,1.38,1.27,1.28] 
item5_means_ag = [1.384,1.457,1.344,1.236]
item5_means_e_ag = [1.57,1.31,1.23,1.48]
item9_means_ag = [1.291,1.437,1.298,1.364]
item9_means_e_ag = [1.19,0.95,1.12,1.35] 
item7_means_ag = [1.46,1.285,1.298,1.502]
item7_means_e_ag = [1.16,1.19,1.12,1.18]

#where the samples correspond to the same ones used in the ratings analysis with combo4
item2_means_ag2 = [1.747,1.594,1.687,1.611]
item4_means_ag2 = [1.575,1.193,1.541,1.507]
item1_means_ag2 = [1.828,1.614,1.443,1.449]
item8_means_ag2 = [1.551,1.697,1.283,1.692]
item5_means_ag2 = [1.467,1.193,1.311,1.295]
item9_means_ag2 = [1.112,1.446,1.16,1.552]
item7_means_ag2 = [1.234,1.09,1.256,1.15]

x = [1,2,3,4] # the label locations

fig, ax = plt.subplots(1,2,figsize=cm2inch(21,12))
ax[0].errorbar(x, item2_means, marker="o",yerr=item2_means_e, capsize=10,label='Ariel HS')
ax[0].errorbar(x, item4_means, marker="o",yerr=item4_means_e, capsize=10, label='Omo LS')
ax[0].errorbar(x, item1_means, marker="o",yerr=item1_means_e, capsize=10,label='Ariel LS')
ax[0].errorbar(x, item8_means, marker="o",yerr=item8_means_e, capsize=10,label='Tide LS')
ax[0].errorbar(x, item5_means, marker="o",yerr=item5_means_e, capsize=10,label='Omo HS')
ax[0].errorbar(x, item9_means, marker="o",yerr=item9_means_e, capsize=10,label='Tide hS')
ax[0].errorbar(x, item7_means, marker="o",yerr=item7_means_e, capsize=10,label='Persil LS')

ax[1].errorbar(x, item2_means_ag, marker="o",yerr=item2_means_e_ag, capsize=10,label='Ariel HS')
ax[1].errorbar(x, item4_means_ag, marker="o",yerr=item4_means_e_ag, capsize=10, label='Omo LS')
ax[1].errorbar(x, item1_means_ag, marker="o",yerr=item1_means_e_ag, capsize=10,label='Ariel LS')
ax[1].errorbar(x, item8_means_ag, marker="o",yerr=item8_means_e_ag, capsize=10,label='Tide LS')
ax[1].errorbar(x, item5_means_ag, marker="o",yerr=item5_means_e_ag, capsize=10,label='Omo HS')
ax[1].errorbar(x, item9_means_ag, marker="o",yerr=item9_means_e_ag, capsize=10,label='Tide hS')
ax[1].errorbar(x, item7_means_ag, marker="o",yerr=item7_means_e_ag, capsize=10,label='Persil LS')

xmin=-0.50
xmax=3.5

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean person location')
ax[0].set_xlabel('Test')
ax[1].set_xlabel('Test')

ax[1].set_yticks([])
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height])
ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products_combo4'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()
