import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# get current working directory
current_dir=os.getcwd()

# create a directory for daily_candles in the current directory
if not os.path.isdir('daily_candles'):
    os.mkdir('daily_candles')

# define a functiont that generate candles fitures from a prepared data frame
def candles(symbol, df):
    # extract the fields
    dates=df['date']
    ope=df['open']
    hig=df['high']
    low=df['low']
    clo=df['close']
    vol=df['volume']
    
    # define a figure with subplots
    fig, ax = plt.subplots(2,1,figsize=(16,9),sharex=True,gridspec_kw={'height_ratios': [1, 3], 'hspace': 0})
    # set x values
    xvals=np.arange(1,len(ope)+1)
    # Color the values green, red, or orange based upon close and open values
    for i in range(len(low)):
        #print(hig[i],low[i])
        if clo[i]>ope[i]:
            COLOR='green'
        elif clo[i]<ope[i]:
            COLOR='red'
        else:
            COLOR='orange'

        # If the open and close are the same (i.e. color orange) then the vlines must be padded with a small float to still appear
        if COLOR=='orange':
            ax[1].vlines(x=xvals[i], ymin=low[i], ymax=hig[i], color=COLOR, linestyle='-', linewidth=2)
            ax[1].vlines(x=xvals[i], ymin=ope[i]-.05, ymax=clo[i]+.05, color=COLOR, linestyle='-', linewidth=6)
        # Plot two vertical lines. A thinner line for low to high. A thicker line for open and close.
        else:
            ax[1].vlines(x=xvals[i], ymin=low[i], ymax=hig[i], color=COLOR, linestyle='-', linewidth=2)
            ax[1].vlines(x=xvals[i], ymin=ope[i], ymax=clo[i], color=COLOR, linestyle='-', linewidth=6)
        # plot volume as bars in the smaller subplot
        ax[0].bar(xvals[i], vol[i], color=COLOR)
    # Label axis
    ax[0].set_ylabel('Volume')
    ax[1].set_ylabel('Price [USD]')
    # enable grid lines
    ax[1].grid(True)
    # collect every fifth date for cleaner labeling of x-ticks
    dates_mod=dates[::-5]
    xvals_mod=np.arange(1,len(dates)+1)[::-5]  
    ax[1].set_xticks(xvals_mod,rotation=315, labels=dates_mod)
    # plot super title      
    plt.suptitle(f'90 Day Candles\n{symbol}')
    # save the figure   
    plt.savefig(f'{current_dir}/daily_candles/{symbol}_candles.jpg')
        
