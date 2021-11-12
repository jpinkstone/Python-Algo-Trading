# Python-Algo-Trading
A Python bot that uses the RSI Index to choose when to buy and sell stocks. This is a personal project I completed myself.

This bot uses Alpaca to paper trade stocks. The program web scrapes live stock prices from Yahoo Finance to use and calculate the RSI Index for certain stocks. In addition, the program has a webserver with live data that shows what the bot is currently doing. All stocks are sold at the end of the day and a log is kept on all actions the bot performs for analysis. 

## Instructions
 - Simply edit the variables.py file to include the stocks you want the program to use. Also, change the Alpaca API key IDs to those of your account in the analysis.py and RSI.py files.
 - Run the app.py program on your computer with python3. Open a broswer window on your local computer and navigate to the URL localhost:8080 to see the live data webapp.

## Program Files
 - The app.py program runs the webapp with Dash and displays/ updates the html content
 - The layout.py program is the base html code for the website that does not get constantly updated
 - The analysis.py program gets live stock prices and completes the buying and selling of stocks
 - The variables.py program contains global variables that all the files use to communicate and organize the states
 - The RSI.py program calculated the RSI index for the chosen stocks and decides when the buy and sell
 - The log file is used to check what the program did and when
