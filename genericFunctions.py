from datetime import datetime
import time

def getFile(value):
    if 'Crypto' in value.lower():
        fileobj=open('crypto.txt')
        return fileobj
    else:
        fileobj=open("stocks.txt")
        return fileobj


def typelist():
    lst = ['Indian Indicies','Stocks','Crypto','Global Indicies']
    return lst


def scanList():
    lst = ['','All', 'NIFTY 100', 'TopGainer', 'TopLoser', 'VolumeBuzzers', 'Scanner']
    return lst

def scanType():
    lst = ['','15m', '1h', '1d']
    return lst

def timeType():
    lst = ['','Buy','Sell','Squeeze','Breakout']
    return lst



def getColor(change):
    if change > 0:
        color = 'Green'
    else:
        color = 'Crimson'
    return color


def getTexthtml(symbol, close, pChange):

    URL = "https://in.tradingview.com/chart/?symbol=NSE:"+symbol.replace("-","_").replace("&","_")
    bgcolor, textColor = getDynamicColor(pChange)
    t = "<div style=\"font-size:14px;border:black;border-width:0.5px; border-style:solid ;text-align:center; border-radius: 15px; background:"+bgcolor+"\">" \
                                                                                                                                                       "<a href ="+URL+" target = \"_blank\"><span style=\"color:"+textColor+"\">"+str(symbol)+"</span></a><br>" \
                                                                                                                                                                                                                                               "<span style=\"color:"+textColor+"\">"+str(close)+"</span><br><span style=\"color:"+textColor+"\">"+str(pChange)+"%"+"</span></div>"
    return t


def getTimefolder(timeline):
    if '15m' in timeline:
        return 'minute'
    elif '1h' in timeline:
        return 'hour'
    elif '1d' in timeline:
        return 'day'



def getDynamicColor(change):
    try:
        dynamicColor = 'white'
        textcolor = 'black'
        if(float(change)>=3):
            dynamicColor = 'darkgreen'
            textcolor = 'white'
        elif(1<float(change)<3):
            dynamicColor = 'olivedrab'
            textcolor ='white'
        elif(0<float(change)<=1):
            dynamicColor = 'gold'
            textcolor ='black'
        elif(float(change)==0):
            dynamicColor = 'orange'
            textcolor ='black'
        elif(0>float(change)>-1):
            dynamicColor ='orange'
            textcolor ='white'
        elif(-1>float(change)>-3):
            dynamicColor ='coral'
            textcolor ='black'
        elif(float(change)<=-3):
            dynamicColor ='Crimson'
            textcolor ='white'
    except:
        dynamicColor = 'white'
        textcolor = 'black'

    return (dynamicColor,textcolor)



def gettime(start,end=None, period = None):
    """Retruns start time in Epoch time and end time in Epoch time delta"""
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

def getDownloadtimestamp():
    time = str(datetime.today().strftime("%H:%M:%S"))
    strng = "<span style=font-size:10px>last download  :  "+time+"</span>"
    return strng
