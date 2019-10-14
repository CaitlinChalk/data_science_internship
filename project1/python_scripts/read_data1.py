"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import pandas as pd
import numpy as np
from convert_PFs import convert_PFs #function to convert structured data to RUMM format

data = pd.read_excel('../data/raw/Saudi_data.xlsx') #read raw data

#replace NaN with -1
#data.fillna(-1)
#data.replace(np.nan,-999,inplace=True) #replace NaNs with -999
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
#Rasch input file structure: id, facets, PFs, items
#------------------------------------------------------------------------------

facet_list = np.unique(usual_brand) #count number of distinct laundry brands

#create dictionary for facets, and replace brands with integers 
facets = usual_brand
facet_dict = {}
for i in range(len(facet_list)):
    facet_dict[i] = {facet_list[i]: i}
    facets.replace(facet_dict[i], inplace=True)
    
#%% person factors
   
#age_list = np.unique(person_factors.loc[:,"Age Of Respondent (ageres)"])
#age = person_factors.loc[:,"Age Of Respondent (ageres)"]   
#age_dict = {}
#for i in range(len(age_list)):
#    age_dict[i] = {age_list[i]: i}
#    age.replace(age_dict[i], inplace=True)
    
#%%    
PFs_RUMM = person_factors.copy() 
convert_PFs(person_factors, PFs_RUMM) #function to convert PF data into RUMM format
PFs_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
PFs_RUMM = PFs_RUMM.astype(int)




















