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

# getKline
print "---------------- getKline --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'SALTBTC','interval':'5m'}
print "****test valid symbol, interval"
test = bn.getKline(queryParams)
print
print "****test valid symbol, interval, limit"
queryParams = {'symbol':'SALTBTC','limit':20,'interval':'1M'}
test = bn.getKline(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':1507574763000,'endTime':1507574763999,'interval':'1m'}
print "****test valid symbol, interval, limit, startTime, endTime"
test = bn.getKline(queryParams)
print
print "################################# NEGATIVE TESTS (returns 0) ###################"
print
print "****test valid symbol, interval, limit too high"
queryParams = {'symbol':'SALTBTC','limit':501,'interval':'1M'}
test = bn.getKline(queryParams)
print
queryParams = {'symbol':'FAKEBTC','limit':501,'interval':'5m'}
print "****test invalid symbol, interval, limit too high"
test = bn.getKline(queryParams)
print
queryParams = {'limit':50,'interval':'5m'}
print "****test missing mandatory value"
test = bn.getKline(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'endTime':1507574763999,'interval':'3m'}
print "****test valid symbol, interval, limit, startTime present and missing endTime"
test =  bn.getKline(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':15035747630,'endTime':1507574763999,'interval':'8h'}
print "****test valid symbol, interval, limit, startTime or endTime invalid number"
test =  bn.getKline(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':15035747630,'endTime':'someinvalidvalue','interval':'8h'}
print "****test valid symbol, interval, limit, startTime or endTime invalid type"
test =  bn.getKline(queryParams)
print
queryParams = {'symbol':'SALTBTC','limit':5,'startTime':150357476300,'endTime':1507574763999,'interval':'fudgepop'}
print "****test valid symbol, limit, startTime, endTime, invalid interval type"
test = bn.getKline(queryParams)
