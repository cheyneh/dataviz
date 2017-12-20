
import json
import datetime

import numpy as np
import pandas as pd

def load_data_dict():
    with open('data.json') as f:
        data = json.load(f)
    return data

try:    data
except: data = load_data_dict()



class Data(object):
    def __init__(self):
        self.raw_data = data

    def get_dataframe(self, metric='score'):
        data = {ts: {sid: self.raw_data[ts][sid][metric] for sid in self.raw_data[ts]} 
                for ts in self.raw_data}
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        return df



        


if __name__ == '__main__':
    data = Data()


