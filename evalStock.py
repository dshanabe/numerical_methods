import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# get current working directory
current_dir=os.getcwd()

# create a directory for daily_candles in the current directory
if not os.path.isdir('linear_analysis'):
    os.mkdir('linear_analysis')


# 2. Define the linear model: y = m*x + b
def linear_model(x, m, b):
    return m * x + b

def linearTrend(symbol, df):

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
    midpoints=[]
    miderrors=[]
    for i in range(len(ope)):
        error=(hig[i]-low[i])/2
        miderrors.append(error)
        midpoints.append(low[i]+error)
        #ax[1].vlines(x=xvals[i], ymin=low[i], ymax=hig[i], linestyle='-', linewidth=2)
    #ax[1].scatter(xvals, midpoints, marker='.')
    ax[1].set_ylabel('Price [USD]')
    # enable grid lines
    ax[1].grid(True)
    # collect every fifth date for cleaner labeling of x-ticks
    dates_mod=dates[::-5]
    xvals_mod=np.arange(1,len(dates)+1)[::-5]  
    ax[1].set_xticks(xvals_mod,rotation=315, labels=dates_mod)
    # plot super title      

    # save the figure   
    
    # Calculate weighted linear fit 
    x = xvals
    y = midpoints
    y_err = miderrors

    # 3. Fit the model with weights (sigma = y errors)
    popt, pcov = curve_fit(linear_model, x, y, sigma=y_err, absolute_sigma=True)

    # 4. Extract fit parameters and their uncertainties
    m, b = popt
    m_err, b_err = np.sqrt(np.diag(pcov))

    print(f"Slope (m) = {m:.3f} ± {m_err:.3f}")
    print(f"Intercept (b) = {b:.3f} ± {b_err:.3f}")

    # 5. Plot the data with error bars and the fit
    x_fit = np.linspace(min(x), max(x), len(y))
    y_fit = linear_model(x_fit, m, b)

    ax[1].errorbar(x, y, yerr=y_err, fmt='o', label='Data', capsize=5)
    ax[1].plot(x_fit, y_fit, 'r-', label='Weighted Fit')
    ax[0].hlines(xmin=min(xvals), xmax=max(xvals) ,y=0, linestyle='-', linewidth=2, color='Black')
    detrend_percent=100*(y-y_fit)/y_fit
    ax[0].plot(x_fit,detrend_percent,linewidth='2')
    ax[0].grid(True)
    ax[0].set_ylabel('% From Weighted Model')
    amp=max(abs(detrend_percent))
    ax[0].set_ylim([-amp,amp])
    ax[0].set_facecolor('lightgray')     

    score=round(100*(clo.tolist()[-1]-y_fit.tolist()[-1])/y_fit.tolist()[-1],2)
    if score<0:
        plt.suptitle(f'Linear Trend Score\nMost recent close value for {symbol} is {score}% below the trend: BUY')
    else:
        plt.suptitle(f'Linear Trend Score\nMost recent close value for {symbol} is {score}% above the trend: SELL')
    plt.savefig(f'{current_dir}/linear_analysis/{symbol}_linear_trend_analysis.jpg')
    
    return score
