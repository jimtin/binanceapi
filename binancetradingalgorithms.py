import splunk_as_a_database
import json

# Trade Hypothesis 1: If price increases each hour over 2 hours, the next hour will see another price rise
# Trade Hypothesis 2: If price stops increasing hour over hour, I should sell as it will fall soon
# Considerations: Optimising this algorithm will take time, as I will have limited resources to trade ALL rising stocks
# Benchmark against: BTC, ETH, EOS and BNB


# Function to get the average price over time of a token
def gettokenpriceovertime(exchange, token, timeframe, FilePath):
    # Construct base query
    basequery = constructexchangesplunksearch(exchange, FilePath, timeframe)
    # Search splunk to get a list of unique tokens for that exchange
    # Each exchange deals with things a little differently so will need to construct searches based on the exchange
    # Have already validated the exchange in the constructexchangesplunksearch function, so proceed on assumption it is valid
    if exchange == "binance":
        # Use symbol to get token symbol
        # Confirm that token exists
        splunkquery = basequery + " | dedup symbol | table symbol"
        # The list search term will need to know how to search
        searchterm = "symbol"
    elif exchange == "coinbase":
        # Use base to get token
        # Confirm that token exists
        splunkquery = basequery + " | dedup base | table base"
        # The list search term will need to know how to search
        searchterm = "base"

    # Now search splunk
    tokenlist = splunk_as_a_database.querysplunk(splunkquery, FilePath)
    tokenexists = searchdict(tokenlist, searchterm, token)
    if tokenexists:
        print("Token exists")
        # Now build the splunk search to get the token value over time
        
    else:
        print("Token does not exist, try again")


# Function to construct initial splunk query
def constructexchangesplunksearch(exchange, FilePath, timeframe="24h"):
    # Ensure exchange is presented as a string
    exchange = str(exchange)
    # Ensure timeframe is presented as a string
    timeframe = str(timeframe)
    # Confirm that the exchange being requested exists
    exchangeinfo = splunk_as_a_database.querysplunk("search index=* | dedup exchange | table exchange", FilePath)
    exchangeexists = searchdict(exchangeinfo, 'exchange', exchange)
    if exchangeexists:
        print("Exchange selection valid, continuing")
        # The timeframe for splunk searches within searches can be found here: https://docs.splunk.com/Documentation/Splunk/8.0.2/Search/Specifytimemodifiersinyoursearch
        # For ease of use, will specify only 3 options for this search. 2 hours, 24 hours, 7 days
        # Using this information, construct the splunk search
        # Construct initial Splunk search
        splunksearch = "search index=* exchange=" + exchange
        # Now split based upon the input to timeframe
        if timeframe == "24h":
            splunksearch = splunksearch + " earliest=-24h latest=now"
        elif timeframe == "7d":
            splunksearch = splunksearch + " earliest=-7d latest=now"
        elif timeframe == "2h":
            splunksearch = splunksearch + " earliest=-2h latest=now"
        else:
            print("Incorrect value put in. Please use 2h, 24h or 7d")
            return "IncorrectValue"
        return splunksearch
    else:
        print("Exchange value selected not valid, re-enter and try again")


# Search for values in a dictionary
def searchdict(list, searchdictval, searchterm):
    for k in list:
        if k[searchdictval] == searchterm:
            return True
    return False

