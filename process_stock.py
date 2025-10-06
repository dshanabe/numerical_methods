import fetchStock
import vizStock
import evalStock
from datetime import date, timedelta
import pandas as pd

# A function to process all stocks in the symbol list.
def process(symbol_list, first_datetime_str, final_datetime_str):
    print(f"Data from {first_datetime_str} to {final_datetime_str}")
    for symbol in symbol_list:
        # Call on writeTable to download data and write pandas df
        df=fetchStock.writeTable(symbol, first_datetime_str, final_datetime_str)
        # Call on candles to generate candles figure
        vizStock.candles(symbol,df)
        
        evalStock.linearTrend(symbol,df)
        
        #evalStock.movingAverage(symbol,df)
        #evalStock.volatilityScore(symbol,df)
        
    return True
        
if __name__ == "__main__":
    # Define a list of stock tickers for analysis
    symbol_list=['AAPL','F','YUM']

    # Get today's date. Format the date as a string for yfinance. 
    today = date.today()
    final_datetime_str = today.strftime("%Y-%m-%d")

    # Find the date that was 90 calendar days in the past
    ninety_days_ago = today - timedelta(days=90)

    # Format it as a string for yfinance
    first_datetime_str = ninety_days_ago.strftime("%Y-%m-%d")
    
    # Call on process to do full analysis of all symbols in symbol list. 
    process(symbol_list, first_datetime_str, final_datetime_str)
