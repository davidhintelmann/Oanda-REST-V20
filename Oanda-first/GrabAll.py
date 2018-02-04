import datetime as datetime
import time
import numpy as np
import NormCur as nc
import OHLC as oc

token = oc.GrabToken()
start_time = '2017-12-20T00%3A00%3A00.000000000Z' #2018-01-01T21 new year 2018
freq = 'S5'
BA = 'M'

def GrabAllCandles():
    first = datetime.datetime.now()
    ieu, *_, Ceu, tickseu = oc.GrabCandles(token,
        'EUR_USD', start_time, freq, BA)
    firstLoaded = datetime.datetime.now()-first

    second = datetime.datetime.now()
    iej, *_, Cej, ticksej = oc.GrabCandles(token,
        'EUR_JPY', start_time, freq, BA)
    secondLoaded = datetime.datetime.now()-second

    firstLoaded = str(firstLoaded)
    timee = firstLoaded.split(':')
    firstLoaded = float(timee[2])
    secondLoaded = str(secondLoaded)
    timee = secondLoaded.split(':')
    secondLoaded = float(timee[2])
    print(firstLoaded+secondLoaded)
    if firstLoaded+secondLoaded < 2:
        print('Waiting for connection... Grabbing Data...')
        wait = 2.0-firstLoaded+secondLoaded
        time.sleep(wait)

    third = datetime.datetime.now()
    iea, *_, Cea, ticksea = oc.GrabCandles(token,
        'EUR_AUD', start_time, freq, BA)
    thirdLoaded = datetime.datetime.now()-third

    thirdLoaded = str(thirdLoaded)
    timee = thirdLoaded.split(':')
    thirdLoaded = float(timee[2])
    print(firstLoaded+secondLoaded+thirdLoaded)
    if firstLoaded+secondLoaded+thirdLoaded < 2:
        print('Waiting for connection... Grabbing Data...')
        waitTwo = 2.0-firstLoaded+secondLoaded+thirdLoaded
        time.sleep(waitTwo)

    fourth = datetime.datetime.now()
    iec, *_, Cec, ticksec = oc.GrabCandles(token,
        'EUR_CAD', start_time, freq, BA)
    fourthLoaded = datetime.datetime.now()-fourth

    fourthLoaded = str(fourthLoaded)
    timee = fourthLoaded.split(':')
    fourthLoaded = float(timee[2])
    print(firstLoaded+secondLoaded+thirdLoaded+fourthLoaded)
    if tickseu == ticksej == ticksea == ticksec:
        return ieu, Ceu, iej, Cej, iea, Cea, iec, Cec, tickseu
    else:
        print('\nWARNING: Ticks do not span same time '+
            'interval in\n GrabAllCandles func. '+
            'Called from Graball.py')
        print('EUR_USD ticks {} EUR_JPY ticks {}'.format(tickseu,ticksej))
        print('EUR_CAD ticks {} EUR_AUD ticks {}\n'.format(ticksec,ticksea))
        return ieu, Ceu, iej, Cej, iea, Cea, iec, Cec, tickseu
