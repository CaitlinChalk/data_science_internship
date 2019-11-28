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

#%% nationality
labels = ['','Rep. 1', 'Rep. 2']
saudi_means = [1.62,1.611,1.49]
other_means = [1.484,1.438,1.312]
eqypt_means = [1.068,0.987,0.99]

saudi_means_ag = [1.423,1.419,1.343]
other_means_ag = [1.528,1.241,1.533]
eqypt_means_ag = [1.34,1.277,1.305]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(2,2,figsize=cm2inch(21,12))

rects1 = ax[0,0].bar(- 1.5*width, 1.505, width, label='Saudi')
rects2 = ax[0,0].bar(0, 1.29, width, label='Other')
rects3 = ax[0,0].bar(1.5*width, 0.936, width, label='Eqyptian')

rects1b = ax[0,1].bar( - 1.5*width, 1.42, width, label='Saudi (428, 428)')
rects2b = ax[0,1].bar(0, 1.425, width, label='Other (175, 159)')
rects3b = ax[0,1].bar(1.5*width, 1.289, width, label='Eqyptian (109, 101)')

rects1 = ax[1,0].bar(x - width, saudi_means, width, label='Saudi')
rects2 = ax[1,0].bar(x, other_means, width, label='Other')
rects3 = ax[1,0].bar(x+width, eqypt_means, width, label='Eqyptian')

rects1b = ax[1,1].bar(x - width, saudi_means_ag, width, label='Saudi (109, 101)')
rects2b = ax[1,1].bar(x, other_means_ag, width, label='Other (109, 101)')
rects3b = ax[1,1].bar(x+width, eqypt_means_ag, width, label='Eqyptian (109, 101)')


xmin=0.00
xmax=1.65

ax[0,1].set_ylim([xmin,xmax])
ax[1,1].set_ylim([xmin,xmax])
ax[0,0].set_ylim([xmin,xmax])
ax[1,0].set_ylim([xmin,xmax])


ax[0,0].set_title('Ratings')
ax[0,1].set_title('Agreements')

ax[0,0].set_ylabel('Mean score')

ax[0,1].set_yticks([])
ax[1,0].set_yticks([])
ax[1,1].set_yticks([])

ax[0,0].set_xticks([])
ax[0,1].set_xticks([])
#ax[1,0].set_xticks([])
ax[1,1].set_xticks([])
ax[1,0].set_xticks(x)
ax[1,0].set_xticklabels(labels)
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[0,1].get_position()
ax[0,1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

box = ax[1,1].get_position()
ax[1,1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'nationality_combo2'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% employment
labels = ['','Rep. 1', 'Rep. 2']
ft_means = [1.74,1.55,1.763]
se_means = [1.436,1.429,1.409]
pt_means = [1.265,1.363,1.302]
pa_means = [1.149,0.968,1.105]
un_means = [1.056,1.334,1.493]
st_means = [1.02,1.034,1.072]

ft_means_ag = [1.407,1.313,1.753]
se_means_ag = [0.961,0.907,0.987]
pt_means_ag = [1.158,1.102,1.121]
pa_means_ag = [1.174,1.384,1.25]
un_means_ag = [1.164,1.072,1.285]
st_means_ag = [1.371,1.318,1.337]



x = np.arange(len(labels))  # the label locations
width = 0.12  # the width of the bars

fig, ax = plt.subplots(2,2,figsize=cm2inch(21,12))

rects1 = ax[0,0].bar(- 1.5*width, 1.707, width, label='Full time')
rects2 = ax[0,0].bar(0, 1.432, width, label='Unemployed')
rects3 = ax[0,0].bar(1.5*width, 1.163, width, label='Parent')

rects1b = ax[0,1].bar( - 1.5*width, 1.808, width, label='Full time (214, 235)')
rects2b = ax[0,1].bar(0, 1.297, width, label='Unemployed (194, 185)')
rects3b = ax[0,1].bar(1.5*width, 1.353, width, label='Parent (131, 125)')

rects1 = ax[1,0].bar(x - 3*width, ft_means, width, label='Full time')
rects2 = ax[1,0].bar(x-2*width, se_means, width, label='')
rects2 = ax[1,0].bar(x-width, pt_means, width, label='')
rects3 = ax[1,0].bar(x, pa_means, width, label='')
rects3 = ax[1,0].bar(x+width, un_means, width, label='')
rects3 = ax[1,0].bar(x+2*width, st_means, width, label='')

rects1 = ax[1,1].bar(x - 3*width, ft_means_ag, width, label='Full time (52, 53)')
rects2 = ax[1,1].bar(x-2*width, se_means_ag, width, label='Self employed (52, 53)')
rects2 = ax[1,1].bar(x-width, pt_means_ag, width, label='Part time (52, 53)')
rects3 = ax[1,1].bar(x, pa_means_ag, width, label='Parent (52, 53)')
rects3 = ax[1,1].bar(x+width, un_means_ag, width, label='Unemployed (52, 53)')
rects3 = ax[1,1].bar(x+2*width, st_means_ag, width, label='Student (52, 53)')


xmin=0.00
xmax=1.85

ax[0,1].set_ylim([xmin,xmax])
ax[1,1].set_ylim([xmin,xmax])
ax[0,0].set_ylim([xmin,xmax])
ax[1,0].set_ylim([xmin,xmax])


ax[0,0].set_title('Ratings')
ax[0,1].set_title('Agreements')

ax[0,0].set_ylabel('Mean score')

ax[0,1].set_yticks([])
ax[1,0].set_yticks([])
ax[1,1].set_yticks([])

ax[0,0].set_xticks([])
ax[0,1].set_xticks([])
#ax[1,0].set_xticks([])
ax[1,1].set_xticks([])
ax[1,0].set_xticks(x)
ax[1,0].set_xticklabels(labels)
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[0,1].get_position()
ax[0,1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

box = ax[1,1].get_position()
ax[1,1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

fig.tight_layout()

figname = 'employment_combo'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()


