# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:12:25 2019

@author: matcc
#converts structured data into format required for RUMM input
Contains: convert2RUMM
"""

#Ignores NaN responses - modification is required when missing data is referred to by something other than NaN 
#INPUT: 1) data_old - questionnaire style data frame, organised into columns
#       2) id1 - id1 = 1: corresponds to responses with text and numbers (e.g. excellent 5). In this case, the 'remove_text' 
#                    function is applied to remove all text from each response (e.g. leaving 5 only)
#                id1 = 0: remove_text is not called
#RETURNS: 1) data_RUMM - data in format for RUMM software - each response labelled in unit intervals, starting from 0
#         2) output_key - key to define replaced responses, with the quantity of each response (in brackets)

#NOTE: if data is organised into statements with corresponding numbers, run the "remove_text" function first
#if data consists of text only, and the item order is important, this function should be modifed to allow for manual ordering of items
import numpy as np
import pandas as pd
from data_manipulation import remove_text

def convert2RUMM (data_old,id1): 
    nd = data_old.ndim #dimension of data - series (1) or data frame (>1)
    data_RUMM = data_old.copy() #copy old data to RUMM data
    if nd == 1: #series data
        if id1 == 1:  #remove all text from data if id1 = 1          
            original_key = remove_text(data_RUMM) #get original key (i.e. before text was removed), for the output key
        unique_list = np.unique(data_RUMM, return_counts=True) #list of distinct responses (facets, person factors or items), with quantity of each
        response_list0 = unique_list[0] #unique responses
        counts = unique_list[1] #corresponding quantity of each response      
        response_list = response_list0[~pd.isnull(response_list0)] #remove NaN responses
        counts = counts[~pd.isnull(response_list0)] #removing counts corresponding to NaN responses
        response_dict = {} #initialise dictionary to replace responses with integers
        response_key = {} #initialise dictionary to define the key for each replacement 
        quantity = {} #dictionary to store quantity of each replaced reponse (outputs in a separate column when input data has 1 dimesnion)
        for i in range(len(response_list)):
            response_dict[response_list[i]] = i #create dictionary to redefine responses as integers
            #create key for reference: contains response and quantity of each
            if id1 == 0: #when no text has been removed  
                response_key[i] = str(response_list[i])  + ' ' + '(' + str(counts[i]) + ')' 
            else: #if text was removed, use the original responses in the output key
                response_key[i] = str(original_key[response_list[i]])  + ' ' + '(' + str(counts[i]) + ')' 
            quantity[i] = str(counts[i])
        data_RUMM.replace(response_dict, inplace=True) #replace responses in series with the corresponding integers
        output_key  = pd.Series(response_key, name=data_old.name) #Series containing key for replaced responses
        output_key = pd.concat([output_key, pd.Series(quantity, name='Quantity')],axis=1)
    else:  #data frame         
        for j in range(len(data_RUMM.columns)): #loop through all columns in data
            if id1 == 1:            
                original_key = remove_text(data_RUMM.iloc[:,j]) #remove all text from data if id1 = 1 (deals with each column separately)
            unique_list = np.unique(data_RUMM.iloc[:,j], return_counts=True)  #list of distinct responses in each column
            response_list0 = unique_list[0]
            counts = unique_list[1]
            response_list = response_list0[~pd.isnull(response_list0)] #remove NaNs 
            counts = counts[~pd.isnull(response_list0)]  
            if j == 0:
                response_dict = {} #initialise dictionary 
                response_key = {}   #initialise key        
            for i in range(len(response_list)):
                if not response_list[i] in response_dict:
                    key = len(response_dict)
                    response_dict[response_list[i]] = key #create dictionary to redefine responses as integers (for reference purposes)
                    if id1 == 0: #no text has been removed
                        response_key[key] = str(response_list[i])  + ' ' + '(' + str(counts[i]) + ')'
                    else: #text has been removed
                        response_key[key] = str(original_key[response_list[i]])  + ' ' + '(' + str(counts[i]) + ')' 
                    
            data_RUMM.iloc[:,j].replace(response_dict, inplace=True) #replace responses in data frame column with the corresponding integers
            Series0 = pd.Series(response_key,name=data_old.columns[j]) #create series for each column of data           
            if j == 0:
                output_key = Series0 #add first series to output key
            else:
                output_key = pd.concat([output_key,Series0], axis=1) #concatenate each series into one data frame, containing key for each replacement
        
    return data_RUMM, output_key

#To do: generalise incase missing data isn't represented by NaN.
#The following code could be used to replace digits (999 in this example), but it doesn't seem to work when trying to replace NaNs
#response_list = np.delete(response_list0, np.argwhere(response_list0 == 999))
#counts = np.delete(counts, np.argwhere(response_list0 == 999))



            
