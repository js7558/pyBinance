#!/usr/bin/python
#
# show Binance order book for a given trading pair
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

# get the order book using the specified params
orderBook = bn.getOrderBook(queryParams) 

# print it out 
print "ASKS"
orderBook['asks'].reverse() # reverse asks so that lowest ask is at the bottom instead of the top
for i in (orderBook['asks']):
	print "qty is " + i[0] + " for a total of " + i[1]

print "BIDS"
for i in orderBook['bids']:
	print "qty is " + i[0] + " for a total of " + i[1]

