import json, requests, os
import numpy as np
import pandas as pd
from pathlib import Path

token_path = Path(__file__).parents[1]
token_path = os.path.join(token_path,'res/oanda_api_key.json')

def GrabToken(path=token_path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data['token']

def GrabCandles(token, instru, start, gran, based, count=1000):
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json"}
    gran = 'granularity=' + gran
    uri = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}&count={}'.format(instru,based,start,gran,count)
    resp = requests.get(uri,headers=header)
    response = resp.text
    OHLC = json.loads(response)
    amount_OHLC = len(OHLC["candles"])
    ticks = amount_OHLC

    if based == 'BA':
        bid_close = np.empty((0, amount_OHLC), float)
        ask_close = np.empty((0, amount_OHLC), float)
        bid_open = np.empty((0, amount_OHLC), float)
        ask_open = np.empty((0, amount_OHLC), float)
    elif based == 'M':
        mid_close = np.empty((0, amount_OHLC), float)
        mid_open = np.empty((0, amount_OHLC), float)
        mid_high = np.empty((0, amount_OHLC), float)
        mid_low = np.empty((0, amount_OHLC), float)
    else:
        print('\nError: get_candles func based parameter did not match ' +
        '\'BA\' or \'M\'. Can not create numpy arrays.\n')

    for i in range(0, amount_OHLC):
        if based == 'BA':
            bid_close = np.append(bid_close,OHLC["candles"][i]["bid"]["c"])
            ask_close = np.append(ask_close,OHLC["candles"][i]["ask"]["c"])
            bid_open = np.append(bid_open,OHLC["candles"][i]["bid"]["o"])
            ask_open = np.append(ask_open,OHLC["candles"][i]["ask"]["o"])
        elif based == 'M':
            mid_close = np.append(mid_close, OHLC["candles"][i]["mid"]["c"])
            mid_open = np.append(mid_open, OHLC["candles"][i]["mid"]["o"])
            mid_high = np.append(mid_high, OHLC["candles"][i]["mid"]["h"])
            mid_low = np.append(mid_low, OHLC["candles"][i]["mid"]["l"])
        else:
            print('\nError: get_candles func based parameter did not match' +
             '\'BA\' or \'M\'. Can not appened numpy arrays.\n')


    if based == 'BA':
        bid_close = bid_close.astype(float)
        ask_close = ask_close.astype(float)
        bid_open = bid_open.astype(float)
        ask_open = ask_open.astype(float)
        return instru, bid_close, ask_close, bid_open, ask_open, ticks
    elif based == 'M':
        mid_close = mid_close.astype(float)
        mid_open = mid_open.astype(float)
        mid_high = mid_high.astype(float)
        mid_low = mid_low.astype(float)
        return instru, mid_open, mid_high, mid_low, mid_close, ticks
    else:
        print('\nError: get_candles func based parameter did not match '+
        '\'BA\' or \'M\'. Can not change type of np arrays from str to float.\n')
        return None

#pandas

def GrabOHLC(token, instru, start, gran, based, count=500):
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json"}
    gran = 'granularity=' + gran
    uri = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}&count={}'.format(instru,based,start,gran,count)
    resp = requests.get(uri,headers=header)
    response = resp.text
    OHLC = pd.read_json(response, orient='columns')
    ticks = len(OHLC["candles"])

    if based == 'BA':
        bid_close = np.empty(ticks, float)
        bid_open = np.empty(ticks, float)
        bid_high = np.empty(ticks, float)
        bid_low = np.empty(ticks, float)

        ask_close = np.empty(ticks, float)
        ask_open = np.empty(ticks, float)
        ask_high = np.empty(ticks, float)
        ask_low = np.empty(ticks, float)

        time = []
        volume = np.empty(ticks, int)

    elif based == 'M':
        mid_close = np.empty(ticks, float)
        mid_open = np.empty(ticks, float)
        mid_high = np.empty(ticks, float)
        mid_low = np.empty(ticks, float)

        time = []
        volume = np.empty(ticks, int)

    else:
        print('\nError: get_candles func based parameter did not match ' +
        '\'BA\' or \'M\'. Can not create numpy arrays.\n')

    for i in range(ticks):
        if based == 'BA':
            bid_close[i] = float(OHLC["candles"][i]["bid"]["c"])
            bid_open[i] = float(OHLC["candles"][i]["bid"]["o"])
            bid_high[i] = float(OHLC["candles"][i]["bid"]["h"])
            bid_low[i] = float(OHLC["candles"][i]["bid"]["l"])

            ask_close[i] = float(OHLC["candles"][i]["ask"]["c"])
            ask_open[i] = float(OHLC["candles"][i]["ask"]["o"])
            ask_high[i] = float(OHLC["candles"][i]["ask"]["h"])
            ask_low[i] = float(OHLC["candles"][i]["ask"]["l"])

            time.append(OHLC["candles"][i]["time"])
            volume[i] = OHLC["candles"][i]["volume"]

        elif based == 'M':
            mid_close[i] = float(OHLC["candles"][i]["mid"]["c"])
            mid_open[i] = float(OHLC["candles"][i]["mid"]["o"])
            mid_high[i] = float(OHLC["candles"][i]["mid"]["h"])
            mid_low[i] = float(OHLC["candles"][i]["mid"]["l"])

            time.append(OHLC["candles"][i]["time"])
            volume[i] = OHLC["candles"][i]["volume"]

        else:
            print('\nError: get_candles func based parameter did not match' +
             '\'BA\' or \'M\'. Can not appened numpy arrays.\n')

    if based == 'BA':
        return (instru, time, volume, bid_open, bid_high, bid_low, bid_close,
        ask_open, ask_high, ask_low, ask_close, ticks)

    elif based == 'M':
        return instru, time, volume, mid_open, mid_high, mid_low, mid_close, ticks

    else:
        print('\nError: get_candles func based parameter did not match '+
        '\'BA\' or \'M\'. Can not change type of np arrays from str to float.\n')
        return None


def requestOHLC(token, instru, start, gran, based, count=500):
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json",
              'Connection':'Keep-Alive'
              }
    s = requests.Session()
    url =  'https://stream-fxpractice.oanda.com/v3/instruments/' + instru + '/candles?'
    param = {'price':based,'from':start,'granularity':gran,'count':count}

    resp = s.get(url,headers=header,params=param)
    print(resp.text)
