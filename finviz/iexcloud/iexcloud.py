import json 
import requests
import pandas as pd
from datetime import datetime, timedelta

class iexCloud():
    def __init__(self):
        self.base_url = "https://cloud.iexapis.com"
        try:
            #f = open('iexcloud_keys.json') #--> for testing the module
            f = open('iexcloud/iexcloud_keys.json',)
            key = json.load(f)
            self.token = key['key']
            f.close()
        except Exception as e:
            print(str(e))

    def get_request(self, path, advanced=None):
        if advanced:
            url = f'{self.base_url}{path}&token={self.token}'
        else:
            url = f'{self.base_url}{path}?token={self.token}'
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"connection to api failed ... error code - {r.status_code}")

    def get_max_time_series_df(self, ticker):
        try:
            #r = self.get_request(f'/stable/stock/{ticker}/chart/max')
            r = self.get_request(f'/stable/stock/{ticker}/chart/5y')
            data_lst = []

            for i in r:
                data_lst.append([i['date'], i['close']])

            df = pd.DataFrame(data_lst, columns=['Date', ticker])
            print(f"Fetching time series data for {ticker}")
            return df
        except Exception as e:
            print(str(e))

    def get_max_time_series(self, ticker):
        #r = self.get_request(f'/stable/stock/{ticker}/chart/max')
        r = self.get_request(f'/stable/stock/{ticker}/chart/1y')
        return r

    def get_quote(self, ticker):
        r = self.get_request(f'/stable/stock/{ticker}/quote')
        return r

    def get_stock_by_country(self, country_code):
        r = self.get_request(f'/stable/stock/market/collection/country?collectionName={country_code}')
        return r

    def get_momentum_df(self, ticker):
        time_period = 10
        placeholder = 'Placeholder'

        time_series_df = self.get_max_time_series_df(ticker)
        dataframe_length = (len(time_series_df)-1)
        time_series_df['Momentum'] = placeholder

        for i in range(dataframe_length, -1, -1):
            if i == (time_period-1):
                break
            else:
                time_series_df.iloc[i, time_series_df.columns.get_loc('Momentum')] =\
                ((time_series_df.iloc[i, time_series_df.columns.get_loc(ticker)] -\
                time_series_df.iloc[i - (time_period), time_series_df.columns.get_loc(ticker)]) / time_period)
        
        time_series_df = time_series_df[time_series_df['Momentum'] != placeholder]
        time_series_df['Momentum'] = time_series_df['Momentum'].astype(float)

        dataframe_length = (len(time_series_df)-1)
        time_series_df['Momentum Change'] = placeholder

        for i in range(dataframe_length, 0, -1):
            time_series_df.iloc[(i), time_series_df.columns.get_loc('Momentum Change')] =\
            ((time_series_df.iloc[i, time_series_df.columns.get_loc('Momentum')] -\
            time_series_df.iloc[(i-1), time_series_df.columns.get_loc('Momentum')]))
        
        time_series_df = time_series_df[time_series_df['Momentum Change'] != placeholder]
        time_series_df['Momentum Change'] = time_series_df['Momentum Change'].astype(float)

        return time_series_df

    def get_moving_average_df(self, ticker):
        time_period = 912
        time_series_df = self.get_max_time_series_df(ticker)

        time_series_df['Moving Average'] = time_series_df[ticker].rolling(time_period).mean()
        print(time_series_df)

        return time_series_df

    def get_financials(self, ticker):
        #/stock/{symbol}/stats/
        r = self.get_request(f'/stable/stock/{ticker}/financials')
        if not r:
            return
        else:
            for i in r['financials']:
                data_dict = {
                    'Symbol': ticker, 
                    'EBITDA': i['EBITDA'],
                    'Revenue': i['revenue'],
                    'Net Income': i['netIncome'],
                }

        return data_dict

    def get_stats(self, ticker):
        stats = self.get_request(f'/stable/stock/{ticker}/stats')
        #latest_share_price = self.get_request(f'/stable/stock/{ticker}/delayed-quote')
        latest_share_price = self.get_request(f'/stable/stock/{ticker}/previous')

        if not stats or not latest_share_price:
            return
        else:
            data_dict = {
                'Symbol': ticker,
                'Market Capitalization': stats['marketcap'],
                'Dividend': stats['dividendYield'],
                'PE Ratio': stats['peRatio'],
                '200 Day MA': stats['day200MovingAvg'],
                #'Share Price': latest_share_price['delayedPrice']
                'Share Price': latest_share_price['close']

            }

        return data_dict

    def get_news(self, ticker):
        news = self.get_request(f'/stable/stock/{ticker}/news/last/100')

        data = []
        for article in news:
            unix_time = article['datetime']
            updated_datetime = (datetime.fromtimestamp(unix_time/1000)).strftime('%Y-%m-%d %H:%M:%S')

            row = {
                #'date': article['datetime'],
                'date': updated_datetime,
                'headline': article['headline'],
                'url': article['url']
            }
            data.append(row)
        
        df = pd.DataFrame(data=data)

        return df

    def get_income_statement(self, ticker):
        years = [
            2017,
            2018,
            2019,
            2020,
            2021
        ]

        dataframe_rows = {
                'Indicator': ['Revenue', 'Cost of Revenue', 'Gross Profit', 'Earnings before Interest & Tax', 'R&D']
            }

        for year in years:
            financials = self.get_request(f'/stable/stock/{ticker}/income?period=annual&limit=1&subattribute=fiscalYear|{year}', True)

            data = [
                financials['income'][0]['totalRevenue'],
                financials['income'][0]['costOfRevenue'],
                financials['income'][0]['grossProfit'],
                financials['income'][0]['ebit'],
                financials['income'][0]['researchAndDevelopment'],
            ]

            dataframe_rows[year] = data

        df = pd.DataFrame(data=dataframe_rows)

        return df

        
    
    def get_balance_sheet(self, ticker):
        years = [
            2017,
            2018,
            2019,
            2020,
            2021
        ]

        dataframe_rows = {
                'Indicator': ['Assets', 'Cash', 
                'Retained Earnings', 'Inventory', 'Debt']
            }

        for year in years:
            financials = self.get_request(f'/stable/stock/{ticker}/balance-sheet?period=annual&limit=1&subattribute=fiscalYear|{year}', True)

            data = [
                financials['balancesheet'][0]['totalAssets'],
                financials['balancesheet'][0]['currentCash'],
                financials['balancesheet'][0]['retainedEarnings'],
                financials['balancesheet'][0]['inventory'],
                financials['balancesheet'][0]['longTermDebt'],
            ]

            dataframe_rows[year] = data

        df = pd.DataFrame(data=dataframe_rows)

        return df


    def get_financial_ratios(self, ticker):
        years = [
            2017,
            2018,
            2019,
            2020,
            2021
        ]

        dataframe_rows = {
                'Indicator': ['Current Ratio', 'Debt to Assets', 'P/E Ratio', 'Return on Assets', 'Earnings Yield (EPS)']
            }
        
        for year in years:
            ratios = self.get_request(f'/stable/time-series/FUNDAMENTAL_VALUATIONS/{ticker}/annual?limit=1&subattribute=fiscalYear|{year}', True)

            data = [
                    ratios[0]['currentRatio'],
                    ratios[0]['debtToAssets'],
                    ratios[0]['pToE'],
                    ratios[0]['returnOnAssets'],
                    ratios[0]['earningsYield']
                ]

            dataframe_rows[year] = data

        df = pd.DataFrame(data=dataframe_rows)

        for year in years:
            df[year] = df[year].apply(lambda x: float("{:.3f}".format(x)))

        return df


if __name__ == "__main__":
    obj = iexCloud()
    r = obj.get_momentum_df('AAPL')

