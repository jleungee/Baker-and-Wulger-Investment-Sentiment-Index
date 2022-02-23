# Baker-and-Wulger-Investment-Sentiment-Index
A **Web Scraping project** which utilizes **Selenium** and **BeautifulSoup** to get the data in the **Baker and Wulger Index** within the period of 2017-07 to 2021-07. 

## Baker and Wulger Index
Investment Sentiment has been an increasing important field of study in finance and one of the pioneers in this field are Malcolm Baker and Jeffrey Wurgler, 
who constructed the popular Baker and Wulger Index (BW Index) in their famous 2006 paper (http://people.stern.nyu.edu/jwurgler/papers/wurgler_baker_cross_section.pdf).
In their paper, they used 6 parameters and principal analysis to quantify investment sentiment, namely:
1. Closed-end fund discount (CEFD) - the average difference between the net asset values (NAV) of closed-end stock fund shares and their market prices.
2. NYSE share turnover (NYSE)** - the ratio of reported share volume to average shares listed from the NYSE Fact Book
3. Number of IPOs (NIPO)***
4. Average first-day returns (RIPO)
5. Share of equity issues in total equity and debt issues (S)
6. Dividend premium (PDND)***

** As seen from Wulger's personal website (http://people.stern.nyu.edu/jwurgler/), he removes the NYSE measures from his newest update of the index.
*** 12-month lagged


## Project Introduction
I tried to reconstruct the Baker and Wulger index for different sources on the internet. However, the data can hardly be matched and I guess I just treat it as a Web Scraping
Exercise.
Here are some documents in this repository:
1. get_closeendfund.py - Closed-end fund data are scraped by using Selenium
2. get_equityissue.py - IPOs and SPOs data are scraped by using Selenium
3. pdnd.py - Dividend Premium data are scraped by using BeautifulSoup, requests and yfinance
4. baker and wulger.py - Further cleaning of all data and retrieving new IPOs data
5. Validation of BW Index - Testing the R^2 and significance of the original BW Index and the data I retrieved
6. bw.zip - All the csv files used and returned in this projects

Below are some further explanation of each section:

### 1. Getting closed-end Fund data 
At Close-End Fund Advisors (https://cefdata.com/cefaindex/), they includes differnet closed-end fund index from various sectors, as well as their Discount 
(Current Discount or Premium to NAV), and Net Asset value. The website provides weekly data in the format of an interative data. Therefore, 
Selenium is needed to iterate through all tables, i.e. click the date list, get all dates' xpath, copy the table *10000 by using Selenium (get_closeendfund.py).


### 2. Getting Equity and Debt Issuance Data
For equity issuance data, they could also be retreived from Nasdaq ("https://www.nasdaq.com/market-activity/spos") which have very similar formatting with the Nasdaq IPO data 
and the same program (get_equityissue.py) can be used to get them. I summed the SPOs in each week to get the weekly equity issuance data.
For debt issuance data, I can hardly find any detailed data source with weekly or monthly frequency. The closest thing I can get is the Nonfinancial Corporate Business; Debt
Securities and Loans; Liability, Level data from FRED (https://fred.stlouisfed.org/tags/series?t=corporate%3Bdebt&et=&ptic=1127&ob=pv&od=&tg=&tt=). To estimate weekly/monthly
debt issuance, I took the quarterly first difference and average them in a weekly/monthly scale.


### 3. Getting dividend premium data
The stocks considered to calculate are those listed in S&P 500. I did a quick scraping to get the stocks' tickers from Wikipedia
("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies") by using requests and BeautifulSoup. With the tickers, I can retrieve their dividends data from Yahoo Finance API
(yfinance). Dividend payers are those who have positive dividends in that year, and Non-dividend payers are those who don't. After separating the stocks in to payers and 
non-payers, I scraped the Price-to-Book ratio (which Book-to-Market Ratio is its reverse) of all the stocks from macrotrends (https://www.macrotrends.net/) (PS. there is "apple" 
in the scraping url but somehow it works) by using requests and BeautifulSoup. With all these data, I can calculate the weekly difference in Book-to-Market ratio of dividend 
payers and non-diviend payers.


### 4.1 Getting IPOs data
For 2017-2020 IPOs data, Wulger has suggested to get them Jay Ritter's website (https://site.warrington.ufl.edu/ritter/ipo-data/), where he will suggest you to get them from 
IPOScoop.com (https://www.iposcoop.com/scoop-track-record-from-2000-to-present/). To facilitate reading, I have done a bit formatting and saved it in IPOS.csv.
For IPO data after 2020, they could be retrieved from Nasdaq ("https://www.nasdaq.com/market-activity/ipos") where all the data, again, were stored in an interactive table.
Thus, Selenium is used to iterate through all the tables and retrieve the data (get_equityissue.py). From Nasdaq, I can get the symbols and Offer Amount of the new IPOs, 
to get the first day return,  I utilizes the yahoo finance API (yfinance) where I can obtain the first dat opening and closing price to get the first day return, only companies
that are still trading were considered (baker and wulger.py).


### 4.2 Cleaning Data for the BW Index
Cleaning the aforementioned data and combine them into one dataframe.


### 5. Validation of BW Index
Running regressions of the original data against the BW Index and the data I retrieved against the BW Index.
1. Original Data 

![Original](https://user-images.githubusercontent.com/70565542/155175176-2ed1f31e-1b4b-4d57-93a4-918b3dea8e13.png)

2. New Data (Sm is the parameter S adjusted in monthly)
![New ](https://user-images.githubusercontent.com/70565542/155406753-05d1972b-44af-4319-bcde-01da40d21647.png)







