import streamlit as st
from generics import genericFunctions as gf
from dataModule import dataModule as dM




def uiCreator():
    symbol = None
    change = None
    close = None
    value = st.sidebar.selectbox('select', gf.scannerlist())
    st.title(f"{value} data")
    #st.write(f"You selected {value}")
    if 'Crypto' in value:
        symbol, close, change = dM.getData(value)
    elif 'Stocks' in value:
        symbol, close, change = dM.getpriceData()
    elif 'TopGainer' in value:
        symbol, close, change = dM.getTopGainer()
    elif 'TopLoser' in value:
        symbol, close, change = dM.getTopLoser()
    elif 'VolumeBuzzers' in value:
        symbol, close, change = dM.getMostActive()


    one, two, three, four, five= st.columns(5)
    try:
        for i in range(0,len(symbol), 5):
            with one:
                st.metric(symbol[i].replace(".NS",""), close[i], f"{round(change[i],1)}%")
            with two:
                st.metric(symbol[i+1].replace(".NS",""), close[i+1], f"{round(change[i+1],1)}%")
                print(i+1)
            with three:
                st.metric(symbol[i+2].replace(".NS",""), close[i+2], f"{round(change[i+2],1)}%")
                print(i+2)
            with four:
                st.metric(symbol[i+3].replace(".NS",""), close[i+3], f"{round(change[i+3],1)}%")
                print(i+3)
            with five:
                st.metric(symbol[i+4].replace(".NS",""), close[i+4], f"{round(change[i+4],1)}%")
            print(i+3)
    except:
        pass




uiCreator()