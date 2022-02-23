# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 21:39:56 2022

@author: jeffr
"""

import pandas as pd
from tqdm import tqdm
import datetime
import regex as re
import numpy as np
import yfinance as yf
from functools import reduce


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




# Closed end fund (CEFD)
# the average difference between the net asset values (NAV) of closed-end 
# stock fund shares and their market prices
cef = pd.read_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\CEF.csv")
cef = cef[["Date","Discount","Net Assets"]]
sum_assets = cef[["Date","Net Assets"]].groupby("Date").sum()
sum_assets.columns = ["sum"]
cef = pd.merge(cef,sum_assets,on="Date",how="left")
cef["Discount"] = cef["Discount"] * cef["Net Assets"]/cef["sum"]

cef = cef[["Date","Discount"]].groupby("Date").sum()
cef.columns = ["CEFD"]
cef.index = pd.to_datetime(cef.index)
cef = pd.merge(fixdate[["Date","week"]],
                cef,
                on="Date",
                how="left").drop(["Date"],axis=1)
cef = cef[cef["week"]>27].fillna(method="bfill").dropna()
cef = cef.groupby("week").sum()




# IPOs, (NIPO) and (RIPO) 2017-2020
# from https://www.iposcoop.com/
ipos = pd.read_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\IPOS.csv")
ipos = ipos[["Date","Opening Price","1st Day Close"]]
ipos["Date"] = pd.to_datetime(ipos["Date"])
ipos.columns = ["Date","op","ed"]
ipos["RIPO"] = np.log(ipos["ed"])-np.log(ipos["op"])
IPOs = ipos.drop(["op","ed"],axis=1).groupby("Date").sum()
NIPO = ipos.drop(["op","ed"],axis=1).groupby("Date").count()
IPOs = pd.concat([IPOs,NIPO],axis=1)
IPOs.columns = ["RIPO","NIPO"]

# IPOs, (NIPO) and (RIPO) 2020-2021
ipoissue = pd.read_csv(
    "C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\equityissue.csv").iloc[:,1:]
ipoissue = ipoissue[["Date","Symbol"]]
ipoissue["Date"] = pd.to_datetime(ipoissue["Date"])
# Getting new IPOs first day price from Yahoo Finance, 
# takes a long time to run
new_ipo = ipoissue[ipoissue["Date"]  >'2020-09-11']
RIPO2 = []
error = []
new_ipo["Symbol"] = [
    re.sub("'","-",i)+"N" if "'"in i else i for i in new_ipo["Symbol"]]
for i in tqdm(range(len(new_ipo.iloc[:,0]))):
    try:
        t = new_ipo["Symbol"][i]
        tick_temp = yf.Ticker(t).history(period="max").iloc[0,:]    
        RIPO2.append(np.log(tick_temp["Close"]) - np.log(tick_temp["Open"]))
    except:
        error.append(t)
        RIPO2.append(np.nan)
new_ipo["RIPO"] = RIPO2
new_ipo["Symbol"] = [1 if i not in error else 0 for i in new_ipo["Symbol"]]
NIPO = new_ipo.groupby("Date").sum()["Symbol"]
RIPO = new_ipo[["Date","RIPO"]].groupby("Date").sum()
IPOs2 = pd.concat([RIPO,NIPO],axis=1)
IPOs2.columns = ["RIPO","NIPO"]
IPOs2 = IPOs2.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
IPO = pd.concat([IPOs,IPOs2])
IPO = pd.merge( # shift 12 months
    fixdate[["Date","week"]],
    IPO,
    on="Date",
    how = "left").drop(["Date"],axis=1).groupby("week").sum().shift(52)




# Share of equity - ratio of equity issue and debt issue (S)
spoissue = pd.read_csv(
    "C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\equityissuespo.csv").iloc[:,1:]
spoissue["Offer Amount"] = pd.to_numeric(spoissue["Offer Amount"])
spoissue["Date"] = pd.to_datetime(spoissue["Date"])
sm = pd.merge(fixdate,
              spoissue[["Date","Offer Amount"]],
              on="Date",
              how="left")[["month","Offer Amount"]].groupby("month").sum()
spoissue = pd.merge(fixdate,
                    spoissue[["Date","Offer Amount"]],
                    on="Date",
                    how="left")[["week","Offer Amount"]].groupby("week").sum()
debtissue = pd.read_csv(
    "C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\BCNSDODNS.csv")
debtissue.columns = ["Date","debt"]
debtissue["Date"] = pd.to_datetime(debtissue["Date"])
debtissue["debt"] = pd.to_numeric(
    debtissue["debt"].apply(lambda x: np.nan if str(x) == "." else x)).diff()
debtissue = pd.merge(fixdate,
                      debtissue[debtissue["Date"]>="2016-12-31"],
                      on="Date",
                      how="left")
count = []
quarter = 1
for i in debtissue.iloc[:,4]:
    count.append(quarter)
    if str(i) != "nan":
        quarter += 1
debtissue["quarter"] = count
debtissue = pd.merge(debtissue.iloc[:,[0,1,2,3,5]],
                      debtissue.fillna(0).groupby("quarter").mean()[["debt"]],
                      on="quarter",
                      how="left").iloc[2:,:]
debtissue = debtissue[debtissue["debt"]!=0]
debtissue["debt"] = debtissue["debt"] * 1000000000
dm = debtissue[["month","debt"]].groupby("month").sum() # monthly
debtissue = debtissue[["week","debt"]].groupby("week").sum()
S = pd.merge(spoissue,debtissue,on="week")
Sm = pd.merge(sm,dm,on="month") # monthly
Sm["Sm"] = S["Offer Amount"]/S["debt"] # monthly
Sm = Sm.drop(["Offer Amount","debt"],axis=1) # monthly
S["S"] = S["Offer Amount"]/S["debt"]
S = S.drop(["Offer Amount","debt"],axis=1)
S = pd.merge(S,
              pd.merge(fixdate[["month","week"]],
                      Sm,
                      on="month",
                      how="left"),
              on="week",
              how="left").groupby("week").last()




# (PDND) differnece of the average market to book ratio of dividend payers and
# non payers
pdnd = pd.read_csv(
    "C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\MB ratio.csv").iloc[:,1:]
div = pd.read_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\div.csv")
div = div.set_index("year").stack()
div.index.names = ["year","tick"]
div = pd.DataFrame(div,columns=["div"])
div[div["div"] == 0] = -1
pdnd = pd.merge(pdnd,
                div,
                on=["tick","year"])
pdnd["PDND"] = pdnd["MB ratio"]*pdnd["div"]
pdnd = pdnd.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
pdnd = pdnd[["week","PDND","div"]].groupby(["week","div"]).sum()
pdnd = pdnd.groupby("week").mean().shift(52) # shifting 12 months




# Construction of the Baker and Wulger Index
# Weekly
bw = reduce(lambda x,y: pd.merge(x,y,on="week"),[cef,IPO,S,pdnd])
bw = bw[(bw!=0).all(1)]
bww = bw.drop(["Sm","month"],axis=1)
bww.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\bww.csv")

# Monthly
bwm = reduce(lambda x,y: pd.merge(x,y,on="month"),
             [bw[["month","Sm"]].groupby("month").mean(),
              bw[["NIPO","month"]].groupby("month").sum(),
              bw[["RIPO","month"]].groupby("month").sum(),
              bw[["CEFD","PDND","month"]].groupby("month").mean()])
bwm.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\bwm.csv")

print(bwm)

