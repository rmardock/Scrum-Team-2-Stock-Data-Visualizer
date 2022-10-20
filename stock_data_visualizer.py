import json
import requests

# Function to query API
# Sybmol will be provided by user input from its respective function
# I tested this function using test values and it does work 
# It will return ALL information from the last 20 years in JSON format 
# We can build a function to parse the information into a usable format after completing other modules

# Global variables for function, output size, and API key parameters
functionType = "TIME_SERIES_DAILY"
outputSize = "full"
key = "DLEZPCELNFARX2UF"

# Function to get data from the API
def queryAPI(functionType, symbol, outputSize, key):
    # URL construction for API request
    url = "https://www.alphavantage.co/query?function=" + functionType + "&symbol=" + symbol + "&outputsize=" + outputSize + "&apikey=" + key
    # Query API
    response = requests.request("GET", url)
    # Format data as JSON object
    data = response.json()
    # Return data
    return data
