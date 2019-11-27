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
#item8_error = [0.4,0.43,0.56,0.32]
item9_means = [1.417, 1.447, 1.425, 1.4]
item1_means = [1.337, 1.366, 1.345, 1.363]
item45_means = [1.316,1.346,1.324,1.342]
item67_means = [1.072,1.098,1.079,1.098]

item8_means_ag = [1.391,1.413,1.424,1.519]
item9_means_ag = [1.285, 1.288, 1.306, 1.278]
item1_means_ag = [1.728, 1.728, 1.746, 1.714]
item45_means_ag = [1.324,1.326,1.342,1.390]
item67_means_ag = [1.255,1.259,1.278,1.250]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(21,12))
rects1 = ax[0].bar(x - 2*width, item8_means, width, label='Tide LS')
rects2 = ax[0].bar(x - width, item9_means, width, label='Tide HS')
rects3 = ax[0].bar(x, item1_means, width, label='Ariel LS')
rects4 = ax[0].bar(x + width, item45_means, width, label='Omo (LS and HS)')
rects5 = ax[0].bar(x + 2*width, item67_means, width, label='Persil (LS and HS)')

rects1b = ax[1].bar(x - 2*width, item8_means_ag, width, label='Tide LS')
rects2b = ax[1].bar(x - width, item9_means_ag, width, label='Tide HS')
rects3b = ax[1].bar(x, item1_means_ag, width, label='Ariel LS')
rects4b = ax[1].bar(x + width, item45_means_ag, width, label='Omo (LS and HS)')
rects5b = ax[1].bar(x + 2*width, item67_means_ag, width, label='Persil (LS and HS)')

xmin=0.00
xmax=1.80

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])


ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean score')
ax[0].set_xticks(x)
ax[0].set_xticklabels(labels)
ax[1].set_yticks([])
ax[1].set_xticks([])
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height])
ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products_combo2'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% comparison of products (after initial data analysis, combo1)

labels = ['All products (excluding Xtra)']
#item8_means = [1.447, 1.447, 1.452, 1.372]
#item9_means = [1.417, 1.447, 1.425, 1.372]
#item1_means = [1.337, 1.366, 1.345, 1.363]
#item45_means = [1.316,1.346,1.324,1.342]
#item67_means = [1.072,1.098,1.079,1.098]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(19,12))
rects1 = ax[0].bar(x - 4*width, 1.763, width, label='Bonux HS')
rects2 = ax[0].bar(x - 3*width, 1.735, width, label='Ariel HS')
rects3 = ax[0].bar(x -2*width, 1.422, width, label='Tide HS')
rects4 = ax[0].bar(x - width, 1.411, width, label='Omo LS')
rects5 = ax[0].bar(x , 1.400, width, label='Tide LS')
rects6 = ax[0].bar(x + 1*width, 1.337, width, label='Ariel LS')
rects7 = ax[0].bar(x + 2*width, 1.227, width, label='Omo HS')
rects8 = ax[0].bar(x + 3*width, 1.101, width, label='Persil LS')
rects9 = ax[0].bar(x + 4*width, 0.974, width, label='Persil HS')


rects1 = ax[1].bar(x - 4*width, 1.508, width, label='Bonux HS')
rects2 = ax[1].bar(x - 3*width, 1.291, width, label='Ariel HS')
rects3 = ax[1].bar(x -2*width, 1.283, width, label='Tide HS')
rects4 = ax[1].bar(x - width, 1.422, width, label='Omo LS')
rects5 = ax[1].bar(x , 1.421, width, label='Tide LS')
rects6 = ax[1].bar(x + 1*width, 1.724, width, label='Ariel LS')
rects7 = ax[1].bar(x + 2*width, 1.246, width, label='Omo HS')
rects8 = ax[1].bar(x + 3*width, 1.330, width, label='Persil LS')
rects9 = ax[1].bar(x + 4*width, 0.945, width, label='Persil HS')

xmin=0.00
xmax=1.80

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])

ax[0].set_ylabel('Mean score')

ax[0].set_xticks([])
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[0].set_xticklabels(labels)

#ax.legend()

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height])
ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products_combo1'
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
item4_means = [1.431,1.475,1.442,1.377]
item1_means = [1.372,1.335,1.106,1.207]
item8_means = [1.35,1.672,1.137,1.421]
item5_means = [1.21,1.356,1.296,1.145]
item9_means = [1.047,1.754,1.432,1.624]
item7_means = [0.93,1.101,1.432,1.119]

item2_means_ag = [1.25,1.273,1.303,1.272]
item4_means_ag = [1.476,1.388,1.425,1.421]
item1_means_ag = [1.713,1.697,2.016,1.963]
item8_means_ag = [1.082,1.469,1.394,1.265]
item5_means_ag = [1.384,1.457,1.344,1.236]
item9_means_ag = [1.291,1.437,1.298,1.364]
item7_means_ag = [1.46,1.285,1.298,1.502]

#where the samples correspond to the same ones used in the ratings analysis with combo4
item2_means_ag2 = [1.747,1.594,1.687,1.611]
item4_means_ag2 = [1.575,1.193,1.541,1.507]
item1_means_ag2 = [1.828,1.614,1.443,1.449]
item8_means_ag2 = [1.551,1.697,1.283,1.692]
item5_means_ag2 = [1.467,1.193,1.311,1.295]
item9_means_ag2 = [1.112,1.446,1.16,1.552]
item7_means_ag2 = [1.234,1.09,1.256,1.15]

x = np.arange(len(labels))  # the label locations
width = 0.1  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(21,12))
rects1 = ax[0].bar(x - 3*width, item2_means, width, label='Ariel HS')
rects2 = ax[0].bar(x - 2*width, item4_means, width, label='Omo LS')
rects3 = ax[0].bar(x-width, item1_means, width, label='Ariel LS')
rects4 = ax[0].bar(x, item8_means, width, label='Tide LS')
rects5 = ax[0].bar(x + width, item5_means, width, label='Omo HS')
rects6 = ax[0].bar(x + 2*width, item9_means, width, label='Tide HS')
rects7 = ax[0].bar(x + 3*width, item7_means, width, label='Persil LS')

rects1 = ax[1].bar(x - 3*width, item2_means_ag2, width, label='Ariel HS')
rects2 = ax[1].bar(x - 2*width, item4_means_ag2, width, label='Omo LS')
rects3 = ax[1].bar(x-width, item1_means_ag2, width, label='Ariel LS')
rects4 = ax[1].bar(x, item8_means_ag2, width, label='Tide LS')
rects5 = ax[1].bar(x + width, item5_means_ag2, width, label='Omo HS')
rects6 = ax[1].bar(x + 2*width, item9_means_ag2, width, label='Tide HS')
rects7 = ax[1].bar(x + 3*width, item7_means_ag2, width, label='Persil LS')

xmin=0.00
xmax=2.05

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])

ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean score')

ax[0].set_xticks(x)
ax[0].set_xticklabels(labels)
ax[1].set_xticks([])
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

figname = 'products_combo42'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()
