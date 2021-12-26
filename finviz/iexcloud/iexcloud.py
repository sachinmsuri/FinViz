import json 
import requests
import pandas as pd


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

    def get_request(self, path):
        url = f'{self.base_url}{path}?token={self.token}'
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"connection to api failed ... error code - {r.status_code}")

    def get_max_time_series(self, ticker):
        #r = self.get_request(f'/stable/stock/{ticker}/chart/max')
        r = self.get_request(f'/stable/stock/{ticker}/chart/5y')
        return r

    def get_max_time_series_df(self, ticker):
        #r = self.get_request(f'/stable/stock/{ticker}/chart/max')
        r = self.get_request(f'/stable/stock/{ticker}/chart/5y')
        data_lst = []

        for i in r:
            data_lst.append([i['date'], i['close']])

        df = pd.DataFrame(data_lst, columns=['Date', ticker])
        print(f"Fetching time series data for {ticker}")
        return df

    def get_quote(self, ticker):
        r = self.get_request(f'/stable/stock/{ticker}/quote')
        return r

    def get_stock_by_country(self, country_code):
        r = self.get_request(f'/stable/stock/market/collection/country?collectionName={country_code}')
        return r

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
        r = self.get_request(f'/stable/stock/{ticker}/stats')
        #for i in r:
        if not r:
            return
        else:
            data_dict = {
                'Symbol': ticker,
                'Market Capitalization': r['marketcap'],
                'Dividend': r['dividendYield'],
                'PE Ratio': r['peRatio'],
            }

        return data_dict



if __name__ == "__main__":
    obj = iexCloud()
    r = obj.get_stats('AAPL')
    print(r)