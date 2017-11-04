# pyBinance
Python based class and utilities for using the Binance Crytpocurrency Exchange


--- Overview ---

Implementation of the functionality for Public API and Account Endpoints described at
https://www.binance.com/restapipub.html#user-content-public-api-endpoints

Heavy emphasis on checking and validating inputs.   My approach here was to create a pandas dataframe for each 
API path exposed by Binance containing the type, value, enum, maximums, and other constraints for input parameters.  
The values passed into the API call are checked against this definition via the validateParams method for each 
call to avoid unnecessary sending of requests.   Extensive use of python logging to help with diagnostics. 

To keep things simple, most methods just take a python dictionary (I called it queryParams in most of the 
examples and test scripts but the name doesn't matter) as their only argument. The keys in this dictionary 
correspond to the inputs specified in the Binance API documentation (symbol, quantity, price, timestamp, etc).  
The intent here was to make it possible to refer primarily to the Binance API documentation for specifying inputs
for API calls.  Passing them in a dictionary makes the order they are specified in unimportant.

Each method is documented fairly well in Binance.py.  I also wrote documentation for each method on the wiki. 

Test scripts for each major method can be found in the tests/ directory. A few for helper methods are there as well.

Example scripts for select use cases can be found in the examples/ directory


--- Installation ---

1) Clone repository
2) Make sure you have pandas installed (i.e. pip install pandas)
3) Run various tests scripts (or all of them) in tests/ .   logging.ini is configured for INFO to stdout and DEBUG to binance.log for these test scripts.   
4) Obtain valid secret and api key values from Binance.  The ones in use in the test-<method>.py scripts are the examples from Binance's API documentation so result in invalid key errors for any requests that require key and signature.
5) Look at the examples in the examples/ directory to get some ideas of how to use the module.  You can configure config.ini in this directory with your apikey and secret (obtained in #4 above) to actually start building your own applications.
  


--- Versions ---

-----  v0.1.1 ----------

Initial release

-----  v0.1.2 ----------

Fixed a few bugs and rejiggered some logic
- Fixed checks for secret and apikey so that public API calls did not have to provide keys
- Wrong path for signed APIs (I had v1 in the path instead of v3)
- Consolidated /api/v3/order and /api/v3/order/test into single method createOrder with a test flag as the 2nd argument
- Fixed issue with small floating point numbers being converted to scientific notation.  getQueryString now converts them
	back to float with 8 point precision, which seems to be the max precision on Binance
- Undocumented constraint on Binance is that an order of type=MARKET cannot contain a price or timeInForce.  Fixed this 
	by only adding price and timeInForce when type=LIMIT in createOrder


