# binanceapi
Library for interacting with Binance APIs (REST and wapi)

# Usage
## Getting a Binance API Key
Information can be found here: https://www.binance.com/en/support/articles/360002502072

**Note: do not share your secret key unless you know exactly what you are doing**
**Note: Make sure you only store your public and private keys somewhere safe and secure**

## Initial usage
### All the Keys
The binance keys need to be in a .json format. This allows the binance API library to read the keys and keep them in memory
The format should be as follows:
{
    "binance":{
        "PublicKey": "YourPublicKeyHere",
        "SecretKey": "YourSecretKeyHere"
    }
}
It is recommended that you create this file without going through the console as this will prevent your keys from ending up in bash history etc.

### Start the program
Make sure you have Python version 3.7 `python -v` or `python --version`
Load usebinance into python console: `import usebinance`
Follow the prompts, inputting your file path. Note that using the Python 3 Path library enables you to put in the file path using forward slashes (/) then python converts it to the relevant Operating System.


