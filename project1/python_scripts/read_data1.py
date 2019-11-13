"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import pandas as pd
import numpy as np
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text
from data_manipulation import remove_extremes

data = pd.read_excel('../Rasch_analysis/Data1_Saudi/raw/Saudi_data.xlsx') #read raw data

#separate raw data into different components by column name
#------------------------------------------------------------------------------

c1 = "Usual Brand P6M"
usual_brand = data.loc[:,c1] 
c1 = "Brands Of Laundry Detergents Used In Past 6 Months - Household"
c2 = "Proportion Of Loads Used Liquid Bleach Together With Regular Laundry Detergent In Past 6 Months"
laundry_habits = data.loc[:,c1:c2]

c1 = "Overall Rating For Usual Laundry Detergent"
c2 = "Value For Price/ Money For Usual Laundry Detergent"
usual_ratings = data.loc[:,c1:c2]

c1 = "Rating For Cleaning Laundry Overall"
c2 = "Rating For Being Easy To Dissolve/ Dissolve In The Dispenser"
ratings = data.loc[:,c1:c2]

c1 = "Agreement With This Product Provides Excellent Value"
c2 = "Agreement With I Would Recommend This Product To My Family And Friends"
agreements = data.loc[:,c1:c2]

c1 = "Attitude Towards Benefit Removes All Greasy Food Stains With No Pretreating (Scrubbing Or Extra Products)"
c2 = "Attitude Towards Benefit Fully Dissolves Leaving Behind No Residue In The Machine, Or On My Laundry"
attitudes = data.loc[:,c1:c2]

c1 = "Sex Of Respondent"
c2 = "Household Income US$"
person_factors = data.loc[:,c1:c2]

del data

#sort components further:
#------------------------------------------------------------------------------

#some columns in usual_ratings belong in ratings instead
#labels of rating columns in laundry_options
r1 = "Overall Rating For Usual Laundry Detergent"
r2 = "Relative Category Rating For Usual Laundry Detergent"
r3 = "Performance vs. Expectations For Usual Laundry Detergent"
r4 = "Distinctiveness Vs Other Products For Usual Laundry Detergent"
r5 = "Value For Price/ Money For Usual Laundry Detergent"

#add extra ratings from usual_ratings to the ratings data matrix
#ratings['Overall Product Rating'] = usual_ratings.loc[:,r1]
#ratings['Relative Category Rating'] = usual_ratings.loc[:,r2]
#ratings['Performance vs Expectation'] = usual_ratings.loc[:,r3]
#ratings['Distinctiveness'] = usual_ratings.loc[:,r4]
#ratings['Value for money'] = usual_ratings.loc[:,r5]

#separate purchase intent as a variable (to analyse later if required)
purchase_intent = usual_ratings.loc[:,"Purchase Intent For Usual Laundry Detergent"]

#remove purchase intent and ratings from usual_ratings (to leave opininions only)
#usual_ratings = usual_ratings.drop(columns="Purchase Intent For Usual Laundry Detergent")
#usual_ratings = usual_ratings.drop(columns=[r1,r2,r3,r4,r5])

#separate respondent id from person_factors
id1 = person_factors.loc[:,"Respondent Serial"]  
#remove id, sex (not necessary, all female) and US$ income (use SR instead) from person_factors
person_factors = person_factors.drop(columns="Respondent Serial")
person_factors = person_factors.drop(columns="Sex Of Respondent")
person_factors = person_factors.drop(columns="Household Income US$")

#combine attitudes and opinions
attitudes_and_opinions = pd.concat([attitudes, usual_ratings], axis=1, sort=False) #concatenates horizontally
#del [attitudes, usual_ratings]

#store original values
#PFs_original = person_factors.copy() #store original values

#% restructure for Rasch analysis
#facets

facets_RUMM, facets_key = convert2RUMM(usual_brand,0) #function to convert data into RUMM format, outputs replacement key
facets_RUMM = facets_RUMM.astype(int) #ensure all values are integers (1 as opposed to 1.0 for example)
    
# person factors
      
PFs_RUMM, PFs_key = convert2RUMM(person_factors,0) #function to convert PF data into RUMM format
PFs_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
PFs_RUMM = PFs_RUMM.astype(int) #ensure integer values

# items

agreements_RUMM, agreements_key = convert2RUMM(agreements,1) #convert to RUMM format
agreements_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
agreements_RUMM = agreements_RUMM.astype(int) #ensure integer values

# ratings

ratings_RUMM, ratings_key = convert2RUMM(ratings,1) #convert to RUMM format
ratings_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
ratings_RUMM = ratings_RUMM.astype(int) #ensure integer values


#% consider a subset of facets only
combination = False
facets_of_interest = np.array([1,2,3,4,5,6,7,8,9,10]) #list of facets of interest
facet_index = facets_of_interest - 1
if len(facets_of_interest) < len(facets_key): #if some facets have been removed
    facet_select = facets_RUMM.isin(facet_index) #series of selected facets
    facet_index = facet_select[facet_select==True].index #index of facets of interest
    #trim data files so they only include facets of interest
    id1 = id1.iloc[facet_index] 
    facets_RUMM = facets_RUMM.iloc[facet_index] 
    PFs_RUMM = PFs_RUMM.iloc[facet_index,:]
    agreements_RUMM = agreements_RUMM.iloc[facet_index] 
    ratings_RUMM = ratings_RUMM.iloc[facet_index] 

#%

misfit_ID = []

misfits = True #true if ID of misfitting people is included, to remove from the analysis

if misfits:

    ID = 'personID' #facetID if facet analysis, personID otherwise
    
    persons = pd.read_excel('../Rasch_analysis/Data1_Saudi/combined_persons_facet_agree2.xlsx') #individual person fit data
    misfits1 = persons.loc[:,'Extm'][persons.loc[:,'Extm']=='extm'] 
    misfit_ID1 = persons.loc[misfits1.index,ID]

    persons = persons[persons.loc[:,'Extm']!='extm' ] #remove extremes
    misfits2 = persons.loc[:,'FitResid'][abs(persons.loc[:,'FitResid'])>2.5]
    misfit_ID2 = persons.loc[misfits2.index,ID]

    misfit_ID = misfit_ID1.append(misfit_ID2)
    #id of non-misfitting people
    id_non_misfit = persons.loc[:,ID] - misfit_ID
    non_misfit_ID = persons.loc[id_non_misfit.isna(),ID]


extremes = False #% remove extreme scores (i.e. people that put the same answer for everything) and misfits
extract = True #extract only the people of interest from a given file

if extremes:
    agreements_RUMM, id1, PFs_RUMM, facets_RUMM, extreme_persons = remove_extremes(agreements_RUMM,id1,PFs_RUMM,facets_RUMM,misfit_ID)

if extract:
    id_extract = id1.isin(non_misfit_ID)
    id_extract = id_extract[id_extract].index #id of non-misfits (corresponding to original id series)
    #extract non-misfits only from data
    agreements_RUMM = agreements_RUMM.iloc[id_extract]  
    id1 = id1.iloc[id_extract]
    PFs_RUMM = PFs_RUMM.iloc[id_extract]
    facets_RUMM = facets_RUMM.iloc[id_extract]
    
#% rescore data

rescore = False

if rescore:
    ratings_RUMM.replace(1,0,inplace=True)
    ratings_RUMM.replace(2,1,inplace=True)
    ratings_RUMM.replace(3,2,inplace=True)
    ratings_RUMM.replace(4,3,inplace=True)
    
    ratings_RUMM, id1, PFs_RUMM, facets_RUMM, extreme_persons = remove_extremes(ratings_RUMM,id1,PFs_RUMM,facets_RUMM)
    
    
    
#%% delete items

items_del = [15,5,13,14,16,2]

ratings_RUMM2 = ratings_RUMM.copy()
agreements_RUMM2 = agreements_RUMM.copy()

for i in range(len(items_del)):
    col = agreements_RUMM2.columns[items_del[i]-1]
    #ratings_RUMM.drop(columns=col, inplace=True)
    agreements_RUMM.drop(columns=col, inplace=True)
#id_new.drop(id_new.index[k], axis=0, inplace=True)


#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
if len(facets_of_interest) > 1 and combination == False: #multifacet analysis
    #RUMM_ratings = pd.concat([id1, id1, facets_RUMM, ratings_RUMM], axis=1)
    RUMM_ratings = pd.concat([id1, facets_RUMM, ratings_RUMM], axis=1)
    RUMM_agreements = pd.concat([id1, facets_RUMM, agreements_RUMM], axis=1)

    RUMM_ratings_key = pd.concat([facets_key, ratings_key], axis=1) 
    RUMM_agreements_key = pd.concat([facets_key, agreements_key], axis=1) 
else: #single facet analysis
    RUMM_ratings = pd.concat([id1, PFs_RUMM, ratings_RUMM], axis=1)
    RUMM_agreements = pd.concat([id1, PFs_RUMM, agreements_RUMM], axis=1)

    RUMM_ratings_key = pd.concat([PFs_key, ratings_key], axis=1) 
    RUMM_agreements_key = pd.concat([PFs_key, agreements_key], axis=1)
#write data and corresponding key to excel worksheet

with pd.ExcelWriter("Saudi_ratings.xlsx") as writer:
    RUMM_ratings.to_excel(writer, sheet_name = 'data', index=None, header=False)
    RUMM_ratings_key.to_excel(writer, sheet_name = 'key')

with pd.ExcelWriter("Saudi_agreements.xlsx") as writer:
    RUMM_agreements.to_excel(writer, sheet_name = 'data', index=None, header=False)
    RUMM_agreements_key.to_excel(writer, sheet_name = 'key')















