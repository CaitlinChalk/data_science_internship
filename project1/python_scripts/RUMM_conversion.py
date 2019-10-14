# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:12:25 2019

@author: matcc
function to convert structured data into format required for RUMM input 
input: questionnaire style data, organised into columns
output: data in format for RUMM software - each response labelled in unit intervals, starting from 0
NOTE: if data is organised into statements with corresponding numbers, run the "remove_text" function first
if data consists of text only, and the item order is important, this function should be modifed to allow for manual ordering of items
"""

import numpy as np
import pandas as pd

def convert2RUMM (data_old,data_RUMM): 
    nd = data_old.ndim #dimension of data - series (1) or data frame (>1)
    if nd == 1: #series data
        response_list = np.unique(data_old) #list of distinct responses (facets, person factors or items)
        response_list = response_list[~pd.isnull(response_list)] #remove NaNs 
        response_dict = {} #initialise dictionary
        for i in range(len(response_list)):
            response_dict[response_list[i]] = i #create dictionary to redefine responses as integers
            
        data_RUMM.replace(response_dict, inplace=True) #replace responses in series with the corresponding integers
        
    else:  #data frame      
        for j in range(len(data_old.columns)): #loop through all columns in data
            response_column = data_old.iloc[:,j] #convert each column separately (each column corresponds to different data/responses)
            response_list = np.unique(response_column)  #list of distinct responses
            response_list = response_list[~pd.isnull(response_list)] #remove NaNs 
            response_dict = {} #initialise dictionary
            for i in range(len(response_list)):
                response_dict[response_list[i]] = i #create dictionary to redefine responses as integers
        
            data_RUMM.loc[:,j].replace(response_dict, inplace=True) #replace responses in data frame column with the corresponding integers
            
#To do: generalise incase missing data isn't represented by NaN