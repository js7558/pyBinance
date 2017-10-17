#!/usr/bin/python
#
# Send an order via Binance API.
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
queryParams['symbol'] = 'XVGBTC'   # start with a cheap asset so if you goof it won't be terrible
queryParams['side'] = 'BUY'
#queryParams['type'] = 'LIMIT'
queryParams['type'] = 'MARKET'
queryParams['timeInForce'] = 'GTC'
queryParams['quantity'] = 1.0
queryParams['price'] = 0.0000005

# this logging configuration is sketchy
binance = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini')

# create Binance object
bn = Binance()

# set keys
bn.setSecretKey(readConfig('secret'))
bn.setAPIKey(readConfig('apikey'))

myorder = bn.createOrder(queryParams,True) 	# the testFlag=True  here makes it a test
#myorder = bn.createOrder(queryParams) 	 # the absense of testFlag makes this execute a trade
print myorder

