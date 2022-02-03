from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
#import dash
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
        df.loc[(df['Market Capitalization'] <= 250000000), 'Market Capitalization Ranges'] = '$0 - $250m'
        df.loc[(df['Market Capitalization'] >= 250000000) & (df['Market Capitalization'] <= 500000000), 'Market Capitalization Ranges'] = '$250m - $500m'
        df.loc[(df['Market Capitalization'] >= 500000000) & (df['Market Capitalization'] <= 1000000000), 'Market Capitalization Ranges'] = '$500m - $1,000m'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 10000000000), 'Market Capitalization Ranges'] = '$1,000m - $10,000m'
        df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 50000000000), 'Market Capitalization Ranges'] = '$10,000m - $50,000m'
        df.loc[(df['Market Capitalization'] >= 5000000000) & (df['Market Capitalization'] <= 100000000000), 'Market Capitalization Ranges'] = '$50,000m - $100,000m'
        df.loc[(df['Market Capitalization'] >= 100000000000) & (df['Market Capitalization'] <= 500000000000), 'Market Capitalization Ranges'] = '$100,000m - $500,000m'
        df.loc[(df['Market Capitalization'] >= 500000000000), 'Market Capitalization Ranges'] = 'Greater than $500,000m'

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
    
    html.Br(),

    # dcc.Checklist(
    #         id = 'moving_average_selector',
    #         options=[
    #             {'label': 'Moving Average', 'value': 'Moving Average'},
    #         ],
    #         value=[],
    #         style = {
    #                 'display':'flex', 
    #                 'justifyContent':'center',
    #                 'align-items':'center',
    #                 'margin': 'auto',
    #                 'color': 'white',
    #                 }
    #         ),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),

    html.Br(),

    dcc.Dropdown(id='marketcap_selector',
                options=[
                    {'label': "0 - $250Millon", 'value': "0 - $250 millon"},
                    {'label': "$250Million - $500Million", 'value': "$250Million - $500Million"},
                    {'label': "$500Million - $1Billion", 'value': "$500Million - $1Billion"},
                    {'label': '$1Billion - $10Billion', 'value': '$1Billion - $10Billion'},
                    {'label': '$10Billion - $50Billion', 'value': '$10Billion - $50Billion'},
                    {'label': '$50Billion - $100Billion', 'value': '$50Billion - $100Billion'},
                    {'label': '$100Billion - $500Billion', 'value': '$100Billion - $500Billion'},        
                    {'label': 'Over $500Billion ', 'value': 'Over $500Billion'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Market Capitalization",
                searchable=True,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='dividend_selector',
                options=[
                    {'label': '0% - 2.5%', 'value': '0% - 2.5%'},
                    {'label': '2.5% - 5%', 'value': '2.5% - 5%'},
                    {'label': '5% - 7.5%', 'value': '5% - 7.5%'},
                    {'label': '7.5% - 10%', 'value': '7.5% - 10%'},
                    {'label': '10% - 15%', 'value': '10% - 15%'},
                    {'label': '15% - 20%', 'value': '15% - 20%'},
                    {'label': 'Greater than 20%', 'value': 'Greater than 20%'},

                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Dividend Yield",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),
    
    dcc.Dropdown(id='pe_selector',
                options=[
                    {'label': 'Less than -10', 'value': 'Less than -10'},
                    {'label': '-10 - 0', 'value': '-10 - 0'},
                    {'label': '0 - 10', 'value': '0 - 10'},
                    {'label': '10 - 20', 'value': '10 - 20'},
                    {'label': '20 - 30', 'value': '20 - 30'},
                    {'label': '30 - 40', 'value': '30 - 40'},
                    {'label': '40 - 50', 'value': '40 - 50'},
                    {'label': '50 - 75', 'value': '50 - 75'},
                    {'label': '75 - 100', 'value': '75 - 100'},
                    {'label': 'Greater than 100', 'value': 'Greater than 100'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by PE Ratio Scores",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='revenue_selector',
                options=[
                    {'label': '$0 - $250,000,000', 'value': '$0 - $250,000,000'},
                    {'label': '$250,000,000 - $500,000,000', 'value': '$250,000,000 - $500,000,000'},
                    {'label': '$500,000,000 - $1,000,000,000', 'value': '$500,000,000 - $1,000,000,000'},
                    {'label': '$1,000,000,000 - $10,000,000,000', 'value': '$1,000,000,000 - $10,000,000,000'},
                    {'label': '$10,000,000,000 - $50,000,000,000', 'value': '$10,000,000,000 - $50,000,000,000'},
                    {'label': '$50,000,000,000 - $100,000,000,000', 'value': '$50,000,000,000 - $100,000,000,000'},
                    {'label': 'Greater than $100,000,000,000', 'value': 'Greater than $100,000,000,000'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Revenue",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='ebitda_selector',
                options=[
                    {'label': 'Less than -$100,000,000', 'value': 'Less than -$100,000,000'},
                    {'label': '-$100,000,000 - -$50,000,000', 'value': '-$100,000,000 - -$50,000,000'},
                    {'label': '-$50,000,000 - $0', 'value': '-$50,000,000 - $0'},
                    {'label': '$0 - $250,000,000', 'value': '$0 - $250,000,000'},
                    {'label': '$250,000,000 - $500,000,000', 'value': '$250,000,000 - $500,000,000'},
                    {'label': '$500,000,000 - $1,000,000,000', 'value': '$500,000,000 - $1,000,000,000'},
                    {'label': '$1,000,000,000 - $10,000,000,000', 'value': '$1,000,000,000 - $10,000,000,000'},
                    {'label': 'Greater than $10,000,000,000', 'value': 'Greater than $10,000,000,000'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Earnings (EBITDA)",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),
])

#Callbacks
@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("stockselector", "value"),
    Input("sectorselector", "value"),
    Input("marketcap_selector", "value"),
    Input("dividend_selector", "value"),
    Input("pe_selector", "value"),
    Input("revenue_selector", "value"),
    Input("ebitda_selector", "value")])

def time_series_stock(ticker_dropdown, sector_dropdown, marketcap_selector, 
                        dividend_selector, pe_selector, revenue_selector,
                        ebitda_selector):
    #Flatten list
    if any(isinstance(i, list) for i in ticker_dropdown):
        ticker_dropdown = [item for elem in ticker_dropdown for item in elem]

    graphs = []

    #Draw time series of a single stock
    for ticker in ticker_dropdown:
        stock_df = obj_iexcloud.get_max_time_series_df(ticker)
        graphs.append(go.Scatter(
            x = stock_df['Date'],
            y = stock_df[ticker],
            mode = 'lines',
            name = ticker,
            textposition = 'bottom center',
        ))

    parameters = {
        'Market Capitalization Ranges': marketcap_selector,
        'Dividend Ranges': dividend_selector,
        'PE Ratio Ranges': pe_selector,
        'Revenue Ranges': revenue_selector,
        'EBITDA Ranges': ebitda_selector
    }
    filled_parameters = {}
    for key, value in parameters.items():
        if value:
            filled_parameters[key] = value

    #Draw time series of sectors and filter
    sector_df = read_ticker_symbols()
    sector_df = sector_df[sector_df['Sector'].isin(sector_dropdown)]
    print(sector_df)
    #if marketcap_dropdown:
    for key in  filled_parameters:
        #sector_df = sector_df.loc[(sector_df['Market Capitalization Ranges'].isin(marketcap_dropdown))]
        sector_df = sector_df.loc[(sector_df[key].isin(filled_parameters[key]))]
    stock_list = list(sector_df['Symbol'])[0:20]
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
