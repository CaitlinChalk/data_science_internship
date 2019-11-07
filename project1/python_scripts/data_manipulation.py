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
#RETURN: data with removed extremes, list of extreme person IDs with their corresponding selected score (for all questions) 
def remove_extremes(data,id1,PFs,persons = []):
    data_new = data.copy() #copy old data to new 
    id_new = id1.copy()
    PFs_new = PFs.copy()
    #initialise extreme_info
    cols = {'Extreme person ID', 'test ID', 'Selected score'}
    extreme_info = pd.DataFrame([],columns=cols)
    k=-1
    for i in range(len(data)):
        k=k+1
        row = data.iloc[i,:] #each row corresponds to each person
        min1 = min(data.min(axis=1)) #minimum value 
        max1 = max(data.max(axis=1)) #maximum value
        if len(set(row)) == 1: #if row contains only one element
           if row.iloc[0] == min1 or row.iloc[0] == max1:  #if selected element is an extreme (either a min or max)              
               data_new.drop(data_new.index[k], axis=0, inplace=True) #delete that row from data_new
               id_new.drop(id_new.index[k], axis=0, inplace=True) #delete corresponding person from id_new
               PFs_new.drop(PFs_new.index[k], axis=0, inplace=True)
               k=k-1 #reduce index because one row has been deleted in data_new
               person = id1.iloc[i]
               id2 = i+1
               value = row.iloc[0]
               Data0 = pd.DataFrame([[person,id2,value]],columns=cols)
               extreme_info = extreme_info.append(Data0, ignore_index=True)
    person_index = id1.isin(persons)[id1.isin(persons)==True].index #index of extra persons to be removed (if the argument is passed)
    data_new.drop(person_index, axis=0, inplace=True)
    id_new.drop(person_index, axis=0, inplace=True)
    PFs_new.drop(person_index, axis=0, inplace=True)
    
    return data_new, id_new, PFs_new, extreme_info
            
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

    