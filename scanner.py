import os
import plotly.graph_objects as go
import pandas

df = None

arrSqueeze = []
arrSell = []
arrBuy = []
arrBreakout = []

tup = None

def Scrapper(timeframe):
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

        #Below is for Keltner Channel Calculations
        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()

        # df['upper_keltner'] = df['20sma'] + (df['ATR']*1.5)
        # df['lower_keltner'] = df['20sma'] - (df['ATR']*1.5)
        df['upper_keltner'] = df['20sma'] + (df['ATR'])
        df['lower_keltner'] = df['20sma'] - (df['ATR'])


        #------------------squeeze----------
        def in_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner'] \
                   and df['Close'] < df['upper_keltner']


        def out_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner'] \
                   and df['Close'] > df['upper_keltner'] \
                   and df['Volume'] >= (df['20smavol']*2)


        df['squeeze_on'] = df.apply(in_squeeze, axis=1)
        df['squeeze_off'] = df.apply(out_squeeze, axis=1)

        if df.iloc[-1]['squeeze_on']: #and df.iloc[-1]['squeeze_off']:
            arrSqueeze.append(symbols)

        #-------------Sell----------------
        def SellCondition(df):
            return df['Low'] > df['upper_band'] and df['Close'] > df['5EMA'] and df['Open'] > df['5EMA'] \
                   and df['Low'] > df['5EMA'] and df['Close'] < df['Open']

        df['sell'] = df.apply(SellCondition, axis=1)

        if df.iloc[-1]['sell']:
            arrSell.append(symbols)

        #------------_Buy---------------
        def buy(df):
            # return df['High'] < df['lower_keltner'] and df['lower_keltner'] < df['lower_band'] and\
            #        df['High'] < df['5EMA']
            return df['5EMA'] < df['lower_band'] and df['5EMA'] < df['lower_keltner']

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

    return (arrBuy, arrSell, arrSqueeze)