"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import os

os.chdir('C:\\Users\\Caitlin\\Documents\\data_science_internship\\project1\\python_scripts')

import pandas as pd
import numpy as np
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text
from data_manipulation import remove_extremes

data = pd.read_excel('..\\Rasch_analysis\\Data1_Saudi\\raw\\Saudi_data.xlsx') #read raw data

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

c1 = "Rating For Cleaning Laundry Overall"
c2 = "Agreement With I Would Recommend This Product To My Family And Friends"
rat_agreements = data.loc[:,c1:c2]

c1 = "Attitude Towards Benefit Removes All Greasy Food Stains With No Pretreating (Scrubbing Or Extra Products)"
c2 = "Attitude Towards Benefit Fully Dissolves Leaving Behind No Residue In The Machine, Or On My Laundry"
attitudes = data.loc[:,c1:c2]

#c1 = "Region"
c1 = "Nationality Of Respondent"
c2 = "Age Of Respondent (ageres)"
c3 = "Marital Status"
c4 = "Employment Of Respondent"
c5 = "Size Of Household"
c6 = "Number Of Children In Household Under 16"
c7 = "Monthly Household Income"
c8 = "How Usually Wash Laundry"
c9 = "Type Of Main Washing Machine"
c10 = "Number Of Times Per Week Wash In Washing Machine"
c11 = "Type Of Laundry Detergent Usually Use"
c12 = "How Much Scent Like On Laundry"
c13 = "Whether Usually Use Fabric Softener - Personal"
c14 = "Whether Usually Use Liquid Bleach - Personal"
person_factors = data.loc[:,[c8,c9,c10,c11,c12,c13,c14]]
#person_factors = usual_ratings.copy()
#person_factors = data['Whether Bought Currently Used Laundry Detergent Before']
#person ID
id1 = data.loc[:,"Respondent Serial"]
id_original = id1.copy()
#%
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
#id1 = person_factors.loc[:,"Respondent Serial"]  
#remove id, sex (not necessary, all female) and US$ income (use SR instead) from person_factors
#person_factors = person_factors.drop(columns="Respondent Serial")
#person_factors = person_factors.drop(columns="Sex Of Respondent")
#person_factors = person_factors.drop(columns="Household Income US$")
#person_factors = person_factors.drop(columns="Nationality Of Respondent")
#person_factors = person_factors.drop(columns="Marital Status")
#person_factors = person_factors.drop(columns="Household Income SR")

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


#data of interest: ratings or agreements?
data_type = "ratings"
if data_type == "ratings":
    data_interest = ratings
elif data_type == "agreements":
    data_interest = agreements
elif data_type == "both":
    data_interest = rat_agreements
# items

data_RUMM, data_key = convert2RUMM(data_interest,1) #convert to RUMM format
data_RUMM.replace(np.nan,-1,inplace=True) #replace NaNs with -1
data_RUMM = data_RUMM.astype(int) #ensure integer values


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
    data_RUMM = data_RUMM.iloc[facet_index] 

#% handle misfitting and extreme persons in the data

misfit_ID = []

misfits = False #true if ID of misfitting people is included, to remove from the analysis

if misfits:

    ID = 'personID' #facetID if facet analysis, personID otherwise
    
    persons = pd.read_excel('../Rasch_analysis/Data1_Saudi/final_persons_'+data_type+'2.xlsx') #individual person fit data
    #persons = pd.read_excel('../Rasch_analysis/Data1_Saudi/final_persons_agreements2.xlsx')
    persons2 = pd.read_excel('../Rasch_analysis/Data1_Saudi/id_products_combo4r3.xlsx')
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
extract = False #extract only the people of interest from a given file

if extremes:
    data_RUMM, id1, PFs_RUMM, facets_RUMM, extreme_persons = remove_extremes(data_RUMM,id1,PFs_RUMM,facets_RUMM,misfit_ID)

if extract:
    
    #non_misfit_ID = persons2.iloc[:,0]  
    id_extract = id1.isin(non_misfit_ID)
    id_extract = id_extract[id_extract].index #id of non-misfits (corresponding to original id series)
    #extract non-misfits only from data
    data_RUMM = data_RUMM.iloc[id_extract]  
    id1 = id1.iloc[id_extract]
    PFs_RUMM = PFs_RUMM.iloc[id_extract]
    facets_RUMM = facets_RUMM.iloc[id_extract]
    #id_rating = id1.copy()
    #id_agree = id1.copy()
#% rescore data

rescore = False

if rescore:
    data_RUMM.replace(1,0,inplace=True)
    data_RUMM.replace(2,1,inplace=True)
    data_RUMM.replace(3,2,inplace=True)
    data_RUMM.replace(4,3,inplace=True)
    
    data_RUMM, id1, PFs_RUMM, facets_RUMM, extreme_persons = remove_extremes(data_RUMM,id1,PFs_RUMM,facets_RUMM)
    
    
    
#% delete items

delete_items = True

if delete_items:
    if data_type == "ratings":
        items_del = [7,11,18]
    elif data_type == "agreements":
        items_del = [2,5,13,14,15,16]
    elif data_type == "both":
        items_del = [2,3,5,7,8,9,10,11,12,13,14,16,20,23,28,31,32,33,34]

    data_RUMM2 = data_RUMM.copy()
#agreements_RUMM2 = agreements_RUMM.copy()

    for i in range(len(items_del)):
        col = data_RUMM2.columns[items_del[i]-1]
        data_RUMM.drop(columns=col, inplace=True)
    #agreements_RUMM.drop(columns=col, inplace=True)
#id_new.drop(id_new.index[k], axis=0, inplace=True)

#% product manipulations
    
#% remove facets
facets_of_interest = np.array([1,2,3,4,5,6,7,8,9,10]) #list of facets of interest
facet_index = facets_of_interest - 1
facet_select = facets_RUMM.isin(facet_index) #series of selected facets
#facet_index = facet_select[facet_select==True].index #index of facets of interest
#trim data files so they only include facets of interest
id1 = id1[facet_select] 
facets_RUMM = facets_RUMM[facet_select] 
PFs_RUMM = PFs_RUMM[facet_select]
data_RUMM = data_RUMM[facet_select] 

facet_quantity =[]
for i in range(len(facets_of_interest)):
    facet_quantity.append(len(facets_RUMM[facets_RUMM==facet_index[i]])) 

n_final = min(facet_quantity) 
#n_remove = facet_quantity - 
#%remove random selection of data0
sample = False
if sample:
    fac = [1,2,4,5,7,8,9] #facet number to sample
    #number of samples to drop
    for i in range(len(fac)):
        n = facet_quantity[i]-n_final 
        facet_sample = facets_RUMM[facets_RUMM==fac[i]-1].sample(n) #random sample containing this facet
        facets_RUMM.drop(facet_sample.index,inplace=True) #remove sample from facets
        data_RUMM.drop(facet_sample.index,inplace=True) #remove sample from data
        id1.drop(facet_sample.index,inplace=True)

#%combine facets 4&5 = 2, 6&7 = 3, 8 = 4, 9 = 5
#facets_RUMM.replace([1-1,2-1],0,inplace=True)
#facets_RUMM.replace([6-1,7-1],2,inplace=True)
#facets_RUMM.replace(8-1,1,inplace=True)
#facets_RUMM.replace(9-1,2,inplace=True)


#%% person factor manipulations
#c2 = "Age of Respondent (ageres)"
#c3 = "Marital Status"
#c4 = "Employment of Respondent"
#c5 = "Size of Household"
#c6 = "Number of Children in Household Under 16"
#c7 = "Region"

#% remove PFs
if PFs_RUMM.ndim == 1:
        
    remove = False

    if remove:
        PF_of_interest = np.array([0,1,2,3,4,5,6,7,8]) #list of facets of interest
        PF_select = PFs_RUMM.isin(PF_of_interest) #series of selected facets
        id1 = id1[PF_select] 
        facets_RUMM = facets_RUMM[PF_select] 
        PFs_RUMM = PFs_RUMM[PF_select]
        data_RUMM = data_RUMM[PF_select]

    #c1 = nationality of respondent
    #change to saudi (14), eqyptian (2) + others
    PFs_RUMM.replace([0,1,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19],99,inplace=True)
    PFs_RUMM.replace(14,0,inplace=True) #saudi
    PFs_RUMM.replace(2,1,inplace=True) #eqyptian
    PFs_RUMM.replace(99,2,inplace=True) #other  
    
    PF_levels = np.unique(PFs_RUMM)
    PF_quantity =[]
    for i in range(len(PF_levels)):
        PF_quantity.append(len(PFs_RUMM[PFs_RUMM==PF_levels[i]]))

    sample = True
    if sample:
    #PF = [1,2,3] #facet number to sample
    #n = [27,33,8] #number of samples to drop
        for i in range(len(PF_levels)):
            n = PF_quantity[i] - min(PF_quantity)
            PF_sample = PFs_RUMM[PFs_RUMM==PF_levels[i]].sample(n) #random sample containing this facet
            PFs_RUMM.drop(PF_sample.index,inplace=True) #remove sample from facets
            data_RUMM.drop(PF_sample.index,inplace=True) #remove sample from data
            id1.drop(PF_sample.index,inplace=True)

if PFs_RUMM.ndim > 1:

#c1 = nationality of respondent
#change to saudi (14), eqyptian (2) + others
    if c1 in PFs_RUMM.columns:
        PFs_RUMM.loc[:,c1].replace([0,1,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19],99,inplace=True)
        PFs_RUMM.loc[:,c1].replace(14,0,inplace=True) #saudi
        PFs_RUMM.loc[:,c1].replace(2,1,inplace=True) #eqyptian
        PFs_RUMM.loc[:,c1].replace(99,2,inplace=True) #other    
        
#c2 = age of respondent
#combine 30-34 (2), 35-40 (3), 41-45 (4) and 46-50 (5)
    if c2 in PFs_RUMM.columns:
        PFs_RUMM.loc[:,c2].replace([2,3,4,5],2,inplace=True) #30-50
        PFs_RUMM.loc[:,c2].replace(6,3,inplace=True) #under 18

#c3 = marital status
#combine widowed, single and divorced
    if c3 in PFs_RUMM.columns:
        PFs_RUMM.loc[:,c3].replace([0,2,3],0,inplace=True) #not married

#c4 = employment of respondent 
#combine unemployed (7), looking (8) and retired (4)
#combine business (3) and self employed (5)
#combine student (6) and part time (1)
    #PFs_RUMM.loc[:,c4].replace([1,6],1,inplace=True) #part-time/student
    if c4 in PFs_RUMM.columns:            
        PFs_RUMM.loc[:,c4].replace([3,5],3,inplace=True) #self employed 
        PFs_RUMM.loc[:,c4].replace([4,7,8],4,inplace=True) #unemployed

#c5 = size of household
#combine one (2), two (6) and three (5)
#combine 6 and 7+
    if c5 in PFs_RUMM.columns:
        PFs_RUMM.loc[:,c5].replace([2,5,6],2,inplace=True) #3 or less
        PFs_RUMM.loc[:,c5].replace([3,4],3,inplace=True) #6 or more

#c6 = number of children under 16
#combine 3 (5),4 (1),5 (0),6+ (4)
    if c6 in PFs_RUMM.columns:    
        PFs_RUMM.loc[:,c6].replace([0,1,4,5],0,inplace=True) #3+
        PFs_RUMM.loc[:,c6].replace(2,1,inplace=True) #none
        PFs_RUMM.loc[:,c6].replace(3,2,inplace=True) #one
        PFs_RUMM.loc[:,c6].replace(6,3,inplace=True) #two

#c7 = Monthly household income
#combine 11250 (0) & 13750 (1)
#combine 16250 (2), 18750 (3), 21250 (7)
    if c7 in PFs_RUMM.columns:
        PFs_RUMM.loc[:,c7].replace([0,1],0,inplace=True) #10.001 - 15.000
        PFs_RUMM.loc[:,c7].replace([2,3,7],1,inplace=True) #over 15.000
        PFs_RUMM.loc[:,c7].replace(4,2,inplace=True) #5.001 - 7.500
        PFs_RUMM.loc[:,c7].replace(5,3,inplace=True) #7.501 - 10.000 
        PFs_RUMM.loc[:,c7].replace(6,4,inplace=True) #under 5.000
        PFs_RUMM.loc[:,c7].replace(8,5,inplace=True) #prefer not to say


        PF = PFs_RUMM.loc[:,c7]
    
        PF_levels = np.unique(PF)
        PF_quantity =[]
        for i in range(len(PF_levels)):
            PF_quantity.append(len(PF[PF==PF_levels[i]]))



#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
if len(facets_of_interest) > 1 and combination == False: #multifacet analysis
    #RUMM_ratings = pd.concat([id1, id1, facets_RUMM, ratings_RUMM], axis=1)
    RUMM_data = pd.concat([id1, data_RUMM], axis=1)
    #RUMM_agreements = pd.concat([id1, facets_RUMM, agreements_RUMM], axis=1)

    RUMM_data_key = pd.concat([PFs_key, data_key], axis=1) 
    #RUMM_agreements_key = pd.concat([facets_key, agreements_key], axis=1) 
else: #single facet analysis
    RUMM_data = pd.concat([id1, PFs_RUMM, data_RUMM], axis=1)
    #RUMM_agreements = pd.concat([id1, PFs_RUMM, agreements_RUMM], axis=1)

    RUMM_data_key = pd.concat([PFs_key, data_key], axis=1) 
    #RUMM_agreements_key = pd.concat([PFs_key, agreements_key], axis=1)
#write data and corresponding key to excel worksheet

if data_type == "ratings":
    name = "Saudi_ratings.xlsx"
elif data_type == "agreements":
    name = "Saudi_agreements.xlsx"
elif data_type == "both":
    name = "Saudi_both.xlsx"
    
with pd.ExcelWriter(name) as writer:
    RUMM_data.to_excel(writer, sheet_name = 'data', index=None, header=False)
    RUMM_data_key.to_excel(writer, sheet_name = 'key')

#with pd.ExcelWriter("Saudi_agreements.xlsx") as writer:
#    RUMM_agreements.to_excel(writer, sheet_name = 'data', index=None, header=False)
#    RUMM_agreements_key.to_excel(writer, sheet_name = 'key')

#%% output removed person ids to excel file

write_misfits = True

data_ra = pd.read_excel('..\\Rasch_analysis\\Data1_Saudi\\rating_questions\\all_person_locations.xlsx')
data_ag = pd.read_excel('..\\Rasch_analysis\\Data1_Saudi\\agreement_questions\\all_person_locations.xlsx')
#%% write misfitting people to file
if write_misfits:
    
    rating_removed_id = id_original[~id_original.isin(id_rating)]
    agreement_removed_id = id_original[~id_original.isin(id_agree)]
    both_removed_id = rating_removed_id[rating_removed_id.isin(agreement_removed_id)]
    
    loc_ra = data_ra['Location'][data_ra['personID'].isin(rating_removed_id)] 
    loc_ag = data_ag['Location'][data_ag['personID'].isin(agreement_removed_id)] 
    fr_ra = data_ra['FitResid'][data_ra['personID'].isin(rating_removed_id)] 
    fr_ag = data_ag['FitResid'][data_ag['personID'].isin(agreement_removed_id)] 
    
    files_out = [rating_removed_id,loc_ra,fr_ra,agreement_removed_id,loc_ag,fr_ag,both_removed_id]

    for i in range(len(files_out)):
        new_index = list(range(len(files_out[i])))
        index_dict = dict(zip(files_out[i].index,new_index))
        files_out[i].rename(index_dict,inplace=True)

    id_out = pd.concat([rating_removed_id,loc_ra,fr_ra,agreement_removed_id,loc_ag,fr_ag,both_removed_id],axis=1,ignore_index=True)

    with pd.ExcelWriter('misfitting_people.xlsx') as writer:
        id_out.to_excel(writer, index=None, header=False)
                
#%% plot misfitting people to illustrate why they were removed 

plot_misfits = True
save_fig = False

if plot_misfits:
    
    import matplotlib.pyplot as plt
    
    misfits = pd.read_excel('misfitting_people.xlsx',header=None)
    id_ra = misfits[0]
    id_ag = misfits[3]
    
    loc_ra = misfits[1]
    loc_ag = misfits[4]
    
    fr_ra = misfits[2]
    fr_ag = misfits[5]
        
    #remove extremes
    fr_ra2 = fr_ra[fr_ra!='...']
    id_ra2 = id_ra[fr_ra2.index]
    loc_ra2 = loc_ra[fr_ra2.index]
    
    fr_ag2 = fr_ag[fr_ag!='...']
    id_ag2 = id_ag[fr_ag2.index]
    loc_ag2 = loc_ag[fr_ag2.index]

    #original data
    ratings_new = ratings.copy()
    agreements_new = agreements.copy()
    ratings_key = remove_text(ratings_new)
    agreements_key = remove_text(agreements_new)
    
    ratings1 = ratings_new[id_original.isin(id_ra)]
    agreements1 = agreements_new[id_original.isin(id_ag)]
    ratings2 = ratings_new[id_original.isin(id_ra2)]
    agreements2 = agreements_new[id_original.isin(id_ag2)]
    
    #rescore agreements resonses to coincide with ratings
    agreements2.replace(2,100,inplace=True)
    agreements2.replace(1,75,inplace=True)
    agreements2.replace(0,50,inplace=True)
    agreements2.replace(-1,25,inplace=True)
    agreements2.replace(-2,0,inplace=True)

    sd_ra = ratings2.std(axis=1)
    sd_ag = agreements2.std(axis=1)
   
    fig,ax = plt.subplots(2)
    ax[0].plot(loc_ra2,fr_ra2,'o')
    ax[1].plot(loc_ag2,fr_ag2,'o')
    
    for label,x,y in zip(sd_ra,loc_ra2,fr_ra2):
            if (label>25): #& (label0==0):
                ax[0].plot(x,y,'o',color='red')
                
    for label,x,y in zip(sd_ag,loc_ag2,fr_ag2):
            if (label>25): #& (label0==0):
                ax[1].plot(x,y,'o',color='red')


    ax[1].set_xlabel('Person location (logits)',FontSize=12)
    ax[1].set_ylabel('Fit residual',FontSize=12)
    ax[0].set_title('Ratings analysis',FontSize=12)
    ax[1].set_title('Agreements analysis',FontSize=12)
    
    ax[1].legend(['Low raw score SD','High raw score SD'])
    
    plt.tight_layout()

    figname = 'misfits'

    if save_fig:
        plt.savefig(figname+'.pdf')
        plt.savefig(figname+'.jpg')







