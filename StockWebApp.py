#Description: Stock market dashboard

# Import the libraries
import yfinance as fy
import streamlit as st
import pandas as pd
from PIL import Image

# Add a title and an image for landing page
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
    return start_date, end_date, stock_symbol

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
start, end, symbol = get_input()

#Get the data
df = get_data(symbol, start, end)
#Get the company name
company_name = get_company_name(symbol.upper())

#Display the close price
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

#Display the volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

#Get statistics on the data
st.header('Data Statistics')
st.write(df.describe())

#Calculate and display the stocks expected return
close_px = df['Adj Close']
rets = close_px / close_px.shift(1) - 1
st.header(company_name+" Return Rate\n")
st.line_chart(rets)
