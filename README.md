# Baker-and-Wulger-Investment-Sentiment-Index
A Web Scraping exercise which utilizes Selenium and BeautifulSoup to reconstruct the Baker and Wulger Index within the period of 2017-07 to 2021-07

## Baker and Wulger Index
Investment Sentiment has been an increasing important field of study in finance and one of the pioneers in this field are Malcolm Baker and Jeffrey Wurgler, 
who constructed the popular Baker and Wulger Index (BW Index) in their famous 2006 paper. In their paper, they used 6 parameters and principal analysis to quantify
investment sentiment, namely:
1. Closed-end fund discount (CEFD) - the average difference between the net asset values (NAV) of closed-end stock fund shares and their market prices.
2. NYSE share turnover (NYSE)* - the ratio of reported share volume to average shares listed from the NYSE Fact Book
3. Number of IPOs (NIPO)
4. Average first-day returns (RIPO)
5. Share of equity issues in total equity and debt issues (S)
6. Dividend premium (PDND)

** As seen from Wulger's personal website (http://people.stern.nyu.edu/jwurgler/), he removes the NYSE measures from his newest update of the index.


## Project Introduction
Since 2018, Wulger has not updated its sentiment index and sadly I need to use it in my project. Hence, I tried to reconstruct the index for different source on the internet.

### Getting closed-end Fund data from Close-End Fund Advisors (https://cefdata.com/cefaindex/) - get_closeendfund.py
At the website, they includes differnet closed-end fund index from various sectors, as well as their Discount (Current Discount or Premium to NAV), and Net Asset value. 
The website provides weekly data in the format of an interative data. Therefore, Selenium is needed to iterate through all tables, 
i.e. click the date list, get all dates' xpath, copy the table *10000 by using Selenium.

### Getting IPOs data

