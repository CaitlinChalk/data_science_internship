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
item9_means = [1.417, 1.447, 1.425, 1.372]
item1_means = [1.337, 1.366, 1.345, 1.363]
item45_means = [1.316,1.346,1.324,1.342]
item67_means = [1.072,1.098,1.079,1.098]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots(figsize=cm2inch(14,9))
rects1 = ax.bar(x - 2*width, item8_means, width, label='Tide LS')
rects2 = ax.bar(x - width, item9_means, width, label='Tide HS')
rects3 = ax.bar(x, item1_means, width, label='Ariel LS')
rects4 = ax.bar(x + width, item45_means, width, label='Omo (LS and HS)')
rects5 = ax.bar(x + 2*width, item67_means, width, label='Persil (LS and HS)')

ax.set_ylabel('Mean score')
#ax.set_title('A comparison of laundry product mean scores')
ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products1'
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

fig, ax = plt.subplots(figsize=cm2inch(14,9))
rects1 = ax.bar(x - 4*width, 1.763, width, label='Bonux HS')
rects2 = ax.bar(x - 3*width, 1.735, width, label='Ariel HS')
rects3 = ax.bar(x -2*width, 1.422, width, label='Tide HS')
rects4 = ax.bar(x - width, 1.411, width, label='Omo LS')
rects5 = ax.bar(x , 1.400, width, label='Tide LS')
rects6 = ax.bar(x + 1*width, 1.337, width, label='Ariel LS')
rects7 = ax.bar(x + 2*width, 1.227, width, label='Omo HS')
rects8 = ax.bar(x + 3*width, 1.101, width, label='Persil LS')
rects9 = ax.bar(x + 4*width, 0.974, width, label='Persil HS')

ax.set_ylabel('Mean score')
#ax.set_title('A comparison of laundry product mean scores')
ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'products2'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

