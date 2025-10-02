import os
import yfinance as yf
import pandas as pd

class yf_extract(object):
    def __init__(self):
        self.cwd = os.getcwd()
        self.futures_list = ['NQ=F', 'ES=F', 'YM=F']

    def update_futures_ticker(self, ticker):
        '''
        Get historical price data for a ticker
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        Send data to a parquet file
        '''
        instrument = yf.Ticker(ticker)
        price_history = instrument.history(period='max', interval='1d').reset_index()
        price_history['Date'] = pd.to_datetime(price_history['Date']).dt.date
        price_history = price_history.drop('Dividends', axis=1)
        price_history = price_history.drop('Stock Splits', axis=1)

        price_history.to_parquet(os.path.join(self.cwd, 'FuturesData', ticker + '.parquet'), index=False)

        print("Updated historical price data for: " + ticker)
    
    def update_futures(self):
        '''
        Update all futures instruments (self.futures_list) with latest historical data
        '''
        for instrument in self.futures_list:
            self.update_futures_ticker(instrument)

    def show_data(self, ticker):
        '''
        Show data from parquet a file
        '''

        df = pd.read_parquet(os.path.join(self.cwd, 'FuturesData', ticker + '.parquet'))

        return df


if __name__ == "__main__": 
    print(yf_extract().show_data("NQ=F"))
