
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

## Oanda-first<br>
This folder contains a means to look at past FOREX prices, and compare them.  

###Functions in OHLC.py 
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
### Function in GrabAll.py  
GrabAllCandles() grabs different prices at a time from 'EUR' currency  
Returns only instru and ask close as numpy arrays.

```
GrabAll()
```  

### Function in NormCur.py  
NormCur() requires Bid close (s for scale and n for normalize).  
This is an ad hoc way to scale Currencies with vastly different prices to be "on top" on one another.  
Returns normalized or scaled prices as numpy array.


```
NormCur(BCn, BCs)
```
Now use matplotlib.pyplot to plot simple line graphs to see if you plot the same data as Oanda shows in their downloadable app.  
This will show you are connecting with their API correctly.  

## Oanda-Event<br>  
This folder contains event driven software to stream live tick feed data.  
There has been plenty learned from (Oanda-first) which is to be implemented in the Backtest folder. 

### enivro.py
The python file one would edit when switching from demo mode (monopoly money) to a live brokerage account, see more at Oandas API website. There are two functions to either GrabToken() or GrabID() which will grab the users info from the res folder (needs to be edited with ones own API key from [Oanda](https://developer.oanda.com/rest-live-v20/introduction/)

### events.py
A simple python script only has two classes since this is a very simple event driven progrom with only two events. The first event is TickEvent class and the other is OrderEvent class. When ever new OHLC data is downloaded, from steam.py, this new data will be queued as a new event for the program. The other type of event is OrderEvent which happens when ever strategy.py script conditions are met.

### strategytest.py
This is the brains of the program and unfortuntely only has a very simple script as this event driven python program will not produce a profit, this is for educational purposes only!

### steam.py
This file is used to request an http session with [Oanda](https://developer.oanda.com/rest-live-v20/account-ep/) endpoints.

### trading.py
The heart of the program will be executed with this script. All events processed with this file and functions are imported, from files above, to download and execute trades on a live demo account (can be upgraded to a live brokerage account but this is outside the scope of this repo). 
 
### Backtest folder 
#### Functions in downloadOHLC.py  
GrabHistoryPrice() is a class that requires 4 parameters to initialize and one optional parameter.  
Returns one HTTP response.  

```
GrabHistoryPrice(domain, token, instru, gran, count=500)
```

##### Methods for this class
requestHistStream() is a method that begins an http connection to the endpoint /v3/instruments/ from Oanda's API. This method is never called directly. All other methods in this class build of this one.

```
requestHistStream()
```

downloadSingle() is a method that downloads the single FOREX instrument data in JSON format.

```
downloadSingle()
```

downloadAll() is a method that downloads the all FOREX instruments data in JSON format. The FOREX instruments included are in list found in this method. One can find more about these endpoints [here](https://developer.oanda.com/rest-live-v20/instrument-ep/).

```
downloadAll()
```
#### enviroB.py  
This is the python file one would edit when switching from demo mode (monopoly money) to a live brokerage account, see more at Oandas API website. There are two functions to either GrabToken() or GrabID() which will grab the users info from the res folder (needs to be edited with ones own API key from [Oanda](https://developer.oanda.com/rest-live-v20/introduction/)

#### plotOHLC.py 
This file has one class to plot OHLC data to visually inspect the data.
plotOHLC() has two arugments, the first one is the primary currency and the second is the granularity of the data (ie 5 second candles, 10 minute, 1 days, etc).

`
plotOHLC(primarycur, gran=None)
`

## <br>
**Please note**
A live tick stream has been developed based on [Quant Start](https://www.quantstart.com/articles/Forex-Trading-Diary-1-Automated-Forex-Trading-with-the-OANDA-API) tutorial on an event driven software to control an automatted trading platform. **WARNING** FOR EDUCATIONAL PURPOSES ONLY.

This code will require folder called res in parent directory (this folder). The res folder will need to have a ids.json file for ID and an oanda_api_key.json file for API token issued by Oanda (example json files in res folder). Token and ID Key can be obtained for free from Oanda.
