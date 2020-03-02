import socket
from pathlib import Path
import json
from time import sleep
import xmltodict
import requests
from requests.auth import HTTPBasicAuth

# Use Splunks REST API as a database

# FilePath = input("Input FilePath for Splunk settings")

# Put the data from Binance into a database for future post processing
# Create a simple UDP sender. There is nothing secret about the data, so sending in the clear is fine
def splunkudpsender(datatosend, splunksettings):
    # First, import splunk settings
    SplunkIP = splunksettings["SplunkIP"]
    SplunkPort = int(splunksettings["SplunkPort"])
    # Now convert the message to bytes
    MESSAGE = str.encode(datatosend)
    # Set up the socket to send (btw, how good is python)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Send datagram (UDP)
    sock.sendto(MESSAGE, (SplunkIP, SplunkPort))
    sock.close()
    sleep(0.01)


# Retrieve data from database


# Get splunk settings so I know where to send data
def getsplunksettings(FilePath):
    FilePath = str(FilePath)
    filepath = Path(FilePath)
    f = open(filepath)
    splunksettingsjson = f.read()
    splunksettings = json.loads(splunksettingsjson)
    return splunksettings["SplunkSettings"]


# Query Splunk to get information
def querysplunk(SearchQuery, FilePath):
    # Ensure that SearchQuery is a string
    SearchQuery = str(SearchQuery)
    # Get splunk settings
    splunksettings = getsplunksettings(FilePath)
    # Set up base API
    apirequest = splunksettings["BaseURL"] + "/services/search/jobs/"
    # Get the session key
    sessionkey = getsplunksessionkey(FilePath)
    data = {
        "search": SearchQuery
    }
    session = requests.session()
    session.headers.update({"Content-Type": "application/json"})
    session.headers.update({'Authorization': 'Splunk ' + sessionkey})
    information = session.post(apirequest, data=data, verify=False)
    # The information returned is in xml, and I really just want the sessionkey, so convert
    information = xmltodict.parse(information.text)
    sid = information['response']['sid']
    # Now get the search status
    apirequest = apirequest + "/" + sid
    information = session.post(apirequest, data=data, verify=False)
    print(information.text)
    # If the splunk search status is not done, wait 5 seconds then try again
    sleep(5)
    information = session.post(apirequest, data=data, verify=False)
    print(information.text)
    # todo: now that this is working will need to split out results etc 



# Query Splunk to get any messages
def getsplunkmessages(FilePath):
    # Set up the api query
    apirequest = "https://localhost:8089/services/messages"
    # Get Splunk Settings
    splunksettings = getsplunksettings(FilePath)
    # Set up the session
    session = requests.session()
    information = requests.get(apirequest, auth=HTTPBasicAuth(str(splunksettings["UserName"]), str(splunksettings["Password"])), verify=False)
    return information.text


# Query Splunk to get a session key, this can be used to secure comms afterwards
def getsplunksessionkey(FilePath):
    # Get Splunk Settings
    splunksettings = getsplunksettings(FilePath)
    # Set up the api query
    apirequest = "https://localhost:8089/services/auth/login"
    # The Splunk REST API requires the username and password to be URL encoded. However, Python Requests does this when it's turned into a dictionary
    session = requests.session()
    data={"username": splunksettings["UserName"], "password":splunksettings["Password"]}
    information = session.get(apirequest, data=data, verify=False)
    # The data returned is in xml format, so convert into a dictionary
    information = xmltodict.parse(information.text)
    return information['response']['sessionKey']
