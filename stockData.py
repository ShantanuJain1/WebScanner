import concurrent.futures
from datetime import *


import genericFunctions as gf
from nsepython import *
import pandas as pd

"""This module is responsible for fetching the data from sources"""

''' Global Variables'''
Symbol = []
LastPrice = []
pChange = []



def getpriceData():
    symbol = []
    lastPrice = []
    pChange = []
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25')
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
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY500%20MULTICAP%2050%3A25%3A25')
    df = pd.DataFrame(positions['data'])
    df = df.sort_values(by="pChange", ascending=True)
    df = df.head(20)
    count = df.shape[0]
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'].values[i])
        pChange.append(df['pChange'].values[i])
    print((symbol, lastPrice, pChange))
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

def getNifty100():
    symbol = []
    lastPrice = []
    pChange = []
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20100')
    df = pd.DataFrame(positions['data'])
    count = df.shape[0]
    for i in range(0, count):
        symbol.append(df['symbol'].values[i])
        lastPrice.append(df['lastPrice'].values[i])
        pChange.append(df['pChange'].values[i])
    return (symbol, lastPrice, pChange)


def getSymbols(file):
    symbols = [(line.strip()) for line in gf.getFile(file)]

def deleteFilesfromFolder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def fetchStockData(symbol):
    global Symbol, LastPrice, pChange
    data = nse_eq(symbol)
    df = pd.DataFrame.from_dict(data)
    close = (df['priceInfo']['lastPrice'])
    Symbol.append(symbol)
    LastPrice.append(close)
    pChange.append(round(df['priceInfo']['pChange'],1))


def get_StockData(symbols):
    global Symbol, LastPrice, pChange
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetchStockData, symbols)
    print(f"Completed execution in {time.time() - start}")
    return (Symbol, LastPrice, pChange)


# for getting option chain
# https://www.nseindia.com/json/option-chain/option-chain.json
# nseindia.com/api/option-chain-indices?symbol=NIFTY ( you just need to change symbol to BankNifty)



def getIndiciesData():
    symbol = []
    lastPrice = []
    pChange = []
    positions = nsefetch('https://www.nseindia.com/api/allIndices')
    ndf = pd.DataFrame(positions['data'])
    ndf = ndf.head(30)
    df = ndf.iloc[15:]
    count = df.shape[0]
    for i in range(0, count):
        symbol.append(df['index'].values[i])
        lastPrice.append(df['last'].values[i])
        pChange.append(df['percentChange'].values[i])
    return (symbol, lastPrice, pChange)