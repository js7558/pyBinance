#!/usr/bin/python
#
# Show personal order history per asset on Binance API
#
#
##################################################################################
# MIT License
# 
# Copyright (c) 2017 Jason Shaw
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
##################################################################################

import sys
sys.path.append('..') 	# append .. to the current path so it can find Binance.py
from Binance import Binance
import logging.config
import logging.handlers
import logging
import ConfigParser
import json
import pandas as pd
import time

def readConfig(key):
        # read in configuration
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
	return config.get('KEYS',key)

queryParams={}
queryParams['symbol'] = (raw_input("Name of Symbol: ")).upper()
queryParams['limit'] = int(raw_input("Number of Rows: "))	# note cast to int here, otherwise python makes this a string

# this logging configuration is sketchy
binance = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini')

# create Binance object
bn = Binance()

# set keys
bn.setSecretKey(readConfig('secret'))
bn.setAPIKey(readConfig('apikey'))

print "MY ORDER HISTORY OF " + queryParams['symbol']
# fetch order list into a pandas dataframe, add human readable date/time, and print out a few columns of interest
df = pd.DataFrame(bn.getAllOrders(queryParams))
df['date'] = df['time'].apply(lambda x: (time.strftime('%Y-%m-%d',(time.localtime(x/1000)))))
df['time'] = df['time'].apply(lambda x: (time.strftime('%H:%M:%S',(time.localtime(x/1000)))))
print df.loc[:,['orderId','date','time','side','price','origQty']]

