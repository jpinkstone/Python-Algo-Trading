import yfinance as yf
import datetime
import requests
import bs4
import time
import alpaca_trade_api as tradeapi
from bs4 import BeautifulSoup
from urllib.request import urlopen

#stored = [263,262.93,263.05,263.09,263.31,263.39,263.67,263.59,263.65,263.15,262.92,262.96,262.41,261.80]
##stored = []
##update_time = time.strftime("%M")
##
##while True:
##    if update_time != time.strftime("%M"):
##        update_time = time.strftime("%M")
##
##        data = yf.Ticker("AAPL")
##        print(data.info["bid"])

#ALPACA
API_ENDPOINT ="https://paper-api.alpaca.markets"
API_KEY_ID = "ADD HERE"
API_SECRET_KEY = "ADD HERE"

api = tradeapi.REST(API_KEY_ID, API_SECRET_KEY, base_url=API_ENDPOINT)

open_positions = api.get_position('TSLA')
print(open_positions)

# open_positions = api.list_orders(nested=True)
# print(open_positions)

#print(api.submit_order(symbol='FB', qty=5, side='sell', type='market', time_in_force='gtc'))

##def parsePrice():
##    url = 'https://finance.yahoo.com/quote/FB'
##    page = urlopen(url)
##    soup = bs4.BeautifulSoup(page,"html.parser")
##    price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
##    return float(price.replace(',',''))
##while True:
##    print(parsePrice())

##today = datetime.datetime.today().isoformat()
##data = yf.Ticker("AAPL")
##tickerDF = data.history(period='1d', start='2021-2-2', end=today[:10])
##priceLast = tickerDF
##print(priceLast)

##if len(stored) >= 14:
##    new_stored = stored[-14:]
##    new_diff_up, new_diff_down = [], []
##    for x in range(0, 13):
##        if new_stored[x+1] > new_stored[x]:
##            new_diff_up.append(new_stored[x+1] - new_stored[x])
##        elif new_stored[x+1] < new_stored[x]:
##            new_diff_down.append(new_stored[x] - new_stored[x+1])
##    avg_up = sum(new_diff_up) / len(new_diff_up)
##    avg_down = sum(new_diff_down) / len(new_diff_down)
##
##    rsi = 100 - (100/(1+(avg_up/avg_down)))
##    print(rsi)
##
##prices = {'GOOGL': [], 'NVDA': [], 'AAPL': [], 'NVAX': [], 'FB': []}
##
##for x in range(0, 4):
##    for stock in ['GOOGL', 'NVDA', 'AAPL']:
##        prices[stock].append(x)
##
##prices['GOOGL'] = prices['GOOGL'][-2:]
##print(prices)
##
##gg=[]
##print(len(gg))

# for keys, values in data.info.items():
#     print(keys + ": " + str(values))

# msft.info['bid'] = price
# msft.info['dayHigh'] = high
# buytrigger = high - 1
    
# if msft.info['bid'] >= buytrigger
#     print("buynow")
    
        

# get stock info
# print(msft.info['ask'])
# print(msft.info['bid'])
# print(msft.info['open'])
