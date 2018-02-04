import pandas as pd

from events import TickEvent

class backTestStrat(obejct):
    def __init__(self, instru, units):
        self.instru = instru
        self.units = units
        #self.events_backque = events_backque

        bidAtime = {}
        askAtime = {}

    def AppendTB(self, event):
        bidAtime[event.time] = event.bid
        askAtime[event.time] = event.ask
