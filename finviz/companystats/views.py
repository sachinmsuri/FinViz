from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from parameters import engine_string
import pandas as pd

# Create your views here.

def companystats(request):
    return render(request, 'companystats.html', {})

def read_ticker_symbols():
    try:
        df = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)    
        return df
    except Exception as e:
        print(str(e))

def get_symbols():
    dropdown_options = []
    df = read_ticker_symbols()
    for index, row in df.iterrows():
        dropdown_options.append({'label': row['Name'], 'value': row['Symbol']})
    return dropdown_options

def read_ticker_stats():
    try:
        df_name = pd.read_sql('SELECT * from db_ingestion_tickers', engine_string)
        #df_name = df_name[['Symbol', 'Name', 'Sector']]

        df_stats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)

        df = pd.merge(df_stats ,df_name, on='Symbol', how='inner')

        df = df[['Name', 'Sector', 'Symbol', 'Market Capitalization', 'Dividend', 'PE Ratio',	
                'EBITDA', 'Revenue', 'Net Income']]

        return df
    except Exception as e:
        print(str(e))
