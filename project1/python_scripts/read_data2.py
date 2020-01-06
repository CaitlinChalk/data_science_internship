"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import pandas as pd
import numpy as np
from scipy import stats
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text
from data_manipulation import remove_extremes
from string import ascii_lowercase

data = pd.read_excel('../Data2_Shaving/shaving_data.xlsx') #read raw data

#% functions
#remove subset of data according to specified factor
#factor can be either people or products for removal
#other is the 'other' factor (e.g. people, if factor is products)
def remove_factor(factor,other,items,n,n_min = 1000):
    factor2 = factor.copy()
    unique_list = np.unique(factor2)
    for i in range(len(unique_list)):
        if len(factor2[factor2==unique_list[i]])<n or len(factor2[factor2==unique_list[i]])>n_min:
            index = factor2[factor2==unique_list[i]].index
            factor.drop(index, inplace =True)
            other.drop(index, inplace =True)
            items.drop(index, inplace =True)
    
    unique_list2 = np.unique(factor)
    final_count = [] #initialise array to count number of responses for each person
    for i in range(len(unique_list2)):
        final_count.append(len(factor[factor==unique_list2[i]]))
        
    return final_count

#%sort data
#------------------------------------------------------------------------------
data1 = data[data.loc[:,"Shave Number"]==1]
data = data[data.loc[:,"Test Aspect"]=="Chemistry"]
id1 = data.loc[:,"assessor"] #person ID
items = data.loc[:,"Q1":"Q10"] #questions
product = data.loc[:,"Product"] #product/facet being tested
shave = data.loc[:,"Shave Number"] #number of shave (of multiple, per person)
aspect = data.loc[:,"Test Aspect"]

#% select one shave only
single_shave = False

if single_shave:
    shave_no = [1,2,3,4,5]

    id1 = id1[shave.isin(shave_no)]
    items = items[shave.isin(shave_no)]
    product = product[shave.isin(shave_no)]
    aspect = aspect[shave.isin(shave_no)]
    shave = shave[shave.isin(shave_no)]

save_pattern = False #run if the pattern of respondents for each product is required (for visualisation)

if save_pattern:

    id_unique = np.unique(id1)
    pattern = pd.Series(id_unique)
    pattern.name='Person ID'
    prod = np.unique(product)
    for i in range(len(prod)):
        prod_list=[]
        for j in range(len(id_unique)):
            prod2 = product[id1==id_unique[j]]
            prod3 = prod2[prod2==prod[i]]
            id_per_prod = len(prod3)
            prod_list.append(id_per_prod)
        series1 = pd.Series(prod_list)
        series1.name = prod[i]
        pattern = pd.concat([pattern,series1], axis=1)
        
    with pd.ExcelWriter("response_pattern_chemistry4.xlsx") as writer:        
        pattern.to_excel(writer, index=None, header=True)
    


#%% consider certain products only
#prods = ['Prod 1','Prod 2','Prod 3','Prod 4']
prod_only = ['Prod 6','Prod 18', 'Prod 19','Prod 2','Prod 29','Prod 31','Prod 32']
prods = prod_only + ['Prod 6 Control','Prod 18 Control', 'Prod 19 Control', 'Prod 2 Control', 'Prod 29 Control', 'Prod 31 Control', 'Prod 32 Control']
 
facet_select = product.isin(prods) #series of selected facets
id1 = id1[facet_select] 
product = product[facet_select] 
items = items[facet_select] 
aspect = aspect[facet_select]
shave = shave[facet_select]

#number of responses for each product  
product_count1 = remove_factor(product,id1,items,1)

remove = False

if remove:      
    #remove people who haven't answered enough questions
    id_count1 = remove_factor(id1,product,items,4)        
    #remove products with an insufficient number of respondents
    product_count2 = remove_factor(product,id1,items,4)      
    #remove people who haven't answered enough questions again
    id_count2 = remove_factor(id1,product,items,1)
    
#%remove certain controls (only keep those which were answered by the same people, for the same product aspect)
remove_controls = False

if remove_controls:

    id2 = id1.copy()    
    product2 = product.copy()
    aspect2 = aspect.copy()

    id_product = id1[product.isin(prod_only)]
    aspect_product = aspect[product.isin(prod_only)]
    for i in range(len(product2)):
        if 'Control' in product2.iloc[i]:
            id_test = id_product[id_product==id2.iloc[i]]
            as_test = aspect_product[aspect_product==aspect2.iloc[i]]
            if  len(id_test)==0 or len(as_test)==0:
                id1.drop(id2.index[i], inplace = True)
                product.drop(id2.index[i], inplace = True)
                items.drop(id2.index[i], inplace = True)
                aspect.drop(id2.index[i], inplace = True)

#% convert product to RUMM format

#products   
product_RUMM, product_key = convert2RUMM(product,0) #function to convert PF data into RUMM format

#aspects
PF_RUMM, PF_key = convert2RUMM(aspect,0) 
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

if extremes: #TO DO: edit to make PFs an optional argument, edit for facet analysis
    items, id1, product_RUMM, extreme_persons = remove_extremes(items,id1,product_RUMM,misfit_ID)
    
#% rescore data

rescore = True

if rescore:
    items.replace(1,0,inplace=True)
    items.replace(2,0,inplace=True)
    items.replace(3,0,inplace=True)
    items.replace(4,1,inplace=True)
    items.replace(5,1,inplace=True)
    
    if extremes:
        items, id1, product_RUMM, extreme_persons = remove_extremes(items,id1,product_RUMM)
    
replace = False

if replace: 
    product_RUMM.loc[:].replace([1,3,5,7,9,11],1,inplace=True) #combine controls 
    product_RUMM.loc[:].replace(4,3,inplace=True) #product 2
    product_RUMM.loc[:].replace(6,4,inplace=True) #product 29
    product_RUMM.loc[:].replace(8,5,inplace=True) #product 31 or product 6
    product_RUMM.loc[:].replace(10,6,inplace=True) #product 6
    
#%% delete items and data

items_del = []

items2 = items.copy()

for i in range(len(items_del)):
    col = items2.columns[items_del[i]-1]
    items.drop(columns=col, inplace=True)

sample = False
if sample:
    fac = [1] #facet number to sample        
    for i in range(len(fac)):
        n = 100 #number of samples to drop
        facet_sample = product_RUMM[product_RUMM==fac[i]].sample(n) #random sample containing this facet
        product_RUMM.drop(facet_sample.index,inplace=True) #remove sample from facets
        items.drop(facet_sample.index,inplace=True) #remove sample from data
        id1.drop(facet_sample.index,inplace=True)

#id_new.drop(id_new.index[k], axis=0, inplace=True)
        
#%% rack or stack the data
    #EDIT TO MAKE GENERAL FOR MORE THAN 2 SHAVES
    #[i + '0' for i in str(test)] --> use something like this to append 0 etc to every element in list
stack = True
if stack:
    shave_select = [1,2]
    for i in range(len(shave_select)-1):
        id1a = id1[shave==shave_select[i]].array
        new
        id1 = pd.concat([id1[shave==shave_select[i]],id1[shave==shave_select[i+1]]],axis=0)
        product_RUMM = pd.concat([product_RUMM[shave==shave_select[i]],product_RUMM[shave==shave_select[i+1]]],axis=0)
        items = pd.concat([items[shave==shave_select[i]],items[shave==shave_select[i+1]]],axis=0)
        shave = pd.concat([shave[shave==shave_select[i]],shave[shave==shave_select[i+1]]],axis=0)

#%% convert numerical data to string and replace numbers with letters
        #to do: convert to general function
           
alphabet = list(ascii_lowercase)
prod_list = np.unique(product_RUMM)
letter_list = []
product_RUMM = product_RUMM.apply(str) #convert to string  
for i in range(len(prod_list)):
    letter = alphabet[i]
    product_RUMM.replace(str(i),letter,inplace=True)
    letter_list.append(letter)

product_key["Letter"] = letter_list

shave_list = np.unique(shave)
shave = shave.apply(str) #convert to string  
for i in range(len(shave_list)):
    letter = alphabet[i]
#    shave.replace(str(i+1),letter,inplace=True)


#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
RUMM_out = pd.concat([id1, id1, product_RUMM, shave, items], axis=1)

#write data and corresponding key to excel worksheet

with pd.ExcelWriter("first_shave.xlsx") as writer:
    RUMM_out.to_excel(writer, sheet_name = 'data', index=None, header=False)
    product_key.to_excel(writer, sheet_name = 'key')















