import os
import time

import pandas

df = None

arrSqueeze = []
arrSell = []
arrBuy = []
arrBreakout = []

tup = None

def Scrapper(timeframe):
    start = time.time()
    global arrBuy, arrSell, arrBreakout, arrSqueeze
    arrBuy.clear()
    arrSell.clear()
    arrBreakout.clear()
    arrSqueeze.clear()
    #print(timeframe)
    for filename in os.listdir('dataset/{}'.format(timeframe)):
        symbols = filename.split(".")[0]
        df = pandas.read_csv("dataset/{}/{}".format(timeframe,filename))
        if df.empty:
            continue

            # below is for SMA Calculations
        df['20sma'] = df['Close'].rolling(window=20).mean()

        # Below is for EMA calculations
        df['5EMA'] = df['Close'].ewm(span=5,adjust=False).mean()
        df['EMA'] = df['Close'].ewm(span=21,adjust=False).mean()
        df['stdv'] = df['EMA'].rolling(window=21).std()

        # Below is for Lower and Upperbands of EMA
        df['lower_band'] = round(df['EMA'] - (3* df['stdv']),1)
        df['upper_band'] = round(df['EMA'] + (3* df['stdv']),1)

        # Below is for Simple Moving average of Volume
        df['20smavol'] = round(df['Volume'].rolling(window=20).mean(),0)
        # 10 SMA volume
        df['10smavol'] = round(df['Volume'].rolling(window=10).mean(),0)

        #Below is for Keltner Channel Calculations
        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()

        # df['upper_keltner'] = df['20sma'] + (df['ATR']*1.5)
        # df['lower_keltner'] = df['20sma'] - (df['ATR']*1.5)
        df['upper_keltner'] = df['20sma'] + (df['ATR'])
        df['lower_keltner'] = df['20sma'] - (df['ATR'])


        #-----GreenCandle------
        def greenCandle(df):
            return df['Close'] > df['Open']

        def redCandle(df):
            return df['Close'] < df['Open']

        df['greenCandle'] = df.apply(greenCandle, axis=1)
        df['redCandle'] = df.apply(redCandle, axis=1)

        #------------------squeeze----------
        def in_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner'] \
                   and df['Close'] < df['upper_keltner'] and df['Volume'] <= df['10smavol']


        def out_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner'] \
                   and df['Close'] >= df['upper_keltner'] \
                   and df['Volume'] >= (df['20smavol']*2)

        def breakdown(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner'] \
                   and df['Close'] < df['lower_keltner'] \
                   and df['Volume'] >= (df['20smavol']*2)



        df['squeeze_on'] = df.apply(in_squeeze, axis=1)
        df['breakout'] = df.apply(out_squeeze, axis=1)
        df['breakdown'] = df.apply(breakdown, axis=1)

        if df.iloc[-1]['squeeze_on'] and not df.iloc[-1]['breakout']:
            arrSqueeze.append(symbols)

        if df.iloc[-1]['breakout'] and df.iloc[-1]['greenCandle']:
            arrBreakout.append(symbols)

        #-------------Sell----------------
        def SellCondition(df):
            return df['Low'] > df['upper_band'] and df['Low'] > df['upper_keltner'] and \
                   df['Low'] > df['5EMA']

        df['sell'] = df.apply(SellCondition, axis=1)

        # Condition for Breakdown( Candle breaking out of channel) or sell is true
        sellOnTop = df.iloc[-1]['sell'] and df.iloc[-1]['redCandle']
        breakDown = df.iloc[-1]['breakdown'] and df.iloc[-1]['redCandle']
        if sellOnTop or breakDown:
            arrSell.append(symbols)

        #------------_Buy---------------
        def buy(df):
            return df['5EMA'] < df['lower_band']

        df['buy'] = df.apply(buy, axis=1)

        if not df.iloc[-2]['buy'] and df.iloc[-1]['buy']:
            arrBuy.append(symbols)

        # #------------Volume Buzzers---------------
        # def vol(df):
        #     return df['Volume'] > (df['20smavol'])*3
        #
        # df['Volume'] = df.apply(vol, axis=1)
        #
        # if df.iloc[-1]['Volume']:
        #     arrVol.append(symbols)
    end = time.time()
    print(f'scan completed in :{end - start}')
    return (arrBuy, arrSell, arrSqueeze, arrBreakout)
