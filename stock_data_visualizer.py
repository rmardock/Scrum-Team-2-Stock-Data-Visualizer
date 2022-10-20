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

while(True):

    print("\nStock Data Visualizer")
    print("----------------------")

    # Ask the user for the stock symbol they would like to visualize
    user_symbol = input("Enter the stock symbol you are looking for: ")
    print()
    # Pass the symbol to the queryAPI function
    # this will not be necessary down the road because everything will be passed at once
    queryAPI(functionType, user_symbol, outputSize, key)

    # Check if the user would like to visualize another stock
    user_continue = input("Would you like to view more stock data? Press 'y' to continue: ")
    if(user_continue == "y"):
        continue
    else:
        break