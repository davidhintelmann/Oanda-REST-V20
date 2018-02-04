from os.path import join
from glob2 import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from json import load

class plotOHLC(object):
    def __init__(self, primary_cur, gran=None):
        self.primary_cur = primary_cur
        self.gran = gran

        glob_path = ('/Users/DavidH/Documents/GitHub/Event-Oanda/Price-History/'+
          self.primary_cur+'/*')
        path_to_json = glob(glob_path)
        #print(path_to_json)
        #self.OHLC = pd.read_json()
        if gran == 'S5':
            for folder in path_to_json:
                temp_glob = glob(folder+'/[5S]*.json')
                print(temp_glob)
                #json_file = join(temp_path,)


tst = plotOHLC('EUR','S5')
