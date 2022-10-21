import json
import requests
import pygal

# Function to query API
# Sybmol will be provided by user input from its respective function
# I tested this function using test values and it does work 
# It will return ALL information from the last 20 years in JSON format 
# We can build a function to parse the information into a usable format after completing other modules

# Global variable for while loop
run = True

# Global variable for invalid selection input text
invalidInputText = "Invalid option! Enter the number of the option you want to select: "

# Global variables for function, output size, and API key parameters
outputSize = "full"
key = "DLEZPCELNFARX2UF"
    
# Function to to supply prompt and get user input
def userInput(prompt, inputText):
    # Prompt user
    print(prompt)
    # Get user input
    selection = input(inputText)
    # Return user input
    return selection

# Function to get user input for chart type
def chartSelection():
    # User input prompt variable
    prompt = "Select the chart you would like from the following options:\n1. Line Chart\n2. Bar Chart\n"
    # Input text variable
    inputText = "Enter the chart type (1, 2): "
    # Call userInput function
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while(selection != "1" or selection != "2"):
        selection = userInput("", invalidInputText)
    if(selection == "1"):
        return "line"
    elif(selection == "2"):
        return "bar"
    
# Function to get user input for time series selection
def timeSeries():
    # User input prompt variable
    prompt = "Select the Time Series of the chart you wan to generate:\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n"
    # Input Text variable 
    inputText = "Enter the time series option (1, 2, 3, 4): "
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while(selection != "1" or selection != "2" or selection != "3" or selection != "4"):
        selection = userInput("", invalidInputText)
    if(selection == "1"):
        return "TIME_SERIES_INTRADAY"
    if(selection == "2"):
        return "TIME_SERIES_DAILY"
    if(selection == "3"):
        return "TIME_SERIES_WEEKLY"
    if(selection == "4"):
        return "TIME_SERIES_MONTHLY"

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

# While loop to run program and allow for repetition
while(run == True):

    print("\nStock Data Visualizer")
    print("----------------------")

    # Ask the user for the stock symbol they would like to visualize
    user_symbol = input("Enter the stock symbol you are looking for: ")
    print()
    
    # Call function for chart selection and assign value ("line" or "bar")
    # This value will be used to open the correct chart in the browser
    chartOption = chartSelection()
    
    # Call function for time series selection and assign value
    functionType = timeSeries()
    
    # Pass the symbol to the queryAPI function
    # this will not be necessary down the road because everything will be passed at once
    queryAPI(functionType, user_symbol, outputSize, key)

    # Check if the user would like to visualize another stock
    user_continue = input("Would you like to view more stock data? Press 'y' to continue: ")
    if(user_continue == "y"):
        # Repeat program by iterating through while loop again
        run = True
    else:
        # End program
        run = False