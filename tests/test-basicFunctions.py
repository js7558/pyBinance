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

# getSigtnature
print "---------------- getSignature --------------"
totalParams = bytes("symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559").encode('utf-8')
secretKey = bytes("NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j").encode('utf-8')
signature = bn.getSignature(secretKey, totalParams)
print signature

# getTimestamp
print "---------------- getTimeStamp --------------"
timestamp = bn.getTimestamp()
print timestamp

# getServerTime
print "---------------- getServerTime --------------"
servertime = bn.getServerTime()
print servertime

# testConnectivity
print "---------------- testConnectivity --------------"
test = bn.testConnectivity()
print test

# getSymbols
print "---------------- getSymbols --------------"
test = bn.getSymbols()
print test
#print 'symbol is ETHBTC'
#test = bn.getSymbols('ETHBTC')
#print test
