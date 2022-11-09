import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
from datetime import datetime, timedelta

def brent_adj():
    """get dkk adjusted brent prices per liter

    Input:
        None

    Raise:
        None

    Output:
        brent_hist: pd.Dataframe
            contains all the brent hist year-to-date

    ----------------------------------------

    TODO:
        [] Set per_liter as bool parameter
        [] set period parameter
        [] set interval as parameter

    """
    brent = yf.Ticker('BZ=F')
    brent_hist = brent.history(period = "ytd", interval = '60m')
    brent_hist.reset_index(inplace = True)
    brent_hist['Datetime'] = pd.to_datetime(brent_hist['Datetime'])
    brent_hist['Date'] = pd.to_datetime(brent_hist['Datetime'], format = '%Y-%m-%d')

    exchange_rate = web.DataReader('DKK=X', 'yahoo', brent_hist['Datetime'].min(), brent_hist['Datetime'].max())
    exchange_rate.reset_index(inplace = True)
    exchange_rate['Date'] = pd.to_datetime(exchange_rate['Date'], format = '%Y-%m-%d')
    exchange_rate['Date'] =exchange_rate['Date'].astype(str)
    cols = ['Open', 'High', 'Low', 'Close']
    use = ['Date']

    for i in cols:
        tmp = f'{i}_exchange'
        exchange_rate[tmp] = exchange_rate[i]
        use.append(tmp)

    brent_hist['Date'] = brent_hist['Date'].astype(str)
    brent_hist['Date'] = [i.split(' ')[0] for i in brent_hist['Date']]
    brent_hist = brent_hist.merge(exchange_rate[use], on = 'Date')

    brent_hist['Close_adj'] = brent_hist['Close'] * brent_hist['Close_exchange'] / 158.99
    brent_hist['Open_adj'] = brent_hist['Open'] * brent_hist['Open_exchange'] / 158.99
    brent_hist['High_adj'] = brent_hist['High'] * brent_hist['High_exchange'] / 158.99
    brent_hist['Low_adj'] = brent_hist['Low'] * brent_hist['Low_exchange'] / 158.99

    return brent_hist
