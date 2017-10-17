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

# getAggTrades
print "---------------- getAggTrades --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'ETHBTC'}
print "****test valid symbol"
test = bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','fromId':1766960}
print "****test valid symbol, fromId"
test = bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5}
print "****test valid symbol, limit"
test = bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':1507574763000,'endTime':1507574763999,'fromId':1766960}
print "****test valid symbol, fromId, limit, startTime, endTime"
test = bn.getAggTrades(queryParams)
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
queryParams = {'symbol':'FAKEBTC','limit':501,'fromId':1766960}
print "****test invalid symbol, fromId, limit too high"
test = bn.getAggTrades(queryParams)
print
print "****test valid symbol, fromId, limit too high"
queryParams = {'symbol':'SALTBTC','limit':501,'fromId':1766960}
test = bn.getAggTrades(queryParams)
print
queryParams = {'limit':50,'fromId':1766960}
print "****test missing mandatory value"
test = bn.getAggTrades(queryParams)
print
queryParams = {'limit':50,'invalidKey':'1766960'}
print "****test invalid key"
test = bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'endTime':1507574763999,'fromId':1766960}
print "****test valid symbol, fromId, limit, startTime present and missing endTime"
test =  bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':15035747630,'endTime':1507574763999,'fromId':1766960}
print "****test valid symbol, fromId, limit, startTime or endTime invalid number"
test =  bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':1503574763000,'endTime':1507574763999}
print "****test valid symbol, fromId, limit, startTime and endTime diff > 24 hours"
test =  bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':15035747630,'endTime':'someinvalidvalue','fromId':1766960}
print "****test valid symbol, fromId, limit, startTime or endTime invalid type"
test =  bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':150357476300,'endTime':1507574763999,'fromId':'fudgepop'}
print "****test valid symbol, limit, startTime, endTime, invalid fromId type"
test = bn.getAggTrades(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':150357476300,'endTime':1507574763999,'fromId':'1766960'}
print "****test valid symbol, limit, startTime, endTime, invalid fromId type due to typo (int enclosed in quotes)"
test = bn.getAggTrades(queryParams)
