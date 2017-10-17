#!/usr/bin/python

import pandas as pd
import sys
sys.path.append('../')
from Binance import Binance
import logging.config
import logging.handlers
import logging
import os


# this logging configuration is sketchy
binance = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini')


# create Binance object
bn = Binance()

# set keys
bn.setSecretKey('NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
bn.setAPIKey('vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A')

# getTicker
print "---------------- getTicker --------------"
print "---------------- tickerType = 24hr --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'SALTBTC'}
print "****test valid symbol for tickerType = 24hr"
test = bn.getTicker('24hr',queryParams)
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
print
queryParams = {'symbol':'FAKEBTC'}
print "****test invalid symbol for tickerType = 24hr"
test = bn.getTicker('24hr',queryParams)
print
queryParams = {}
print "****test missing mandatory value tickerType = 24hr"
test = bn.getTicker('24hr',queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5}
print "****test valid symbol, other invalid attribute for tickerType = 24hr"
test =  bn.getTicker('24hr',queryParams)
print
print
print "---------------- tickerType = allPrices--------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {}
print "****test empty queryParams for tickerType = allPrices"
test = bn.getTicker('allPrices',queryParams)
print
print "****test  queryParams not passed for tickerType = allPrices"
test = bn.getTicker('allPrices')
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
queryParams = {'symbol':'BNBBTC'}
print "****test valid but extraneous symbol for tickerType = allPrices"
test = bn.getTicker('allPrices',queryParams)
print
queryParams = {'symbol':'FAKEBTC'}
print "****test invalid symbol for tickerType = allPrices"
test = bn.getTicker('allPrices',queryParams)
print
print
print "---------------- tickerType = allBookTickers --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {}
print "****test empty queryParams for tickerType = allBookTickers"
test = bn.getTicker('allBookTickers',queryParams)
print
print "****test  queryParams not passed for tickerType = allBookTickers"
test = bn.getTicker('allBookTickers')
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
queryParams = {'symbol':'BNBBTC'}
print "****test valid but extraneous symbol for tickerType = allBookTickers"
test = bn.getTicker('allBookTickers',queryParams)
print
queryParams = {'symbol':'FAKEBTC'}
print "****test invalid symbol for tickerType = allBookTickers"
test = bn.getTicker('allBookTickers',queryParams)
