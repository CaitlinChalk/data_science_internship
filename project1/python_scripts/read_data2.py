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

data = pd.read_excel('../Data2_Shaving/shaving_data.xlsx') #read raw data

#functions
#function to select person at random over every shave
#main purpose - item anchoring
def select_every_person(shave_select,id_in,id_ignore=[]):
    person_index = []
    id_in.drop(id_ignore,inplace=True)
    id_list = np.unique(id_in)
    for i in range(len(id_list)):
        person = id_in[id_in==id_list[i]].index
        selection = random.choice(person)
        person_index.append(selection)

    index_out = id_in[person_index].index
    return index_out

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

#%sort data
#------------------------------------------------------------------------------
select_aspect = True
if select_aspect:
    aspects = ["Chemistry"]
    data = data[data.loc[:,"Test Aspect"].isin(aspects)]
id1 = data.loc[:,"assessor"] #person ID
items = data.loc[:,"Q1":"Q10"] #questions
product = data.loc[:,"Product"] #product/facet being tested
shave = data.loc[:,"Shave Number"] #number of shave (of multiple, per person)
aspect = data.loc[:,"Test Aspect"]

#% select one shave only
single_shave = False

if single_shave:
    shave_no = [1,2,3]

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

if extremes:
    items_1, id1_1, product_RUMM_1, extreme_persons = remove_extremes(items,id1,product_RUMM) 
    items_1, id1_1, product_RUMM_1, extreme_persons2 = remove_extremes(items[shave==2],id1[shave==2],product_RUMM[shave==2]) 
    items.drop(extreme_persons.index,inplace=True)
    #items = items.dropna()       
    id1 = id1[items.index]
    product_RUMM = product_RUMM[items.index]
    shave = shave[items.index]

rescore = True

if rescore:
    items.replace(1,0,inplace=True)
    items.replace(2,0,inplace=True)
    items.replace(3,0,inplace=True)
    items.replace(4,1,inplace=True)
    items.replace(5,1,inplace=True)
    
    if extremes:
        items_1, id1_1, product_RUMM_1, extreme_persons = remove_extremes(items,id1,product_RUMM) 
        items_1, id1_1, product_RUMM_1, extreme_persons2 = remove_extremes(items[shave==2],id1[shave==2],product_RUMM[shave==2]) 
        #items.drop(extreme_persons.index,inplace=True)
        #items = items.dropna()       
        #id1 = id1[items.index]
        #product_RUMM = product_RUMM[items.index]
        #shave = shave[items.index]
            
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

stack = False
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

shave, shave_key = alphabet_conversion(shave)


    #product_key["Letter"] = letter_list

#shave_list = np.unique(shave)
#shave = shave.apply(str) #convert to string  
#for i in range(len(shave_list)):
#    letter = alphabet[i]
#    shave.replace(str(i+1),letter,inplace=True)


#% select each person at random over all 10 shaves

#select_every_person = False

#if select_every_person:
#    person_index = []
#    for j in range(len(shave_select)):
#        id_temp = id1[shave==shave_select[j]]
#        id_list = np.unique(id_temp)
#        for i in range(len(id_list)):
#            person = id_temp[id_temp==id_list[i]].index
#            selection = random.choice(person)
#            person_index.append(selection)

 #   id1 = id1[person_index]
 #   product_RUMM = product_RUMM[person_index]
 #   shave = shave[person_index]
 #   items = items.loc[person_index,:]
 
    
#%%stack the same people rating the same products, for each shave number
track = False
if track:
    shave_select = [10,9,8,7,6,5,4,3,2,1] #shave number to select the people for tracking (chose the one with the lowest number of participants)    
    #remove people who don't have a complete set of shaves, after the removal of the extremes
    id_list0 = np.unique(id1) 
    id_keep = []
    n = len(shave_select)
    id2 = id1.copy() #copy id list
    equal_samples = False
    if equal_samples:
        for i in range(len(id_list0)): #loop through each id
            person_prods = product_RUMM[id1==id_list0[i]] #products tested by each person
            prod_list = np.unique(person_prods)
            for j in range(len(prod_list)):
                no_shaves = len(person_prods[person_prods==prod_list[j]])
                if no_shaves < n: #if the number of shaves is less than the number under consideration
                    index1 = person_prods[person_prods==prod_list[j]].index
                    id2.drop(index1, axis=0, inplace=True)
    
        #only use data which has a full set of shaves            
        id1 = id1[id2.index]
        product_RUMM = product_RUMM[id2.index]
        shave = shave[id2.index]
        items = items.loc[id2.index,:]
#%    
    person_index = [] #initialise array of unique id indexes
    for j in range(len(shave_select)):
        if j == 0: #j = 0 corresponds to the last shave number
            id_temp = id1[shave==shave_select[j]]    
            id_list = np.unique(id_temp) #unique list of ids for corresponding shave number
            #select one test/product at random for each id
            for i in range(len(id_list)):
                person = id_temp[id_temp==id_list[i]].index
                selection = random.choice(person)
                person_index.append(selection)
            #list of unique ids with corresponding products for tracking (convert series to list)
            id_track = np.array(id1[person_index].array).tolist()
            product_track = np.array(product_RUMM[person_index].array).tolist()
            
            
            id_stack = id1[person_index] #make a copy of id tracking list
            id_original = id1[person_index] #keep copy of original id list
            #edit id for repeated shaves by adding the shave number afterwards (so that ids are distinct for each shave)
            index1 = id_stack.index
            id_stack = [str(id_stack.iloc[i]) + str(shave_select[j]) for i in range(len(id_stack))]
            id_stack = pd.Series(id_stack,index=index1)
            #create first sequence for stacked data, to be concatenated with data for remaining shave numbers
            id_stack = id_stack.astype(int)           
            product_stack = product_RUMM[index1]
            item_stack = items.loc[index1,:]
            shave_stack = shave[index1] 
        if j > 0:
            #select ids and products for new shave number
            id2 = id1[shave==shave_select[j]] 
            id2_list = np.unique(id2)
            prod2 = product_RUMM[shave==shave_select[j]]
            #extract the same ids and same tests as for the last shave (i=0)
            index_list = [] #initialise index list            
            for k in range(len(id2_list)):
                #find index for current shave, corresponding to the data for the last shave
                id2k = id2_list[k]
                if id2k in np.array(id_track):
                    ind_track = person_index[id_track.index(id2k)]
                    id0 = id2k               
                    prod0 = product_track[id_track.index(id2k)]  
                    index2 = prod2[(id2==id0) & (prod2==prod0)].index 
                else:
                    prod2k = random.choice(prod2[id2==id2k].array)
                    index2 = id2[(id2==id2k) & (prod2==prod2k)].index
                    id_track.append(id2k)
                    product_track.append(prod2[index2[0]])
                    person_index.append(index2[0])
                if len(index2) > 0:
                    index_list.append(index2[0]) #add index to list
            #extract the data            
            id_stack1 = id1[index_list] 
            id_original = pd.concat([id_original,id_stack1]) #keep copy of original id (before editing)
            product_stack1 = product_RUMM[index_list]
            item_stack1 = items.loc[index_list,:]
            shave_stack1 = shave[index_list]
            #id_track = id_stack1.copy() #update ids for tracking throughout
            #product_track = product_stack1.copy()
            #edit id for repeated shaves by adding the shave number afterwards
            #TO DO - make this optional
            index1 = id_stack1.index
            id_stack1 = [str(id_stack1.iloc[i]) + str(shave_select[j]) for i in range(len(id_stack1))]
            id_stack1 = pd.Series(id_stack1,index=index1)
            id_stack1 = id_stack1.astype(int)
            
            #concatenate data for each shave number
            id_stack = pd.concat([id_stack,id_stack1])
            product_stack = pd.concat([product_stack,product_stack1])
            item_stack = pd.concat([item_stack,item_stack1])
            shave_stack = pd.concat([shave_stack,shave_stack1])
    
    #copy stacked data to output data    
    id1 = id_stack.copy()
    product_RUMM = product_stack.copy()
    items = item_stack.copy()
    shave = shave_stack.copy()

#%%

person_list = np.unique(id1)
index_keep = []
for i in range(len(person_list)):
    person_prods = product_RUMM[id1==person_list[i]]
    product_i = random.choice(person_prods.array)
    person_index = id1[(id1==person_list[i]) & (product_RUMM==product_i)].index
    index_keep.extend(person_index.values)
    
index_keep = np.array(index_keep)
id1 = id1[index_keep]
product_RUMM = product_RUMM[index_keep]
shave = shave[index_keep]
items = items.loc[index_keep,:]


#%%
#remove extreme people from unique index list
anchor = False
if anchor:
    extreme_index = extreme_persons.index
    id_index = id_original.index
    id_ignore = id_index.isin(extreme_index)
    id_ignore = id_index[id_ignore]

    unique_index = select_every_person(shave_select,id_original)

    id_anchor = id1[unique_index] 
    product_anchor = product_RUMM[unique_index]
    items_anchor = items.loc[unique_index,:]
    shave_anchor = shave[unique_index]          
    
#% output final data set
#concatenate data - in this case with separate ratings and agreements
    
RUMM_out = pd.concat([id1, id1, shave, product_RUMM, items], axis=1, ignore_index = True)
if anchor:
    RUMM_anchor = pd.concat([id_anchor, shave_anchor, items_anchor], axis=1, ignore_index=True)

#write data and corresponding key to excel worksheet
index_out = True
if index_out:
    save_index = []
    for i in range(len(id1.index)):
        save_index.append(id1.index[i])
    save_index = pd.Series(save_index)

with pd.ExcelWriter("first_shave.xlsx") as writer:
    RUMM_out.to_excel(writer, sheet_name = 'data', index=None, header=False)
    if anchor:
        RUMM_anchor.to_excel(writer, sheet_name = 'anchor data', index=None, header=False)
    product_key.to_excel(writer, sheet_name = 'key')
    save_index.to_excel(writer, sheet_name = 'index')














