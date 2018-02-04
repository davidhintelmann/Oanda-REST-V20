import json, requests

from events import TickEvent
from enviro import STREAM_DOMAIN, GrabToken, GrabID

class GrabPrice(object):
    def __init__(self, domain, token, ID_num, instru, event_queue):
        self.domain = domain
        self.token = token
        self.ID_num = ID_num
        self.instru = instru
        self.event_queue = event_queue

    def requestStream(self):
        try:
            s = requests.Session()

            header = {'Authorization':'Bearer '+ self.token,
                      'Accept-Datetime-Format':'UNIX',
                      'Content-Type':'application/octet-stream',
                      'Connection':'Keep-Alive'
                      }
            param = {'instruments':self.instru}
            url = ('https://' + self.domain + '/v3/accounts/' + self.ID_num +
                '/pricing/stream?')
            resp = s.get(url,headers=header,params=param,stream=True)

            return resp
        except Exception as e:
            s.close()
            print('Error in requestStream func, can not connect to stream\n'+
            str(e))

    def streamPrices(self):
        OHLC = self.requestStream()
        for line in OHLC.iter_lines():
            try:
                decoded_line = line.decode('utf-8')
                OHLC = json.loads(decoded_line)
            except Exception as e:
                print('Error in streamPrices func, can not parse\n'+ str(e))
            else:
                if OHLC['type'] == 'PRICE':
                    #status = OHLC['status'] # ie 'tradeable'
                    #can_trade = OHLC['tradeable'] #boolean value, ie True
                    instru = OHLC['instrument']
                    time = OHLC['time']
                    bid = OHLC['bids'][0]['price']
                    #bid_liq = OHLC['bids'][0]['liquidity']
                    #bid_close = OHLC['closeoutBid']
                    ask = OHLC['asks'][0]['price']
                    #ask_liq = OHLC['asks'][0]['liquidity']
                    #ask_close = OHLC['closeoutAsk']
                    #####print(time)

                    tickOHLC = TickEvent(instru, float(time), float(bid), float(ask))
                    self.event_queue.put(tickOHLC)
                elif OHLC['type'] == 'HEARTBEAT':
                    time_HB = OHLC['time']
                    print('{} : HEARTBEAT'.format(time_HB))

"""
#testing this script with print func above (line 54)

#comment out self.event_queue and delete the parameter
#in GrabPrice self.event_queue to test script

token = GrabToken()
ID_Num = GrabID()

testGrab = GrabPrice(STREAM_DOMAIN,token,ID_Num,'EUR_USD')

testGrab.streamPrices()
"""
