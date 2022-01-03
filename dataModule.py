import yfinance as yf
from datetime import *
import genericFunctions as gf
from nsepython import *
import pandas as pd

"""This module is responsible for fetching the data from sources"""


def getData(file):
    """Fetching the data from yahoo finance api"""
    lst_close =  []
    lst_change = []
    lst_ticker = []
    symbols = [(line.strip()) for line in gf.getFile(file)]

    data = yf.download(symbols, interval='1d', start=datetime.datetime.today() - timedelta(1), threads=2)

    for symbol in symbols:
        # try:
        deleteFilesfromFolder("dataset/currentdata")
        data.to_csv(f"dataset/currentdata/{symbol}.csv")
        closePrice = data['Close'][symbol].values[0]
        openPrice = data['Open'][symbol].values[0]
        prevClose = data['Close'][symbol].values[1]
        change = round(((prevClose -closePrice)/closePrice)*100,1)
        print(symbol, closePrice, change)
        lst_ticker.append(symbol.replace(".NS",""))
        lst_close.append(round(closePrice,1))
        lst_change.append(change)

    return (lst_ticker,lst_close,lst_change)



def getpriceData():
    symbol = []
    lastPrice = []
    pChange = []
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    df = pd.DataFrame(positions['data'])
    count = df.shape[0]
    print(count)
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'][i])
        pChange.append(df['pChange'][i])

    return (symbol, lastPrice, pChange)


def getTopGainer():
    symbol = []
    lastPrice = []
    pChange = []
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    df = pd.DataFrame(positions['data'])
    df = df.sort_values(by="pChange" , ascending = False)
    df = df.head(20)
    #count = nse_get_top_gainers().shape[0]
    count = df.shape[0]
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'][i])
        pChange.append(df['pChange'][i])

    return (symbol, lastPrice, pChange)


def getTopLoser():
    symbol = []
    lastPrice = []
    pChange = []
    # df = nse_get_top_losers()
    # count = nse_get_top_losers().shape[0]
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    df = pd.DataFrame(positions['data'])
    df = df.sort_values(by="pChange", ascending=True)
    df = df.head(20)
    #count = nse_get_top_gainers().shape[0]
    count = df.shape[0]
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'].values[i])
        pChange.append(df['pChange'].values[i])
    return (symbol, lastPrice, pChange)


def getMostActive():
    symbol = []
    lastPrice = []
    pChange = []
    df = nse_most_active(sort='volume')
    count = nse_most_active(sort='volume').shape[0]
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(round(df['lastPrice'].values[i],1))
        pChange.append(round(df['pChange'].values[i],1))
    return (symbol, lastPrice, pChange)


def getSymbols(file):
    symbols = [(line.strip()) for line in gf.getFile(file)]

def deleteFilesfromFolder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def get_StockData(symbols):
    lstSymb = []
    lastPrice = []
    pChange = []
    for symbol in symbols:
        data = nse_eq(symbol)
        #print(data)
        df = pd.DataFrame.from_dict(data)
        # print(df.columns.values)

        close = (df['priceInfo']['lastPrice'])
        change = (df['priceInfo']['pChange'])

        print(f" change is {symbol} {close} {change}")
        lstSymb.append(symbol)
        lastPrice.append(close)
        pChange.append(round(df['priceInfo']['pChange'],1))

    return (symbols, lastPrice, pChange)