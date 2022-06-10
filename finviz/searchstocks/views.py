from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from iexcloud.iexcloud import iexCloud
from json import dumps
import pandas as pd
from parameters import engine_string

# Create your views here.
def search_stock(request):
    if request.method == 'POST':
        stock = request.POST['search_stock']
        obj = iexCloud()

        try:
            stock_name = obj.get_quote(stock)
            time_series = obj.get_max_time_series(stock)

            #format data for chartjs
            chartjs_data = []
            for i in time_series:
                chartjs_data.append({'x':i['date'], 'y':i['close']})

            dataJSON = dumps(chartjs_data)        
        except Exception as e:
            dataJSON = "Error"
        
        return render(request, 'search_stock.html', {'chartjs_data': dataJSON, 'stock_name': stock_name})
        
    else:
        return render(request, 'search_stock.html', {'search_stock': 'Enter a stock quote'})

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

def colormap_value(table_name, range):
    try:
        df_colormaps = pd.read_sql(f'SELECT * FROM db_ingestion_{table_name}_colormaps;', engine_string)
        df_colormaps = df_colormaps[df_colormaps['Metric'] == range]
        print(df_colormaps)

        color = df_colormaps['Color'].iloc[0]
        return color
    except Exception as e:
        print(str(e))

def stock_information(ticker, metric):
    df_tickerstats = pd.read_sql(f'SELECT * FROM db_ingestion_tickerstats', engine_string)
    df_tickerstats = df_tickerstats[df_tickerstats['Symbol'] == ticker]

    if metric == 'marketcap':
        updated_metric = 'Market Capitalization Ranges'
    if metric == 'dividend':
        updated_metric = 'Dividend Ranges'
    if metric == 'ebitda':
        updated_metric = 'EBITDA Ranges'
    if metric == 'peratio':
        updated_metric = 'PE Ratio Ranges'
    if metric == 'revenue':
        updated_metric = 'Revenue Ranges'


    range = df_tickerstats[updated_metric].iloc[0]

    return range


def get_company_stats():
    try:
        df = pd.read_sql(f'SELECT * FROM db_ingestion_tickerstats', engine_string)
    except Exception as e:
        print(str(e))

    return df

