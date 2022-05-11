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
from forecasting.views import predict_sentiment


##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('forecasting', external_stylesheets=external_stylesheets)

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


##############################################################################################

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                value = [],
                placeholder="Companies listed on Nasdaq",
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),
    
    dcc.Graph(id="forecasting-chart", config={'displayModeBar': False}),
    
])

#Callbacks
@app.callback(
    Output("forecasting-chart", "figure"), 
    [Input("stockselector", "value")])

def time_series_stock(ticker_dropdown):
    print(predict_sentiment(ticker_dropdown))

    #Flatten list
    #if any(isinstance(i, list) for i in ticker_dropdown):
    #    ticker_dropdown = [item for elem in ticker_dropdown for item in elem]
