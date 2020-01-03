# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:27:57 2019 

@author: matcc
script containing functions to manipulate data
contains: remove_text, remove_extremes, ammend_facet_key
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
    #option argument - persons: an additional list of people to remove from the data. If it isn't provided, no extra people are removed
    #Note - factor can be facets of person factors (for the removal of corresponding extreme person data)
#RETURN: data with removed extremes, list of extreme person IDs with their corresponding selected score (for all questions) 
def remove_extremes(data,id1,factor,persons = []):
    data_new = data.copy() #copy old data to new 
    id_new = id1.copy()
    factor_new = factor.copy()
    #initialise extreme_info
    min_row = data.min(axis=0) #row corresponding to participant selecting lowest scores for all questions
    max_row = data.max(axis=0) #row corresponding to participant selecting highest scores for all questions
    #remove extreme rows from the data
    data_new = data.loc[(data!=min_row).any(axis=1)] 
    data_new = data_new.loc[(data_new!=max_row).any(axis=1)]
    #remove id, PFs, facets corresponding to the extreme rows
    id_new = id_new.loc[(data!=min_row).any(axis=1)]
    id_new = id_new.loc[(data!=max_row).any(axis=1)]
    factor_new = factor_new.loc[(data!=min_row).any(axis=1)]
    factor_new = factor_new.loc[(data!=max_row).any(axis=1)]    
    #get ids of participants who selected extreme scores (for reference)
    id_extreme = id1 - id_new
    extreme_info = id1.loc[id_extreme.isna()]
    extreme_info.rename('Extreme person ID',inplace=True)
    #remove additional persons, if a list is provided as an argument. Otherwise, no extra persons will be removed
    person_index = id1.isin(persons)[id1.isin(persons)==True].index #index of extra persons to be removed (if the argument is passed)
    data_new.drop(person_index, axis=0, inplace=True)
    id_new.drop(person_index, axis=0, inplace=True)
    factor_new.drop(person_index, axis=0, inplace=True)
    
    return data_new, id_new, factor_new, extreme_info
            
#function to ammend facet quantities (with extremes removed) 
#INPUT: old facet list, old facet key, IDs of extreme persons
#OUTPUT: new facet key with ammended quantities with extreme persons removed
def ammend_facet_key(facets_old,key,ID): 
    key_new = key.copy()
    extrm_facets = facets_old.iloc[ID.values-1] #facets associated with extreme people
#******** N.B. in this case, the person IDs range from 1-999, and the facets were ordered accordingly (from 0-998). 
#The line of code above will need ammending if this isn't the case ********
    extrm_facet_list = np.unique(extrm_facets, return_counts=True)[0] #list of distinct facets (corresponding to extreme persons)
    extrm_facet_count = np.unique(extrm_facets, return_counts=True)[1] #number of each extreme person
    extreme_facet_out = {} #initialise key for output information
    col_name = key.columns[1] #second column of key = original facet quantity
    for i in range(len(extrm_facet_list)):
        facet = extrm_facet_list[i] #facet associated with extreme person
        n_removes = extrm_facet_count[i] #number of extreme persons the facet is associated with
        old_value = key_new.loc[facet,col_name] #original facet quantity
        key_new.replace({key_new.loc[facet,col_name]:int(old_value)-n_removes}, inplace=True) #reduce original quantity by number of extreme persons
        extreme_facet_out['Facet '+str(facet+1)] = str(n_removes) + ' removed' #output information
        
    return key_new, extreme_facet_out            

    