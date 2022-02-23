# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 17:02:41 2022

@author: jeffr
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from functools import reduce
import datetime


# Getting dates, weeks, months, and years in a fixed date range
def get_fixedday(start = datetime.datetime(2015,12,31),
                  end = datetime.datetime(2022,1,25)):
    date = [start + datetime.timedelta(i) for i in range((end-start).days)]
    year = [i.year for i in date]
    month = [i.month for i in date]
    week,month=[],[]
    c_week = [i.strftime("%V") for i in date]+["done"]
    c_month = [i.strftime("%m") for i in date]+["done"]
    count = 1
    for i in range(len(year)):
        week.append(count)
        if c_week[i+1] != c_week[i]:
            count += 1   
    count = 1
    for i in range(len(year)):
        month.append(count)
        if c_month[i+1] != c_month[i]:
            count += 1      
    return pd.DataFrame({"Date":date,"year":year,"month":month,"week":week})
fixdate = get_fixedday()



# Getting the monthly Baker and Wulger components
bwm = pd.read_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\bwm.csv")


# Getting the original data for Baker and Wulger index
bw_ref = pd.read_csv(
    "C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\Investor_Sentiment_Data_20190327_POST.csv")
bw_ref = bw_ref.iloc[93:,0:8]
bw_ref.columns = ['yearmo','SENTu', 'SENT', 'pdnd', 'ripo', 'nipo', 'cefd', 's']
# Some cleaning
for i in bw_ref.columns[1:]:
    bw_ref[i] = pd.to_numeric(
        bw_ref[i].apply(
            lambda x: np.nan if str(x) == "." or str(x) == "na" else x))



# Simple OLS on the original Baker and Wulger Index
results = smf.ols(
    'SENT ~ cefd + ripo + nipo + s + pdnd - 1', 
    data=bw_ref.iloc[93:,:]).fit(cov_type = "HC0")
print(results.summary())




# Regressing the data I collected with the original Baker and Wulger Index
# There are only 18 matching observations but still return ~90% R^2
bw_reg = pd.concat([
    bw_ref.iloc[(714-93):,:].dropna().reset_index()[["SENTu","SENT"]],
    bwm.reset_index()],
    axis=1).dropna().drop("month",axis=1)

results = smf.ols(
    'SENT ~ CEFD + RIPO + NIPO + Sm + PDND - 1', 
    data=bw_reg).fit(cov_type="HC0")
print(results.summary())















