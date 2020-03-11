from pathlib import Path
import pyfiglet # For a bit of fun :)
import json
import binanceAPIlibrary
import splunk_as_a_database
from time import sleep
import datetime
import coinbaselibrary


# Get file path for keys
def main(BinanceFilepath="", SplunkSettings="", TimeWindow=60):
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to Binancian Library")
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

    # Load the settings into the file
    binancekeys = getbinancekeys(BinanceKeysFilePath)
    print("Binance Keys Loaded")
    splunksettings = splunk_as_a_database.getsplunksettings(SplunkSettingsFilepath)
    print("Splunk settings loaded")

    # Now start running the program
    print("Getting crypto prices")
    while 1:
        print("Getting Data")
        cryptopricemovementgathering(binancekeys, splunksettings)
        print("Waiting 120 seconds")
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


    # todo: create a live query mode using the python 'blessed' library

# todo: figure out a way to encrypt the secret key in memory. Will probably need to change programming languages
