
def getFile(value):
    if 'Crypto' in value:
        fileobj=open('crypto.txt')
        return fileobj
    else:
        fileobj=open("stocks.txt")
        return fileobj


def scannerlist():
    lst = ['Stocks','Crypto', 'TopGainer', 'TopLoser', 'VolumeBuzzers']
    return lst
