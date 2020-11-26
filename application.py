import os
import csv
import requests
import json
import robin

from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import robin_stocks as rh
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if 'username' in session:
        rh.authentication.login(session['username'], session['password'])
        return render_template("index.html")
    try:
        rh.authentication.logout()
    except:
        print('whoops')
    return render_template('signin.html', error=False)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route("/results", methods=['POST'])
def results():
    symbol = str(request.form.get('ticker'))
    interval = request.form.get('interval')
    start = request.form.get('start')
    end = request.form.get('end')
    print(symbol)
    data = yf.download(symbol, start, end, interval=interval)
    # print(data)
    # print(data.index)
    # print(data.columns)
    print(data['Adj Close'])
    # data['Adj Close'].plot()
    # plt.savefig('curr.png')
    return render_template('results.html', ticker=symbol, data=data)

@app.route("/validate", methods=['POST'])
def validate():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        session['username'] = username
        session['password'] = password
        try:
            rh.authentication.logout()
        except:
            print('whoops')
        rh.authentication.login(username, password)
        rh.order_buy_limit('AAPL', 1, .05)
    except:
        session['username'] = None
        session['password'] = None
        return render_template('signin.html', error=True)
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route("/buy", methods=['POST'])
def buy():
    symbol = request.form.get('Ticker')
    amount = request.form.get('Amount')
    if request.form.get('Limit') is None:
        robin.buy(amount, symbol)
    else:
        limit = request.form.get('Limit')
        robin.buy(amount, symbol, limit)
    return redirect(url_for('index'))

@app.route("/sell", methods=['POST'])
def sell():
    symbol = request.form.get('Ticker')
    amount = request.form.get('Amount')
    if request.form.get('Limit') is None:
        robin.sell(amount, symbol)
    else:
        limit = request.form.get('Limit')
        robin.sell(amount, symbol, limit)
    return redirect(url_for('index'))