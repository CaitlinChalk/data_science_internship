"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import os

os.chdir("C:\\Users\\Caitlin\\Documents\\data_science_internship\\project1\\python_scripts")

import pandas as pd
import numpy as np
from scipy import stats
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text
from data_manipulation import remove_extremes
from string import ascii_lowercase
import random
import math

data = pd.read_excel('../data/fragrance_data.xlsx') #read raw data


#function to convert numeric series to alphabetical
#returns conversion key as dataframe
def alphabet_conversion(df_in):
    df_out = df_in.copy()      
    alphabet = list(ascii_lowercase)
    df_list = np.unique(df_out)
    letter_list = []
    df_out = df_out.apply(str) #convert to string  
    for i in range(len(df_list)):
        letter = alphabet[i]
        df_out.replace(str(df_list[i]),letter,inplace=True)
        letter_list.append(letter)
    
    conversion_data = {'number': df_list, 'letter': letter_list}
    conversion_key = pd.DataFrame(data=conversion_data)    
    
    return df_out, conversion_key


#%%sort data
#------------------------------------------------------------------------------

study = "standard"

if study == "Words":
    c1 = study+" Alert"
    c2 = study+" Surprised"

if study == "Munchkin":
    c1 = study+" Interested [Alert]"
    c2 = study+" Surprised"

if study == "F-POPS":
    c1 = "F-POPS.ANGRY"
    c2 = "F-POPS.NEUTRAL"
    
if study == "standard":
    c1 = "memorable"
    c2 = "standsout"

id1 = data["Subject"] #person ID
items = data.loc[:,c1:c2] #questions
product = data["Product"] #product/facet being tested
total = data["OFR"] #overall score

#drop nans
items.dropna(how='all',inplace=True)
#drop weird 0.5s
is0_5 = items[items==0.5].copy()
is0_5.dropna(how='all',inplace=True)
items.drop(is0_5.index,inplace=True)

id1 = id1[items.index]
product = product[items.index]
total = total[items.index]



    
#%% convert product to RUMM format
#products   
product_RUMM, product_key = convert2RUMM(product,0) #function to convert PF data into RUMM format

#items
items_RUMM, items_key = convert2RUMM(items,0)

#total score
#total = total.astype(int)
PF_RUMM, PF_key = convert2RUMM(total,0) 
#%

misfit_ID = []

misfits = False #true if ID of misfitting people is included, to remove from the analysis

if misfits:

    ID = 'personID' #facetID if facet analysis, personID otherwise
    
    persons = pd.read_excel('../Rasch_analysis/Data1_Saudi/usual_combined_persons.xlsx') #individual person fit data
    misfits1 = persons.loc[:,'Extm'][persons.loc[:,'Extm']=='extm'] 
    misfit_ID1 = persons.loc[misfits1.index,ID]

    persons = persons[persons.loc[:,'Extm']!='extm' ] #remove extremes
    misfits2 = persons.loc[:,'FitResid'][abs(persons.loc[:,'FitResid'])>2.5]
    misfit_ID2 = persons.loc[misfits2.index,ID]

    misfit_ID = misfit_ID1.append(misfit_ID2)

#% remove extreme scores (i.e. people that put the same answer for everything)
extremes = False

if extremes:
    items_1, id1_1, product_RUMM_1, extreme_persons = remove_extremes(items,id1,product_RUMM) 
    items.drop(extreme_persons.index,inplace=True)
    #items = items.dropna()       
    id1 = id1[items.index]
    product_RUMM = product_RUMM[items.index]

rescore = True

if rescore:
    items_RUMM.replace(1,0,inplace=True)
    items_RUMM.replace(2,0,inplace=True)
    items_RUMM.replace(3,0,inplace=True)
    items_RUMM.replace(4,0,inplace=True)
    items_RUMM.replace(5,1,inplace=True)
    items_RUMM.replace(6,1,inplace=True)
    items_RUMM.replace(7,1,inplace=True)
    items_RUMM.replace(8,1,inplace=True)
    items_RUMM.replace(9,1,inplace=True)

    
    if extremes:
        items_1, id1_1, product_RUMM_1, extreme_persons = remove_extremes(items,id1,product_RUMM) 

            
replace = False

if replace: 
    product_RUMM.loc[:].replace([1,3,5,7,9,11],1,inplace=True) #combine controls 
    product_RUMM.loc[:].replace(4,3,inplace=True) #product 2
    product_RUMM.loc[:].replace(6,4,inplace=True) #product 29
    product_RUMM.loc[:].replace(8,5,inplace=True) #product 31 or product 6
    product_RUMM.loc[:].replace(10,6,inplace=True) #product 6
    
#% delete items and data

items_del = []

items2 = items.copy()

for i in range(len(items_del)):
    col = items2.columns[items_del[i]-1]
    items.drop(columns=col, inplace=True)
    
    
#product_RUMM, product_key2 = alphabet_conversion(product_RUMM)
    
    
#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
RUMM_out = pd.concat([id1, id1, product_RUMM, items_RUMM], axis=1, ignore_index = True)

with pd.ExcelWriter("fragrance.xlsx") as writer:
    RUMM_out.to_excel(writer, sheet_name = 'data', index=None, header=False)
    product_key.to_excel(writer, sheet_name = 'key')















