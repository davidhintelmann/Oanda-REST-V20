
# Oanda REST API example

This folder has two small apps developed for interfacing with [Oandas](http://developer.oanda.com) REST API.
 Specifically using Oandas V-20 REST API.  
 
Oanda-first only has downloading historical data prices for 'EUR_USD' FOREX prices, and scaling two different currencies.  
While Oanda-Event is an intro to an event driven software for streaming live prices from Oanda
as well building on what was learned from Oanda-first to begin data collection for backtesting.
Inspiration for the event driven software written in python comes from [Quant Start](https://www.quantstart.com/articles/Forex-Trading-Diary-1-Automated-Forex-Trading-with-the-OANDA-API).  
**Warning, this is for educational purposes only.**

Dependencies       	| Version          |
--------------------|------------------|
Python 				| 3.6.4   		  	|
glob2			       | 0.5     	      |
matplotlib 			| 2.1.0			  	|
numpy 					| 1.13.3 				|
pandas 				| 0.22.0   			| 

**Oanda-first**<br>
This folder contains a means to look at past FOREX prices, and compare them.
**Functions in OHLC.py**  
GrabToken() will grab users API token from res folder.  
Returns token as string.  

```
GrabToken(path=token_path)
```
GrabCandles() requires 6 parameters and returns 12 values.  
Parameter gran is granularity or frequency of tick data (OHLC data).   
Returns instru, time, volume, bid OHLCs, ask OHLCs, ticks as numpy arrays. 

```
GrabCandles(token, instru, start, gran, based, count=1000)
```
**Function in GrabAll.py**  
GrabAllCandles() grabs different prices at a time from 'EUR' currency  
Returns only instru and ask close as numpy arrays.

```
GrabAll()
```  

**Function in NormCur.py**  
NormCur() requires Bid close (s for scale and n for normalize).  
This is an ad hoc way to scale Currencies with vastly different prices to be "on top" on one another.  
Returns normalized or scaled prices as numpy array.


```
NormCur(BCn, BCs)
```
Now use matplotlib.pyplot to plot simple line graphs to see if you plot the same data as Oanda shows in their downloadable app.  
This will show you are connecting with their API correctly.  

**Oanda-Event**<br>  
This folder contains event driven software to stream live tick feed data.  
There is plently learned from the previous folder (Oanda-first) which is planned to be implemented here found in Backtest folder.  
**Functions in Backtest folder**  
**Functions downloadOHLC.py**  
GrabHistoryPrice() requires 4 parameters to initialize with one optional parameter.  
Returns one HTTP response.  

```
GrabHistoryPrice(domain, token, instru, gran, count=500)
```

**Please note**
This code will require folder called res in parent directory (parent to this folder). The res folder will need to have a ids.json file for ID and an oanda_api_key.json file for API token issued by Oanda (example json files in res folder). Token and ID Key can be obtained for free from Oanda.
