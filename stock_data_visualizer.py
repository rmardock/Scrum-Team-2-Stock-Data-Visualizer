import json
import requests
import pygal
import datetime

# Global variable for while loop
run = True


# Function to to supply prompt and get user input
def userInput(prompt, inputText):
    # Prompt user
    print(prompt)
    # Get user input
    selection = input(inputText)
    # Return user input
    return selection

# Function to get user input for dates
def userInputDates(inputText):
    # Get user input from dates function
    selection = input(inputText)
    # Return user input
    return selection

# Function to get user input for chart type
def chartSelection(invalidInputText):
    # User input prompt variable
    prompt = "Select the chart you would like from the following options:\n1. Line Chart\n2. Bar Chart\n"
    # Input text variable
    inputText = "Enter the chart type (1, 2): "
    # Call userInput function
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while (selection != "1" and selection != "2"):
        selection = userInput("", invalidInputText)
    if (selection == "1"):
        return "line"
    elif (selection == "2"):
        return "bar"


# Function to get user input for time series selection
def timeSeries(invalidInputText):
    # User input prompt variable
    prompt = "Select the Time Series of the chart you wan to generate:\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n"
    # Input Text variable
    inputText = "Enter the time series option (1, 2, 3, 4): "
    selection = userInput(prompt, inputText)
    # If user selection is not a given option, prompt user to try again
    while (selection != "1" and selection != "2" and selection != "3" and selection != "4"):
        selection = userInput("", invalidInputText)
    if (selection == "1"):
        return "TIME_SERIES_INTRADAY"
    if (selection == "2"):
        return "TIME_SERIES_DAILY"
    if (selection == "3"):
        return "TIME_SERIES_WEEKLY"
    if (selection == "4"):
        return "TIME_SERIES_MONTHLY"

# Function to get user input for start date
def startDate():
    date_format = '%Y-%m-%d'
    inputText = "Enter the start Date (YYYY-MM-DD): "
    selection = userInputDates(inputText)
    # using try-except blocks for handling the exceptions
    while True:
        try:
            # formatting the date using strptime() function
            dateObject = datetime.datetime.strptime(selection, date_format)
            # formatting the dateObject to exclude time
            dateObjectWithoutTime = dateObject.strftime(date_format)
            print(dateObjectWithoutTime)
            # If the date validation goes wrong
        except ValueError:
            # printing the appropriate text if ValueError occurs
            print("Incorrect date format. Enter the start Date in YYYY-MM-DD format: ")
            selection = userInputDates(inputText)
        else:
            #No error, break loop
            break
    return dateObjectWithoutTime

# Function to get user input for end date
def endDate():
    date_format = '%Y-%m-%d'
    inputText = "Enter the end Date (YYYY-MM-DD): "
    selection = userInputDates(inputText)
    # using try-except blocks for handling the exceptions
    while True:
        try:
            # formatting the date using strptime() function
            dateObject = datetime.datetime.strptime(selection, date_format)
            # formatting the dateObject to exclude time
            dateObjectWithoutTime = dateObject.strftime(date_format)
            print(dateObjectWithoutTime)
            # If the date validation goes wrong
        except ValueError:
            # printing the appropriate text if ValueError occurs
            print("Incorrect date format. Enter the end Date in YYYY-MM-DD format: ")
            selection = userInputDates(inputText)
        else:
            # No error, break loop
            break
    return dateObjectWithoutTime

# Function to parse data
# We will need to replace the second column ["2022-10-20"] with a variable stemming from date selection functions
def parseData(data, timeSeries):
    open = data[timeSeries]["2022-10-20"]["1. open"]
    high = data[timeSeries]["2022-10-20"]["2. high"]
    low = data[timeSeries]["2022-10-20"]["3. low"]
    close = data[timeSeries]["2022-10-20"]["4. close"]
    return open, high, low, close


# Function to assign time series for JSON
def jsonTime(timeOption):
    if (timeOption == "TIME_SERIES_INTRADAY"):
        return "Time Series (5min)"
    elif (timeOption == "TIME_SERIES_DAILY"):
        return "Time Series (Daily)"
    elif (timeOption == "TIME_SERIES_WEEKLY"):
        return "Weekly Time Series"
    elif (timeOption == "TIME_SERIES_MONTHLY"):
        return "Monthly Time Series"


# Function to index data into dictionary
def indexData(data, timeSeries):
    # Variable for iterating dictionary
    i = 0
    # Dictionary for indexing data
    graphData = {
        "open": {},
        "high": {},
        "low": {},
        "close": {}
    }
    # Iterates data and indexes it in dictionary
    for dates in data[timeSeries]:
        open, high, low, close = parseData(data, timeSeries)
        graphData["open"][i] = open
        graphData["high"][i] = high
        graphData["low"][i] = low
        graphData["close"][i] = close
        i += 1
    return graphData


# Function to build chart
def buildChart(graphData, chartType, data, timeSeries):
    # Variable for iterating dictionary
    i = 0
    # List for adding values to graphs
    list = []
    # If line chart is selected
    if (chartType == "line"):
        # Create line chart
        lineChart = pygal.Line()
        # For all data entries, iterate and add to list
        for dates in data[timeSeries]:
            list.append(float(graphData["open"][i]))
            i += 1
        # Add elements to graph
        lineChart.add("Open", list)
        # Render graph in browser
        lineChart.render_in_browser()
    # If bar chart is selected
    if (chartType == "bar"):
        # Create bar chart
        barChart = pygal.Bar()
        # For all data entries, iterate and add to list
        for dates in data[timeSeries]:
            list.append(float(graphData["open"][i]))
            i += 1
        # Add elements to graph
        barChart.add("Open", list)
        # Render graph in browser
        barChart.render_in_browser()
    # Error handling
    elif (chartType != "line" and chartType != "bar"):
        # Error message
        print("ERROR")


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
while (run == True):
    # Variable for invalid selection input text
    invalidInputText = "Invalid option! Enter the number of the option you want to select: "
    invalidInputDatesFormat = "Invalid date! Enter the date in YYYY-MM-DD format:  "
    # Variables for output size and API key parameters
    outputSize = "full"
    key = "DLEZPCELNFARX2UF"

    print("\nStock Data Visualizer")
    print("----------------------")

    # Ask the user for the stock symbol they would like to visualize
    user_symbol = input("Enter the stock symbol you are looking for: ")
    print()

    # Call function for chart selection and assign value ("line" or "bar")
    # This value will be used to open the correct chart in the browser
    chartOption = chartSelection(invalidInputText)

    # Call function for time series selection and assign value
    functionType = timeSeries(invalidInputText)

    # Call function for start date
    startTime = startDate()

    # Call function for end date
    endTime = endDate()

    # Checks to see if start time value is after endtime and resets if true
    while (startTime >= endTime):
        print("Start date cannot be later than or equal to End date. Enter the dates again.")
        startTime = startDate()
        endTime = endDate()

    # Assign correct format for JSON based on user selection
    jTime = jsonTime(functionType)

    # Pass the symbol to the queryAPI function
    data = queryAPI(functionType, user_symbol, outputSize, key)
    # Call function to parse and index data for graph
    # ***Uncomment after time selection functions are completed***
    #graphData = indexData(data, jTime)
    # Builds chart and opens it in browser
    # ***Uncomment after time selection functions are completed***
    #buildChart(graphData, chartOption, data, jTime)
    # Check if the user would like to visualize another stock
    user_continue = input("Would you like to view more stock data? Press 'y' to continue: ")
    if (user_continue == "y"):
        # Repeat program by iterating through while loop again
        run = True
        # Empty dictionary
        dict = {}
    else:
        # End program
        run = False
