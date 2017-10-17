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

# createOrder
print "---------------- createOrder --------------"
print "################################# POSITIVE TESTS (returns 1 or r) ###################"
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0}
print "****test valid mandatory inputs"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'123456778'}
print "****test valid mandatory inputs plus some optional"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'223456778'}
print "****test valid mandatory inputs plus some optional"
test = bn.createOrder(queryParams)
print
queryParams = {'stopPrice':3.0,'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'223456778'}
print "****test valid mandatory inputs plus some optional"
test = bn.createOrder(queryParams)
print
queryParams = {'icebergQty':10.5,'stopPrice':3.0,'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'223456778'}
print "****test valid mandatory inputs plus some optional"
test = bn.createOrder(queryParams)


print "################################# NEGATIVE TESTS (returns 0) ###################"
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0}
print "****test valid mandatory inputs, valid parameter missing"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','price':1.0}
print "****test valid mandatory inputs, valid parameter missing"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':5,'type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0}
print "****test valid mandatory inputs present with invalid type"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':12,'price':2.0}
print "****test valid mandatory inputs present with invalid type"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'DUCK','type':'LIMIT','timeInForce':'GTC','quantity':13.0,'price':2.0}
print "****test valid mandatory inputs present with valid type but not in enum"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'FAKEBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':13.0,'price':2.0}
print "****test valid mandatory inputs present with valid type but not in enum"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'ETHBTC','side':'BUY','type':'BANANA','timeInForce':'GTC','quantity':13.0,'price':2.0}
print "****test valid mandatory inputs present with valid type but not in enum"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'ETHBTC','side':'BUY','type':'MARKET','timeInForce':'DARTH VADER','quantity':13.0,'price':2.0}
print "****test valid mandatory inputs present with valid type but not in enum"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'123456778','timestamp':150774295}
print "****test valid mandatory inputs, invalid user proved timestamp, plus some optional"
test = bn.createOrder(queryParams)
print
queryParams = {'symbol':'SALTBTC','side':'BUY','type':'LIMIT','timeInForce':'GTC','quantity':1.0,'price':2.0,'newClientOrderId':'123456778','timestamp':'abcdefghijklm'}
print "****test valid mandatory inputs, invalid user proved timestamp type but length ok, plus some optional"
test = bn.createOrder(queryParams)
print
