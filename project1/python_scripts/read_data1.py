"""
Script to open and re-structure Saudi data
raw data structure:
    usual brand, laundry habits, misc opinions (inc overall rating), ratings, agreements, attitudes, Person Factors
"""

import pandas as pd
import numpy as np

data = pd.read_excel('../data/raw/Saudi_data.xlsx') #read raw data

#separate data 

#column dividers for data separation
c1 = "Usual Brand P6M"
c2 = "Whether Usually Use Liquid Bleach - Personal"
c3 = "Rating For Cleaning Laundry Overall"
c4 = "Agreement With This Product Provides Excellent Value"
c5 = "Attitude Towards Benefit Removes All Greasy Food Stains With No Pretreating (Scrubbing Or Extra Products)"
c6 = "Sex Of Respondent"

usual_brand = data.loc[:,c1] #list of usual landry brands (i.e. facets in Rasch analysis)
    
laundry_habits = data.loc[:,c1+1:c2]

laundry_opinions = data.loc[:,c2+1:c3]

ratings = data.loc[:,c3+1:c4]

agreements = data.loc[c4+1:c5]

person_factors = data.loc[c5+1:c6]

#restructure for Rasch analysis

facets = np.unique(usual_brand) #count number of distinct laundry brands