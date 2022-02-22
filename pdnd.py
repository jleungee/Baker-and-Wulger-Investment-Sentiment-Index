# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 18:13:35 2022

@author: jeffr
"""

import requests 
import pandas as pd
from bs4 import BeautifulSoup
import regex as re
import yfinance as yf
from tqdm import tqdm
import datetime

# Getting dates, weeks, months, and years in a fixed date range
def get_fixedday(start = datetime.datetime(2016,12,31),
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

# S&P 500 Wikipedia page for getting the tickers of S&P 500 tickers
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")
souplist = [re.sub("\n","",i.get_text()) for i in soup.find_all("td")]
wiki = []
for i in range(len(souplist)):
    if i%9 == 0:
        temp = []
        wiki.append(temp)
    temp.append(souplist[i])

# 505 common stocks from S&P 500
wiki = pd.DataFrame(wiki).iloc[:505,:]
ticklist = wiki.iloc[:,0] # Just getting the ticker list
tickchange = {"BRK.B":"BRK-B","BF.B":"BF-B"}
for i in range(len(ticklist)):
    if ticklist[i] in tickchange:
        ticklist[i] = tickchange[ticklist[i]]




# Dividend history from yahoo finance
for i in tqdm(range(len(ticklist))):
    t = ticklist[i]
    tick = yf.Ticker(t)
    tickdiv = tick.dividends
    tickdiv.index = pd.to_datetime(tickdiv.index)
    tickdiv = pd.merge(fixdate[["Date","year"]], 
                        tickdiv[tickdiv.index > "2017-01-01"],
                        on = "Date",
                        how = "left").dropna()
    
    # Just to see if that week has any dividends
    # A firm is a payer in year t if it has positive dividends per share
    tickdiv = tickdiv[["year","Dividends"]].groupby("year").sum()      
    tickdiv[tickdiv["Dividends"]>0] = 1
    tickdiv[tickdiv["Dividends"]<=0] = 0
    tickdiv.columns = [t] # Change column names
        
    # Merging dataframes into a large dataframe
    if i == 0:
        div = tickdiv
    else:
        div = pd.merge(div,tickdiv,on="year",how="left")
    
div = div.fillna(0)
div.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\div.csv")




# Getting Price to Book Ratio from mactrotrend.com
for tick in tqdm(range(len(ticklist))):
    t = ticklist[tick]
    url = f"https://www.macrotrends.net/stocks/charts/{t}/apple/price-book"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    souplist = [
        i.get_text() for i in soup.find_all("td") 
        if sum([j.isalpha() for j in i.get_text()]) == 0 ]
    pb = []
    for i in range(len(souplist)):
        if i%4 == 0:
            temp = []
            pb.append(temp)
        temp.append(souplist[i])
    pb = pd.DataFrame(pb,
                      columns=["Date",
                                "Stock Price",
                                "Book Value per Share",
                                "MB ratio"]).iloc[:-40,:]
    
    pb["Date"] = pd.to_datetime(pb["Date"])
    pb = pb[pb["Date"] >= "2016-12-31"]
    pb["MB ratio"] = 1/pd.to_numeric(pb["MB ratio"])
    pb["tick"] = t
    pb = pd.merge(fixdate[["Date","year","month","week"]],pb,on="Date",how="left")
    pb = pb.fillna(method = 'bfill')[
        ["Date","year","month","week","MB ratio",'tick']].dropna()
    
    if tick == 0:
        pb_df = pb
    else:
        pb_df = pd.concat([pb_df,pb])       
pb_df.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\MB Ratio.csv")
        
