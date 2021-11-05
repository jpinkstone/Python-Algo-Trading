import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import time, datetime, plotly
import plotly.graph_objs as go
from analysis import market_clock, positions, buy, sell, sell_trail, price
from layout import html_layout
from variables import *

start_time = time.time()
update_time = time.strftime("%M")

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "JP Algo Trading Bot Dashboard"
app.layout = html_layout

@app.callback(Output('live-update-nav', 'children'), Input('interval-component', 'n_intervals'))
def update_nav(n):
    check()
    global state, state_icon

    return [
        html.Ul([
            html.Li([
                html.Button(["Status", html.Div([], className="spinner-grow spinner-grow-sm " + state_icon + " ms-2")], className="btn btn-light", disabled=True)
            ], className='nav-item'),
            html.Li([
                html.A(datetime.datetime.now().strftime('%a %b %d %I:%M:%S %p'), className="nav-link")
            ], className="nav-item")
        ], className='navbar-nav')
        ]

@app.callback(Output('live-update-market', 'children'), Input('interval-component', 'n_intervals'))
def update_metrics(n):
    global state

    if state == "API connection lost":
        return[
            html.Li('API connection lost. Trying to reconnect...', className='list-group-item')
        ]
    else:
        m_clock = market_clock()
        timestamp, is_open, next_open = m_clock[0], m_clock[1], m_clock[2]
        return [
            html.P('Current date: {}'.format(pd.Timestamp.date(timestamp)), className="fw-bold mt-3"), 
            html.P('Current time: {}'.format(timestamp.strftime('%I:%M:%S %p')), className="fw-bold"), 
            html.P('Market open: {}'.format(is_open), className="fw-bold"), 
            html.P('Next open: {}'.format(pd.Timestamp.date(next_open)), className="fw-bold")
            ]

@app.callback(Output('live-update-terminal', 'children'), Input('interval-component', 'n_intervals'))
def update_terminal(n):
    global terminal

    final = []
    for data in terminal[-10:]:
        final.append(html.P(data, className="card-text"))
    return final

@app.callback(Output('live-update-status', 'children'), Input('interval-component', 'n_intervals'))
def update_status(n):
    global state, state_icon, buy_sell, strategies

    uptime = time.time() - start_time
    return [
        html.Div([
            html.Div([
                html.P(["Status", html.Div([], className="spinner-grow spinner-grow-sm " + state_icon + " mx-2", role="status"), "(" + state + ")"], className="card-text"),
                html.P('Uptime: {}'.format(str(datetime.timedelta(seconds=uptime)).split('.', 1)[0]), className="card-text mb-3"),
                html.P("Updates performed: {}".format(n), className="card-text")
            ], className="col"),
            html.Div([
                html.P("Buy/ Sell: {}".format(buy_sell), className="card-text"),
                html.P("Current Algo Strategy: {}".format(strategies), className="card-text")
            ], className="col")
        ], className="row")
    ]

@app.callback(Output('live-update-stocks', 'children'), Input('interval-component', 'n_intervals'))
def update_stocks(n):
    global stocks, prices

    final = []

    for stock in stocks:
        final.append(html.Li(stock + ': ' + str(prices[stock]), className="list-group-item"))

    return [
        html.Ul(final, className="list-group list-group-flush text-center")
    ]

# @app.callback(Output('live-graph', 'figure'), Input('interval-component', 'n_intervals'))
# def update_graph(n):
#     global stocks, prices, live_graph_stock

#     x_time = list(range(-60, int(time.strftime("%M"))+1))[-15:]
#     data = []
#     index = live_graph_stock
    
#     data = go.Scatter(
#         x = x_time, 
#         y = prices[stocks[index]], 
#         name=stocks[index], 
#         mode="lines+markers"
#     )

#     if live_graph_stock == 4:
#         live_graph_stock = 0
#     else:
#         live_graph_stock+=1

#     return {'data':[data], 'layout':go.Layout(xaxis = dict(range=[min(x_time), max(x_time)]), yaxis = dict(range=[min(prices[stocks[index]]), max(prices[stocks[index]])]), title="Live RSI Values")}

def strategy():
    global update_time, stocks, buy_sell, prices
    if update_time != time.strftime("%M") and buy_sell:
        update_time = time.strftime("%M")

        if int(time.strftime("%I")) == 3 and int(time.strftime("%M")) == 50:
            buy_sell = False
            for stock in stocks:
                try:
                    if positions(stock) > 0:
                        if sell(stock, positions(stock)):
                            add_log("Sold all of stock " + stock + " at 3:50pm")
                        else:
                            add_log("Wanted to sell stock " + stock + " at 3:50pm but the order failed")
                except:
                    add_log("Wanted to sell stock " + stock + " at 3:50pm but the acccount had no positions")
        else:
            for stock in stocks:

                prices[stock].append(price(stock))

                if len(prices[stock]) == 16:
                    diff_up, diff_down, rsi = [], [], -1.0
                    for x in range(0, 15):
                        if prices[stock][x+1] > prices[stock][x]:
                            diff_up.append(prices[stock][x+1] - prices[stock][x])
                        elif prices[stock][x+1] < prices[stock][x]:
                            diff_down.append(prices[stock][x] - prices[stock][x+1])
                    if len(diff_up) == 0:
                        rsi = 0.0
                    else:
                        avg_up = sum(diff_up) / 15
                    if len(diff_down) == 0:
                        rsi = 100.0
                    else:
                        avg_down = sum(diff_down) / 15
                    if rsi != 0.0 and rsi != 100.0:
                        rsi = 100 - (100 / (1 + (avg_up / avg_down)))
                    add_log("Calculated RSI for " + stock + ": " + str(rsi))
                    prices[stock] = prices[stock][-15:]

                    rsi_current = rsi

                    if rsi_current < 30:
                        if buy(stock, 5):
                            add_log("Bought stock " + stock + " at RSI: " + str(rsi_current))
                        else:
                            add_log("Wanted to buy stock " + stock + " at RSI: " + str(rsi_current) + " but the buy order failed")
                    elif rsi_current > 70:
                        try:
                            if positions(stock) > 0:
                                if sell(stock, positions(stock)):
                                    add_log("Sold stock " + stock + " at RSI: " + str(rsi_current))
                                else:
                                    add_log("Wanted to sell stock " + stock + " at RSI: " + str(rsi_current) + " but the sell order failed")
                        except:
                            add_log("Wanted to sell stock " + stock + " at RSI: " + str(rsi_current) + " but the account did not have positions")

def check():
    global state, state_icon, buy_sell, stocks, prices
    if market_clock() == 'error':
        state = "API connection lost"
        state_icon = 'text-danger'
        add_log("Connection lost with API...")
    elif market_clock()[1]:
        state = "Active"
        state_icon = "text-success"
        strategy()
    else:
        state = "Idle"
        state_icon = 'text-warning'
        buy_sell = True
        for stock in stocks:
            prices[stock] = []

def add_log(text):
    global terminal
    f = open("log.txt", "a")
    f.write(str(datetime.datetime.now().strftime('%a %b %d %I:%M:%S %p')) + ' - ' + text + '\n')
    f.close()
    terminal.append(text)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
