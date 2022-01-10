import streamlit as st
import stockData, genericFunctions as gf
import cryptoData
import globalData
import scanner
from DataModule import dataDownloader


def uiCreator():
    symbol = None
    change = None
    close = None
    timeframe = ""


    type = st.sidebar.selectbox('Select Type', gf.typelist())

    if 'Stocks' in type:
        scan = st.sidebar.selectbox('Classifier', gf.scanList())
    else:
        scan = ""

    if "Scanner" in scan:
        timeframe = st.sidebar.selectbox('TimeLine', gf.scanType())
        type = st.sidebar.selectbox('ScanType', gf.timeType())
        Buy, Sell , Squeeze, Breakout = scanner.Scrapper(gf.getTimefolder(timeframe))
        if 'Buy' in type:
            if(len(Buy) ==  0):
                st.write("No Data for the range")
            symbol, close, change = stockData.get_StockData(Buy)
        elif 'Sell' in type:
            if(len(Sell) ==  0):
                st.write("No Data for the range")
            symbol, close, change = stockData.get_StockData(Sell)
        elif 'Squeeze' in type:
            if(len(Squeeze) ==  0):
                st.write("No Data for the range")
            symbol, close, change = stockData.get_StockData(Squeeze)
        elif 'Breakout' in type:
            if(len(Breakout) ==  0):
                st.write("No Data for the range")
            symbol, close, change = stockData.get_StockData(Breakout)


    st.title(f"{type} {scan} {timeframe} data")


    if 'Crypto' in type:
        symbol, close, change = cryptoData.getCryptoData()

    if 'Indian Indicies' in type:
        symbol, close, change = stockData.getIndiciesData()

    if 'Global Indicies' in type:
        st.write(globalData.getGlobalData())
        st.plotly_chart(globalData.plotGlobal(), use_container_width=True)


    if type == 'Stocks':
        if 'NIFTY 100' in scan:
            symbol, close, change = stockData.getNifty100()
        if 'TopGainer' in scan:
            symbol, close, change = stockData.getTopGainer()
        elif 'TopLoser' in scan:
            symbol, close, change = stockData.getTopLoser()
        elif 'VolumeBuzzers' in scan:
            symbol, close, change = stockData.getMostActive()
        elif 'Scanner' in scan:
            st.write('timeframe')
        elif 'All' in scan:
            symbol, close, change = stockData.getpriceData()




    one, two, three, four, five, six, seven, eight = st.columns(8)
    try:
        for i in range(0,len(symbol), 8):
            with one:
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with two:
                i=i+1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with three:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with four:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with five:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with six:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with seven:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with eight:
                i+=1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)

    except:
        pass

        if symbol is not None:
            symbol.clear()
            close.clear()
            change.clear()

    fifteen = st.sidebar.button(label="Download 15m Data", on_click=dataDownloader.getMinutedata)
    if fifteen:
        st.sidebar.write(gf.getDownloadtimestamp(), unsafe_allow_html=True)


    hour = st.sidebar.button(label="Download 1h Data", on_click=dataDownloader.getHourdata)
    if hour:
        st.sidebar.write(gf.getDownloadtimestamp(), unsafe_allow_html=True)


    day = st.sidebar.button(label="Download 1d Data", on_click=dataDownloader.getDaydata)
    if day:
        st.sidebar.write(gf.getDownloadtimestamp(), unsafe_allow_html=True)

def timestamp():
    st.sidebar.write(gf.getDownloadtimestamp(), unsafe_allow_html=True)

uiCreator()