# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:30:43 2018

@author: Vishnu
"""

import pandas as pd
import os
import glob
from pymongo import MongoClient

db_client = MongoClient('52.221.4.121', 38128)
os.chdir('C:/Users/hp/Documents/Python Scripts/AIC/data')
# os.chdir('/home/dev/QAbot/Data')
path = glob.glob("*.csv")

def FAQdata(path):
    for i in path:
        df = pd.read_csv(i)
        data = dict(zip(df.Question, df.Answer))
        for key, value in data.items():
            db_client.local.FAQ.insert_one({'Question': key, 'Answer': value, 'keyword': i.split('_')[0].lower()})

FAQdata(path)