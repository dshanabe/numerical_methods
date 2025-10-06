import yfinance as yf
import time
import pandas as pd
import os

# get current working directory
current_dir=os.getcwd()

# create a directory for temp_tables in the current directory
if not os.path.isdir('temp_tables'):
    os.mkdir('temp_tables')

# define a simple function for rounding floats
def rounded(value):
    return round(value,3)

# define a function to download data, write a table, and read it as a pandas df
def writeTable(symbol, first_datetime_str, final_datetime_str):
    
    # Download stock data for local symbol. 
    # These 1 seconds delays before and after the call are important for safe interaction with yfinance
    time.sleep(1)
    data = yf.download([symbol], start=first_datetime_str, end=final_datetime_str, progress=False)
    time.sleep(1)
    print(f'downloaded {symbol} start={first_datetime_str} end={final_datetime_str}')
    # Write a new table. (Overwrite is true. )
    doc=open(f'{current_dir}/temp_tables/{symbol}_dailydata.txt','w')
    # Write the header
    doc.write(f"date open high low close volume")
    # convert each element of the table to lists. 
    dat = data.index.tolist()
    ope = data['Open'].values.flatten()
    hig = data['High'].values.flatten()
    low = data['Low'].values.flatten()
    clo = data['Close'].values.flatten()
    vol = data['Volume'].values.flatten()
    # write each element of each list to the table, row by row
    for i in range(len(ope)):
        date=str(dat[i]).split(' ')[0]
        doc.write(f"\n{date} {rounded(ope[i])} {rounded(hig[i])} {rounded(low[i])} {rounded(clo[i])} {vol[i]}")
    # close the table
    doc.close()
    # Use pandas to load the csv table as a df object
    df=pd.read_csv(f'{current_dir}/temp_tables/{symbol}_dailydata.txt', delimiter=' ')
      
    return df
