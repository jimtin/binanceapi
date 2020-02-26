from pathlib import Path
import pyfiglet # For a bit of fun :)
import json


# Get file path for keys
def main(filepath=""):
    # Create welcome banner for a bit of fun :)
    welcome_banner = pyfiglet.figlet_format("Welcome to Binancian Library")
    print(welcome_banner)
    #print("Getting filepath for Public and Secret keys. Note: DO NOT PUT KEYS DIRECTLY INTO CONSOLE")
    if filepath == "":
        filepath = input("Put filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    else:
        filepath = filepath

    # Use Path functionality to convert string into a filepath. Note this will allow the option to be cross platform
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    filepath = Path(filepath)
    # Open file
    f = open(filepath)
    keydatajson = f.read()
    keydata = json.loads(keydatajson)
    binancePublicKey = keydata['binance']['PublicKey']
    binanceSecretKey = keydata['binance']['SecretKey']
    PublicKey = binancePublicKey
    SecretKey = binanceSecretKey
    Keys = [PublicKey, SecretKey]
    print("Binance Keys Loaded")
    return keydata['binance']

    # todo: create a live query mode using the python 'blessed' library

# todo: figure out a way to encrypt the secret key in memory. Will probably need to change programming languages
