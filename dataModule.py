import yfinance as yf
from datetime import *
import genericFunctions as gf
from nsepython import *


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
        closePrice = data['Close'][symbol].values[0]
        openPrice = data['Open'][symbol].values[0]
        prevClose = data['Close'][symbol].values[1]

        change = round(((prevClose -closePrice)/closePrice)*100,1)
        lst_ticker.append(symbol)
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

    for i in range(0, count-1):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'][i])
        pChange.append(df['pChange'][i])

    return (symbol, lastPrice, pChange)


def getTopGainer():
    symbol = []
    lastPrice = []
    pChange = []
    df = nse_get_top_gainers()
    count = nse_get_top_gainers().shape[0]
    for i in range(0, count-1):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'][i])
        pChange.append(df['pChange'][i])

    return (symbol, lastPrice, pChange)


def getTopLoser():
    symbol = []
    lastPrice = []
    pChange = []
    df = nse_get_top_losers()
    count = nse_get_top_losers().shape[0]
    for i in range(0, count-1):
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
    for i in range(0, count-1):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'].values[i])
        pChange.append(df['pChange'].values[i])
    return (symbol, lastPrice, pChange)

