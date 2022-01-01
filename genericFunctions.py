


def getFile(value):
    if 'Crypto' in value:
        fileobj=open('ctest.txt')
        return fileobj
    else:
        fileobj=open("stest.txt")
        return fileobj


def typelist():
    lst = ['Stocks','Crypto']
    return lst


def scanList():
    lst = ['TopGainer', 'TopLoser', 'VolumeBuzzers','All']
    return lst



def getColor(change):
    if change > 0:
        color = 'green'
    else:
        color = 'red'
    return color


def getTexthtml(symbol, close, pChange):
    URL = "https://in.tradingview.com/chart/gCiOEGU4/?symbol=NSE:"+symbol
    t = "<div><span style=\"background:"+getColor(pChange)+"; color:white\">"+str(symbol)+"</span><br>" \
                                                                                          "<span>"+str(close)+"</span><br><span>"+str(pChange)+"%"+"</span></div>"
    print(t)
    return t
