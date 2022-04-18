import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf # https://pypi.org/project/yfinance/
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

# DASHBOARD HEADERS AND TITLES#
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('Stock Prices')
st.markdown('#### Based on stocks from [*Kiplinger 22 Stocks for 2022*](https://www.kiplinger.com/investing/stocks/stocks-to-buy/603893/22-best-stocks-to-buy-for-2022)')

# SIDEBAR #
st.sidebar.header('Choose A Stock')
stocklist = st.sidebar.selectbox('Select one symbol', ( 'DIS', 'UBER','QUASX','IAC', 'DXC', 'BABA', 'LFUS', 'SCHW', 'ABC', 'FAGAX', 'AGK', 'OGK', 'AMZN', 'PSA', 'BAC', 'CVS', 'SBUX', 'CCI', 'TROW', 'CVX', 'O', 'EPR'))
today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
st.sidebar.header('Displaying:')
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

# STOCK DATA #
# Download data
df = yf.download(stocklist,start= start_date,end= end_date, progress=False)

# Bollinger Bands
indicator_bb = BollingerBands(df['Close'])
bb = df
bb['Upper (Overbought)'] = indicator_bb.bollinger_hband()
bb['Lower (Oversold)'] = indicator_bb.bollinger_lband()
bb = bb[['Close','Upper (Overbought)','Lower (Oversold)']]

# Moving Average Convergence Divergence
macd = MACD(df['Close']).macd()

# Resistence Strength Indicator
rsi = RSIIndicator(df['Close']).rsi()

# MAIN PAGE #

# Display stock name and symbol
st.write(stocklist)

# Plot the prices and the bolinger bands
st.write('Stock Bollinger Bands')
st.line_chart(bb)

progress_bar = st.progress(0)

# Plot MACD
st.write('Stock Moving Average Convergence Divergence (MACD)')
st.area_chart(macd)

# Plot RSI
st.write('Stock RSI ')
st.line_chart(rsi)

# Data of recent days
st.write('Recent data ')
st.dataframe(df.tail(10))