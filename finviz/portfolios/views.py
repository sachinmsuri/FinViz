from django.shortcuts import render
import pandas as pd
from parameters import engine_string

# Create your views here.

def create_portfolio(request):
        return render(request, 'portfolios.html', {})

def read_ticker_symbols():
    try:
        df_tickers = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)
        df_tickerstats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)
        df = pd.merge(df_tickers, df_tickerstats, how='inner', on='Symbol')

        return df
    except Exception as e:
        print(str(e))

def get_symbols():
    dropdown_options = []
    df = read_ticker_symbols()
    for index, row in df.iterrows():
        dropdown_options.append({'label': row['Name'], 'value': row['Symbol']})
    return dropdown_options
