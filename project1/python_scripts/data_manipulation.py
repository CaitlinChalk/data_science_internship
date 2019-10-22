# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:27:57 2019 

@author: matcc
script containing functions to manipulate data
contains: remove_text, remove_extremes
"""

#function calls
import numpy as np
import pandas as pd
import re

#function that removes text in each data cell, leaving behind only the digits (positive or negative)
#INPUT: data to remove text
#OUTPUT: edited data
#RETURN: dictionary containing replacement info
def remove_text(data):
    items = np.unique(data) #list of unique items in data
    txt2dig_dict = {} #initialse dictionary to define replacements
    txt2dig_dict_out = {} #initialise dictionary for output
    for i in range(len(items)):
        text = items[i] #distinct string found in data cell
        find = re.findall(r'-?\d+',text) #extracts digits (positive and negative) in string
        if (len(find) == 0):
            print('There are no digits in data cell', i, 'for the following item:', data.name)
            break
        digit = int(find[0]) #convert to digit
        txt2dig_dict[text] = digit #create replacement dictionary  
        txt2dig_dict_out[digit] = text #output replacement dictionary (it's easier to work with this format, as opposed to the line above)
    data.replace(txt2dig_dict, inplace=True) #replace all data entries according to the dictionary
    
    return txt2dig_dict_out

#function to remove extreme data, defined as the persons who select the same answer at the extreme end (i.e. all 5s or all 0s) for all options
#Note - these persons can't be placed on the Rasch analysis scale
#INPUT: data for removal of extreme persons, and corresponding identifiers for each person
#RETURN: data with removed extremes, list of extreme person IDs with their corresponding selected score (for all questions) 
def remove_extremes(data,id1):
    data_new = data.copy() #copy old data to new 
    #initialise extreme_info
    cols = {'Extreme person ID', 'test ID', 'Selected score'}
    extreme_info = pd.DataFrame([],columns=cols)
    for i in range(len(data)):
        row = data.iloc[i,:] #each row corresponds to each person
        min1 = min(data.min(axis=1)) #minimum value 
        max1 = max(data.max(axis=1)) #maximum value
        if len(set(row)) == 1: #if row contains only one element
            if row[0] == min1 or row[0] == max1:  #if selected element is an extreme (either a min or max)              
                data_new.drop(i, axis=0, inplace=True) #delete that row from data new
                person = id1[i]
                id2 = i+1
                value = row[0]
                Data0 = pd.DataFrame([[person,id2,value]],columns=cols)
                extreme_info = extreme_info.append(Data0, ignore_index=True)
            
    return data_new, extreme_info
            
            

    