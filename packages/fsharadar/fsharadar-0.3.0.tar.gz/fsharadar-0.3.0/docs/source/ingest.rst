========================
Ingesting Sharadar Files
========================

Before being processed within the Zipline pipeline, a new data set needs to be
preliminarily ingested into a data bundle of the Zipline data layer. Each data
bundle is located in a dedicated folder having
a common structure consisting of the `SQLite <https://www.sqlite.org/index.html>`_
database and a collection of `bcolz <https://github.com/Blosc/bcolz>`_ data files.

The following code snippets illustrate the user interface implemented by the fsharadar
module for ingesting `Sharadar <https://www.quandl.com/publishers/SHARADAR>`_
Equity Prices (SEP)  and Daily
Metrics of Core US Fundamental Data.
In accordance to the Zipline
approach, the interface is defined via the method *ingest()*.  Contrary to Zipline, the signature
of this method is bundle-specific and includes additional arguments for specifying names
of the Sharadar csv files. 


Ingesting US Equity Prices
--------------------------

The Sharadar data collection with US Equity Prices consists of three files: Tickers,
SEP and Actions.
The Tickers file contains the asset identifier, ticker name, and additional
metadata, such as asset category (e.g. Common Domestic Stock). The SEP file provides
the split-adjusted open, high, low, close, (OHLC) end-of-day prices and volumes. Finally,
Actions adds information about splits and dividends. All these files are processed
together for producing and storing the corresponding data bundle *flounder-sharadar-sep*
with computed unadjusted prices.

.. code-block:: python

    from fsharadar import sep

    sharadar_tickers_file = "./SHARADAR_TICKERS.csv"
    sharadar_sep_file = "./SHARADAR_SEP.csv"
    sharadar_actions_file = "./SHARADAR_ACTIONS.csv"   

    try:
        sep.ingest(tickers_file=sharadar_tickers_file,
                   data_file=sharadar_sep_file,
                   actions_file=sharadar_actions_file)
    except Exception as e:
        print('error:', e)
    

Ingesting Daily Metrics of Core US Fundamental Data
---------------------------------------------------

Sharadar Daily Metrics contains a daily set of six charachteristics:
enterprise value (ev), enterprise value over EBIT (evebit), enterprise
value over EBITDA (evebitda), market capitalization (marketcap),
price to book value (pb), price earnings (pe), and price sales (ps).
Based on the FSharadar extension, they are maintained as
the *flounder-sharadar-daily* data bundle and can be ingested and subsequently
loaded into the Zipline pipeline with the *fsharadar.daily* module. 


.. code-block:: python

    from fsharadar import daily		

    sharadar_tickers_file = "./SHARADAR_TICKERS.csv"
    sharadar_daily_file = "./SHARADAR_DAILY.csv"

    try:
        daily.ingest(tickers_file=sharadar_tickers_file,
                     data_file=sharadar_daily_file)
    except Exception as e:
        print(e)
