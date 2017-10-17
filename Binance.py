#!/usr/bin/python
# 
# Class to use the Binance API described at https://www.binance.com/restapipub.html
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

import hmac
import hashlib
import time
import requests
import pandas as pd
import numpy as np
import inspect
import logging
import sys

# need to deal with version
version= '0.1.2'

class Binance:
	def __init__(self, logger=None):
		# set up logging handler and suppress 'No handlers' message by adding NullHandler
		# note that handler/format/etc setup needs to be specified in the calling program
		# for any of the logger messages in this module to print
		self.logger = logger or logging.getLogger(__name__)
		self.logger.addHandler(logging.NullHandler())

	def __version__(self):
		# not sure if this is how I'm supposed to do it
		return version
	
	def setAPIKey(self, apikey):
		#
		# ---- DESCRIPTION ---
		# sets apikey
		# 
		# ---- INPUTS ---
		# apikey: the apikey 
		#
		# ---- OUTUTS ---
		# returns 1

		self.apikey = apikey
		return 1

	def setSecretKey(self, secret):
		#
		# ---- DESCRIPTION ---
		# sets secret 
		# 
		# ---- INPUTS ---
		# secret: the secret key
		#
		# ---- OUTUTS ---
		# returns 1

		self.secret = secret
		return 1
		

	def sendHTTPRequest(self, path, verb='get', query_string='',myheaders={}):
		# this is an internal function that sends HTTP requests for other functions in this class
		baseurl = 'https://www.binance.com'
		url = baseurl + path

		self.logger.debug("path is %s",path)
		self.logger.debug("verb is %s",verb)
		self.logger.debug("query_string is %s",query_string)
		self.logger.debug("myheaders is %s",myheaders)

		if (verb.lower() == 'get'):
			r = requests.get(url, params=query_string, headers=myheaders)
		elif (verb.lower() == 'post'):
			r = requests.post(url, params=query_string, headers=myheaders)
		elif (verb.lower() == 'delete'):
			r = requests.delete(url, params=query_string, headers=myheaders)

		# to do
		#  - check and handle different response codes
		return r

	def requestSender(self, path, verb, queryParams={}, expected={}, signed=False):
		# this is an internal function that sends the request and checks the return value
		# check values passed in against the definition provided by Binance
		self.logger.info("queryParams contains %s",queryParams)
		if(self.validateParams(queryParams,expected)): 
			# get query_string and sign as necessary
			query_string = self.getQueryString(queryParams) 
			self.logger.info("query string is %s", query_string)
			myheaders={}	
			if (signed):
				# Check if secret key is set. For type = Signed both signature and api key required.
				try:
					self.secret
				except:
					self.logger.error("secret key not set, perhaps call setSecretKey?")
					return 0


				# Check if API key is set. For type = Signed both signature and api key required.
				try:
					self.apikey
				except:
					self.logger.error("API key not set, perhaps call setAPIKey?")
					return 0

				self.logger.debug("API key setting being used is %s",self.apikey)
				myheaders = {'X-MBX-APIKEY':self.apikey}

				query_string = query_string + '&signature=' + self.getSignature(self.secret,query_string)	
				self.logger.info("signed query string is %s", query_string)


			# send off the request
			try:
				r = self.sendHTTPRequest(path, verb, query_string,myheaders).json()
			except:
				self.logger.error("HTTP error, returning 0")
				return 0
		else:
			self.logger.error("aok failed, return 0 in final else")
			return 0

		self.logger.info("successful, returning r")
		self.logger.debug("r is %s",r)
		
		return r

	def getSignature(self, secretKey, totalParams):
		#
		# ---- DESCRIPTION ---
		# Creates a signature for payloads as described in the 
		# Binance API documentation under the heading
		#	SIGNED Endpoint Examples for POST /api/v3/order
		# 
		# ---- INPUTS ---
		# secretKey: the secret key
		# totalParams:  the message we're wanting to hash. Per the documentation, 
		#
		#	totalParams is defined as the query string concatenated with the request body.
		#
		# ---- OUTUTS ---
		# hexdigest formatted HMAC SHA256 signature
		self.logger.info("signature is %s", hmac.new(secretKey, msg=totalParams, digestmod=hashlib.sha256).hexdigest())
		return hmac.new(secretKey, msg=totalParams, digestmod=hashlib.sha256).hexdigest()

	def getQueryString(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Assembles query parameters into a query string 
		# 
		# ---- INPUTS ---
		# validated (by validateParams) python dictionary of input parameters
		# 	ex.  {'symbol':'SALTBTC','limit':5} 
		# 
		#
		# ---- OUTUTS ---
		# HTTP query string
		# 
		# ---- NOTES ---
		queryString=''
		for key, value in queryParams.iteritems():
			if (type(value) == int):
				value = str(value)
			elif (type(value) == float):
				# remove scientific notation formatting in float, 8 characters of precision 
				value = '{:.8f}'.format(value)
				value = str(value)

			queryString = queryString + key + '=' + value + '&'	
			self.logger.debug("adding key and value to queryString %s %s", key, value)
		
		# we need to remove the final & here, hence [:-1]
		self.logger.debug("final queryString is %s", queryString[:-1])
		return queryString[:-1]

	def getTimestamp(self,queryParams={}):
		#
		# ---- DESCRIPTION ---
		# Check for and create a millisecond timestamp to include in SIGNED requests
		# 
		# ---- INPUTS ---
		# queryParams dictionary
		#
		# ---- OUTUTS ---
		# queryParams dictionary or 0 if there is an error
		# 
		if('timestamp' in queryParams):
			if ((len(str(queryParams['timestamp'])) == 13)):
				# strings actually fool this but it gets caught later in the type validation
				self.logger.info("found valid user provided timestamp %s",queryParams['timestamp'])
				return queryParams
			else:
				self.logger.error("user provided timestamp invalid %s",queryParams['timestamp'])
				return 0
				
		else:
			queryParams['timestamp'] = int(round(time.time() * 1000))
			self.logger.info("did not find user provided timestamp, generated %s",queryParams['timestamp'])

		return queryParams

	def testConnectivity(self):
		#
		# ---- DESCRIPTION ---
		# Checks the server connectivity with GET /api/v1/ping
		# 
		# ---- INPUTS ---
		# None:
		#
		# ---- OUTUTS ---
		# HTTP status code of the request to this URL
		# 
	
		path = '/api/v1/ping'
		verb = 'get'
		r = self.sendHTTPRequest(path, verb)
		self.logger.debug("HTTP response code to %s is %s", path, r)
		return r.status_code
		
	def getServerTime(self):
		#
		# ---- DESCRIPTION ---
		# Gets the server time with GET /api/v1/time
		# 
		# ---- INPUTS ---
		# None:
		#
		# ---- OUTUTS ---
		# The value in the serverTime attribute of the resulting json file
		# 
	
		path = '/api/v1/time'
		verb = 'get'
		r = self.sendHTTPRequest(path,verb).json()
		self.logger.debug("serverTime is  is %s", r['serverTime'])
		return r['serverTime']

	def getSymbols(self):
		#
		# ---- DESCRIPTION ---
		# Gets a list of valid symbols currently traded on Binance. This is
		# used as input validation for 'symbol' in most API calls
		# 
		# ---- INPUTS ---
		# none
		#
		# ---- OUTUTS ---
		# returns python list of current available symbols
		# 
		# ---- NOTES ---
		# They do not offer  an API function for this so we  use /api/v1/ticker/allPrices
		# to get a list of current prices for all assets and just extract the names
		# of the assets from there to check our symbol against
		path = '/api/v1/ticker/allPrices'
		verb = 'get'
		symbols = []
		try:
			r = self.sendHTTPRequest(path,verb).json()
		except:
			self.logger.error("HTTP error, returning 0")
			return 0

		for i in r:
			symbols.append(i['symbol'])

		self.logger.debug("symbols is %s", symbols)
		return symbols

	def validateParams(self,queryParams, expected):	
		# this is an internal function that validates parameters passed in against
		# the parameter specifications of the API
		# 
		# returns 1 if things are fine, 0 if not
		#
		if (not expected.empty):		# make sure expected has values in it
			for key, value in queryParams.iteritems():
				self.logger.debug("testing key %s",key)
				# mark all parameters in queryParams in expected['FOUND']
				if expected['NAME'].str.contains(key).any():
					a = expected.index[expected['NAME'].str.match(key)]
					expected.set_value(a,'FOUND',True)
				else:
					self.logger.error("key not found %s",key)
					return 0
				
				# Check the type.  Could be improved
				paramType = str(type(value)).split("\'")[1] # this extracts the string that is the type
				self.logger.debug("paramType calculated is %s",  paramType)
				self.logger.debug("comparison is to %s",  expected.iloc[a]['TYPE'].any())
				if(not paramType == expected.iloc[a]['TYPE'].any()):
					self.logger.error("type mismatch, return 0, %s %s %s", key, value, paramType)
					return 0

				else:
					self.logger.debug("no type mismatch, %s %s %s", key, value, paramType)

				# check if values exceed MAXIMUM, if provided
				if ('MAXIMUM' in expected.columns and expected.iloc[a]['MAXIMUM'].any()):
					if (queryParams[key] > expected.loc[expected['NAME'] == key,'MAXIMUM'].iloc[0]):
						self.logger.info("key %s exceeded MAXIMUM %s, return 0", key, str(int(expected.loc[expected['NAME'] == key,'MAXIMUM'].iloc[0])))
						return 0
				else:
					self.logger.debug("no maximum for %s", key)

				# see if expected['VALID'] is set. This indicates enum values, so we check these against the 
				# values passed in and return an error if the value is not in the enum
				#if (expected.iloc[a]['VALID'].any()):
				if ('VALID' in expected.columns and expected.iloc[a]['VALID'].any()):
					self.logger.debug("expected.iloc[a]['VALID'].any() is %s", expected.iloc[a]['VALID'].any())
					if(not value in expected.iloc[a]['VALID'].any()):
						self.logger.error("key %s with value %s  not found in %s, return 0", key, value, expected.iloc[a]['VALID'].any())
						return 0
				else:
					self.logger.debug("no enum for %s", key)


			# see if there are any cases expected['FOUND'] == False and expected['MANDATORY'] == True
			# this indicates that a required parameter was not found
			if (len(expected[(expected['FOUND'] == False) & (expected['MANDATORY'] == True)]) > 0):
				self.logger.error("mandatory columns missing return 0 %s", expected[(expected['FOUND'] == False) & (expected['MANDATORY'] == True)])
				return 0

			return 1
		else:	# if no values in expected, make sure queryParams is also empty
			if (any(queryParams)):
				# expected is empty but queryParams is not
				self.logger.error("expected is empty but queryParams contains unexpected values, return 0 ")
				return 0
			else:
				# both expected and queryParams are empty
				return 1

	
	def getOrderBook(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Gets the order book for a given asset with GET /api/v1/depth
		# 
		# ---- INPUTS ---
		# python dictionary of input parameters
		# 	ex.  {'symbol':'SALTBTC','limit':5} 
		# 
		#
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		# The documentation says limit <= 100 but seems to be at odds with how the system behaves. 
		# Trying various values resulted in an error message
		#		{"code":-1100,"msg":"Illegal characters found in parameter 'limit'; 
		#		legal range is '50, 20, 100, 500, 5, 200, 10'."}
		# No other values seem to work aside from the list above, so we value check the input for limit
		# to make sure it is in the legal range 


		# valid values
		enumSymbols = self.getSymbols()
		enumLimit = [5,10,20,50,100,200,500]

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'limit','TYPE':'int','MANDATORY':False,'DEFAULT':100,'FOUND':False,'MAXIMUM':500,'VALID':enumLimit}, ignore_index=True)


		# API specific inputs
		path = '/api/v1/depth'
		verb = 'get'
		
		return self.requestSender(path, verb, queryParams, expected)
	
		
	def getAggTrades(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Gets the compressed, aggregated trades from GET /api/v1/aggTrades
		# 
		# ---- INPUTS ---
		# python dictionary of input parameters
		# 	ex.  {'symbol':'SALTBTC','limit':5,'startTime':1507045646123,'endTime':1507045646456,'fromId':11234} 
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#
		# Limit uses 500 for values > 500 (i.e. if limit = 6000 then 500 rows are returned). Really large values 
		# return an error, so the logic in this function will set limit = 500 if the passed value exceeds 500
		#
		# The documentation specifies a type of LONG for fromId, startTime, and endTime.  Python evaluates a 13
		# digit number (such as an epoch time in ms) as an int, so the type we specify in expected is int for these.
		# This should keep floats or strings from sneaking by and we add some checks to make sure the values are reasonable.
		#

		# valid values
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'limit','TYPE':'int','MANDATORY':False,'DEFAULT':500,'FOUND':False,'MAXIMUM':500}, ignore_index=True)
		expected = expected.append({'NAME':'fromId','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'startTime','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'endTime','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		# API specific values
		path = '/api/v1/aggTrades'
		verb = 'get'

		# API specific checks for startTime, endTime, and limit
		# Per the documentation:  "If both startTime and endTime are sent, limit should not be sent 
		# AND the distance between startTime and endTime must be less than 24 hours."
		if (('startTime' in queryParams) and ('endTime' in queryParams)):
			if ((len(str(queryParams['startTime'])) == 13) and (len(str(queryParams['endTime'])) == 13)):
				if ((queryParams['endTime'] - queryParams['startTime'])	 < 1000*60*60*24):
					# remove limit if startTime and endTime are set, valid, and have appropriate range
					queryParams.pop('limit',None)
					self.logger.info("removed queryParams['limit'] due to presense of startTime and endTime")
				else:
					self.logger.error("difference betweeen startTime and endTime > 24 hours , return 0 ")
					return 0
			else:
				self.logger.error("startTime and/or endTime contain invalid values , return 0 ")
				return 0
		else:
			if('startTime' in queryParams):
				self.logger.error("startTime present, endTime missing , return 0 ")
				return 0
			elif('endTime' in queryParams):
				self.logger.error("endTime present, startTime missing , return 0 ")
				return 0
			else:
				self.logger.info ("both endTime and startTime missing , proceeding ")
				
							
		return self.requestSender(path, verb, queryParams, expected)

	def getKline(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Gets the kline intervals from GET /api/v1/kline
		# 
		# ---- INPUTS ---
		# python dictionary of input parameters
		# 	ex.  {'symbol':'SALTBTC','limit':5,'startTime':1507045646123,'endTime':1507045646456,'interval':'5m'} 
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#
		# pandas dataframe containing parameter definitions from Binance API documentation
		
		# valid values 
		enumSymbols = self.getSymbols()
		enumIntervals = ['1m','3m','5m','15m','30m','1h','2h','4h','6h' '8h','12h','1d','3d','1w','1M']
		
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'limit','TYPE':'int','MANDATORY':False,'DEFAULT':500,'FOUND':False,'MAXIMUM':500}, ignore_index=True)
		expected = expected.append({'NAME':'interval','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumIntervals}, ignore_index=True)
		expected = expected.append({'NAME':'startTime','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'endTime','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)

		# API specific values
		path = '/api/v1/klines'
		verb = 'get'

		# check time inputs
		# the documentation does not specifically mention time limit spacing, limit spacing as in other api calls
		# so just checking the basic length of timestamps.
		if (('startTime' in queryParams) and ('endTime' in queryParams)):
			if ((len(str(queryParams['startTime'])) != 13) or (len(str(queryParams['endTime'])) != 13)):
				self.logger.error("startTime or endTime contain invalid values, return 0 ")
				return 0
		else:
			if(('startTime' in queryParams) or ('endTime' in queryParams)):
				self.logger.error("startTime or endTime missing, return 0 ")
				return 0


		return self.requestSender(path, verb, queryParams, expected)

	def getTicker(self, tickerType, queryParams={}):
		#
		# ---- DESCRIPTION ---
		# Gets ticker outputs 
		#	- the 24 hour ticker for a specified asset with GET /api/v1/ticker/24hr
		#	- the current symbol and price for all assets with GET /api/v1/ticker/allPrices
		#	- the current book for all assets with GET /api/v1/ticker/allBookTickers
		# 
		# ---- INPUTS ---
		# All 3 API calls require a tickerType in ['24hr','allPrices','allBookTickers']
		# 
		# Additional input for symbol if tickerType is '24hr':
		# 	 - /api/v1/ticker/24hr: {'symbol':'SALTBTC'}
		#
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		# This consolidates 3 separate relatively simple API calls into a single method.  


		# pandas dataframe containing parameter definitions from Binance API documentation 
		expected = pd.DataFrame()

		if (tickerType == '24hr'):
			# valid values 
			enumSymbols = self.getSymbols()
			expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
			path = '/api/v1/ticker/24hr'
		elif (tickerType == 'allPrices'):
			path = '/api/v1/ticker/allPrices'
		elif (tickerType == 'allBookTickers'):
			path = '/api/v1/ticker/allBookTickers'
		else:
			# invalid tickerType
			self.logger.error("Invalid tickerType %s",tickerType)
			return 0
			
		# API specific inputs
		verb = 'get'

		return self.requestSender(path, verb, queryParams, expected)

	def createOrder(self, queryParams, testFlag=False):
		#
		# ---- DESCRIPTION ---
		# Creates an order as POST on /api/v3/order if testFlag not specified
		# or /api/v3/order/test if testFlag=True
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()
		enumSide = ['BUY','SELL']
		enumType = ['MARKET','LIMIT']
		enumTIF = ['GTC','IOC']

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'side','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSide}, ignore_index=True)
		expected = expected.append({'NAME':'type','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumType}, ignore_index=True)
		expected = expected.append({'NAME':'quantity','TYPE':'float','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'newClientOrderId','TYPE':'str','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'stopPrice','TYPE':'float','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'icebergQty','TYPE':'float','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
		# if it is a type=LIMIT order we have to send price and timeInForce or the Binance API sends back an error
		if (queryParams['type'] == 'LIMIT'):
			# add price and timeInForce to expected
			expected = expected.append({'NAME':'price','TYPE':'float','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
			expected = expected.append({'NAME':'timeInForce','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumTIF}, ignore_index=True)
		else:
			# it is a market order and we should not include price or timeInForce
			queryParams.pop('price',None)
			queryParams.pop('timeInForce',None)
	
		# API specific values
		verb = 'post'
		signed = True
		
		# set path based on wheter it is a test or not
		if (testFlag):
			# it is a test
			path = '/api/v3/order/test'
			# recvWindow is not specified for /api/v3/order but is for /api/v3/order/test
			expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
			
		else:
			# the real deal
			path = '/api/v3/order'

	


		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def queryOrder(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Queries an order as GET on /api/v3/order
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'orderId','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'origClientOrderId','TYPE':'str','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/order'
		verb = 'get'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def cancelOrder(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Cancels an order as DELETE on /api/v3/order
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'orderId','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'origClientOrderId','TYPE':'str','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'newClientOrderId','TYPE':'str','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/order'
		verb = 'delete'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def getOpenOrders(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Retrieves a list of open orders with GET on /api/v3/openOrders
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/openOrders'
		verb = 'get'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def getAllOrders(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Retrieves a list of orders with GET on /api/v3/allOrders
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'orderId','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'limit','TYPE':'int','MANDATORY':False,'DEFAULT':500,'FOUND':False,'MAXIMUM':500}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/allOrders'
		verb = 'get'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def getAccountInfo(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Retrieves account info with GET on /api/v3/account
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/account'
		verb = 'get'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0

	def getAccountTrades(self, queryParams):
		#
		# ---- DESCRIPTION ---
		# Retrieves account trade history info with GET on /api/v3/myTrades
		# 
		# ---- INPUTS ---
		# - python dictionary of input parameters (see documentation)
		# 
		# ---- OUTUTS ---
		# returns a json object as specified in the API documentation or 0 if there was a problem
		# 
		# ---- NOTES ---
		#

		# enum definitions from documentation
		enumSymbols = self.getSymbols()

		# pandas dataframe containing parameter definitions from Binance API documentation
		expected = pd.DataFrame()
		expected = expected.append({'NAME':'symbol','TYPE':'str','MANDATORY':True,'DEFAULT':'','FOUND':False,'VALID':enumSymbols}, ignore_index=True)
		expected = expected.append({'NAME':'limit','TYPE':'int','MANDATORY':False,'DEFAULT':500,'FOUND':False,'MAXIMUM':500}, ignore_index=True)
		expected = expected.append({'NAME':'fromId','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)

		expected = expected.append({'NAME':'recvWindow','TYPE':'int','MANDATORY':False,'DEFAULT':'','FOUND':False}, ignore_index=True)
		expected = expected.append({'NAME':'timestamp','TYPE':'int','MANDATORY':True,'DEFAULT':'','FOUND':False}, ignore_index=True)
	
		# API specific values
		path = '/api/v3/myTrades'
		verb = 'get'
		signed = True

		# orders require a current timestamp, generate one if it is not passed in
		queryParams = self.getTimestamp(queryParams)
		if (queryParams):
			# send the request
			return self.requestSender(path, verb, queryParams, expected, signed)
		else:
			return 0
