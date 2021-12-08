import json 
import requests
import pandas as pd


class iexCloud():
    def __init__(self):
        self.base_url = "https://cloud.iexapis.com"
        try:
            #f = open('iexcloud_keys.json') --> for testing the module
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
        r = self.get_request(f'/stable/stock/{ticker}/chart/max')
        return r

    def get_max_time_series_df(self, ticker):
        r = self.get_request(f'/stable/stock/{ticker}/chart/max')
        data_lst = []

        for i in r:
            data_lst.append([i['date'], i['close']])

        df = pd.DataFrame(data_lst, columns=['Date', ticker])
        print(df)
        return df

    def get_quote(self, ticker):
        r = self.get_request(f'/stable/stock/{ticker}/quote')
        return r

    def get_stock_by_country(self, country_code):
        r = self.get_request(f'/stable/stock/market/collection/country?collectionName={country_code}')
        return r

if __name__ == "__main__":
    ticker = ['sachin', 'suri']
    if any(isinstance(i, list) for i in ticker):
        ticker = [item for elem in ticker for item in elem]
    print(ticker)
