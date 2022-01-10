import pandas as pd
import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
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


def getCryptoData():
    """Returns tuple of list of all the symbols along with its Current market Price and Percent Change"""

    global headers

    with open('Crypto.txt', 'r') as file:
        data = file.read().rstrip().replace('\n',',')

    url = f"https://query1.finance.yahoo.com/v7/finance/quote?&symbols={data}" \
          f"&fields=regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume"

    symbols = []
    lastPrice = []
    pChange = []

    output = requests.get(url=url, headers=headers).json()
    x = output.get('quoteResponse', [{}])
    df = pd.DataFrame.from_dict(x['result'])
    for i in range(0, (df.shape[0])):
        symbols.append(df['symbol'].values[i])
        lastPrice.append(df['regularMarketPrice'].values[i])
        pChange.append(round(df['regularMarketChangePercent'].values[i],2))

    return symbols, lastPrice, pChange

