class Event(object):
    pass

class TickEvent(Event):
    def __init__(self, instru, time, bid, ask):
        self.type = 'TICK'
        self.instru = instru
        self.time = time
        self.bid = bid
        self.ask = ask

class OrderEvent(Event):
    def __init__(self, instru, units, order_type, direction):
        self.type = 'ORDER'
        self.instru = instru
        self.units = units
        self.order_type = order_type
        self.direction = direction

    def PrintOrder(self):
        print('Curreny Pair: {}  Units: {}  Order Type: {}  Direction: {}'.format(
            self.instru,self.units,self.order_type,self.direction))
