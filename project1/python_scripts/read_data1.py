"""
Script to open and re-structure Saudi data
"""

import pandas as pd

data = pd.read_excel('../data/raw/Saudi_data.xlsx')

col_id = data.columns.get_loc("Proportion Of Loads Used Liquid Bleach Together With Regular Laundry Detergent In Past 6 Months")

laundry_habits = data.iloc[:,0:col_id+1]

col_id2 = data.columns.get_loc("Moment Of Greatest Frustration/ Disappointment About Usual Laundry Detergent")

usual_laundry_rating = data.iloc[:,col_id+1:col_id2+1]