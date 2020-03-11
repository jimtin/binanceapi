import splunk_as_a_database
import binancedatasearching
import pandas
import matplotlib.pyplot as pyplot

# Trade Hypothesis 1: If price increases each hour over 2 hours, the next hour will see another price rise
# Trade Hypothesis 2: If price stops increasing hour over hour, I should sell as it will fall soon
# Considerations: Optimising this algorithm will take time, as I will have limited resources to trade ALL rising stocks
# Benchmark against: BTC, ETH, EOS and BNB


# Function to get the average price over time of a token
def gettokenpriceovertime(exchange, token, timeframe, FilePath):

    # Search splunk to get a list of unique tokens for that exchange
    # Each exchange deals with things a little differently so will need to construct searches based on the exchange
    # Have already validated the exchange in the constructexchangesplunksearch function, so proceed on assumption it is valid
    # todo: expand this to be able to search an array / list of values
    if exchange == "binance":
        binancedatasearching.searchbinancedata(token, timeframe, FilePath)

    elif exchange == "coinbase":
        # Use base to get token
        # Confirm that token exists
        splunkquery = basequery + " | dedup base | table base"
        # The list search term will need to know how to search
        searchterm = "base"
    else:
        return False




        elif exchange == "coinbase":
            splunkquery = basequery + " base=" + token + " | table DateTime, amount, base"
        # Search splunk for the data

        # Return the result of the search

    else:
        print("Token does not exist, try again")
        return False





# Function to munge coinbase dataframe into one with all the right objects
def mungecoinbasedata(DataFrame):
    # Convert the DateTime fields
    DataFrame["DateTime"] = pandas.to_datetime(DataFrame["DateTime"])
    # Convert the amount to a float
    DataFrame["amount"] = pandas.to_numeric(DataFrame["amount"])
    # Convert the base to a string
    DataFrame["base"] = DataFrame["base"].astype('|S')
    return DataFrame


# Function to show get a line plot
# Assume: Pandas dataframe is the input
def coinbaselinegraph(DataFrame):
    # Sort the DataFrame according to dates
    df = DataFrame.sort_values('DateTime', ascending=True)
    df["DateTime"] = pandas.to_datetime(df["DateTime"])
    # Take the DataFrame and set up the plot
    df.plot(kind="line", x="DateTime", y="amount", color="red")
    pyplot.show()


# Get simple coinbase analysis of single token
def simplecoinbaseplot(token, timeframe, FilePath):
    # First get the data
    coinbasedata = gettokenpriceovertime("coinbase", token, timeframe, FilePath)
    # Convert into a dataframe
    df = getdataframe(coinbasedata)
    # Munge coinbase data
    mungeddata = mungecoinbasedata(df)
    # Plot simple line graph
    coinbaselinegraph(mungeddata)




