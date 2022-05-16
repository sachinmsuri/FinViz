from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from parameters import engine_string
import pandas as pd

# Create your views here.

def annualreports(request):
    return render(request, 'annual_reports.html', {})

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


