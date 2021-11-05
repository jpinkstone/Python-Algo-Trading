import alpaca_trade_api as tradeapi
import yfinance as yf
import requests, json, bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen

#ALPACA
API_ENDPOINT ="https://paper-api.alpaca.markets"
API_KEY_ID = "ADD HERE"
API_SECRET_KEY = "ADD HERE"

#ALPHA VANTAGE
ALPHA_KEY = "ADD HERE"
ALPHA_ENDPOINT = "https://www.alphavantage.co/query?"

#YAHOO FINANCE WEB SCRAPING
YF_ENDPOINT = "https://finance.yahoo.com/quote/"

api = tradeapi.REST(API_KEY_ID, API_SECRET_KEY, base_url=API_ENDPOINT)

def price(stock):
    page = urlopen(YF_ENDPOINT+stock)
    soup = bs4.BeautifulSoup(page,"html.parser")
    price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    return round(float(price.replace(',','')), 2)

def market_clock():
    try:
        clock = api.get_clock()

        return (clock.timestamp, clock.is_open, clock.next_open)
    except:
        return 'error'

def positions(symbol):
    open_positions = api.get_position(symbol)
    return int(open_positions.qty)

def buy(symbol, quantity):
    try:
        api.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
        return True
    except:
        return False

def sell(symbol, quantity):
    try:
        api.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')
        return True
    except:
        return False

def sell_trail(symbol, quantity, percent):
    try:
        api.submit_order(symbol=symbol, qty=quantity, side='sell', type='trailing_stop', trail_percent=percent, time_in_force='gtc')
        return True
    except:
        return False

# When open, pull data for 5 stocks
# When RSI < 30, buy 5qty of that stock and set trail percent to 5%: stop at 5 stocks
# When RSI > 70 for bought stock, sell
# Sell all at 3:50pm
