# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:12:25 2019

@author: matcc
function to convert structured data into format required for RUMM input
Ignores NaN responses - modification is required when missing data is referred to by something other than NaN 
input: questionnaire style data, organised into columns
output: data in format for RUMM software - each response labelled in unit intervals, starting from 0
returns: key to define replaced responses, with the quantity of each response
NOTE: if data is organised into statements with corresponding numbers, run the "remove_text" function first
if data consists of text only, and the item order is important, this function should be modifed to allow for manual ordering of items
"""

import numpy as np
import pandas as pd

def convert2RUMM (data_old,data_RUMM): 
    nd = data_old.ndim #dimension of data - series (1) or data frame (>1)
    if nd == 1: #series data
        unique_list = np.unique(data_old, return_counts=True) #list of distinct responses (facets, person factors or items), with quantity of each
        response_list0 = unique_list[0] #unique responses
        counts = unique_list[1] #corresponding quantity of each response      
        response_list = response_list0[~pd.isnull(response_list0)] #remove NaN responses
        counts = counts[~pd.isnull(response_list0)] #removing counts corresponding to NaN responses
        response_dict = {} #initialise dictionary to replace responses with integers
        response_key = {} #initialise dictionary to define the key for each replacement 
        for i in range(len(response_list)):
            response_dict[response_list[i]] = i #create dictionary to redefine responses as integers
            response_key[i] = response_list[i]  + ' ' + '(' + str(counts[i]) + ')' #create key for reference: contains response and quantity of each
            
        data_RUMM.replace(response_dict, inplace=True) #replace responses in series with the corresponding integers
        output_key  = pd.Series(response_key, name=data_old.name) #dataframe containing key 
        return output_key
        
    else:  #data frame  
        for j in range(len(data_old.columns)): #loop through all columns in data
            response_column = data_old.iloc[:,j] #convert each column separately (each column corresponds to different data/responses)
            unique_list = np.unique(response_column, return_counts=True)  #list of distinct responses
            response_list0 = unique_list[0]
            counts = unique_list[1]
            response_list = response_list0[~pd.isnull(response_list0)] #remove NaNs 
            counts = counts[~pd.isnull(response_list0)]  
            response_dict = {} #initialise dictionary to replace responses with integers
            response_key = {}   #initialise dictionary to define the key for each replacement          
            for i in range(len(response_list)):
                response_dict[response_list[i]] = i #create dictionary to redefine responses as integers
                response_key[i] = str(response_list[i])  + ' ' + '(' + str(counts[i]) + ')' #create reference key
        
            data_RUMM.iloc[:,j].replace(response_dict, inplace=True) #replace responses in data frame column with the corresponding integers
            Series0 = pd.Series(response_key,name=data_old.columns[j]) #create series for each column of data           
            if j == 0:
                output_key = Series0 #add first series to output key
            else:
                output_key = pd.concat([output_key,Series0], axis=1) #concatenate each series into one data frame, containing key for each replacement
        return output_key
            
#To do: generalise incase missing data isn't represented by NaN.
#The following code could be used to replace digits (999 in this example), but it doesn't seem to work when trying to replace NaNs
#response_list = np.delete(response_list0, np.argwhere(response_list0 == 999))
#counts = np.delete(counts, np.argwhere(response_list0 == 999))