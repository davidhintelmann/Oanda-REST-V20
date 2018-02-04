import pandas as pd
import os, json, glob2
import numpy as np

from events import TickEvent

class DataHandler(object):
    def __init__(self, instru, file_name):
        self.instru = instru
        self.file_name = file_name
        #self.event_queue = event_queue

    def readJSONdata(self):
        pathing = ('/Users/DavidH/Documents/GitHub/Event-Oanda/Price-History/'+
                    str(self.instru)+'/')
        filename = pathing + str(self.file_name)
        #OHLC = pd.read_json(filename,orient='index')
        try:
            with open(os.path.join(pathing,filename),'r') as j:
                OHLC = json.load(j)
            return OHLC
        except Exception as e:
            j.close()
            print('Error in readJSONdata func, can not open file: '+str(e))

    def StreamJSONdata(self):
        pass #pass JSON as 'TICK' event




        ticks = len(OHLC['candles'])
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










%timeit os.listdir('/Users/DavidH/Documents/GitHub/Event-Oanda/Price-History/')

b = glob2.glob('/Users/DavidH/Documents/GitHub/Event-Oanda/Price-History/*/*.json')
print(b)

        #tickOHLC = TickEvent(instru, time, bid, ask)
        #self.event_queue.put(tickOHLC)

testBTstream = DataHandler('EUR_AUD',
    'EUR_AUD,S5,count3.json')

testBTstream.readJSONdata()
