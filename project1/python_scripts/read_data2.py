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
import random

data = pd.read_excel('../Data2_Shaving/shaving_data_original.xlsx') #read raw data

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

select_aspect = False
if select_aspect:
    aspects = ["Chemistry"]
    data = data[data.loc[:,"Test Aspect"].isin(aspects)]
id1 = data.loc[:,"assessor"] #person ID
items = data.loc[:,"Q1":"Q10"] #questions
product = data.loc[:,"Product"] #product/facet being tested
shave = data.loc[:,"Shave Number"] #number of shave (of multiple, per person)
aspect = data.loc[:,"Test Aspect"]

#% select one shave only
single_shave = True

if single_shave:
    shave_no = [1,2,3,4]

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
    


#% consider certain products only
#prods = ['Prod 1','Prod 2','Prod 3','Prod 4']
prod_only = ['Prod 6','Prod 18', 'Prod 19','Prod 2','Prod 29','Prod 31','Prod 32']
prods = prod_only + ['Prod 6 Control','Prod 18 Control', 'Prod 19 Control', 'Prod 2 Control', 'Prod 29 Control', 'Prod 31 Control', 'Prod 32 Control']

prods = np.unique(product)
remove_controls = False

if remove_controls:
    
    i = 0
    while i < (len(prods)):
        if 'Control' in prods[i]:
            prods = np.delete(prods,i)
            i = i-1
            i = i+1
#%
if len(prods) < len(np.unique(product)):
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
extremes = True

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
    
#% delete items and data

items_del = []

items2 = items.copy()

for i in range(len(items_del)):
    col = items2.columns[items_del[i]-1]
    items.drop(columns=col, inplace=True)

sample = False
if sample:
    fac = [2] #facet number to sample        
    for i in range(len(fac)):
        n = 100 #number of samples to drop
        facet_sample = product_RUMM[product_RUMM==fac[i]].sample(n) #random sample containing this facet
        product_RUMM.drop(facet_sample.index,inplace=True) #remove sample from facets
        items.drop(facet_sample.index,inplace=True) #remove sample from data
        id1.drop(facet_sample.index,inplace=True)

#id_new.drop(id_new.index[k], axis=0, inplace=True)
        
#% rack or stack the data

stack = True
if stack:
    shave_select = [4,3,2,1]
    for i in range(len(shave_select)):  
        if i == 0: #initialise stack
            id_stack = id1[shave==shave_select[i]]
            #edit id for repeated shaves by adding the shave number afterwards
            index1 = id_stack.index
            id_stack = [str(id_stack.iloc[j]) + str(shave_select[i]) for j in range(len(id_stack))]
            id_stack = pd.Series(id_stack,index=index1)
            id_stack = id_stack.astype(int)
            
            product_stack = product_RUMM[shave==shave_select[i]]
            item_stack = items[shave==shave_select[i]]
            shave_stack = shave[shave==shave_select[i]]  
        
        if i > 0:
            #edit id for repeated shaves by adding the shave number afterwards
            id_stack1 = id1[shave==shave_select[i]]
            index1 = id_stack1.index
            id_stack1 = [str(id_stack1.iloc[j]) + str(shave_select[i]) for j in range(len(id_stack1))]
            id_stack1 = pd.Series(id_stack1,index=index1)
            id_stack1 = id_stack1.astype(int)
            
            id_stack = pd.concat([id_stack,id_stack1])
            product_stack = pd.concat([product_stack,product_RUMM[shave==shave_select[i]]])
            item_stack = pd.concat([item_stack,items[shave==shave_select[i]]])
            shave_stack = pd.concat([shave_stack,shave[shave==shave_select[i]]])
        
    id1 = id_stack.copy()
    product_RUMM = product_stack.copy()
    items = item_stack.copy()
    shave = shave_stack.copy()

#% convert numerical data to string and replace numbers with letters
        #to do: convert to general function

alphabet_conversion = False

if alphabet_conversion:
           
    alphabet = list(ascii_lowercase)
    prod_list = np.unique(product_RUMM)
    letter_list = []
    product_RUMM = product_RUMM.apply(str) #convert to string  
    for i in range(len(prod_list)):
        letter = alphabet[i]
        product_RUMM.replace(str(i),letter,inplace=True)
        letter_list.append(letter)

    product_key["Letter"] = letter_list

#shave_list = np.unique(shave)
#shave = shave.apply(str) #convert to string  
#for i in range(len(shave_list)):
#    letter = alphabet[i]
#    shave.replace(str(i+1),letter,inplace=True)


#%% select each person at random over all 10 shaves

select_every_person = False

if select_every_person:
    person_index = []
    for j in range(len(shave_select)):
        id_temp = id1[shave==shave_select[j]]
        id_list = np.unique(id_temp)
        for i in range(len(id_list)):
            person = id_temp[id_temp==id_list[i]].index
            selection = random.choice(person)
            person_index.append(selection)

    id1 = id1[person_index]
    product_RUMM = product_RUMM[person_index]
    shave = shave[person_index]
    items = items.loc[person_index,:]
 
#FINISH : write code to track the same people for the same products over time
    #first remove the people/products from shave 4, then remove the same corresponding products/people from shaves 1-3
    #OR: if person + product not in shave 1-3, then remove.
    #OR: use the data from shave 4 to extract the remaining shaves. i.e. find that person and that product, get the data
    #for the remaining shaves
track = True
if track:
    shave_select = 4
    id_track = id1[shave==shave_select]
            #edit id for repeated shaves by adding the shave number afterwards
            index1 = id_stack.index
            id_stack = [str(id_stack.iloc[j]) + str(shave_select[i]) for j in range(len(id_stack))]
            id_stack = pd.Series(id_stack,index=index1)
            id_stack = id_stack.astype(int)
            
    product_stack = product_RUMM[shave==shave_select[i]]
    item_stack = items[shave==shave_select[i]]
    shave_stack = shave[shave==shave_select[i]]  


#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
RUMM_out = pd.concat([id1, shave, items], axis=1, ignore_index = True)

#write data and corresponding key to excel worksheet

with pd.ExcelWriter("first_shave.xlsx") as writer:
    RUMM_out.to_excel(writer, sheet_name = 'data', index=None, header=False)
    product_key.to_excel(writer, sheet_name = 'key')















