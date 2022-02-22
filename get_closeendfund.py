# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 00:11:18 2022

@author: jeffr
"""
import regex as re
from selenium import webdriver
import pandas as pd
import numpy as np
driver = webdriver.Firefox()
# CEF Advisors' CEF/BDC Indexes
url = "https://cefdata.com/cefaindex/"
driver.get(url)

# As the data is in an interactive table, I need to iterate along dates
date = Select(driver.find_element_by_xpath('//*[@id="datePick"]'))
datelist = date.options
date_text = [i.text for i in datelist]

for i in range(len(datelist)):
    # the same element
    date = Select(driver.find_element_by_xpath('//*[@id="datePick"]'))
    # not click but select      
    date.select_by_index(i)
    
    # Getting the data table
    table_xpath = f'//*[@id="DataTables_Table_0"]/tbody/tr'
    temp = driver.find_elements_by_xpath(table_xpath)
    df_temp = [h.text for h in temp]
    df_part = []
    
    # Formatting the data obtained
    for t in range(len(df_temp)):
        row_temp = df_temp[t].split("Index")
        df_part.append([row_temp[0].split('. ')[1]] + row_temp[1].split())
    df_part = pd.DataFrame(df_part)
    df_part["Date"] = date_text[i]
    
    if i == 0:
        closefund = df_part
    else:
        closefund = pd.concat([closefund,df_part])
    
    # Allow some time for the program to process
    driver.implicitly_wait(2)
driver.close()

# Further cleaning the data and export it into csv
closefund["Date"] = pd.to_datetime(closefund["Date"])
closefund = closefund.set_index("Date")
col = ['Index','Discount','1 Yr Avg Discount','3 Yr Avg Discount',
           '5 Yr Avg Discount','10 Yr Avg Discount','Rel Disc Range(3yr)',
           'Mk Yield','Lev Adj NAV Yield','After Tax Yield',
           'Est. Tax Friction','1 Yr RoC %','3 Yr Dest RoC %','Lev %',
           'Non Lev Expense Ratio','3 Yr NAV Volatility','% Equity Exposure',
           '% Bond Exposure','Holdings','Cash Weighted Duration','Beta (2yr)',
           'Comp NAV TR','Comp Discount','Net Assets',
           'Liquidity - 90 day (K)']
closefund.columns = col

# Change all N/A to np.nan and all cell with "," to numbers
for i in range(1,len(col)):
    for j in range(len(closefund.iloc[:,i])):      
        if closefund.iloc[j,i] == "N/A":
            closefund.iloc[j,i] = np.nan
        if "," in str(closefund.iloc[j,i]):
            closefund.iloc[j,i] = re.sub(",","",closefund.iloc[j,i])
            
    closefund[col[i]] = pd.to_numeric(closefund[col[i]])
closefund.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\CEF.csv")







