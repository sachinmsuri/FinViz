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
from plotly.subplots import make_subplots
from momentum.views import read_ticker_symbols
from momentum.views import get_symbols
from momentum.views import get_sectors
from momentum.views import dropdown_values



##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('momentum', external_stylesheets=external_stylesheets)


#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Companies listed on S&P500",
                style={'backgroundColor': '#1E1E1E'}),
    
    dcc.Dropdown(id='sectorselector',
                options=get_sectors(),
                multi=True,
                clearable = True,
                value = [],
                placeholder="Sectors listed on S&P500",
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),

    dcc.RadioItems(
            id = 'momentum_selector',
            options=[
                {'label': 'Momentum', 'value': 'Momentum'},
                {'label': 'Moving Average', 'value': 'Moving Average'},
            ],
            value='Momentum',
            style = {
                    'display':'flex', 
                    'justifyContent':'center',
                    'align-items':'center',
                    'margin': 'auto',
                    'color': 'white',
                    }
            ),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),

    html.Br(),

    dcc.Dropdown(id='marketcap_selector',
                options=[
                    {'label': '$0 - $250,000,000', 'value': '$0 - $250,000,000'},
                    {'label': '$250,000,000 - $500,000,000', 'value': '$250,000,000 - $500,000,000'},
                    {'label': '$500,000,000 - $1,000,000,000', 'value': '$500,000,000 - $1,000,000,000'},
                    {'label': '$1,000,000,000 - $10,000,000,000', 'value': '$1,000,000,000 - $10,000,000,000'},
                    {'label': '$10,000,000,000 - $50,000,000,000', 'value': '$10,000,000,000 - $50,000,000,000'},
                    {'label': '$50,000,000,000 - $100,000,000,000', 'value': '$50,000,000,000 - $100,000,000,000'},
                    {'label': '$100,000,000,000 - $500,000,000,000', 'value': '$100,000,000,000 - $500,000,000,000'},        
                    {'label': 'Greater than $500,000,000,000', 'value': 'Greater than $500,000,000,000'}
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Market Capitalization",
                searchable=False,
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
    Input("ebitda_selector", "value"),
    Input("momentum_selector", "value")])

def time_series_stock(ticker_dropdown, sector_dropdown, marketcap_dropdown, 
                        dividend_selector, pe_selector, revenue_selector,
                        ebitda_selector, momentum_selector):
    print(momentum_selector)
    #Flatten list
    if any(isinstance(i, list) for i in ticker_dropdown):
        ticker_dropdown = [item for elem in ticker_dropdown for item in elem]

    graphs = []

    #Draw time series of a single stock
    for ticker in ticker_dropdown:
        #stock_df = obj_iexcloud.get_max_time_series_df(ticker)
        # graphs.append(go.Scatter(
        #     x = stock_df['Date'],
        #     y = stock_df['Momentum Change'],
        #     mode = 'lines',
        #     name = f"{ticker} Momentum Change" ,
        #     textposition = 'bottom center',
        # ))
        if momentum_selector == 'Momentum':
            stock_df = obj_iexcloud.get_momentum_df(ticker)
            graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df['Momentum'],
                mode = 'lines',
                name = f"{ticker} Momentum" ,
                textposition = 'bottom center',
            ))
        if momentum_selector == 'Moving Average':
            stock_df = obj_iexcloud.get_moving_average_df(ticker)
            graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df['Moving Average'],
                mode = 'lines',
                name = f"{ticker} Moving Average",
                textposition = 'bottom center',
                yaxis = 'y2'
            ))


    parameters = {
        'Market Capitalization Ranges': marketcap_dropdown,
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

    for key in  filled_parameters:
        sector_df = sector_df.loc[(sector_df[key].isin(filled_parameters[key]))]
    
    
    #stock_list = list(sector_df['Symbol'])[0:20]

    stock_list = list(sector_df['Symbol'])
    for stock in stock_list:
        if momentum_selector == 'Momentum':
            stock_df = obj_iexcloud.get_momentum_df(stock)
            graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df['Momentum'],
                mode = 'lines',
                name = f"{stock} Momentum",
                textposition = 'bottom center',
            ))
        if momentum_selector == 'Moving Average':
            stock_df = obj_iexcloud.get_moving_average_df(stock)
            graphs.append(go.Scatter(
            x = stock_df['Date'],
            y = stock_df['Moving Average'],
            mode = 'lines',
            name = f"{stock} Moving Average",
            textposition = 'bottom center',
            yaxis = 'y2'
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
                    },
            yaxis2 = {'showgrid':False, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                'overlaying': 'y',
                'side': 'right'
                    },
            legend=dict(
                font=dict(
                    color="white"
                    ),
                )
            )
        } 


    return fig
