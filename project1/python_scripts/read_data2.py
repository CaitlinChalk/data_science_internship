"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import os

os.chdir("C:\\Users\\matcc\\LIDA_internship\\project1\\python_scripts")

import pandas as pd
import numpy as np
from scipy import stats
from RUMM_conversion import convert2RUMM #function to convert structured data to RUMM format
from data_manipulation import remove_text
from data_manipulation import remove_extremes
from string import ascii_lowercase
import random
import math
import datetime

data = pd.read_excel('../Data2_Shaving/shaving_data_original.xlsx') #read raw data

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

#function to edit id by appending it with an extra number (corresponding to shave or product for example)
#input: id2 - id series, addition - series containing factor to append to the id
#output: new id
def edit_id(id2,addition):
    index1 = id2.index
    id_new = [str(id2[index1[j]]) + str(addition[index1[j]]) for j in range(len(id2))]
    id_new = pd.Series(id_new,index=index1)
    id_new = id_new.astype(int)
    
    return id_new
#%sort data
#------------------------------------------------------------------------------
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
    shave_no = [2]
    data = data[shave.isin(shave_no)]
    id1 = id1[shave.isin(shave_no)]
    items = items[shave.isin(shave_no)]
    product = product[shave.isin(shave_no)]
    aspect = aspect[shave.isin(shave_no)]
    shave = shave[shave.isin(shave_no)]
    
#%
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
prod_only = ['Prod 6','Prod 18', 'Prod 19', 'Prod 2', 'Prod 31', 'Prod 32', 'Prod 29']
prods = prod_only + ['Prod 6 Control','Prod 18 Control', 'Prod 19 Control','Prod 2 Control','Prod 31 Control','Prod 32 Control','Prod 29 Control']
#%
prods = ['Control 1','Control 2']
#prods = ['Control 2']

#prods = np.unique(product)
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
    data = data[facet_select]
    
#%%track people over multiple tests, not shaves
test_track = True

if test_track:
    #replace months with actual date
    data['Date'].replace('Oct 2018',datetime.datetime(2018,10,1,0,0),inplace=True)
    data['Date'].replace('Nov 2018',datetime.datetime(2018,11,1,0,0),inplace=True)

    #identify dates which are not in the correct datetime format 
    not_dates = []    
    for i in range(len(data['Date'])):
        if type(data['Date'].iloc[i]) != datetime.datetime:
            not_dates.append(data['Date'].iloc[i])
    not_date_list = np.unique(not_dates)
    
    #check not_date_list and replace these dates with the correct datetime format
    data['Date'].replace('12/12/2016',datetime.datetime(2016,12,12,0,0),inplace=True)
    data['Date'].replace('15/6/2016',datetime.datetime(2016,6,15,0,0),inplace=True)
    data['Date'].replace('16/6/2016',datetime.datetime(2016,6,16,0,0),inplace=True)
    data['Date'].replace('8/6/2016',datetime.datetime(2016,6,8,0,0),inplace=True)
    
    #sort data by id and test date, for each product
    for i in range(len(prods)):
        data_i = data[product==prods[i]].copy()
        data_i.sort_values(['assessor','Date'],inplace=True)

        #get list of test numbers for each person    
        test_number = []
        id2 = data_i['assessor']
        id_list = np.unique(id2)
        for j in range(len(id_list)):
            n_tests = len(id2[id2==id_list[j]]) #total number of tests for that person
            test_list = list(range(n_tests)) #list of tests (e.g. [1,2,3])
            test_list = [test_list[x]+1 for x in test_list]
            test_number.extend(test_list) #add test list to array
    
        data_i['Test'] = test_number #add test numbers to original dataframe
    
                    
        data.loc[data_i.index,:] = data_i
    data.sort_values(['assessor','Test'],inplace=True)
    stack_tests = False
    
    if stack_tests:
        data.sort_values(['Test'],inplace=True)

    id1 = data['assessor']
    product = data['Product']
    test_no = data['Test']
    items = data.loc[:,"Q1":"Q10"] 
    
    remove_tests = True #remove tests (e.g. if the sample size is too small for that test)
    
    if remove_tests:
        max_test = 3
        id1 = id1[test_no <= max_test]
        product = product[test_no <= max_test]
        items = items[test_no <= max_test]
        test_no = test_no[test_no <= max_test]
        
#%% change item responses to pairwise 
    
pairwise1 = False
if pairwise1:
    items2 = items.copy()  
    id_list = np.unique(id1)
    index_del = [] #to keep track of removed indices
    for i in range(len(id_list)):
        prod_i = product[id1==id_list[i]]
        con_only = prod_i[prod_i.str.contains('Control')] #controls only
        prod_only = prod_i[~prod_i.str.contains('Control')] #test products only
        prod_list = np.unique(prod_only) #list of unique test products
        #remove control product if there is no corresponding test product
        if len(con_only) > len(prod_only): #if there are more control product responses than test product responses
            for k in range(len(con_only)):
                product_k = con_only.iloc[k].strip(' Control') #name of test product
                if not product_k in prod_only.array: #if corresponding test product isn't in survey data
                    index2 = prod_i[prod_i==con_only.iloc[k]].index[0]
                    items2.drop(index2,inplace=True) #remove control product
                    index_del.append(index2)
        for j in range(len(prod_only)):
            control = prod_only.iloc[j] + ' Control'
            index1 = prod_only[prod_only==prod_only.iloc[j]].index[0]
            if control in prod_i.array:
                index2 = prod_i[prod_i==control].index[0]
                item1 = items.loc[index1,:] #test product responses
                item2 = items.loc[index2,:] #control product responses
                cond1 = item1 > item2
                cond2 = item2 > item1
                cond3 = item1 == item2
                if len(cond1) > 0: #if test prod > control
                    items2.loc[index1,cond1[cond1].index]=1#test product score is higher than control
                    items2.loc[index2,cond1[cond1].index]=0 #control product score is less than test
                if len(cond2) > 0: #if test prod > control
                    items2.loc[index1,cond2[cond2].index]=0 #control product score is less than test 
                    items2.loc[index2,cond2[cond2].index]=1 #test product score is higher than control
                if len(cond3) > 0: #if test prod = control prod
                    equals = np.unique(item1[cond3])
                    for k in range(len(equals)):
                        ans = item1[cond3][item1[cond3]==equals[k]]
                        ans_Q = item1[cond3][item1[cond3]==equals[k]].index
                        if ans.iloc[0] <= 3:
                            items2.loc[index1,ans_Q]=0
                            items2.loc[index2,ans_Q]=0
                        else:
                            items2.loc[index1,ans_Q]=1
                            items2.loc[index2,ans_Q]=1
            else:
                items2.drop(index1,inplace=True)
                index_del.append(index1)
        
        items = items2.copy()
        id1 = id1[items2.index].copy()
        product = product[items2.index].copy()
        shave = shave[items2.index].copy()
        
pairwise2 = False
#restructure data to be in pairwise format
if pairwise2:
    items2 = items.copy()  
    Q_list = items.copy().columns
    id_list = np.unique(id1)
    n_items = len(items.columns)
    col_names = prod_only.copy()
    col_names.append('Control 2') #list of products
    row_names = col_names.copy()
    col_names.append('ID')
    col_names.append('Item')
    rows = row_names*len(id_list)*n_items
    data2 = pd.DataFrame(index=rows, columns=col_names)
    data_pw = pd.DataFrame(columns=['Item1','Item2','Preferred','ID','Question'])
    k=0
    for m in range(n_items):        
        for i in range(len(id_list)):
            data_snip = data2.iloc[k:k+len(row_names),:].copy() #data for person i and item m
            prod_i = product[id1==id_list[i]] #full product list
            prods_only = prod_i[~prod_i.str.contains('Control')] #products only (no controls)
            for j in range(len(prods_only)):
                prod1 = prods_only.iloc[j] #first product for comparison with another
                index1 = prods_only[prods_only==prod1].index[0]
                item1 = items.loc[index1,Q_list[m]]
                col1 = prod1          
                #product - product comparison
                for l in range(j+1,len(prods_only)):
                    prod2 = prods_only.iloc[l]
                    index2 = prods_only[prods_only==prod2].index[0]
                    item2 = items.loc[index2,Q_list[m]]
                    col2 = prod2
                    #compare responses for product 1 and product 2
                    if item1>item2:
                        data_snip.loc[col1,col2] = 1
                        data_snip.loc[col2,col1] = 0
                        data_pw = data_pw.append({'Item1': prod1, 'Item2': prod2, 'Preferred': prod1, 'ID': id_list[i], 'Question': m+1},ignore_index=True)
                    if item2>item1:
                        data_snip.loc[col2,col1] = 1
                        data_snip.loc[col1,col2] = 0
                        data_pw = data_pw.append({'Item1': prod1, 'Item2': prod2, 'Preferred': prod2, 'ID': id_list[i], 'Question': m+1},ignore_index=True)
                    if item2==item1:
                        if item1 <= 3:
                            data_snip.loc[col1,col2] = 0
                            data_snip.loc[col2,col1] = 0
                        else:
                            data_snip.loc[col1,col2] = 1
                            data_snip.loc[col2,col1] = 1
                #product - control comparison
                control = prod1 + ' Control'
                if control in prod_i.array:
                    index2 = prod_i[prod_i==control].index[0]
                    item2 = items.loc[index2,Q_list[0]]
                    col2 = 'Control 2'
                    if item1>item2:
                        data_snip.loc[col1,col2] = 1
                        data_snip.loc[col2,col1] = 0
                    if item2>item1:
                        data_snip.loc[col2,col1] = 1
                        data_snip.loc[col1,col2] = 0
                    if item2==item1:
                        if item1 <= 3:
                            data_snip.loc[col1,col2] = 0
                            data_snip.loc[col2,col1] = 0
                        else:
                            data_snip.loc[col1,col2] = 1
                            data_snip.loc[col2,col1] = 1
                # insert random selection for product with itself
                data_snip.loc[col1,col1] = random.choice([0,1])
            data_snip['ID'] = id_list[i]
            data_snip['Item'] = m+1
            data2.iloc[k:k+len(row_names),:] = data_snip
        
            k=k+len(row_names)
                    
    data3 = data2.copy()
    data3['product']=data3.index #add column of product info
    data3['index'] = list(range(len(data3)))
    
    data3.set_index('index',inplace=True) #set index to be unique ID
    
    items = data3.iloc[:,0:len(row_names)].copy() #copy question responses to data
    id1 = data3['ID'].copy() #extract ID
    product = data3['product'].copy() #extract products 
    question = data3['Item'].copy()
    items = items.dropna(how='all') #remove entries with no responses      
    product = product[items.index]  #remove corresponding product entries  
    question = question[items.index] 
    id1 = id1[items.index] #extract ID
   
    fill_all_nans = False
    
    if fill_all_nans:
        for j in range(len(items.columns)):
            for i in range(len(items)):
                if items.isna().iloc[i,j]:
                    items.iloc[i,j] = random.choice([0,1])
        #rand_1 = 
        
    
    
#%% convert product to RUMM format
#products   
product_RUMM, product_key = convert2RUMM(product,0) #function to convert PF data into RUMM format

#aspects
PF_RUMM, PF_key = convert2RUMM(aspect,0) 
#%

#pairwise
if pairwise2:
    data_pw.iloc[:,0:3], product_key = convert2RUMM(data_pw.iloc[:,0:3],0)

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
        
#%% rack or stack the data
stack = False
rack = True
id_edit = False #True if you want to edit the IDs corresponding to the different shaves or products
if stack: #stack the data, by having the data for different shaves stacked on top of each other
                 #the length of the data increases, while the width stays the same
    id_original = id1.copy()
    if test_track: #rack tests instead of shaves if tracking tests
        shave = test_no.copy()
    shave_select = [3,6] #corresponding to the stacked data
    for i in range(len(shave_select)):  
        if i == 0: #initialise stack
            id_stack = id1[shave==shave_select[i]].copy()
            if id_edit:
                id_stack = edit_id(id_stack,product_RUMM)                        
            product_stack = product_RUMM[shave==shave_select[i]].copy()
            item_stack = items[shave==shave_select[i]].copy()
            shave_stack = shave[shave==shave_select[i]].copy()
        
        if i > 0:
            #edit id for repeated shaves by adding the shave number afterwards
            id_stack1 = id1[shave==shave_select[i]].copy()
            product_stack1 = product_RUMM[shave==shave_select[i]].copy()
            item_stack1 = items[shave==shave_select[i]].copy()
            shave_stack1 = shave[shave==shave_select[i]].copy()
                        
            if id_edit:
                id_stack1 = edit_id(id_stack1,product_RUMM)

            id_stack = pd.concat([id_stack,id_stack1],axis=0)
            product_stack = pd.concat([product_stack,product_stack1],axis=0)
            item_stack = pd.concat([item_stack,item_stack1],axis=0)
            shave_stack = pd.concat([shave_stack,shave_stack1],axis=0)
        
    id1 = id_stack.copy()
    product_RUMM = product_stack.copy()
    items = item_stack.copy()
    shave = shave_stack.copy()

#rack the data, by having the data from different shaves adjacent to each other
#%the length of the data stays the same, while the width increases
if rack:
    id_original = id1.copy()
    if test_track: #rack tests instead of shaves if tracking tests
        shave = test_no.copy()
    shave_select = [1,3]    
    id_list = np.unique(id_original)
    index_both = []
    index0 = []
    index1 = []
    #extract the IDs of the people who have completed both shaves, and those who have completed one or the other only
    for i in range(len(id_list)):
        product_list = np.unique(product_RUMM[id1==id_list[i]])
        for j in range(len(product_list)):
            shave_list = shave[(id1==id_list[i]) & (product_RUMM==product_list[j])]
            if shave_select[0] in shave_list.array and shave_select[1] in shave_list.array:
                index_j = shave_list[shave_list.isin([shave_select[0],shave_select[1]])].index
                index_both.extend(index_j)
            if shave_select[0] in shave_list.array and not shave_select[1] in shave_list.array:
                index_j = shave_list[shave_list.isin([shave_select[0]])].index
                index0.extend(index_j)
            if not shave_select[0] in shave_list.array and shave_select[1] in shave_list.array:
                index_j = shave_list[shave_list.isin([shave_select[1]])].index
                index1.extend(index_j)
#%
    #concat shaves 1 and 2 for the data containing both
    #add rows of NaNs to data that contains one of the two shaves only
    #both shaves:
    items0 = items[shave==shave_select[0]].copy()
    items1 = items[shave==shave_select[1]].copy()
#%    
    #edit column names for the second set of items
    shave1_items = items1.columns
    new_name = shave1_items + 'b' #add b to each item in the second set
    col_dict = dict(zip(shave1_items,new_name))
    items1.rename(columns=col_dict,inplace=True)
    
    #extract the items which correspond to people who completed both shaves
    item_rack0 = items0[items0.index.isin(index_both)].copy() #shave 1
    item_rack1 = items1[items1.index.isin(index_both)].copy() #shave 2
    
    #reindex data for horizontal concatenation
    index_dict = dict(zip(item_rack1.index,item_rack0.index))
    item_rack1.rename(index_dict,inplace=True)
    
    #append data for shave 1 or 2 (for the people who haven't answered both)
    if len(index0) > 0:
        item_rack0 = pd.concat([item_rack0,items0[items0.index.isin(index0)]],axis=0)
    if len(index1) > 0:
        item_rack1 = pd.concat([item_rack1,items1[items1.index.isin(index1)]],axis=0)
    
    #horizontally concatenate the data from the different shaves    
    item_rack = pd.concat([item_rack0,item_rack1],axis=1)   
    
    #corresponding ids and products for the racked data:
    id_rack = id1[item_rack.index].copy()
    product_rack = product_RUMM[item_rack.index].copy()
    shave_rack = shave[item_rack.index].copy()
    
    #copy racked data to output data
    id1 = id_rack.copy()
    product_RUMM = product_rack.copy()
    shave = shave_rack.copy()
    items = item_rack.copy()
    if test_track:
        test_no = shave.copy()

#convert product key to alphabetical
    
product_RUMM, product_key2 = alphabet_conversion(product_RUMM)
   
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

#%
approach4 = False

if approach4:

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

#id1, id_original = edit_id(id1,product_RUMM)
#%
#remove extreme people from unique index list
anchor = True
if anchor:
    if extremes:
        extreme_index = extreme_persons.index
        id_index = id_original.index
        id_ignore = id_index.isin(extreme_index)
        id_ignore = id_index[id_ignore]

    unique_index = select_every_person(np.unique(test_no),id1)

    id_anchor = id1[unique_index] 
    product_anchor = product_RUMM[unique_index]
    items_anchor = items.loc[unique_index,:]
    shave_anchor = shave[unique_index] 
    if test_track: #anchor with test numbers (not shave numbers), if tracking the people over tests
        shave_anchor = test_no[unique_index]         
    
#%% output final data set
#concatenate data - in this case with separate ratings and agreements
    
RUMM_out = pd.concat([id1, id1, product_RUMM, items], axis=1, ignore_index = True)
if pairwise2:
    RUMM_out = pd.concat([id1, id1, product_RUMM, question, items], axis=1, ignore_index = True)
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
    if pairwise2:
        data_pw.to_excel(writer, sheet_name = 'pairwise data', index=None)
    product_key.to_excel(writer, sheet_name = 'key')
    save_index.to_excel(writer, sheet_name = 'index')














