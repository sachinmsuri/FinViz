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
app = DjangoDash('example', external_stylesheets=external_stylesheets)

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

def get_sectors():
    dropdown_options = []
    df = read_ticker_symbols()
    sector_lst = list(df['Sector'].unique())
    for i in sector_lst:
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
                placeholder="Companies listed of Nasdaq",
                style={'backgroundColor': '#1E1E1E'}),
    
    dcc.Dropdown(id='sectorselector',
                options=get_sectors(),
                multi=True,
                clearable = True,
                value = [],
                placeholder="Sectors listed of Nasdaq",
                style={'backgroundColor': '#1E1E1E'}),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),
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
            textposition = 'bottom center',
        ))

    for sector in sector_dropdown:
        df = read_ticker_symbols()
        df = df[df['Sector'] == sector]
        stock_list = list(df['Symbol'])[0:15]
        for stock in stock_list:
            stock_df = obj_iexcloud.get_max_time_series_df(stock)
            graphs.append(go.Scatter(
            x = stock_df['Date'],
            y = stock_df[stock],
            mode = 'lines',
            textposition = 'bottom center',
        ))

    if any(isinstance(i, list) for i in graphs):
        graphs = [item for elem in graphs for item in elem]

    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
                )
            }
    return fig
