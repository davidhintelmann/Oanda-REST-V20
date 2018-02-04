import queue as qu
import threading
import time

from enviro import STREAM_DOMAIN, GrabToken, GrabID
from strategytest import TestStrat
from stream import GrabPrice

def trade(events, strategy):
    while True:
        try:
            event = events.get(False)
        except qu.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.reversionStrat(event)
                else:
                    print(event.type)
        time.sleep(HeartB)

if __name__ == '__main__':
    HeartB = 0.0001
    events = qu.Queue()
    instru = 'EUR_USD'
    token = GrabToken()
    ID_Num = GrabID()

    prices = GrabPrice(STREAM_DOMAIN,token,ID_Num,instru, events)
    strat = TestStrat(instru, events)

    trade_thread = threading.Thread(target=trade, args=(events, strat))
    price_thread = threading.Thread(target=prices.streamPrices, args=[])
    trade_thread.start()
    price_thread.start()
