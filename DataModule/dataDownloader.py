import DataModule.apiCalls as api
import time
from datetime import datetime
import concurrent.futures
import genericFunctions as gf


"""A cron Job can be created in MacOs for this module which will 
automatically run the cron job instnce on weekdays and will download the lastest data"""

def downloadMinuteData(symbol):
    print(f'Fetching Minute data for {symbol}')
    try:
        data = api.downloadYFdata(symbol=symbol, interval='15m', period=15)
    except:
        data = api.downloadMCdata(symbol=symbol, interval='15m', period=15)
    data.to_csv(f'dataset/minute/{symbol}.csv')

def getMinutedata():
    ticker = [(line.strip()) for line in gf.getFile("stocks")]
    start = time.time()
    print("Downloading Day Data at {}".format(datetime.now()))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloadMinuteData, ticker)
    print(f"Completed execution in {time.time() - start}")


def downloadHourData(symbol):
    print(f'Fetching Hour data for {symbol}')
    try:
        data = api.downloadYFdata(symbol=symbol, interval='1h', period=40)
    except:
        data = api.downloadMCdata(symbol=symbol, interval='1h', period=40)
    data.to_csv(f'dataset/hour/{symbol}.csv')

def getHourdata():
    ticker = [(line.strip()) for line in gf.getFile("stocks")]
    start = time.time()
    print("Downloading Day Hour at {}".format(datetime.now()))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloadHourData, ticker)
    print(f"Completed for hour data download execution in {time.time() - start}")


def downloadDayData(symbol):
    print(f'Fetching Day data for {symbol}')
    try:
        data = api.downloadYFdata(symbol=symbol, interval='1d', period=150)
    except:
        data = api.downloadMCdata(symbol=symbol, interval='1d', period=150)
    data.to_csv(f'dataset/day/{symbol}.csv')

def getDaydata():
    ticker = [(line.strip()) for line in gf.getFile("stocks")]
    start = time.time()
    print("Downloading Hour data at {}".format(datetime.now()))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloadDayData, ticker)
    print(f"Completed for day data download execution in {time.time() - start}")



#getDaydata
#getHourdata
#getMinutedata

