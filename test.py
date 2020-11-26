# import yfinance as yf
# # Import the plotting library
# import matplotlib.pyplot as plt

# # Get the data for the stock AAPL
# data = yf.download('AAPL', period="5d", interval="60m")
# # # Plot the close price of the AAPL
# # data['Adj Close'].plot()
# # plt.show()

# aapl = yf.Ticker("AAPL")
# hist = aapl.history(period="5d", interval="60m")
# print(hist['Close'])
# # hist['Close'].plot()
# # plt.show()

# print(data['Close'])
# print(type(data['Close']))

import robin_stocks as rh
import json

# rh.authentication.logout()
rh.authentication.login('agirap@hotmail.com', 'poop')
print()

# content = open('config.json').read()
# config = json.loads(content)
# rh.authentication.login(config['username'], config['password'])

rh.authentication.logout()
rh.order_buy_limit('AAPL', 1, .05)