import json, requests, time
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

startScript = dt.datetime.now()
def get_token(path = 'res/oanda_api_key.json'):
    with open(path) as data_file:
        data = json.load(data_file)
        return data['token']

def get_candles(token, instru, start, gran, based):
    header = {'Authorization': 'Bearer '+ token,
              "Accept-Datetime-Format":'RFC3339',
              "Content-Type": "application/json"}

    gran = 'granularity=' + gran
    uri = 'https://api-fxpractice.oanda.com/v3/instruments/{}/candles?price={}&from={}&{}'.format(instru,based,start,gran)
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
    else:
        print('Error: get_candles func based parameter did not match ' +
        '\'BA\' or \'M\'. Can not create numpy arrays.')

    for i in range(0, amount_OHLC):
        if based == 'BA':
            bid_close = np.append(bid_close,OHLC["candles"][i]["bid"]["c"])
            ask_close = np.append(ask_close,OHLC["candles"][i]["ask"]["c"])
            bid_open = np.append(bid_open,OHLC["candles"][i]["bid"]["o"])
            ask_open = np.append(ask_open,OHLC["candles"][i]["ask"]["o"])
        elif based == 'M':
            mid_close = np.append(mid_close, OHLC_mid["candles"][i]["mid"]["c"])
            mid_open = np.append(mid_open, OHLC_mid["candles"][i]["mid"]["o"])
        else:
            print('Error: get_candles func based parameter did not match' +
             '\'BA\' or \'M\'. Can not appened numpy arrays.')


    if based == 'BA':
        bid_close = bid_close.astype(float)
        ask_close = ask_close.astype(float)
        bid_open = bid_open.astype(float)
        ask_open = ask_open.astype(float)
        return instru, bid_close, ask_close, bid_open, ask_open, ticks
    elif based == 'M':
        mid_close = mid_close.astype(float)
        mid_open = mid_open.astype(float)
        return instru, mid_close, mid_open, ticks
    else:
        print('Error: get_candles func based parameter did not match '+
        '\'BA\' or \'M\'. Can not change type of np arrays from str to float.')
        return None

start_time = '2017-12-29T00%3A00%3A00.000000000Z' #'2017-12-29T00%3A00%3A00.000000000Z'
freq = 'S5' #S15
BA = 'BA' #BA

firstInstruGet = dt.datetime.now()
instrueu, BCeu, ACeu, BOeu, AOeu, ticks = get_candles(get_token(),
    'EUR_USD', start_time, freq, BA)
firstInstruGet = (dt.datetime.now()-firstInstruGet)
secondInstruGet = dt.datetime.now()
instruej, BCej, ACej, BOej, AOej, ticks = get_candles(get_token(),
    'EUR_JPY', start_time, freq, BA)
secondInstruGet = (dt.datetime.now()-secondInstruGet)
thirdInstruGet = dt.datetime.now()
instruec, BCec, ACec, BOec, AOec, ticks = get_candles(get_token(),
    'EUR_CAD', start_time, freq, BA)
thirdInstruGet = (dt.datetime.now()-thirdInstruGet)
fourthInstruGet = dt.datetime.now()
instruea, BCea, ACea, BOea, AOea, ticks = get_candles(get_token(),
    'EUR_AUD', start_time, freq, BA)
fourthInstruGet = (dt.datetime.now()-fourthInstruGet)

ave_BCeu = np.mean(BCeu)
ave_BCej = np.mean(BCej)
scale_uj = ave_BCej/ave_BCeu
norm_BCej = np.round(BCej/scale_uj,5)
diff_BCuj = norm_BCej-BCeu

ave_BCec = np.mean(BCec)
scale_uc = ave_BCec/ave_BCeu
norm_BCec = np.round(BCec/scale_uc,5)
diff_BCuc = norm_BCec-BCeu

ave_BCea = np.mean(BCea)
scale_ua = ave_BCea/ave_BCeu
norm_BCea = np.round(BCea/scale_ua,5)
diff_BCua = norm_BCea-BCeu

s=0
e=ticks
length_se = e-s
BCujMAX = round(np.amax(diff_BCuj[s:ticks]), 5)
BCujMIN = round(np.amin(diff_BCuj[s:ticks]), 5)
slope_BCuj = np.diff(diff_BCuj[s:ticks])
std_dev_muj = round(np.std(slope_BCuj), 5)
mean_muj = np.mean(slope_BCuj)

endScript = (dt.datetime.now()-startScript)

print('Time to run script \n {} \n'.format(endScript))
print('firstInstruGet: {}\n secondInstruGet: {}'.format(firstInstruGet, secondInstruGet))
print('thirdInstruGet: {}\n fourthInstruGet: {}\n'.format(thirdInstruGet, fourthInstruGet))
print('Number of ticks {}'.format(ticks))
print('Beginning of data {} \n'.format(start_time))
print('The maxmium of {}, {} Hedge is {}'.format(instruej, instrueu, BCujMAX))
print('The minimum of {}, {} Hedge is {} \n'.format(instruej, instrueu, BCujMIN))
print('The STD of BCuj slope is {}'.format(std_dev_muj))
print('The mean of BCuj slope is {}'.format(mean_muj))


plt.subplot(3,1,1)
plt.plot(BCeu[s:e], label='BC-'+instrueu)
plt.plot(norm_BCej[s:e], label='BC '+instruej)
plt.plot(norm_BCec[s:e], label='BC '+instruec)
plt.plot(norm_BCea[s:e], label='BC '+instruea)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

plt.subplot(3,1,2)
plt.plot((ACeu-BCeu)[s:e])

plt.subplot(3,1,3)
plt.plot(diff_BCuj[s:e])
plt.plot(diff_BCuc[s:e])
plt.plot(diff_BCua[s:e])
plt.plot(np.zeros(length_se), 'g')

plt.show()
