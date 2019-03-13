
# coding: utf-8

# In[19]:

import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta,time
from ipywidgets import widgets
import matplotlib.pyplot as plt


# In[20]:

signal_df = pd.read_csv("data/news_data/sentiment_backtest_data.csv")
def run_strat(cutoff,delay,txn_fee = 0.0, output_daily_agg = False):
    assert cutoff <=1.0 and cutoff>=0.0
    assert delay > 0 and delay <=60 and delay % 5 ==0

    upper = cutoff
    lower = -cutoff
    score = "sentiment_score"
    buy_signals = np.array([1 if i> upper else 0 for i in signal_df[score]])
    sell_signals = np.array([1 if i< lower else 0 for i in signal_df[score]])
    signals = buy_signals-sell_signals
    longs = buy_signals.sum()
    shorts = sell_signals.sum()
    fees = txn_fee*(buy_signals+sell_signals)
    name = "ret_delay_{}".format(delay)
    datetimes = signal_df.datetime.astype('datetime64[ns]')
    ret = signal_df[name] * signals
    adj_ret = ret - fees
    cum_ret = np.cumsum(ret)
    adj_cum_ret = np.cumsum(adj_ret)
            
    output = """Sentiment News Strategy 
    cutoff strength: {}
    delay in mins: {}
    txn fees/trade: {}
    adj_cum_ret: {}""".format(cutoff,delay,txn_fee,adj_ret.sum())
    #print(output)
    strategy_result = pd.DataFrame({ 
                        "datetime" : datetimes.values,
                        "adj_cum_return" : adj_cum_ret.values,
                       "cum_return" : cum_ret.values,
                       "adj_return" : adj_ret.values,
                       "return" : ret.values})
    if not output_daily_agg:
        return strategy_result
    
    filtered_index = []
    current_date,prev_index = None, 0
    for i,datum in enumerate(strategy_result.itertuples()):
            
        prev_date = strategy_result.iloc[i-1].datetime.date()
        curr_date = strategy_result.iloc[i].datetime.date()
        
        ## if date change:
        if prev_date < curr_date:
            filtered_index.append(i-1)
        
            
        
    return strategy_result.iloc[filtered_index]


def display_backtest(time_till_close_position,sentiment_cutoff):
    strat_results = run_strat(sentiment_cutoff,time_till_close_position,txn_fee = 0.0, output_daily_agg = True)
    fig, ax = plt.subplots()
    dates = strat_results.datetime.map(lambda x: x.date())
    ax.plot_date(x = dates, y=strat_results.cum_return.values,fmt='-b')
    ax.set_ylabel("Cumulative Return")
    datemin = dates.min()
    datemax = dates.max()
    ax.set_xlim(datemin, datemax)

    fig.autofmt_xdate()
    plt.show()
    
def interactive_backtest():
    widgets.interact(display_backtest,time_till_close_position=(5,60,5),sentiment_cutoff=(0,1.00,0.05))



