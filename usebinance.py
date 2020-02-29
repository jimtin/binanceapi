from pathlib import Path
import pyfiglet # For a bit of fun :)
import json
import binancelibrary
import splunk_as_a_database
from time import sleep
import datetime
import coinbaselibrary


# Global Variables
SplunkSettingsFilepath = ""
BinanceKeysFilePath = ""


# Get file path for keys
def main(BinanceFilepath="", SplunkSettings=""):
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to Binancian Library")
    print(welcome_banner)

    # Get the filepaths for the settings
    # Use Path functionality to convert string into a filepath. Note this will allow the option to be cross platform
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    BinanceFilepath = input("Put Binance Settings filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    BinanceKeysFilePath = Path(BinanceFilepath)
    SplunkSettings = input("Put SplunkSettings Filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    SplunkSettingsFilepath = Path(SplunkSettings)

    binancekeys = getbinancekeys(BinanceKeysFilePath)
    print("Binance Keys Loaded")
    splunksettings = splunk_as_a_database.getsplunksettings(SplunkSettingsFilepath)
    print("Splunk settings loaded")
    print("Starting datagathering exercise")
    datagathering(binancekeys, splunksettings, 60)


# Function to start collecting data from binance for practice. Set to run each hour.
def datagathering(binanceKeys, splunkSettings, timewindow):
    #while 1:
    # First get data from binance
    print("Getting binance data " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    pricechangedata = binancelibrary.getpricechanges()
    # Now send binance data to splunk
    print("Sending binance data to Splunk")
    sendtosplunk(pricechangedata, "binance", splunkSettings)
    # Now get coinbase data
    print("Getting coinbase data " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    spotpricedata = coinbaselibrary.combinespotprices()
    print(spotpricedata)
    print("Sending coinbase data to splunk")
    sendtosplunk(spotpricedata, "coinbase", splunkSettings)
    print("Sleeping for an hour now")


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
