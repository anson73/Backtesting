import os
import pandas as pd
from yf_extract import yf_extract
from datetime import datetime, date

class futures_backtest(object):
    def __init__(self, ticker, start_date=None, end_date=None):
        self.futures_data = os.path.join(os.getcwd(), 'FuturesData')
        self.futures_list = yf_extract().futures_list
        self.ticker = ticker

        self.df = pd.read_parquet(os.path.join(self.futures_data, self.ticker + ".parquet"))
        self.apply_date(start_date, end_date)
        
    def apply_date(self, start_date=None, end_date=None):
        if (start_date is not None) and (end_date is not None):
            self.df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]

        elif (start_date is not None):
            self.df = self.df[self.df['Date'] >= start_date]

        elif (end_date is not None):
            self.df = self.df[self.df['Date'] <= end_date]
        
        self.df = self.df.reset_index(drop=True)
        
    def weekly_high(self):
        # Find which day is most likely to create the weekly high
        df = self.df
        df['Date'] = pd.to_datetime(df['Date'])
        df['day_of_week'] = df['Date'].dt.day_name()
        
        df = df.set_index('Date')
        weekly_high_days = df.loc[df.groupby(pd.Grouper(freq='W'))['High'].idxmax()]
        weekly_high_days = weekly_high_days.reset_index(drop=True)
        day_counts = weekly_high_days['day_of_week'].value_counts()

        return day_counts

    def weekly_low(self):
        # Find which day is most likely to create the weekly Low
        df = self.df
        df['Date'] = pd.to_datetime(df['Date'])
        df['day_of_week'] = df['Date'].dt.day_name()
        
        df = df.set_index('Date')
        weekly_low_days = df.loc[df.groupby(pd.Grouper(freq='W'))['Low'].idxmin()]
        weekly_low_days = weekly_low_days.reset_index(drop=True)
        day_counts = weekly_low_days['day_of_week'].value_counts()

        return day_counts
    
    def daily_direction(self):
        # Find whether a day of the week is more likely to be bullish or bearish
        # Find percentage change for each day
        df = self.df
        df['%Change'] = ((df['Close'] - df['Open']) / df['Open'])*100
        df['Date'] = pd.to_datetime(df['Date'])
        df['day_of_week'] = df['Date'].dt.day_name() 
        result = df.groupby('day_of_week')['%Change'].agg(
            Bullish=lambda x: (x > 0).sum(),
            Bearish=lambda x: (x < 0).sum()
        ).reset_index()
        return result

    def yearly_high(self):
        # Find which month is most likely to create the high of the year
        df = self.df
        df['Date'] = df['Date'].astype(str)
        df[['Year', 'Month', 'Day']] = df['Date'].str.split('-', expand=True)
        df = df.groupby(['Year', 'Month'], as_index=False)['High'].max()
        df = df.loc[df.groupby('Year')['High'].idxmax()]

        return df

    def yearly_low(self):
        # Find which month is most likely to create the low of the year
        df = self.df
        df['Date'] = df['Date'].astype(str)
        df[['Year', 'Month', 'Day']] = df['Date'].str.split('-', expand=True)
        df = df.groupby(['Year', 'Month'], as_index=False)['Low'].min()
        df = df.loc[df.groupby('Year')['Low'].idxmin()]

        return df
    
if __name__ == "__main__":
    # print(futures_backtest(ticker='NQ=F', start_date=date(2015, 1, 1), end_date=date(2024, 12, 31)).weekly_low())
    # print(futures_backtest(ticker='NQ=F', start_date=date(2015, 1, 1), end_date=date(2024, 12, 31)).weekly_high())
    # print(futures_backtest(ticker='NQ=F', start_date=date(2015, 1, 1), end_date=date(2024, 12, 31)).daily_direction())
    print()
    