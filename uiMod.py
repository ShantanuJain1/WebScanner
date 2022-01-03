import streamlit as st
import dataModule, genericFunctions as gf
import scanner


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
        Buy, Sell , Squeeze = scanner.Scrapper(gf.getTimefolder(timeframe))
        if 'Buy' in type:
            if(len(Buy) ==  0):
                st.write("No Data for the range")
            symbol, close, change = dataModule.get_StockData(Buy)
        elif 'Sell' in type:
            if(len(Sell) ==  0):
                st.write("No Data for the range")
            symbol, close, change = dataModule.get_StockData(Sell)
        else:
            if(len(Squeeze) ==  0):
                st.write("No Data for the range")
            #st.write(Squeeze)
            symbol, close, change = dataModule.get_StockData(Squeeze)


    st.title(f"{type} {scan} {timeframe} data")


    if 'Crypto' in type:
        symbol, close, change = dataModule.getData(type)

    if type == 'Stocks':
        if 'TopGainer' in scan:
            symbol, close, change = dataModule.getTopGainer()
        elif 'TopLoser' in scan:
            symbol, close, change = dataModule.getTopLoser()
        elif 'VolumeBuzzers' in scan:
            symbol, close, change = dataModule.getMostActive()
        elif 'Scanner' in scan:
            st.write('timeframe')
        elif 'All' in scan:
            symbol, close, change = dataModule.getpriceData()




    one, two, three, four, five, six, seven = st.columns(7)
    try:
        for i in range(0,len(symbol), 7):
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

    except:
        pass


uiCreator()
