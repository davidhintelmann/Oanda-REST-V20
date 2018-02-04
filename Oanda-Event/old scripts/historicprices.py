import json, requests
from time import time
from datetime import datetime
import pandas as pd
import os

#from events import TickEvent
from enviro import API_DOMAIN, GrabToken, GrabID

class GrabHistPrice(object):
    def __init__(self, domain, token, instru, gran, count=500):
        self.domain = domain
        self.token = token
        self.instru = instru
        self.gran = gran
        self.count = count
        self.current_time = time()

    def requestHistStream(self):
        try:
            ses = requests.Session()

            header = {'Authorization':'Bearer '+ self.token,
                      'Accept-Datetime-Format':'UNIX',
                      'Content-Type':'application/octet-stream'
                      }
            param = {'price':'BA','granularity':self.gran,'count':self.count,
                     'to':self.current_time
                    }
            url = ('https://' + self.domain + '/v3/instruments/' + self.instru +
                   '/candles?')

            resp = ses.get(url, headers=header, params=param)

            return resp
        except Exception as e:
            ses.close()
            print('Error in requestHistStream Func, can not connect to api: '+ str(e))


    def downloadAsJSON(self):
        try:
            OHLC = self.requestHistStream()
            #OHLC = OHLC.text
            #OHLCpanda = pd.read_json(OHLC, orient='index')
            OHLC = OHLC.json()
            JSONname = (str(self.gran)+','+str(self.current_time)+
                        ','+'count='+str(self.count)+'.json')
            pathing = ('/Users/DavidH/Documents/GitHub/Event-Oanda/Price-History'+
                        '/'+self.instru)

            #OHLCnorm = pd.DataFrame(OHLCpanda)
            #OHLCnorm.to_json(os.path.join(pathing,JSONname),orient='index')
            with open(os.path.join(pathing,JSONname),'w') as j:
                json.dump(OHLC, j)
        except Exception as e:
            print('Error in downloadAsJSON Func, can not convert to JSON file: '+ str(e))


token = GrabToken()
testOHLC = GrabHistPrice(API_DOMAIN,token,'EUR_USD','S5')


testOHLC.downloadAsJSON()
