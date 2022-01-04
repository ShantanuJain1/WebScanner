


def getFile(value):
    if 'Crypto' in value:
        fileobj=open('crypto.txt')
        return fileobj
    else:
        fileobj=open("stocks.txt")
        return fileobj


def typelist():
    lst = ['Stocks','Crypto']
    return lst


def scanList():
    lst = ['TopGainer', 'TopLoser', 'VolumeBuzzers', 'Scanner', 'All']
    return lst

def scanType():
    lst = ['15m', '1h', '1d']
    return lst

def timeType():
    lst = [' Buy','Sell','Squeeze','Breakout']
    return lst



def getColor(change):
    if change > 0:
        color = 'Green'
    else:
        color = 'Crimson'
    return color


def getTexthtml(symbol, close, pChange):

    URL = "https://in.tradingview.com/chart/gCiOEGU4/?symbol=NSE:"+symbol

    t = "<div style=\"white-space:pre-wrap;border-width:0.5px; border-style:solid ;text-align:center; border-radius: 15px; background:"+getColor(pChange)+"\">" \
              "<a href ="+URL+" target = \"_blank\"><span style=\"color:white\">"+str(symbol)+"</span></a><br>" \
                "<span style=\"color:white\">"+str(close)+"</span><br><span style=\"color:white\">"+str(pChange)+"%"+"</span></div>"
    return t


def getTimefolder(timeline):
    if '15m' in timeline:
        return 'minute'
    elif '1h' in timeline:
        return 'hour'
    elif '1d' in timeline:
        return 'day'

