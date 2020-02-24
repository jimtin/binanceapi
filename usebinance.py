from pathlib import Path
import pyfiglet # For a bit of fun :)
import json

# Create welcome banner for a bit of fun :)
welcome_banner = pyfiglet.figlet_format("Welcome to Binancian Library")
print(welcome_banner)

PublicKey = ""
SecretKey = ""

# Get file path for keys
# def getbinancekeys(filepath) todo: turn this into an actual function
print("Getting filepath for Public and Secret keys. Note: DO NOT PUT KEYS DIRECTLY INTO CONSOLE")
confirm = input("Confirm that file containing keys is in .json format (Y/N)")
if confirm == "Y":
    filepath = input("Put filepath here. Ensure that forward slashes (/) are used regardless of operating system")
    # turn input into string
    filepath = str(filepath)
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
    print("Binance Keys Loaded")
else:
    print("Create correct format then continue")
    exit(code=0)

# todo: create a way to store new keys

# todo: figure out a way to encrypt the secret key in memory
