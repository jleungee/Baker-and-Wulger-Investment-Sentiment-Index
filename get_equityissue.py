# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 16:37:30 2022

@author: jeffr
"""

import regex as re
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

driver = webdriver.Firefox() # Firefox becuz fubuki is my FRIEND

# Getting SPOs and IPOs data from Nasdaq
# url = "https://www.nasdaq.com/market-activity/ipos"
url = "https://www.nasdaq.com/market-activity/spos"
driver.get(url)

# Enlarge the browser
driver.maximize_window()

months = 62 # There are 62 months bewteen 2016-12 - 2022-01
start_page = 3 # the third item of the date bar


for page in range(months):   
    # Pressing the date buttons
    while True:
        try:
            driver.execute_script("window.scrollTo(0, 200)") 
            page_now = max(start_page-page,1)
            
            # Pressing the scroll left button
            if page_now == 1 and page >= start_page:
                WebDriverWait(
                    driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                              "/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/button[1]"))).click()
                        
            # Choose Date by pressing button
            WebDriverWait(
                driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, 
                          f"/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/button[{page_now}]"))).click()
            break
        # To escape Stale Element Error so much more
        except:
            driver.implicitly_wait(5)

    
    while True:
        # Getting the IPOs/SPOs data from table
        try:
            table = driver.find_elements_by_xpath(
                "/html/body/div[2]/div/main/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[5]/div[1]/div[1]/div/table/tbody/tr")
            tablelist = [i.text for i in table]
            break
        # To escape Stale Element Error so much more
        except:
            driver.implicitly_wait(5)
        
    # Concatting all data into a dataframe
    df_temp = []
    for r in range(len(tablelist)):
        tablerow = tablelist[r].split("\n")
        if len(tablerow) < 8:
            tablerow = tablerow[:4]+[""]+tablerow[4:]
        df_temp.append(tablerow)
      
    df_temp = pd.DataFrame(df_temp,columns = ["Symbol","Company Name",
                                              "Exchange/ Market","Price","Shares",
                                              "Date","Offer Amount","Actions"])
    
    if page == 0:
        df = df_temp
    else:
        df = pd.concat([df,df_temp])
driver.close()

# Saving the data
# df.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\equityissue.csv")
df.to_csv("C:\\Users\\jeffr\\Desktop\\FINA 4392\\BandW\\equityissuespo.csv")