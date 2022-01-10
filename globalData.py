# easiest way is  to plot using geopandas, create a dic for country with its value, store it in key dic pair
#convert dict to dataframe and read it using df

import requests
import plotly.graph_objects as go






lst = ["IXIC","FTSE","GDAXI","STOXX50E","BFX","N225",
       "HSI","AORD","NSEI","JKSE","NZ50","TWII",
       "GSPTSE","BVSP","MXX","TA125.TA","CASE30","JN0U.JO"]


country =['USA', 'ENGLAND', 'FRANCE', 'GERMANY','BERLIN','JAPAN','HONGKONG','CHINA','AUSTRALIA','INDIA','INDONESIA','NEWZEALAND'
                                                                                                                    'TAIWAN','CANADA']


headers = {
    'Connection': 'keep-alive',
    #'Cache-Control': 'max-age=0',
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


def getGlobalData():
    global lst
    lst_tup = []
    for item in lst:
        value = item
        payload = f"https://query1.finance.yahoo.com/v7/finance/spark?symbols=%5E{value}" \
                  f"&range=1d&interval=1d&indicators=close&includeTimestamps=false&" \
                  f"includePrePost=false&corsDomain=finance.yahoo.com&.tsrc=finance"
        output = requests.get(payload,headers=headers).json()
        #print(output)
        ticker = output.get('spark', [{}])
        symbol = (ticker['result'][0]['symbol'])
        currency = (ticker['result'][0]['response'][0]['meta']['currency'])
        lastPrice = round((ticker['result'][0]['response'][0]['meta']['regularMarketPrice']),2)
        prevClose = (ticker['result'][0]['response'][0]['meta']['chartPreviousClose'])
        pChange = round(((lastPrice / prevClose)-1)*100,2)
        tup = (item , currency, lastPrice, pChange)
        lst_tup.append(tup)

    return (lst_tup)
    #print(f"{symbol} lastPrice is {lastPrice} {pChange}%")



# df = pd.DataFrame(getGlobalData(), columns = ['Symbol', 'Currency', 'lastPrice', 'pChange'])
# print(df)

# ticker = data.get('quotes', [{}])[0]
# return {
#        'ticker': {
#               'symbol': ticker['symbol'],
#               'shortname': ticker['shortname'],
#               'longname': ticker['longname'],
#               'type': ticker['quoteType'],
#               'exchange': ticker['exchDisp'],
#        },
#        'news': data.get('news', [])


#json path for regular Market Price :  x.spark.result[0].response[0].meta.regularMarketPrice
#json path for previous close : x.spark.result[0].response[0].meta.chartPreviousClose



# How to plot data
#fig = px.choropleth(data_frame = df1,
# locations= "iso_alpha",
# color= "Confirmed",  # value in column 'Confirmed' determines color
# hover_name= "Country",
# color_continuous_scale= 'RdYlGn',  #  color scale red, yellow green
# animation_frame= "Date")
#
# fig.show()



#--------- # To make request faster------------------
# from aiohttp import ClientSession
# import asyncio
# import time
#
# async def get_sites(sites):
#        tasks = [asyncio.create_task(fetch_site(s)) for s in sites]
#        return await asyncio.gather(*tasks)
#
# async def fetch_site(url):
#        async with ClientSession() as session:
#               async with session.get(url) as resp:
#                      data = await resp.json()
#        return data
#
# if __name__ == '__main__':
#        categories = ["inspire", "management", "sports", "life", "funny", "love", "art", "students"]
#
#        sites = [
#               f'https://quotes.rest/qod?category={category}' for category in categories
#        ]
#
#        start_time = time.time()
#        data = asyncio.run(get_sites(sites))
#        duration = time.time() - start_time
#        print(f"Downloaded {len(sites)} sites in {duration} seconds")
#_________________________________________________________________________________________
def plotGlobal():

    fig = go.Figure(go.Scattergeo())
    fig.update_geos(projection_type="natural earth",showland=True, landcolor="LightGreen",
                    showocean=True, oceancolor="LightBlue",
                    showlakes=True, lakecolor="Blue",
                    )
    fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    return fig