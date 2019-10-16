# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:27:57 2019

@author: matcc
script containing functions to manipulate data
INPUT: data to remove text
OUTPUT: edited data
RETURN: dictionary containing replacement info
"""

#function calls
import numpy as np
import re

#function that removes text in each data cell, leaving behind only the digits (positive or negative)
def remove_text(data):
    items = np.unique(data) #list of unique items in data
    txt2dig_dict = {} #initialse dictionary to define replacements
    txt2dig_dict_out = {} #initialise dictionary for output
    for i in range(len(items)):
        text = items[i] #distinct string found in data cell
        find = re.findall(r'-?\d+',text) #extracts digits (positive and negative) in string
        digit = int(find[0]) #convert to digit
        txt2dig_dict[text] = digit #create replacement dictionary  
        txt2dig_dict_out[digit] = text #output replacement dictionary (it's easier to work with this format, as opposed to the line above)
    data.replace(txt2dig_dict, inplace=True) #replace all data entries according to the dictionary
    
    return txt2dig_dict_out
    