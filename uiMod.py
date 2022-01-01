import streamlit as st
import dataModule, genericFunctions as gf




def uiCreator():
    symbol = None
    change = None
    close = None
    type = st.sidebar.selectbox('select', gf.typelist())

    if 'Stocks' in type:
        scan = st.sidebar.selectbox('select', gf.scanList())
    else:
        scan = ""


    st.title(f"{type} {scan} data")


    if 'Crypto' in type:
        symbol, close, change = dataModule.getData(type)

    if type == 'Stocks' and scan != "All":
        #symbol, close, change = dataModule.getpriceData()

        if 'TopGainer' in scan:
            symbol, close, change = dataModule.getTopGainer()
        elif 'TopLoser' in scan:
            symbol, close, change = dataModule.getTopLoser()
        elif 'VolumeBuzzers' in scan:
            symbol, close, change = dataModule.getMostActive()
    else:
        symbol, close, change = dataModule.getData(type)


    one, two, three, four, five, six= st.columns(6)
    try:
        for i in range(0,len(symbol), 1):
            with one:
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            with two:
                i=i+1
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
                # st.metric(symbol[i+1].replace(".NS",""), close[i+1], f"{round(change[i+1],1)}%")
                # print(i+1)
            with three:
                i+=2
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
                # st.metric(symbol[i+2].replace(".NS",""), close[i+2], f"{round(change[i+2],1)}%")
                # print(i+2)
            with four:
                i+=3
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
                # st.metric(symbol[i+3].replace(".NS",""), close[i+3], f"{round(change[i+3],1)}%")
                # print(i+3)
            with five:
                i+=4
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
            #     st.metric(symbol[i+4].replace(".NS",""), close[i+4], f"{round(change[i+4],1)}%")
            # print(i+3)
            with six:
                i+=5
                t = gf.getTexthtml(symbol[i],close[i], change[i])
                st.write(t, unsafe_allow_html=True)
    except:
        pass




uiCreator()