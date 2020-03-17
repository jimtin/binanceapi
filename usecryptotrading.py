from pathlib import Path
import pyfiglet # For a bit of fun :)
import json
from binance import binanceAPIlibrary
import splunk_as_a_database
from time import sleep
import datetime
from coinbase import coinbaselibrary
from coinbase import coinbasedatasearching
from binance import binancedatasearching
import pandas


# Declare the Global Variables needed
Exchanges = pandas.DataFrame()
CoinbaseTokens = pandas.DataFrame()
BinanceTokens = pandas.DataFrame()
SplunkSettings = ""
BinanceFilepath = ""


# Get file path for keys
def main(BinanceFilepath="", SplunkSettings="", TimeWindow=60):
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to CryptoTrading Library")
    print(welcome_banner)

    # Setup the filepaths for getting settings
    # First: Get Binance keys
    if BinanceFilepath == "":
        print("No value supplied for Binance keys, please input values below")
        BinanceFilepath = input("Put Binance Settings filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    # Else statement just to ensure everything is captured
    else:
        BinanceFilepath = BinanceFilepath
    # Now turn into a Path variable using Path library. This allows it to be platform agnostic
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    BinanceKeysFilePath = Path(BinanceFilepath)

    # Second: Get Splunk settings
    if SplunkSettings == "":
        print("No value supplied for Splunk settings, please input values below")
        SplunkSettings = input("Put SplunkSettings Filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    # Else statement just to ensure everything is captured
    else:
        SplunkSettings = SplunkSettings
    # Now turn into a Path variable using Path library. This allows it to be platform agnostic
    SplunkSettingsFilepath = Path(SplunkSettings)

    # Load the settings from the file into memory
    binancekeys = getbinancekeys(BinanceKeysFilePath)
    print("Binance Keys Loaded")
    splunksettings = splunk_as_a_database.getsplunksettings(SplunkSettingsFilepath)
    print("Splunk settings loaded")

    # Get a Splunk Session key
    print("Getting Splunk Session Key")
    sessionkey = splunk_as_a_database.getsplunksessionkey(SplunkSettings)
    print("SessionKey: " + str(sessionkey))

    # Load list of exchanges available, save to global variables
    print("Getting a list of exchanges")
    exchangeinfo = splunk_as_a_database.querysplunk("search index=* | dedup exchange | table exchange", SplunkSettings, sessionkey)
    # Turn exchange info into a DataFrame
    global Exchanges
    Exchanges = pandas.DataFrame(exchangeinfo)
    # Print out list of available exchanges
    print("Available exchanges:")
    print(Exchanges["exchange"])

    # Load options from each exchange being saved to speed up future searching
    # Now get coinbase options, save to global variable
    print("Loading Coinbase exchange tokens available")
    coinbasetokens = coinbasedatasearching.getlistofcoinbasetokens("24h", SplunkSettings)
    global CoinbaseTokens
    CoinbaseTokens = pandas.DataFrame(coinbasetokens)
    # Advise user of the options available
    print("Available Coinbase tokens:")
    print(CoinbaseTokens)

    # Now get binance token list
    print("Loading available Binance tokens")
    binancetokens = binancedatasearching.getlistofbinancetokens("24h", SplunkSettings, sessionkey)
    global BinanceTokens
    BinanceTokens = pandas.DataFrame(binancetokens)
    # Advise user of options available
    print("Available Binance tokens:")
    print(BinanceTokens)

    usetoken = False
    available = []
    while usetoken != True:
        whichtoken = input("Input which token to search for")
        available = tokenselection(whichtoken)
        print(available)
        if len(available) > 0:
            print("We can use this")
            usetoken = True
        else:
            print("Not token by this name :(")
            usetoken = False

    # Get a dataframe of all the data for the token which we currently have
    # tokendata = coinbasedatasearching.searchcoinbasedata(usetoken, timeframe="24h", SplunkSettings)

    # Now start running the program
    print("Getting crypto prices")
    while 1:
        print("Getting Data")
        cryptopricemovementgathering(binancekeys, splunksettings)
        print("Waiting 1200 seconds")
        sleep(120)


# Function to start collecting data from binance for practice. Set to run each hour.
def cryptopricemovementgathering(binanceKeys, splunkSettings):
    print("Getting binance data " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    pricechangedata = binanceAPIlibrary.getpricechanges()
    # Now send binance data to splunk
    print("Sending binance data to Splunk")
    sendtosplunk(pricechangedata, "binance", splunkSettings)
    # Now get coinbase data
    print("Getting coinbase data " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    spotpricedata = coinbaselibrary.combinespotprices()
    print("Sending coinbase data to splunk")
    sendtosplunk(spotpricedata, "coinbase", splunkSettings)


# Function to get binance keys from the BinanceFilePath
def getbinancekeys(filepath):
    # Open the Binance Keys filepath
    f = open(filepath)
    # Format of the data will be json, so convert
    keydatajson = f.read()
    keydata = json.loads(keydatajson)
    # Create a dict with the keys
    Keys = keydata['binance']
    return Keys


# Function to send data to Splunk and include the exchange it is from
def sendtosplunk(data, exchange, splunksettings):
    # Ensure the exchange is a string
    exchange = str(exchange)
    # Iterate through the data provided, adding in the exchange
    for crypto in data:
        # Add in the exchange
        # print(crypto)
        crypto.update({'exchange': exchange})
        crypto.update({'DateTime': str(datetime.datetime.now())})
        # Turn into json
        exchangedata = json.dumps(crypto)
        # Serialize the crypto object into a string
        exchangedata = str(exchangedata)
        # Now send joyfully to Splunk
        splunk_as_a_database.splunkudpsender(exchangedata, splunksettings)

# Function to select which exchange and token to search
def tokenselection(token):
    # Declare the global variables being used
    global CoinbaseTokens
    global BinanceTokens
    # Setup a list of exchanges available in
    exchangesavailable = []
    # Check if element exists in Coinbase
    if token in CoinbaseTokens.values:
        print("Found in Coinbase")
        exchangesavailable.append("coinbase")
    else:
        print("Not found in Coinbase")

    # Check if element exists in Binance
    if token in BinanceTokens.values:
        print("Found in Binance")
        exchangesavailable.append("binance")
    else:
        print("Not found in Binance")

    return exchangesavailable
