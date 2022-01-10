"""Implement yfinance direct api call for downloading the historical data"""

"""Backup for the same would be calling the moneycontrol api for downloading the NSE data"""

import requests
import time
import pandas as pd
from datetime import datetime, timedelta

def getyfEndpoint(symbol, start, end , interval):
    endpoint = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?symbol={symbol}.NS&' \
             f'period1={start}&period2={end}&useYfid=true&interval={interval}&' \
             f'includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=IN&' \
             f'crumb=h.AGGHRJhkT&corsDomain=finance.yahoo.com'
    return endpoint

def getmcEndPoint(symbol, start, end, interval):
    interval = interval.replace('m','')
    endpoint =f'https://priceapi.moneycontrol.com/techCharts/techChartController/history?' \
              f'symbol={symbol}&resolution={interval}&from={start}&to={end}'
    return endpoint

def getyfHeader():
    return {
           'Connection': 'keep-alive',
           'Cache-Control': 'no-cache',
           'DNT': '1',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
           'Sec-Fetch-User': '?1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-Mode': 'navigate',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }

def getyfResponse(symbol, starttime, endtime, interval, headers):
    symbol.replace(".NS","")
    return requests.get(getyfEndpoint(symbol=symbol,start=starttime, end=endtime, interval=interval),headers=headers).json()

def getmcResponse(symbol, starttime, endtime, interval, headers):
    return requests.get(getmcEndPoint(symbol, start=starttime, end=endtime, interval=interval), headers=headers).json()


def gettime(start,end=None, period = None):
    if start or period is None or period.lower() == "max":
        if start is None:
            start = -631159200
        elif isinstance(start, datetime):
            start = int(time.mktime(start.timetuple()))
        else:
            start = int(time.mktime(
                time.strptime(str(start), '%Y-%m-%d')))
    if end is None:
        end = int(time.time())
    elif isinstance(end, datetime):
        end = int(time.mktime(end.timetuple()))
    else:
        end = int(time.mktime(time.strptime(str(end), '%Y-%m-%d')))

    return start, end


def downloadYFdata(symbol='infy', interval='1d', period=10):
    """Takes in symbol ,period, interval as parameter and returns Dataframe for the result"""

    period = validatePeriod(period)
    start, end = gettime(start=datetime.now() - timedelta(period))

    output = getyfResponse(symbol=symbol, starttime=start, endtime=end, interval=interval, headers=getyfHeader())

    data = (output["chart"]["result"][0]["indicators"]["quote"][0])
    timestamp = output["chart"]["result"][0]['timestamp']
    ts = [datetime.fromtimestamp(item).strftime( "%Y-%m-%d %H:%M:%S") for item in timestamp]
    # print(ts)
    # ts = data['time']
    volumes = data["volume"]
    opens = data["open"]
    closes = data["close"]
    lows = data["low"]
    highs = data["high"]

    df = pd.DataFrame({'Time':ts,"Open": opens,"High": highs,"Low": lows,"Close": closes,"Volume": volumes})
    df = df.round({'Open':1, 'Low':1,'Close':1, 'High':1})
    return df


def downloadMCdata(symbol='infy', interval='1d', period=10):
    period = validatePeriod(period)
    symbol = symbol.upper()
    start, end = gettime(start=datetime.now() - timedelta(period))

    output = getmcResponse(symbol=symbol, starttime=start, endtime=end, interval=interval, headers=getyfHeader())
    data = pd.DataFrame.from_dict(output)

    data['Time'] = pd.to_datetime(data['t'], unit='s', )
    #data['Time'].tz_localize('IST')
    data['Open'] = data['o']
    data['High'] = data['h']
    data['Low'] = data['l']
    data['Close'] = data['c']
    data['Volume'] = data['v']
    data.drop(['s','o','h','l','c','t','v','t'], inplace=True, axis=1)
    return data

def validatePeriod(period):
    if period < 10:
        period = 10
    return period



