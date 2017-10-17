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

# getOrderBook
print "---------------- getOrderBook --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'ETHBTC'}
print "****test valid symbol"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5}
print "****test valid symbol, limit"
test = bn.getOrderBook(queryParams)
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
print
queryParams = {'symbol':'SALTBTC','limit':5000}
print "****test valid symbol, limit too high"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':'FAKEBTC'}
print "****test invalid symbol"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':'FAKEBTC','limit':501}
print "****test invalid symbol, limit too high"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':'ETHBTC','limit':42}
print "****test valid symbol, limit not in enum"
test = bn.getOrderBook(queryParams)
print
queryParams = {'limit':50}
print "****test missing mandatory value (symbol)"
test = bn.getOrderBook(queryParams)
print
queryParams = {'limit':5000}
print "****test missing mandatory value (symbol), limit too high"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':'5'}
print "****test valid symbol, invalid limit type due to typo (int enclosed in quotes)"
test = bn.getOrderBook(queryParams)
print
queryParams = {'symbol':123999,'limit':'5'}
print "****test invalid symbol, valid limit"
test = bn.getOrderBook(queryParams)
print
