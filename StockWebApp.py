#Description: Stock market dashboard

# Import the libraries
import yfinance as fy
import streamlit as st
import pandas as pd
from PIL import Image

# Add a title and an image
st.title('Welcome to Your Stock Market Dashboard\n')
st.write('''
Let's **Visually** show data on a stock! Please enter a start date and end date of a stock 
of your choice to analyze.\n
Make sure all fields are filled out to view the most current information from Yahoo Finance.
''')

image = Image.open("stock_image.png")
st.image(image, use_column_width=True)

# Stock Language Dictionary
st.header("Before we get to analyzing, let's review some terminology!")
st.caption("All definitions are from https://www.thestreet.com, https://www.investopedia.com/ and https://towardsdatascience.com")

st.subheader("Ticker:")
st.text("'The ticker symbol is the symbol that is used on the stock exchange to delineate a given stock.' "
        "For example, AMZN is Amazon's ticker,  NYSE is the New York Stock Exchange's ticket (NYSE), "
        "and RY is the Royal Bank of Canada's ticker. Use this as your symbol input!")

st.subheader("Close Price:")
st.text("'The close is the price at which the stock stopped trading during normal trading hours "
        "(after-hours trading can impact the stock price as well). If a stock closes above the previous close, "
        "it is considered an upward movement for the stock. "
        "Vice versa, if a stock's close price is below the previous day's close, the stock is showing a downward movement.'")

st.subheader("Trading Volume:")
st.text("'The key thing to look out for when examining trading volume is spikes in trading volume, "
        "which can indicate the strength of a trend - whether it is high trading volume down or up. "
        "If a stock's price drops and the trading volume is high, it might mean that there is strength to the downward "
        "trend on the stock as opposed to a momentary blip (and vice versa if the price moves up).'")

st.subheader("Rolling Mean (Moving Average): ")
st.text("'Rolling mean/Moving Average (MA) smooths out price data by creating a constantly updated average price. "
        "This is useful to cut down “noise” in our price chart. Furthermore, this Moving Average could act as "
        "“Resistance” meaning from the downtrend and uptrend of stocks you could expect it will follow the trend "
        "and less likely to deviate outside its resistance point.'")

st.subheader("Expected Return: ")
st.text("'Expected Return measures the mean, or expected value, of the probability distribution of investment returns. "
        "The expected return of a portfolio is calculated by multiplying the weight of each asset by its expected return "
        "and adding the values for each investment — Investopedia.'")

#create a sidebar header
st.sidebar.header("Which stock would you like to analyze today?")

#Create a function to get the users input
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2022-01-02")
    end_date = st.sidebar.text_input("End Date", "2022-07-29")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "RY")

    st.sidebar.subheader("Let's see how much money you need to invest today, to earn x amount of annual income from that stock!")
    annual_income = st.sidebar.text_input("$", "1000")
    return start_date, end_date, stock_symbol, annual_income

#Create a function to get the company name
def get_company_name(symbol):
        return symbol.upper()

#Create a function to get the proper company data and the proper time frame from the user
def get_data(symbol, start, end):

    #Load the data
    df = fy.download(symbol, start, end)

    #Get the date range
    # due to date is an index column if we get date directly from yFinance
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    #Set the start and end index rows both to 0
    start_row = 0
    end_row = 0

    #Start the date from the top of the data set and go down to see it the user start date is
    #less than or equal to the date in the data set

    for i in range(0, len(df.index)):
        print(df.index[i])
        print(type(start))
        print(type(df.index[i]))
        if start <= df.index[i]:
            start_row = i
            break

    #Start from the bottom of the data set and look up to see if the users end date is
    #greater than or equal to the date in the data set

    for j in range(0, len(df)):
        if end >= df.index[len(df)-1-j]:
            end_row = len(df)-1-j
            break

    return df.iloc[start_row:end_row+1, :]

#Get the users input
start, end, symbol, annual_income = get_input()

#Get the data
df = get_data(symbol, start, end)
#Get the company name
company_name = get_company_name(symbol.upper())

#Display the investment required to earn x annual income in inputted stock
obj = fy.Ticker(company_name)
my_info = obj.info
dividend_rate = my_info['dividendRate']
int_annual_income = int(annual_income)
num_shares = round(int_annual_income/dividend_rate)

st.subheader("How much do you need to invest to reach your annual income goal?")
st.text("To earn $" + str(int_annual_income) +" a year, at a dividend rate of " + str(dividend_rate))
st.text(", you must have " + str(num_shares) + " shares.\n")

market_price = my_info['regularMarketPrice']
investment = round(market_price*num_shares)
st.text("This is equivalent to investing $" + str(investment) + " in " + str(company_name) + " today!\n")

#Display the close price
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

#Display the volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

#Get statistics on the data
st.header('Data Statistics')
st.write(df.describe())

#Calculate the Moving Average for the last 100 windows (100 days) of stocks closing price and
#take the average for each of the window’s moving average
close_px = df['Adj Close']
mavg = close_px.rolling(window=100).mean()
#Display the moving average
st.header(company_name+" Moving Average\n")
st.line_chart(mavg)

#Calculate and display the stocks expected return
rets = close_px / close_px.shift(1) - 1
st.header(company_name+" Return Rate\n")
st.line_chart(rets)
