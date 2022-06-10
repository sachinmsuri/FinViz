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
from annualreports.views import get_symbols


#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('annualreports', external_stylesheets=external_stylesheets)


##############################################################################################

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                value = [],
                placeholder="Companies listed on S&P500",
                style={'backgroundColor': '#1E1E1E', 'color': 'black'}),
    
    html.Br(),

    html.Div([
       html.H4('Balance Sheet Breakdown'),
       html.H4('Income Statement Breakdown'),
    ], style={
        'display': 'flex', 
        'justify-content': 'space-evenly', 
        'text-align': 'center',
        'color': 'white'
    }),

    html.Div([
        (dcc.Graph(id="balance-sheet", config={'displayModeBar': False})),
        html.Br(),
        (dcc.Graph(id="income-statement", config={'displayModeBar': False}))     
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
    ),

    html.Br(),
    html.Br(),

     html.Div([
       html.H4('Financial Ratios'),
    ], style={
        'text-align': 'center',
        'color': 'white'
    }),


    html.Div(id="financial-ratios"),
    
])

    

#Callbacks
@app.callback(
    Output("balance-sheet", "figure"), 
    [Input("stockselector", "value")])

def balance_sheet(ticker):
    
    graphs = []
    
    if ticker:
    
        df = obj_iexcloud.get_balance_sheet(ticker)

        for column in df.columns:
            if column != 'Indicator':
                graph = go.Bar(
                    name = column,
                    x = df['Indicator'],
                    y = df[column]
                )

                graphs.append(graph)

        
    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
            autosize=True,
            height = 550,
            xaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    },
            yaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    },
            legend=dict(
                font=dict(
                    color="white"
                    ),
                )
            )
        } 
    
    return fig


@app.callback(
    Output("income-statement", "figure"), 
    [Input("stockselector", "value")])

def income_statement(ticker):

    graphs = []
    
    if ticker:

        df = obj_iexcloud.get_income_statement(ticker)

        for column in df.columns:
            if column != 'Indicator':
                graph = go.Bar(
                    name = column,
                    x = df['Indicator'],
                    y = df[column]
                )

                graphs.append(graph)

        
    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
            autosize=True,
            height = 550,
            xaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    },
            yaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    },
            legend=dict(
                font=dict(
                    color="white"
                    ),
                )
            )
        } 
    
    return fig

@app.callback(
    Output("financial-ratios", "children"), 
    [Input("stockselector", "value")])

def news_articles(ticker):

    df = obj_iexcloud.get_financial_ratios(ticker)

    return dash_table.DataTable(
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
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
    )

    



