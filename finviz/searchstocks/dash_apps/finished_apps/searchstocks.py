from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('searchstocks', external_stylesheets=external_stylesheets)

def read_ticker_symbols():
    try:
        df_tickers = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)
        df_tickerstats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)
        df = pd.merge(df_tickers, df_tickerstats, how='inner', on='Symbol')

        #Format Market Capitalisation
        df['Market Capitalization Ranges'] = 'Placeholder'
        df.loc[(df['Market Capitalization'] < 0), 'Market Capitalization Ranges'] = 'Less than $0'
        df.loc[(df['Market Capitalization'] >= 0) & (df['Market Capitalization'] <= 500000000), 'Market Capitalization Ranges'] = '$0 - $500,000,000'
        df.loc[(df['Market Capitalization'] >= 500000000) & (df['Market Capitalization'] <= 1000000000), 'Market Capitalization Ranges'] = '$500,000,000 - $1,000,000,000'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 10000000000), 'Market Capitalization Ranges'] = '$1,000,000,000 - $10,000,000,000'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 50000000000), 'Market Capitalization Ranges'] = '$10,000,000,000 - $50,000,000,000'
        df.loc[(df['Market Capitalization'] >= 5000000000) & (df['Market Capitalization'] <= 100000000000), 'Market Capitalization Ranges'] = '$50,000,000,000 - $100,000,000,000'
        df.loc[(df['Market Capitalization'] >= 100000000000), 'Market Capitalization Ranges'] = 'Greater than $100,000,000,000'

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

##############################################################################################

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Companies listed on Nasdaq",
                style={'backgroundColor': '#1E1E1E'}),
    
    dcc.Dropdown(id='sectorselector',
                options=get_sectors(),
                multi=True,
                clearable = True,
                value = [],
                placeholder="Sectors listed on Nasdaq",
                style={'backgroundColor': '#1E1E1E'}),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),

    html.Br(),

    dcc.Dropdown(id='Market Cap',
                options=[
                    {'label': 'Less than $0', 'value': 'Less than $0'},
                    {'label': '$500,000,000 - $1,000,000,000', 'value': '$500,000,000 - $1,000,000,000'},
                    {'label': '$1,000,000,000 - $10,000,000,000', 'value': '$1,000,000,000 - $10,000,000,000'},
                    {'label': '$10,000,000,000 - $50,000,000,000', 'value': '$10,000,000,000 - $50,000,000,000'},
                    {'label': '$50,000,000,000 - $100,000,000,000', 'value': '$50,000,000,000 - $100,000,000,000'}
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter by Revenue",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),
])

#Callbacks
@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("stockselector", "value"),
    Input("sectorselector", "value")])

def time_series_stock(ticker_dropdown, sector_dropdown):
    #Flatten list
    print(ticker_dropdown)
    if any(isinstance(i, list) for i in ticker_dropdown):
        ticker_dropdown = [item for elem in ticker_dropdown for item in elem]

    graphs = []

    for ticker in ticker_dropdown:
        stock_df = obj_iexcloud.get_max_time_series_df(ticker)
        graphs.append(go.Scatter(
            x = stock_df['Date'],
            y = stock_df[ticker],
            mode = 'lines',
            name = ticker,
            textposition = 'bottom center',
        ))

    for sector in sector_dropdown:
        df = read_ticker_symbols()
        df = df[df['Sector'] == sector]
        stock_list = list(df['Symbol'])[0:10]
        for stock in stock_list:
            stock_df = obj_iexcloud.get_max_time_series_df(stock)
            graphs.append(go.Scatter(
            x = stock_df['Date'],
            y = stock_df[stock],
            mode = 'lines',
            name = stock,
            textposition = 'bottom center',
        ))

    if any(isinstance(i, list) for i in graphs):
        graphs = [item for elem in graphs for item in elem]

    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
            autosize=True,
            xaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                'rangeselector': {
                    'buttons':list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=5, label="5y", step="year", stepmode="backward"),
                            dict(step="all")
                            ])
                        }
                    },
            yaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    }
                )
        } 


    return fig
