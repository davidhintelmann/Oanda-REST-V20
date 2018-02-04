from events import OrderEvent
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class TestStrat(object):

    def __init__(self, instru, events_straque):
        self.instru = instru
        #self.units = units
        self.events_straque = events_straque
        self.ticks = 0
        self.ab_list = []

    def appendTick(self, event):

        self.ab_list.append([event.time,event.bid,event.ask])
        AB = pd.DataFrame(self.ab_list,columns=['time','bid','ask'])
        print(AB)

    def reversionStrat(self, event):
        if event.type == 'TICK':
            self.appendTick(event)
            self.ticks += 1
            if self.ticks >= 2:
                DAB_temp = pd.DataFrame(self.ab_list,columns=['time','bid','ask'])
                DAB = DAB_temp.diff()
                print(DAB[1:]) #first index value is NaN
