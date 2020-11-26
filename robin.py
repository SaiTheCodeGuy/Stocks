import click, json, ui, time
import robin_stocks as rh
import yfinance as yf
import matplotlib.pyplot as plt

from yahoo_fin.stock_info import get_data, get_live_price

benchmarks = dict()

@click.group()
def main():
    print('hello from main')
    

def quote(symbol, interval, start, end):
    print(symbol)
    data = yf.download(symbol, start, end, interval=interval)
    print(data)
    data['Adj Close'].plot()
    plt.show()
    return data

@main.command(help='Gets quotes for all stocks in your watchlist')
@click.argument('interval', type=click.STRING)
@click.option('--start', type=click.STRING)
@click.option('--end', type=click.STRING)
def watchlist(interval, start, end):
    if start is None:
        start="2020-01-01"
    if end is None:
        end="2020-07-23"

    with open('watchlist') as f:
        symbols = f.read().splitlines()
    for symbol in symbols:
        print(symbol)
        data = yf.download(symbol,start,end)
        data['Adj Close'].plot()
        plt.show()
        # ui.success(get_data(symbol, start_date=start, interval=interval))
        # print()
        # print()
    # quotes = rh.get_quotes(symbols)
    # for quote in quotes:
    #     ui.success(f"{quote['symbol']} | {quote['ask_price']}")

# @main.command(help='Buy quantity of stocks by symbol')
# @click.argument('quantity', type=click.INT)
# @click.argument('symbol', type=click.STRING)
# @click.option('--limit', type=click.FLOAT)
def buy(quantity, symbol, limit=None):
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config['username'], config['password'])

    if limit is not None:
        ui.success("buying {} of {} at ${}".format(quantity, symbol, limit))
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        ui.success("buying {} of {}".format(quantity, symbol))
        result = rh.order_buy_market(symbol, quantity)
    if 'detail' in result:
        ui.error(result)
    else:
        ui.success(result)

# @main.command(help='Sell quantity of stocks by symbol')
# @click.argument('quantity', type=click.INT)
# @click.argument('symbol', type=click.STRING)
# @click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit=None):
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config['username'], config['password'])
    
    if limit is not None:
        ui.success("Selling {} of {} at ${}".format(quantity, symbol, limit))
        result = rh.order_sell_limit(symbol, quantity, limit)
    else:
        ui.success("Selling  {} of {}".format(quantity, symbol))
        result = rh.order_sell_market(symbol, quantity)
    ui.success(result)

    if 'detail' in result:
        ui.error(result)
    else:
        ui.success(result)





if __name__ == '__main__':
    main()

