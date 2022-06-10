from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from companystats.views import read_ticker_stats


#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('companystats', external_stylesheets=external_stylesheets)

df = read_ticker_stats()


##############################################################################################

#App layout
app.layout = html.Div([

    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        style_header={
        'backgroundColor': 'black',
        'color': 'white',
        'textAlign': 'center'
        },
        style_cell={
        'backgroundColor': 'black',
        'color': 'white',
        'textAlign': 'left'
        },
        id='S&P500 Table',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        #column_selectable="single",
        #row_selectable="multi",
        page_action="native",
        page_current= 0,
        page_size= 510,
    ),

])

#Callbacks

    



