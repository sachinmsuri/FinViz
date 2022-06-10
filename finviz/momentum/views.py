from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from iexcloud.iexcloud import iexCloud
from json import dumps
import pandas as pd
from parameters import engine_string


# Create your views here.

def momentum(request):
    return render(request, 'momentum.html', {})

def read_ticker_symbols():
    try:
        df_tickers = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)
        df_tickerstats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)
        df = pd.merge(df_tickers, df_tickerstats, how='inner', on='Symbol')
        
        #Format Market Capitalisation
        df['Market Capitalization Ranges'] = 'Placeholder'
        df.loc[(df['Market Capitalization'] <= 250000000), 'Market Capitalization Ranges'] = '$0 - $250,000,000'
        df.loc[(df['Market Capitalization'] >= 250000000) & (df['Market Capitalization'] <= 500000000), 'Market Capitalization Ranges'] = '$250,000,000 - $500,000,000'
        df.loc[(df['Market Capitalization'] >= 500000000) & (df['Market Capitalization'] <= 1000000000), 'Market Capitalization Ranges'] = '$500,000,000 - $1,000,000,000'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 10000000000), 'Market Capitalization Ranges'] = '$1,000,000,000 - $10,000,000,000'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 50000000000), 'Market Capitalization Ranges'] = '$10,000,000,000 - $50,000,000,000'
        df.loc[(df['Market Capitalization'] >= 5000000000) & (df['Market Capitalization'] <= 100000000000), 'Market Capitalization Ranges'] = '$50,000,000,000 - $100,000,000,000'
        df.loc[(df['Market Capitalization'] >= 100000000000) & (df['Market Capitalization'] <= 500000000000), 'Market Capitalization Ranges'] = '$100,000,000,000 - 500,000,000,000'
        df.loc[(df['Market Capitalization'] >= 500000000000), 'Market Capitalization Ranges'] = 'Greater than $500,000,000,000'

        #Format Dividend
        df['Dividend Ranges'] = 'Placeholder'
        df.loc[(df['Dividend'] <= 0), 'Dividend Ranges'] = '0%'
        df.loc[(df['Dividend'] >= 0) & (df['Dividend'] <= 0.025), 'Dividend Ranges'] = '0% - 2.5%'
        df.loc[(df['Dividend'] >= 0.025) & (df['Dividend'] <= 0.05), 'Dividend Ranges'] = '2.5% - 5%'
        df.loc[(df['Dividend'] >= 0.05) & (df['Dividend'] <= 0.075), 'Dividend Ranges'] = '5% - 7.5%'
        df.loc[(df['Dividend'] >= 0.075) & (df['Dividend'] <= 0.1), 'Dividend Ranges'] = '7.5% - 10%'
        df.loc[(df['Dividend'] >= 0.1) & (df['Dividend'] <= 0.15), 'Dividend Ranges'] = '10% - 15%'
        df.loc[(df['Dividend'] >= 0.15) & (df['Dividend'] <= 0.2), 'Dividend Ranges'] = '15% - 20%'
        df.loc[(df['Dividend'] >= 2), 'Dividend Ranges'] = 'Greater than 20%'

        #Format Dividend
        df['PE Ratio Ranges'] = 'Placeholder'
        df.loc[(df['PE Ratio'] <= -10), 'PE Ratio Ranges'] = 'Less than -10'
        df.loc[(df['PE Ratio'] >= -10) & (df['PE Ratio'] <= 0), 'PE Ratio Ranges'] = '-10 - 0'
        df.loc[(df['PE Ratio'] >= 0) & (df['PE Ratio'] <= 10), 'PE Ratio Ranges'] = '0 - 10'
        df.loc[(df['PE Ratio'] >= 10) & (df['PE Ratio'] <= 20), 'PE Ratio Ranges'] = '10 - 20'
        df.loc[(df['PE Ratio'] >= 20) & (df['PE Ratio'] <= 30), 'PE Ratio Ranges'] = '20 - 30'
        df.loc[(df['PE Ratio'] >= 30) & (df['PE Ratio'] <= 40), 'PE Ratio Ranges'] = '30 - 40'
        df.loc[(df['PE Ratio'] >= 40) & (df['PE Ratio'] <= 50), 'PE Ratio Ranges'] = '40 - 50'
        df.loc[(df['PE Ratio'] >= 50) & (df['PE Ratio'] <= 75), 'PE Ratio Ranges'] = '50 - 75'
        df.loc[(df['PE Ratio'] >= 75) & (df['PE Ratio'] <= 100), 'PE Ratio Ranges'] = '75 - 100'
        df.loc[(df['PE Ratio'] >= 100), 'PE Ratio Ranges'] = 'Greater than 100'

        #Format Revenue
        df['Revenue Ranges'] = 'Placeholder'
        df.loc[(df['Revenue'] <= 250000000), 'Revenue Ranges'] = '$0 - $250,000,000'
        df.loc[(df['Revenue'] >= 250000000) & (df['Revenue'] <= 500000000), 'Revenue Ranges'] = '$250,000,000 - $500,000,000'
        df.loc[(df['Revenue'] >= 500000000) & (df['Revenue'] <= 1000000000), 'Revenue Ranges'] = '$500,000,000 - $1,000,000,000'
        df.loc[(df['Revenue'] >= 1000000000) & (df['Revenue'] <= 10000000000), 'Revenue Ranges'] = '$1,000,000,000 - $10,000,000,000'
        df.loc[(df['Revenue'] >= 10000000000) & (df['Revenue'] <= 50000000000), 'Revenue Ranges'] = '$10,000,000,000 - $50,000,000,000'
        df.loc[(df['Revenue'] >= 50000000000) & (df['Revenue'] <= 100000000000), 'Revenue Ranges'] = '$50,000,000,000 - $100,000,000,000'
        df.loc[(df['Revenue'] >= 100000000000), 'Revenue Ranges'] = 'Greater than $100,000,000,000'
        #243,198,000

        #Format EBITDA
        df['EBITDA Ranges'] = 'Placeholder'
        df.loc[(df['EBITDA'] < -100000000), 'EBITDA Ranges'] = 'Less than -$100,000,000'
        df.loc[(df['EBITDA'] < -100000000) & (df['EBITDA'] <= -50000000), 'EBITDA Ranges'] = '-$100,000,000 - -$50,000,000'
        df.loc[(df['EBITDA'] >= -50000000) & (df['EBITDA'] <= 0), 'EBITDA Ranges'] = '-$50,000,000 - $0'
        df.loc[(df['EBITDA'] >= 0) & (df['EBITDA'] <= 250000000), 'EBITDA Ranges'] = '$0 - $250,000,000'
        df.loc[(df['EBITDA'] >= 250000000) & (df['EBITDA'] <= 500000000), 'EBITDA Ranges'] = '$250,000,000 - $500,000,000'
        df.loc[(df['EBITDA'] >= 500000000) & (df['EBITDA'] <= 1000000000), 'EBITDA Ranges'] = '$500,000,000 - $1,000,000,000'
        df.loc[(df['EBITDA'] >= 1000000000) & (df['EBITDA'] <= 10000000000), 'EBITDA Ranges'] = '$1,000,000,000 - $10,000,000,000'
        df.loc[(df['EBITDA'] >= 10000000000), 'EBITDA Ranges'] = 'Greater than $10,000,000,000'

        return df
    except Exception as e:
        print(str(e))

def get_symbols():
    dropdown_options = []
    df = read_ticker_symbols()
    for index, row in df.iterrows():
        dropdown_options.append({'label': row['Name'], 'value': row['Symbol']})
    return dropdown_options

def get_sectors():
    dropdown_options = []
    df = read_ticker_symbols()
    sector_lst = list(df['Sector'].unique())
    for i in sector_lst:
        dropdown_options.append({'label':i, 'value':i})
    return dropdown_options

def dropdown_values(column_name):
    dropdown_options = []
    df = read_ticker_symbols()
    lst = list(df[column_name].unique())
    for i in lst:
        dropdown_options.append({'label':i, 'value':i})
    return dropdown_options