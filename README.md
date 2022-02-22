# Baker-and-Wulger-Investment-Sentiment-Index
A Web Scraping exercise which utilizes Selenium and BeautifulSoup to reconstruct the Baker and Wulger Index within the period of 2017-07 to 2021-07

## Baker and Wulger Index
Investment Sentiment has been an increasing important field of study in finance and one of the pioneers in this field are Malcolm Baker and Jeffrey Wurgler, 
who constructed the popular Baker and Wulger Index (BW Index) in their famous 2006 paper (http://people.stern.nyu.edu/jwurgler/papers/wurgler_baker_cross_section.pdf.
In their paper, they used 6 parameters and principal analysis to quantify
investment sentiment, namely:
1. Closed-end fund discount (CEFD) - the average difference between the net asset values (NAV) of closed-end stock fund shares and their market prices.
2. NYSE share turnover (NYSE)* - the ratio of reported share volume to average shares listed from the NYSE Fact Book
3. Number of IPOs (NIPO)
4. Average first-day returns (RIPO)
5. Share of equity issues in total equity and debt issues (S)
6. Dividend premium (PDND)

** As seen from Wulger's personal website (http://people.stern.nyu.edu/jwurgler/), he removes the NYSE measures from his newest update of the index.


## Project Introduction
Since 2018, Wulger has not updated its sentiment index and sadly I need to use it in my project. Hence, I tried to reconstruct the index for different sources on the internet.
Here are some documents in this repository:
1. get_closeendfund.py - Closed-end fund data are scraped by using Selenium
2. get_equityissue.py - IPOs and SPOs data are scraped by using Selenium
3. pdnd.py - Dividend Premium data are scraped by using BeautifulSoup, requests and yfinance
4. baker and wulger.py - Further cleaning of all data and retrieving new IPOs data
5. Validation of BW Index - Testing the R^2 and significance of the original BW Index and the data I retrieved

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


## 3. Getting dividend premium data
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

Original data against the BW Index
----------------------------------
                                OLS Regression Results                                
=======================================================================================
Dep. Variable:                   SENT   R-squared (uncentered):                   0.675
Model:                            OLS   Adj. R-squared (uncentered):              0.672
Method:                 Least Squares   F-statistic:                              326.4
Date:                Tue, 22 Feb 2022   Prob (F-statistic):                   6.25e-157
Time:                        23:55:09   Log-Likelihood:                         -365.98
No. Observations:                 519   AIC:                                      742.0
Df Residuals:                     514   BIC:                                      763.2
Df Model:                           5                                                  
Covariance Type:                  HC0                                                  
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
cefd          -0.0736      0.004    -19.410      0.000      -0.081      -0.066
ripo          -0.0022      0.001     -2.149      0.032      -0.004      -0.000
nipo           0.0063      0.001      7.861      0.000       0.005       0.008
s              2.2733      0.304      7.476      0.000       1.677       2.869
pdnd          -0.0303      0.002    -13.749      0.000      -0.035      -0.026
==============================================================================
Omnibus:                      188.016   Durbin-Watson:                   0.137
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              925.449
Skew:                           1.532   Prob(JB):                    1.10e-201
Kurtosis:                       8.780   Cond. No.                         524.
==============================================================================


New data against the BW Index
-----------------------------
                                 OLS Regression Results                                
=======================================================================================
Dep. Variable:                   SENT   R-squared (uncentered):                   0.875
Model:                            OLS   Adj. R-squared (uncentered):              0.827
Method:                 Least Squares   F-statistic:                              174.0
Date:                Tue, 22 Feb 2022   Prob (F-statistic):                    1.96e-11
Time:                        23:55:09   Log-Likelihood:                          16.672
No. Observations:                  18   AIC:                                     -23.34
Df Residuals:                      13   BIC:                                     -18.89
Df Model:                           5                                                  
Covariance Type:                  HC0                                                  
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
CEFD           0.0034      0.002      2.207      0.027       0.000       0.006
RIPO          -0.0074      0.046     -0.162      0.871      -0.097       0.082
NIPO           0.0006      0.003      0.252      0.801      -0.004       0.006
Sm            -0.1116      0.065     -1.710      0.087      -0.240       0.016
PDND          -0.0004      0.000     -1.855      0.064      -0.001    2.07e-05
==============================================================================
Omnibus:                        1.185   Durbin-Watson:                   0.819
Prob(Omnibus):                  0.553   Jarque-Bera (JB):                0.405
Skew:                           0.363   Prob(JB):                        0.817
Kurtosis:                       3.111   Cond. No.                     1.87e+03
==============================================================================



