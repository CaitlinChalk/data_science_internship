"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import pandas as pd
import numpy as np
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text

data = pd.read_excel('../data/raw/Saudi_data.xlsx') #read raw data

#separate raw data into different components 
#------------------------------------------------------------------------------

#column dividers for data separation
c1 = "Usual Brand P6M"
c2 = "Brands Of Laundry Detergents Used In Past 6 Months - Household"
c3 = "Overall Rating For Usual Laundry Detergent"
c4 = "Rating For Cleaning Laundry Overall"
c5 = "Agreement With This Product Provides Excellent Value"
c6 = "Attitude Towards Benefit Removes All Greasy Food Stains With No Pretreating (Scrubbing Or Extra Products)"
c7 = "Sex Of Respondent"

#column indices for column names 
c1i = data.columns.get_loc(c1) 
c2i = data.columns.get_loc(c2) 
c3i = data.columns.get_loc(c3) 
c4i = data.columns.get_loc(c4) 
c5i = data.columns.get_loc(c5) 
c6i = data.columns.get_loc(c6) 
c7i = data.columns.get_loc(c7) 

usual_brand = data.iloc[:,c1i] 
 
laundry_habits = data.iloc[:,c2i:c3i]

laundry_opinions = data.iloc[:,c3i:c4i]

ratings = data.iloc[:,c4i:c5i]

agreements = data.iloc[:,c5i:c6i]

attitudes = data.iloc[:,c6i:c7i]

person_factors = data.iloc[:,c7i:len(data.columns)]

del data

#sort components further:
#------------------------------------------------------------------------------

#some columns in laundry_opinions belong in ratings instead
#labels of rating columns in laundry_options
r1 = "Overall Rating For Usual Laundry Detergent"
r2 = "Relative Category Rating For Usual Laundry Detergent"
r3 = "Performance vs. Expectations For Usual Laundry Detergent"
r4 = "Distinctiveness Vs Other Products For Usual Laundry Detergent"
r5 = "Value For Price/ Money For Usual Laundry Detergent"

#add extra ratings from laundry_opinions to the ratings data matrix
ratings['Overall Product Rating'] = laundry_opinions.loc[:,r1]
ratings['Relative Category Rating'] = laundry_opinions.loc[:,r2]
ratings['Performance vs Expectation'] = laundry_opinions.loc[:,r3]
ratings['Distinctiveness'] = laundry_opinions.loc[:,r4]
ratings['Value for money'] = laundry_opinions.loc[:,r5]

#separate purchase intent as a variable (to analyse later if required)
purchase_intent = laundry_opinions.loc[:,"Purchase Intent For Usual Laundry Detergent"]

#remove purchase intent and ratings from laundry_opinions (to leave opininions only)
laundry_opinions = laundry_opinions.drop(columns="Purchase Intent For Usual Laundry Detergent")
laundry_opinions = laundry_opinions.drop(columns=[r1,r2,r3,r4,r5])

#separate respondent id from person_factors
id1 = person_factors.loc[:,"Respondent Serial"]  
#remove id, sex (not necessary, all female) and US$ income (use SR instead) from person_factors
person_factors = person_factors.drop(columns="Respondent Serial")
person_factors = person_factors.drop(columns="Sex Of Respondent")
person_factors = person_factors.drop(columns="Household Income US$")

#combine attitudes and opinions
attitudes_and_opinions = pd.concat([attitudes, laundry_opinions], axis=1, sort=False) #concatenates horizontally
del [attitudes, laundry_opinions]

#store original values
#PFs_original = person_factors.copy() #store original values

#%% restructure for Rasch analysis
#facets

facets_RUMM, facets_key = convert2RUMM(usual_brand,0) #function to convert data into RUMM format, outputs replacement key
facets_RUMM = facets_RUMM.astype(int) #ensure all values are integers (1 as opposed to 1.0 for example)
    
#%% person factors
      
PFs_RUMM, PFs_key = convert2RUMM(person_factors,0) #function to convert PF data into RUMM format
PFs_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
PFs_RUMM = PFs_RUMM.astype(int) #ensure integer values

#%% items
#in these data, item responses include text, as well as a digit score
#2 options:
#1. remove the text and order the item responses according to the remaining numbers
#2. manually define the item response orders from low to high, i.e. create dictionary by hand

#option 1:
#agreements
#agreements_digits = agreements.copy() #copy original data
#remove_text(agreements,agreements_digits) #remove all text

#%%
agreements_RUMM, agreements_key = convert2RUMM(agreements,1) #convert to RUMM format
agreements_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
agreements_RUMM = agreements_RUMM.astype(int) #ensure integer values

#ratings
ratings_RUMM, ratings_key = convert2RUMM(ratings,1) #convert to RUMM format
ratings_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
ratings_RUMM = ratings_RUMM.astype(int) #ensure integer values
#%% output final data set

#concatenate data - in this case with separate ratings and agreements

RUMM_ratings = pd.concat([id1, id1, facets_RUMM, PFs_RUMM, ratings_RUMM], axis=1)
RUMM_agreements = pd.concat([id1, id1, facets_RUMM, PFs_RUMM, agreements_RUMM], axis=1)

RUMM_ratings_key = pd.concat([facets_key, PFs_key, ratings_key], axis=1) 
RUMM_agreements_key = pd.concat([facets_key, PFs_key, agreements_key], axis=1) 

#write data and corresponding key to excel worksheet

with pd.ExcelWriter("Saudi_ratings.xlsx") as writer:
    RUMM_ratings.to_excel(writer, sheet_name = 'data', index=None, header=False)
    RUMM_ratings_key.to_excel(writer, sheet_name = 'key')

with pd.ExcelWriter("Saudi_agreements.xlsx") as writer:
    RUMM_agreements.to_excel(writer, sheet_name = 'data', index=None, header=False)
    RUMM_agreements_key.to_excel(writer, sheet_name = 'key')















