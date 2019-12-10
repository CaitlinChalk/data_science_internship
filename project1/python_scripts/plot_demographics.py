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
egypt_means = [1.068,0.987,0.99]

e_saudi_means = [1.61,1.59,1.51]
e_other_means = [1.32,1.41,1.45]
e_egypt_means = [1.23,1.22,1.23]

saudi_means_ag = [1.51,1.58,1.476]
other_means_ag = [1.381,1.421,1.4]
egypt_means_ag = [1.349,1.369,1.343]

e_saudi_means_ag = [1.3,1.36,1.39]
e_other_means_ag = [1.23,1.22,1.26]
e_eqypt_means_ag = [1.16,1.22,1.24]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(2,2,figsize=cm2inch(21,12))

rects1 = ax[0,0].bar(- 1.5*width, 1.505, width, label='Saudi')
rects2 = ax[0,0].bar(0, 1.29, width, label='Other')
rects3 = ax[0,0].bar(1.5*width, 0.936, width, label='Egyptian')

rects1b = ax[0,1].bar( - 1.5*width, 1.42, width, label='Saudi (428, 453)')
rects2b = ax[0,1].bar(0, 1.425, width, label='Other (175, 165)')
rects3b = ax[0,1].bar(1.5*width, 1.289, width, label='Egyptian (109, 111)')

rects1 = ax[1,0].bar(x - width, saudi_means, width, label='Saudi',yerr = e_saudi_means)
rects2 = ax[1,0].bar(x, other_means, width, label='Other',yerr = e_other_means)
rects3 = ax[1,0].bar(x+width, egypt_means, width, label='Egyptian',yerr = e_egypt_means)

rects1b = ax[1,1].bar(x - width, saudi_means_ag, width, label='Saudi (109, 111)',yerr = e_saudi_means_ag)
rects2b = ax[1,1].bar(x, other_means_ag, width, label='Other (109, 111)',yerr = e_other_means_ag)
rects3b = ax[1,1].bar(x+width, egypt_means_ag, width, label='Egyptian (109, 111)',yerr = e_egypt_means)


xmin=0.00
xmax=1.65

#ax[0,1].set_ylim([xmin,xmax])
#ax[1,1].set_ylim([xmin,xmax])
#ax[0,0].set_ylim([xmin,xmax])
#ax[1,0].set_ylim([xmin,xmax])


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

#plt.savefig('Figures/'+figname+'.pdf')
#plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% employment
labels = ['','Rep. 1', 'Rep. 2']
ft_means = [1.74,1.55,1.763]
se_means = [1.436,1.429,1.409]
pt_means = [1.265,1.363,1.302]
pa_means = [1.149,0.968,1.105]
un_means = [1.056,1.334,1.493]
st_means = [1.02,1.034,1.072]

ft_means_ag = [1.822,1.734,1.718]
se_means_ag = [0.867,0.858,0.796]
pt_means_ag = [1.173,1.177,1.117]
pa_means_ag = [1.337,1.208,1.21]
un_means_ag = [1.214,0.996,1.118]
st_means_ag = [1.319,1.333,1.292]



x = np.arange(len(labels))  # the label locations
width = 0.12  # the width of the bars

fig, ax = plt.subplots(2,2,figsize=cm2inch(21,12))

rects1 = ax[0,0].bar(- 1.5*width, 1.707, width, label='Full time')
rects2 = ax[0,0].bar(0, 1.432, width, label='Unemployed')
rects3 = ax[0,0].bar(1.5*width, 1.163, width, label='Parent')

rects1b = ax[0,1].bar( - 1.5*width, 1.808, width, label='Full time (214, 235)')
rects2b = ax[0,1].bar(0, 1.297, width, label='Unemployed (131, 125)')
rects3b = ax[0,1].bar(1.5*width, 1.353, width, label='Parent (194, 185)')

rects1 = ax[1,0].bar(x - 3*width, ft_means, width, label='Full time')
rects2 = ax[1,0].bar(x-2*width, se_means, width, label='')
rects2 = ax[1,0].bar(x-width, pt_means, width, label='')
rects3 = ax[1,0].bar(x, pa_means, width, label='')
rects3 = ax[1,0].bar(x+width, un_means, width, label='')
rects3 = ax[1,0].bar(x+2*width, st_means, width, label='')

rects1 = ax[1,1].bar(x - 3*width, ft_means_ag, width, label='Full time (52, 58)')
rects2 = ax[1,1].bar(x-2*width, se_means_ag, width, label='Self employed (52, 58)')
rects2 = ax[1,1].bar(x-width, pt_means_ag, width, label='Part time (52, 58)')
rects3 = ax[1,1].bar(x, pa_means_ag, width, label='Parent (52, 58)')
rects3 = ax[1,1].bar(x+width, un_means_ag, width, label='Unemployed (52, 58)')
rects3 = ax[1,1].bar(x+2*width, st_means_ag, width, label='Student (52, 58)')


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

#%% no children
labels = ['','Rep. 1', 'Rep. 2']
a2_means = [1.507,1.483,1.536]
a1_means = [1.391,1.432,1.387]
a3_means = [1.249,1.292,1.275]
a0_means = [1.251,1.271,1.222]


a2_means_ag = [1.484,1.364,1.736]
a1_means_ag = [1.329,1.36,1.298]
a3_means_ag = [1.395,1.3,1.234]
a0_means_ag = [1.118,1.124,1.111]



x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(2,2,figsize=cm2inch(21,12))

rects1 = ax[0,0].bar(-1.5*width, 1.492, width, label='Two')
rects2 = ax[0,0].bar(0, 1.383, width, label='One')
rects3 = ax[0,0].bar(1.5*width, 1.252, width, label='Three plus')
rects3 = ax[0,0].bar(3*width, 1.238, width, label='None')

rects1 = ax[0,1].bar(- 1.5*width, 1.601, width, label='Two (246, 248)')
rects2 = ax[0,1].bar(0, 1.392, width, label='One (176, 168)')
rects3 = ax[0,1].bar(1.5*width, 1.275, width, label='Three plus (162, 180)')
rects3 = ax[0,1].bar(3*width, 1.13, width, label='None (128, 133)')

rects1 = ax[1,0].bar(x - 2*width, a2_means, width, label='')
rects2 = ax[1,0].bar(x-width, a1_means, width, label='')
rects2 = ax[1,0].bar(x, a3_means, width, label='')
rects3 = ax[1,0].bar(x+width , a0_means, width, label='')


rects1 = ax[1,1].bar(x - 2*width, a2_means_ag, width, label='Two (128, 133)')
rects2 = ax[1,1].bar(x-width, a1_means_ag, width, label='One (128, 133)')
rects2 = ax[1,1].bar(x, a3_means_ag, width, label='Three plus (128, 133)')
rects3 = ax[1,1].bar(x + width, a0_means_ag, width, label='None (128, 133)')


xmin=0.00
xmax=1.8

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

figname = 'nochildren_combo'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()


