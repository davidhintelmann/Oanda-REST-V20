import json, sys, time, datetime, requests
import matplotlib.pyplot as plt
import numpy as np

def extract_token(path = 'res/oanda_api_key.json'):
    with open(path) as data_file:
        data = json.load(data_file)
        return data['token']

def get_candles(token):
    #print(token)
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json"}

    instru = 'EUR_USD'
    based = 'BA'
    based_mid = 'M'
    timee = '2017-12-28T15%3A00%3A00.000000000Z'
    gran = 'granularity=M1' # candles freqeuncy

    uri = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}'.format(instru,based,timee,gran)
    uri_mid = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}'.format(instru,based_mid,timee,gran)
    resp = requests.get(uri,headers=header)
    resp_mid = requests.get(uri_mid,headers=header)
    response = resp.text
    response_mid = resp_mid.text
    #print(response)

    OHLC = json.loads(response)
    OHLC_mid = json.loads(response_mid)
    amount_OHLC = len(OHLC["candles"])
    amount_OHLC_mid = len(OHLC_mid["candles"])
    #print(OHLC)
    bid_open = np.empty((0,amount_OHLC), float)
    ask_open = np.empty((0,amount_OHLC), float)
    mid_open = np.empty((0,amount_OHLC_mid), float)

    candles_time = np.empty((0,amount_OHLC), float)
    time_split_minute = np.empty((0,amount_OHLC), str)

    for i in range(0, amount_OHLC):
        bid_open = np.append(bid_open,OHLC["candles"][i]["bid"]["o"])
        ask_open = np.append(ask_open,OHLC["candles"][i]["ask"]["o"])
        mid_open = np.append(mid_open, OHLC_mid["candles"][i]["mid"]["o"])
        candles_time = np.append(candles_time, OHLC["candles"][i]["time"])

        time_split = candles_time[i].split(':')

        YMD_hour, min_freq, sec_freq = time_split

        YMD_hour_split = YMD_hour.split('-')
        #print(YMD_hour_split)

    bid_open2 = bid_open.astype(float)
    ask_open2 = ask_open.astype(float)
    mid_open2 = mid_open.astype(float)
    diff_ask_bid = np.subtract(ask_open2, bid_open2)
    diff_mid_BA = np.subtract(ask_open2, mid_open2)

    n = 360
    ave_DAB = np.mean(diff_ask_bid[:n])
    std_DAB = np.std(diff_ask_bid[:n])
    print(ave_DAB)
    print(std_DAB)

    plt.subplot(4,1,1)
    plt.plot(bid_open2,'b')
    plt.plot(ask_open2,'r')

    plt.subplot(4,1,2)
    plt.plot(mid_open2, 'g')

    plt.subplot(4,1,3)
    plt.plot(diff_ask_bid,'k')

    plt.subplot(4,1,4)
    plt.plot(diff_ask_bid[:350])
    plt.xlabel("time - minute")

    plt.show()

get_candles(token=extract_token())
