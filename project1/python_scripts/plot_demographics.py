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
e_egypt_means_ag = [1.16,1.22,1.24]

#x = np.arange(len(labels))  # the label locations
x = [1,2,3]
width = 0.25  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(19,12))

#rects1 = ax[0].bar(x - width, saudi_means, width, label='Saudi',yerr = e_saudi_means)
#rects2 = ax[0].bar(x, other_means, width, label='Other',yerr = e_other_means)
#rects3 = ax[0].bar(x+width, egypt_means, width, label='Egyptian',yerr = e_egypt_means)

#rects1b = ax[1].bar(x - width, saudi_means_ag, width, label='Saudi (109, 111)',yerr = e_saudi_means_ag)
#rects2b = ax[1].bar(x, other_means_ag, width, label='Other (109, 111)',yerr = e_other_means_ag)
#rects3b = ax[1].bar(x+width, egypt_means_ag, width, label='Egyptian (109, 111)',yerr = e_egypt_means)


ax[0].errorbar(x,saudi_means, marker="o",yerr=e_saudi_means, capsize=10, label='Saudi (109, 111)')
ax[0].errorbar(x,other_means, marker="o",yerr=e_other_means, capsize=10, label='Other (109, 111)')
ax[0].errorbar(x,egypt_means, marker="o",yerr=e_egypt_means, capsize=10, label='Egyptian (109, 111)')

ax[1].errorbar(x,saudi_means_ag, marker="o",yerr=e_saudi_means_ag, capsize=10, label='Saudi (109, 111)')
ax[1].errorbar(x,other_means_ag, marker="o",yerr=e_other_means_ag, capsize=10, label='Other (109, 111)')
ax[1].errorbar(x,egypt_means_ag, marker="o",yerr=e_egypt_means_ag, capsize=10, label='Egyptian (109, 111)')

xmin=-0.3
xmax=3.5

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])
#ax[0,0].set_ylim([xmin,xmax])
#ax[1,0].set_ylim([xmin,xmax])


ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean person location')
ax[0].set_xlabel('Test')

ax[1].set_yticks([])

ax[1].set_xticks([])
ax[0].set_xticks(x)
#ax[0].set_xticklabels(labels)
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0 + box.height*0.0, box.width, box.height*0.9])
    
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.),
      fancybox=True, shadow=True)

fig.tight_layout()

figname = 'nationality_combo2'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% employment
labels = ['','Rep. 1', 'Rep. 2']
ft_means = [1.74,1.55,1.763]
e_ft_means = [1.24,1.56,1.36]
se_means = [1.436,1.429,1.409]
e_se_means = [1.3,1.33,1.38]
pt_means = [1.265,1.363,1.302]
e_pt_means = [1.25,1.23,1.25]
pa_means = [1.149,0.968,1.105]
e_pa_means = [1.08,1.25,1.36]
un_means = [1.056,1.334,1.493]
e_un_means = [1.48,1.44,1.58]
st_means = [1.02,1.034,1.072]
e_st_means = [1.22,1.24,1.29]

ft_means_ag = [1.822,1.734,1.718]
e_ft_means_ag = [1.19,1.28,1.3]
se_means_ag = [0.867,0.858,0.796]
e_se_means_ag = [1.12,1.16,1.12]
pt_means_ag = [1.173,1.177,1.117]
e_pt_means_ag = [1.3,1.33,1.32]
pa_means_ag = [1.337,1.208,1.21]
e_pa_means_ag = [1.19,1.02,1.21]
un_means_ag = [1.214,0.996,1.118]
e_un_means_ag = [1.18,1.33,1.38]
st_means_ag = [1.319,1.333,1.292]
e_st_means_ag = [1.26,1.29,1.28]



x = [1,2,3]  # the label locations
width = 0.12  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(19,12))


ax[0].errorbar(x,ft_means, marker="o",yerr=e_ft_means, capsize=10, label='Full time (52, 58)')
ax[0].errorbar(x,se_means, marker="o",yerr=e_se_means, capsize=10, label='Full time (52, 58)')
ax[0].errorbar(x,pt_means, marker="o",yerr=e_pt_means, capsize=10, label='Full time (52, 58)')
ax[0].errorbar(x,pa_means, marker="o",yerr=e_pa_means, capsize=10, label='Full time (52, 58)')
ax[0].errorbar(x,un_means, marker="o",yerr=e_un_means, capsize=10, label='Full time (52, 58)')
ax[0].errorbar(x,st_means, marker="o",yerr=e_st_means, capsize=10, label='Full time (52, 58)')


ax[1].errorbar(x,ft_means_ag, marker="o",yerr=e_ft_means_ag, capsize=10, label='Full time (52, 58)')
ax[1].errorbar(x,se_means_ag, marker="o",yerr=e_se_means_ag, capsize=10, label='Self employed (52, 58)')
ax[1].errorbar(x,pt_means_ag, marker="o",yerr=e_pt_means_ag, capsize=10, label='Part time (52, 58)')
ax[1].errorbar(x,pa_means_ag, marker="o",yerr=e_pa_means_ag, capsize=10, label='Parent (52, 58)')
ax[1].errorbar(x,un_means_ag, marker="o",yerr=e_un_means_ag, capsize=10, label='Unemployed (52, 58)')
ax[1].errorbar(x,st_means_ag, marker="o",yerr=e_st_means_ag, capsize=10, label='Student (52, 58)')


xmin=-0.5
xmax=3.2

ax[0].set_ylim([xmin,xmax])
ax[1].set_ylim([xmin,xmax])
#ax[0,0].set_ylim([xmin,xmax])
#ax[1,0].set_ylim([xmin,xmax])


ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean person location')
ax[0].set_xlabel('Test')



#ax[1,0].set_xticklabels([])
#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis

box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0 + box.height*0.0, box.width, box.height*0.9])
    
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
      fancybox=True, shadow=True)

fig.tight_layout()

figname = 'employment_combo'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()

#%% no children
labels = ['','Rep. 1', 'Rep. 2']
a2_means = [1.507,1.483,1.536]
e_a2_means = [1.42,1.35,1.32]
a1_means = [1.391,1.432,1.387]
e_a1_means = [1.29,1.28,1.31]
a3_means = [1.249,1.292,1.275]
e_a3_means = [1.47,1.45,1.45]
a0_means = [1.251,1.271,1.222]
e_a0_means = [1.54,1.56,1.52]


a2_means_ag = [1.484,1.364,1.736]
e_a2_means_ag = [1.2,1.11,1.23] 
a1_means_ag = [1.329,1.36,1.298]
e_a1_means_ag = [1.27,1.3,1.3]
a3_means_ag = [1.395,1.3,1.234]
e_a3_means_ag = [1.25,1.31,1.31]
a0_means_ag = [1.118,1.124,1.111]
e_a0_means_ag = [1.2,1.22,1.24]



x = [1,2,3]  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(1,2,figsize=cm2inch(19,12))


ax[0].errorbar(x,a2_means, marker="o",yerr=e_a2_means, capsize=10, label='Two (128, 133)')
ax[0].errorbar(x,a1_means, marker="o",yerr=e_a1_means, capsize=10, label='One (128, 133)')
ax[0].errorbar(x,a3_means, marker="o",yerr=e_a3_means, capsize=10, label='Three plus (128, 133)')
ax[0].errorbar(x,a3_means, marker="o",yerr=e_a3_means, capsize=10, label='None (128, 133)')

ax[1].errorbar(x,a2_means_ag, marker="o",yerr=e_a2_means_ag, capsize=10, label='Two (128, 133)')
ax[1].errorbar(x,a1_means_ag, marker="o",yerr=e_a1_means_ag, capsize=10, label='One (128, 133)')
ax[1].errorbar(x,a3_means_ag, marker="o",yerr=e_a3_means_ag, capsize=10, label='Three plus (128, 133)')
ax[1].errorbar(x,a3_means_ag, marker="o",yerr=e_a3_means_ag, capsize=10, label='None (128, 133)')


xmin=0.00
xmax=1.8

#ax[0,1].set_ylim([xmin,xmax])
#ax[1,1].set_ylim([xmin,xmax])
#ax[0,0].set_ylim([xmin,xmax])
#ax[1,0].set_ylim([xmin,xmax])


ax[0].set_title('Ratings')
ax[1].set_title('Agreements')

ax[0].set_ylabel('Mean person location')
ax[0].set_xlabel('Test')

ax[1].set_yticks([])
ax[1].set_xticks([])
#ax[1,0].set_xticks([])

ax[0].set_xticks(x)

#ax.legend()

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11.5}
# Put a legend to the right of the current axis
box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0 + box.height*0.0, box.width, box.height*0.9])
    
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.),
      fancybox=True, shadow=True)

fig.tight_layout()

figname = 'nochildren_combo'
matplotlib.rc('font', **font)

plt.savefig('Figures/'+figname+'.pdf')
plt.savefig('Figures/'+figname+'.jpg')

plt.show()


