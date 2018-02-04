import json, requests, os, pathlib
from time import time, sleep
from datetime import datetime
import pandas as pd

from enviroB import API_DOMAIN, GrabToken, GrabID

class GrabHistPrice(object):
    def __init__(self, domain, token, instru, gran, count=500):
        self.domain = domain
        self.token = token
        self.gran = gran
        self.instru = instru
        self.count = count
        self.current_time = time()
        self.instrum, self.instrum_two = self.instru.split('_')

    def requestHistStream(self):
        try:
            ses = requests.Session()

            header = {'Authorization':'Bearer '+ self.token,
                      'Accept-Datetime-Format':'UNIX',
                      'Content-Type':'application/octet-stream'
                      }
            param = {'price':'BA','granularity':self.gran,'count':self.count}
            url = ('https://' + self.domain + '/v3/instruments/' + self.instru +
                   '/candles?')

            resp = ses.get(url, headers=header, params=param)

            return resp
        except Exception as e:
            ses.close()
            print('Error in requestHistStream Func, can not connect to api: '+ str(e))


    def downloadSingle(self):
        try:
            OHLC = self.requestHistStream()
            OHLC = OHLC.json()

            JSONname = (str(self.gran)+','+str(self.current_time)+
                        ','+'count='+str(self.count)+'.json')
            pathing = ('/Users/DavidH/Documents/GitHub/Oanda-Event/Price-History/'+
                        self.instrum+'/'+self.instru)
            pathlib.Path(pathing).mkdir(parents=True, exist_ok=True)
            directory = os.path.join(pathing,JSONname)
            with open(directory,'w') as j:
                json.dump(OHLC, j)
        except Exception as e:
            print('Error in downloadSingle Func, can not convert to JSON file: '+ str(e))


    def downloadAll(self):
        if self.instrum == 'EUR':
            try:
                currency_list_EUR = ['CAD','AUD','USD','GBP','JPY','NZD']
                currency_list_EUR.remove(self.instrum_two)
                currency_list = []
                self.downloadSingle() #sloppy, no slowdown in server requests

                for cur in currency_list_EUR:
                    currency_list.append('_'.join([self.instrum,cur]))
            except Exception as e:
                print('Error, caught exception as {}\nIn downloadAll(), first if'.format(e))
            else:
                for i in range(len(currency_list)):
                    start = time()
                    temp_cur = currency_list[i]
                    temp_OHLC = GrabHistPrice(self.domain,self.token,temp_cur,self.gran)
                    temp_OHLC.downloadSingle()
                    end = time()
                    download_time = end - start
                    if download_time <= 0.5:
                        sleep_time = round(0.5-download_time, 4)
                        sleep(sleep_time)
                        print('waiting {} (sec) to download {} JSON files.'.format(sleep_time,temp_cur))
        else:
            print('Error did not find currency to match \'EUR\'.\n')

token = GrabToken()

EUR_OHLC = GrabHistPrice(API_DOMAIN,token,'EUR_USD','S5')
EUR_OHLC.downloadAll()
