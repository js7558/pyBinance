#!/usr/bin/python
#
# get current price of a trading pair
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
sys.path.append('..')   # append .. to the current path so it can find Binance.py
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

# the symbol we want to get a price for <your value here>
symbol_of_interest = (raw_input("Name of Symbol: ")).upper()

# this logging configuration is sketchy
binance = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini')

# create Binance object
bn = Binance()

allPrices = bn.getTicker('allPrices')

try:
	# a list comprehension for extracting the target from json
	price =  [x for x in allPrices if "symbol" in x and x['symbol'] == symbol_of_interest][0]['price']
except:
	print "symbol not found"
else:
	print "The current price of " + symbol_of_interest + " is " + price

