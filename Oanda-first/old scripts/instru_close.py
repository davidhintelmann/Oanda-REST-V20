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
    timee = '2017-12-29T13%3A00%3A00.000000000Z' #2017-12-28T15
    gran = 'granularity=S15' # candles freqeuncy

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
    bid_close = np.empty((0,amount_OHLC), float)
    ask_close = np.empty((0,amount_OHLC), float)
    mid_close = np.empty((0,amount_OHLC_mid), float)

    bid_open = np.empty((0,amount_OHLC), float)
    ask_open = np.empty((0,amount_OHLC), float)
    mid_open = np.empty((0,amount_OHLC_mid), float)

    candles_time = np.empty((0,amount_OHLC), float)
    time_split_minute = np.empty((0,amount_OHLC), str)
    SMA_3 = []
    SMA_3.append(0)
    SMA_3.append(0)
    SMA_3.append(0)

    for i in range(0, amount_OHLC):
        bid_close = np.append(bid_close,OHLC["candles"][i]["bid"]["c"])
        ask_close = np.append(ask_close,OHLC["candles"][i]["ask"]["c"])
        mid_close = np.append(mid_close, OHLC_mid["candles"][i]["mid"]["c"])

        bid_open = np.append(bid_open,OHLC["candles"][i]["bid"]["o"])
        ask_open = np.append(ask_open,OHLC["candles"][i]["ask"]["o"])
        mid_open = np.append(mid_open, OHLC_mid["candles"][i]["mid"]["o"])

        candles_time = np.append(candles_time, OHLC["candles"][i]["time"])

        time_split = candles_time[i].split(':')
        YMD_hour, min_freq, sec_freq = time_split
        YMD_hour_split = YMD_hour.split('-')
        #print(YMD_hour_split)

    bid_close2 = bid_close.astype(float)
    ask_close2 = ask_close.astype(float)
    mid_close2 = mid_close.astype(float)
    bid_open2 = bid_open.astype(float)
    ask_open2 = ask_open.astype(float)
    mid_open2 = mid_open.astype(float)

    for j in range (3,amount_OHLC-3):
        SMA_3.append((np.sum(bid_close2[j:j+3])/3))

    diff_ask_bid_close = np.subtract(ask_close2, bid_close2)
    diff_mid_BA_close = np.subtract(ask_close2, mid_close2)
    diff_ask_bid_open = np.subtract(ask_open2, bid_open2)
    diff_mid_BA_open = np.subtract(ask_open2, mid_open2)
    diff_OC_ask = np.subtract(ask_open2, ask_close2)
    diff_OC_bid = np.subtract(bid_open2, bid_close2)
    diff_OC_BA = np.subtract(diff_OC_ask, diff_OC_bid)
    diff_mid_close = np.subtract(mid_close2[:499], mid_close2[1:500])

    n = 500 #amount_OHLC
    #unique_DABC = np.unique(diff_ask_bid_close[:n])
    min_DABC = np.amin(diff_ask_bid_close[:n])
    min_DABC = round(min_DABC, 9)
    max_DABC = np.amax(diff_ask_bid_close[:n])
    max_DABC = round(max_DABC, 9)
    min_DOC_BA = np.amin(diff_OC_BA[:n])
    min_DOC_BA = round(min_DOC_BA, 9)
    max_DOC_BA = np.amax(diff_OC_BA[:n])
    max_DOC_BA = round(max_DOC_BA, 9)
    ave_DAB_close = np.mean(diff_ask_bid_close[:n])
    std_DAB_close = np.std(diff_ask_bid_close[:n])
    ave_DOC_ask = np.mean(diff_OC_ask[:n])
    std_DOC_ask = np.std(diff_OC_ask[:n])
    min_DMC = round(np.amin(diff_mid_close[:n]) ,9)
    max_DMC = round(np.amax(diff_mid_close[:n]), 9)
    #print(diff_mid_close)
    print('Average of diff_ask_bid_close is {} \n Standard Deviation of diff_ask_bid is {}'.format(ave_DAB_close, std_DAB_close))
    print('Average of diff_OC_ask is {} \n Standard Deviation of diff_OC_ask is {}'.format(ave_DOC_ask, std_DOC_ask))
    print('Minimum of min_DABC is {} \n Maximum of max_DABC is {}'.format(min_DABC, max_DABC))
    print('Minimum of min_DOC_BA is {} \n Maximum of max_DOC_BA is {}'.format(min_DOC_BA, max_DOC_BA))
    #print('SMA_3 is {}'.format(SMA_3))
    #print('Length of SMA_3 Array is {}'.format(len(SMA_3)))
    print('Minimum of min_DMC is {} \n Maximum of max_DMC is {}'.format(min_DMC, max_DMC))

    #SMA_3_len = np.arange(len(SMA_3), dtype=int) #still wrong?
    #print(SMA_3_len)

    plt.subplot(6,1,1)
    plt.plot(bid_close2,'b')
    plt.plot(ask_close2,'r')

    plt.subplot(6,1,2)
    plt.plot(diff_ask_bid_close,'k')

    plt.subplot(6,1,3)
    plt.plot(diff_ask_bid_close[:n])

    plt.subplot(6,1,4)
    plt.plot(diff_OC_ask, 'b')
    plt.plot(diff_OC_bid, 'r')

    plt.subplot(6,1,5)
    plt.plot(diff_mid_close[:n], 'b')
    plt.plot(diff_OC_BA[:n], 'g')

    plt.subplot(6,1,6)
    plt.plot(diff_mid_close[:n], 'b')

    plt.xlabel("time - minute")
    plt.show()

get_candles(token=extract_token())
