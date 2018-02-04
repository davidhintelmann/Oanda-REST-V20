import json, sys, time, datetime, requests
import matplotlib.pyplot as plt
import numpy as np

def get_token(path = 'res/oanda_api_key.json'):
    with open(path) as data_file:
        data = json.load(data_file)
        return data['token']

def get_candles(token, instru, start, gran):
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json"}
    based = 'BA'
    based_mid = 'M'
    gran = 'granularity=' + gran
    print('establishing connection')
    uri = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}'.format(instru,based,start,gran)
    uri_mid = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}'.format(instru,based_mid,start,gran)
    print('connection established')
    resp = requests.get(uri,headers=header)
    resp_mid = requests.get(uri_mid,headers=header)
    response = resp.text
    response_mid = resp_mid.text

    OHLC = json.loads(response)
    OHLC_mid = json.loads(response_mid)
    amount_OHLC = len(OHLC["candles"])
    ticks = amount_OHLC
    amount_OHLC_mid = len(OHLC_mid["candles"])
    bid_close = np.empty((0, amount_OHLC), float)
    ask_close = np.empty((0, amount_OHLC), float)
    mid_close = np.empty((0, amount_OHLC_mid), float)

    bid_open = np.empty((0, amount_OHLC), float)
    ask_open = np.empty((0, amount_OHLC), float)
    mid_open = np.empty((0, amount_OHLC_mid), float)

    candles_time = np.empty((0, amount_OHLC), float)
    time_split_minute = np.empty((0, amount_OHLC), str)
    #######
    #temp_array_min = np.empty((0, amount_OHLC), int)

    #check_min = 0 #both these varibles are loop
    #num_hours = 0 #counters for if statement below

    for i in range(0, amount_OHLC):
        bid_close = np.append(bid_close,OHLC["candles"][i]["bid"]["c"])
        ask_close = np.append(ask_close,OHLC["candles"][i]["ask"]["c"])
        mid_close = np.append(mid_close, OHLC_mid["candles"][i]["mid"]["c"])

        bid_open = np.append(bid_open,OHLC["candles"][i]["bid"]["o"])
        ask_open = np.append(ask_open,OHLC["candles"][i]["ask"]["o"])
        mid_open = np.append(mid_open, OHLC_mid["candles"][i]["mid"]["o"])

        candles_time = np.append(candles_time, OHLC["candles"][i]["time"])

        #time_split = candles_time[i].split(':')
        #YMD_hour, min_freq, sec_freq = time_split

        #min_freq = int(min_freq)
        #temp_array_min = np.append(temp_array_min, min_freq)
        #sec_freq = np.array(sec_freq, dtype=int)
        #print(sec_freq)

        #check_min += temp_array_min[i]
        """
        if check_min == 1770:
            num_hours += 1
            check_min = 0
        """
        #MD_hour_split = YMD_hour.split('-')
        #print(YMD_hour_split)

    #num_mins_left = temp_array_min[-1]
    bid_close = bid_close.astype(float)
    ask_close = ask_close.astype(float)
    mid_close = mid_close.astype(float)

    bid_open = bid_open.astype(float)
    ask_open = ask_open.astype(float)
    mid_open = mid_open.astype(float)

    return (instru, bid_close, ask_close, mid_close,#able to return
            bid_open, ask_open, mid_open, ticks)#num_hours, num_mins_left

start_time = '2017-12-29T00%3A00%3A00.000000000Z'
freq = 'S15'

instrueu, BCeu, ACeu, MCeu, BOeu, AOeu, MOeu, ticks = get_candles(get_token(),
    'EUR_USD', start_time, freq)
instruej, BCej, ACej, MCej, BOej, AOej, MOej, ticks = get_candles(get_token(),
    'EUR_JPY', start_time, freq)

print(ticks)
print(start_time)
ave_BCeu = np.mean(BCeu)
ave_BCej = np.mean(BCej)

#scale EUR_USD and EUR_JPY
scale_uj = ave_BCej/ave_BCeu
norm_BCej = np.round(BCej/scale_uj,5)
diff_BCuj = norm_BCej-BCeu
s=0
e=ticks
length_se = e-s
print(np.amax(diff_BCuj[s:e]))
print(np.amin(diff_BCuj[s:e]))
slope_BCuj = np.diff(diff_BCuj[s:e])
std_dev_muj = np.std(slope_BCuj)
#print(slope_BCuj)
print(round(std_dev_muj, 5))
print(np.mean(slope_BCuj[0:60]))
print(np.mean(slope_BCuj[60:150]))

plt.subplot(3,1,1)
#plt.plot(BCeu-BOeu, label='Diff BC - BO '+instrueu)
plt.plot(BCeu[s:e], label='BC-'+instrueu)
plt.plot(ACeu[s:e],'r',label='AC-'+instrueu)
plt.plot(norm_BCej[s:e], label='BC '+instruej)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

plt.subplot(3,1,2)
plt.plot(ACeu-BCeu)
#plt.plot(ACej-BCej, label='Spread '+instruej)

plt.subplot(3,1,3)
plt.plot(diff_BCuj[s+1:e+2])
plt.plot(slope_BCuj, 'm.', ms=3)
plt.plot(np.zeros(length_se), 'g')

plt.show()
