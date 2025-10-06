import fetchStock
import vizStock
import evalStock
from datetime import date, timedelta
import pandas as pd
import numpy as np

# A function to process all stocks in the symbol list.
def process(symbol_list, first_datetime_str, final_datetime_str):
    print(f"Data from {first_datetime_str} to {final_datetime_str}")
    for symbol in symbol_list:
        # Call on writeTable to download data and write pandas df
        df=fetchStock.writeTable(symbol, first_datetime_str, final_datetime_str)
        # Call on candles to generate candles figure
        vizStock.candles(symbol,df,50)
        
        # Do linear analysis
        score50=evalStock.linearTrend(symbol,df,50)
        score200=evalStock.linearTrend(symbol,df,200)
        
        perf.write(f"\n{first_datetime_str} {final_datetime_str} {symbol} {score50} {score200}")
        
        # Do moving average analysis
        #evalStock.movingAverage(symbol,df)
        
        # Do volatility analysis
        #evalStock.volatilityScore(symbol,df)
        
        # Do long term model analysis
        #evalStock.modelAnalysis()
        
        # Do a NN prediction
        #predictStock.feedforwardNN()
        
    return True
        
if __name__ == "__main__":
    # Define a list of stock tickers for analysis
    symbol_list=['AAPL','F','YUM']

    perf=open('performance.txt','w')
    perf.write("first_datetime_str final_datetime_str symbol score50 score200")
    TIME_MACHINE_LIST=np.arange(3,-1,-1)
    print(TIME_MACHINE_LIST)

    for TIME_MACHINE in TIME_MACHINE_LIST:
        # Get false today's date. Format the date as a string for yfinance. 
        false_today = date.today() - timedelta(days=int(TIME_MACHINE))

        final_datetime_str = false_today.strftime("%Y-%m-%d")

        # Find the date that was N calendar days in the past
        n_days_ago = false_today - timedelta(days=365)

        # Format it as a string for yfinance
        first_datetime_str = n_days_ago.strftime("%Y-%m-%d")
        print(first_datetime_str, final_datetime_str)
        # Call on process to do full analysis of all symbols in symbol list. 
        process(symbol_list, first_datetime_str, final_datetime_str)
        
    perf.close()
