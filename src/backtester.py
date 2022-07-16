#This is an application to backtest portoflios

#Import required libraries
import pandas as pd
import empyrical
import requests
import warnings
from retrying import retry
from prettytable import PrettyTable
from secrets import IEX_SANDBOX

warnings.simplefilter(action='ignore', category=(FutureWarning, UserWarning))

#define chunks for batch API call
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def _historic_prices(
    symbol,
    start_date,
    end_date
    )

   #Call portfolio holdings for to backtest.
    df_holdings = pd.read_pickle('./backtest/data/target_portoflio_holdings_trimmed.pkl')
    df_holdings = pd.DataFrame(df_holdings)

    #convert tickers to list
    tickers = df_holdings['TICKER'].tolist()
    prices = []

    #chunk list of tickers for batch call
    ticker_groups = list(chunks(tickers, 100))
    ticker_strings = []
    for i in range(0, len(ticker_groups)):
        ticker_strings.append(','.join(ticker_groups[i]))

    #Create list of prices 
    for ticker_string in ticker_strings:   
        batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={ticker_string}&types=quote&token={IEX_SANDBOX}'
        data = requests.get(batch_api_url).json()
        for ticker in ticker_string.split(','):
            prices.append(
                data[ticker]['quote']['latestPrice']
                ) 

