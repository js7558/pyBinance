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

# cancelOrder
print "---------------- cancelOrder --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'SALTBTC'}
print "****test valid mandatory input symbol"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','orderId':112234}
print "****test valid mandatory inputs plus some optional"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','orderId':112234,'origClientOrderId':'13434234234dafadsf'}
print "****test valid mandatory inputs plus some optional"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','orderId':112234,'recvWindow':13434234234}
print "****test valid mandatory inputs plus some optional"
test = bn.cancelOrder(queryParams)
print

print "################################# NEGATIVE TESTS (returns 0) ###################"
print
queryParams = {'orderId':112234}
print "****test valid mandatory inputs, valid parameter missing"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':12.5,'orderId':3334344}
print "****test valid mandatory inputs present with invalid type"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','origClientOrderId':'123456778','timestamp':150774295}
print "****test valid mandatory inputs, invalid user proved timestamp, plus some optional"
test = bn.cancelOrder(queryParams)
print
queryParams = {'symbol':'ETHBTC','orderId':999999,'timestamp':'abcdefghijklm'}
print "****test valid mandatory inputs, invalid user proved timestamp type but length ok, plus some optional"
test = bn.cancelOrder(queryParams)
print
